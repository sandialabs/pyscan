from typing import Optional, Type
import os

import numpy as np

# import h5py
import torch
from torch.distributions import Normal
from torch.optim import LBFGS, Adam
import gpytorch
from gpytorch.means import Mean, ConstantMean, ZeroMean
from gpytorch.kernels import ScaleKernel, RBFKernel, MaternKernel
from gpytorch.mlls import ExactMarginalLogLikelihood
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.distributions import MultivariateNormal

from .optimum_helpers import *


# === Initial Conditions and File Path information ===
# DATA_FILEPATH: str = "paraboloid_example.hdf5"
# DATASET_NAME: str = "paraboloid_example_data"

# MAX_TRAINING_ITER: int = 1
# LOSS_THRESHOLD: float = 1e-6 # determines an early stop in training if a plateau is hit early to minimize computational waste


# ***** would need to implement these in collect_initial_data()
# NUM_INITIAL_SEARCH_RUNS: int = 10
# INITIAL_RUN_STRATEGY: str = "grid" # random or grid



class GPModel(gpytorch.models.ExactGP):
	def __init__(
		self, 
		train_x: torch.Tensor,
		train_y: torch.Tensor,
		mean_module: gpytorch.means=ConstantMean(),
		covar_module: gpytorch.kernels=ScaleKernel(RBFKernel()),
		likelihood: gpytorch.likelihoods=GaussianLikelihood(),
	):
		super(GPModel, self).__init__(
			train_x,
			train_y,
			likelihood,
		)
		self.mean_module = mean_module
		self.covar_module = covar_module

	def forward(self, x):
		mean_x = self.mean_module(x)
		covar_x = self.covar_module(x)
		return MultivariateNormal(mean_x, covar_x)

def train_GP(
	model: GPModel,
	X_train: torch.Tensor,
	y_train: torch.Tensor,
	max_epoch: int,
	min_loss_threshold: float,
	optimizer: torch.optim.Optimizer, # assume to be already fitted with the model parameters
	percent_cpu_usage: float= 0.75,
	debug: bool=False,
) -> None:
	"""
	Train a Gaussian Process model with the collected data set

	Ensure that that optimizer has already been fit with the model parameters.
	"""
	
	device = assign_pytorch_device()
	if device == "cpu":
		num_cores = os.cpu_count()
		cores_to_use =  np.floor(percent_cpu_usage * num_cores)
		torch.set_num_threads(cores_to_use) # number of cores that can be used

	# assign all training objects to the same device; errors otherwise
	model.to(device)
	model.likelihood.to(device)
	X_train.to(device)
	y_train.to(device)

	model.train()
	model.likelihood.train()
	
	mll = ExactMarginalLogLikelihood(model.likelihood, model)

	# training loop
	def closure():
		optimizer.zero_grad()
		output = model(X_train)
		loss = -mll(output, y_train)
		loss.backward()
		return loss
	
	last_loss = 0.0

	# iterate training
	for epoch in range(max_epoch):
		loss = optimizer.step(closure)
		delta_loss = torch.abs((last_loss - loss)).item()
		if delta_loss <= min_loss_threshold:
			break # reduce wasted computation when training plateau is reached
		last_loss = loss.item()
		
		if debug is True:
			# help find issues with training
			print(f"Epoch {epoch} | loss: {last_loss}")
	
	model.eval()
	model.likelihood.eval()

	return None
	
def acquisition(
	mean: torch.Tensor,
	stdev: torch.Tensor,
	target_max: float,
	acquisition_type: str="EI",
	ei_threshold: float=1e-3, 
	pi_threshold:  float=1e-2,
) -> torch.Tensor:
	"""
	Acquisition function -- can either choose the next parameters based on the maximum Probability of Improvement (PI) or
	the maximum Expected Improvement (EI). Expected improvement is generally considered superior.

	Thresholds should be tuned based on the problem at hand.

	Returns the indices of the domain grid being used for the GP model which contains the next points to evaluate.
	"""
	OFFSET_ZERO: float = 1E-9

	difference = mean - target_max
	score = difference / (stdev + OFFSET_ZERO)

	if (acquisition_type == "PI"):
		probability_of_improvement = Normal(0, 1).cdf(score)
		max_probability_improvement = np.max(np.asarray(probability_of_improvement))
		next_index_improve = np.argmax(np.asarray(probability_of_improvement))
		# stop threshold
		if max_probability_improvement <= pi_threshold:
			return next_index_improve, False
	
	elif (acquisition_type == "EI"):
		expected_improvement = (
			difference * Normal(0, 1).cdf(score) + 
			stdev * Normal(0, 1).log_prob(score).exp()
		)
		expected_improvement[stdev <= 0.0] = 0.0 # filter negatives
		max_expected_improvement = np.max(np.asarray(expected_improvement))
		next_index_improve = np.argmax(np.asarray(expected_improvement))
		# stop threshold
		if max_expected_improvement <= ei_threshold:
			return next_index_improve, False
		
	return next_index_improve, True


def run_optimization(
	model: GPModel,
	X_train: torch.Tensor,
	y_train: torch.Tensor,
	domain_tensor: torch.Tensor,
	# save_filepath: str,
	# dataset_name: str,
	optimizer: torch.optim.Optimizer,
	# max_data_acquisitions: int=30,
	max_epoch: int=30,
	acquisition_type: str="EI",
	ei_threshold: float= 1e-3,
	pi_threshold: float= 1e-2,
	min_loss_threshold: float=1e-6,
	# save_filepath: str=DATA_FILEPATH,
	# dataset_name: str=DATASET_NAME,
	percent_cpu_usage: float=0.75,
	debug: bool=False,
) -> None:

	
	gp_info_dict = {
		"max_epoch": max_epoch,
		"loss_threshold": min_loss_threshold,
		"percent_cpu_usage": percent_cpu_usage,
		"debug": debug,
	}
	
	# TODO: retain model info for online learning like between for loop iter

	# for i in np.arange(max_data_acquisitions):
		
	# train Gaussian process model on collected data set
	train_GP(
		model=model,
		X_train=X_train,
		y_train=y_train,
		max_epoch=max_epoch,
		min_loss_threshold=min_loss_threshold,
		percent_cpu_usage=percent_cpu_usage,
		optimizer=optimizer,
		debug=debug
	)
	
	# gather statistics on the set search domain
	with torch.no_grad():
		predictions = model.likelihood(model(domain_tensor))
		mean = predictions.mean
		stdev = predictions.stddev
	
	y_train_array = y_train.numpy()

	# acquire next data points to train on
	next_input_index, running = acquisition(
		mean=mean,
		stdev=stdev,
		target_max=y_train_array.max(),
		acquisition_type=acquisition_type,
		ei_threshold=ei_threshold,
		pi_threshold=pi_threshold,
	)

	next_domain_values = domain_tensor[next_input_index]
	return next_domain_values, running

	# *** pass either the domain index / domain values to your function that can gather more data

	# call run_experiment on next_domain_values

	# add next_domain_values to x_data

	# add result of run_experiment to y_data


	# *** logic for saving data as it runs, as well as saving the GP model weights?


	# if improvement threshold is met
	# if next_input_index is None:
	# 	break
		

def create_domain_tensor(
	domain_info_list: list[tuple[float]]
) -> tuple[torch.Tensor, tuple[torch.Tensor]]:
	"""
	Creates and returns a data_tensor_array that sets the domain for all the combinations of the varied input conditions to be passed to the Gaussian Process model.
	Also returns the grid_tuple that contains domain combinations for graphing convenience, if desired. 

	nested_domain_list structure expected to be: 
	[
		(variable1_min, variable1_max, variable1_step_size),
		(variable2_min, variable2_max, variable2_step_size),
		...
	]

	"""

	tensor_list: list[torch.Tensor] = []

	# create range for each variable
	for domain_tuple in domain_info_list:
		domain = torch.arange(*domain_tuple)
		tensor_list.append(domain)

	# create grid from all variable ranges
	grid_tuple = torch.meshgrid(tensor_list, indexing="ij")
	
	flattened_tensors = []

	for tensor in grid_tuple:
		flat_tensor = tensor.reshape(-1)
		flattened_tensors.append(flat_tensor)
	
	# stack along the new dimension (dim=1) to get (N, D); N data points with D dimensions
	data_tensor_array = torch.stack(flattened_tensors, dim=1)

	return data_tensor_array, grid_tuple



# def collect_initial_data(
# 	file_path: str,
#     data_set_name: str,
#     data_tensor_array: torch.Tensor,
# 	num_search_runs: int = NUM_INITIAL_SEARCH_RUNS,
# 	run_strategy: str =INITIAL_RUN_STRATEGY,
# ) -> None:


# 	# need to implement function ***
	

# 	# collect data points on the provided/created data_tensor_array
# 	# run_experiment()

# 	# needs to generate the following initial data set
# 	X_data: np.ndarray = []
# 	y_data: np.ndarray = []

# 	return X_data, y_data


def run_experiment():

	# *** implement logic for data collection
	# returns new y_data


	return None



def bayes_opt_main(
	domain_info_list: list[tuple[float]], # (min, max, step_size) for each variable
	# max_data_acquisitions: int,
	X_init,
	y_init,
	# save_filepath: str,
	# dataset_name: str,
	optimizer_class: Type[T_Optim]=LBFGS,
	# learning_rate: Optional[float]=None,
	optimizer_kwargs: dict={"line_search_fn": "strong_wolfe", "lr": 1e-3},
	max_num_epochs: int=30,
	min_loss_threshold: float=1e-6,
	acquisition_type: str="EI",
	ei_threshold: float= 1e-3,
	pi_threshold: float= 1e-2,
	percent_cpu_usage: float=0.75,
	# initialize: bool=True,
	debug: bool= False,
):

	data_tensor_array, _ = create_domain_tensor(domain_info_list)

	# if learning_rate is not None:
	# 	optimizer_kwargs["lr"] = learning_rate

	gp_info_dict = {
		"max_epoch": max_num_epochs,
		"min_loss_threshold": min_loss_threshold,
		"percent_cpu_usage": percent_cpu_usage,
		"debug": debug,
	}

	optimization_info_dict = {
		"domain_tensor": data_tensor_array,
		# "max_data_aqcuisitions": max_data_acquisitions,
		"acquisition_type": acquisition_type,
		"ei_threshold": ei_threshold,
		"pi_threshold": pi_threshold,
		# "save_filepath": save_filepath,
		# "dataset_name": dataset_name,
	}

	# # Create a fresh data set
	# if initialize is True:

	# 	# need to implement this function ***
	# 	X_train, y_train = collect_initial_data(
	# 		DATA_FILEPATH,
	# 		DATASET_NAME,
	# 		data_tensor_array,
	# 	)
	# # Load existing data set
	# else:
		
	# 	# *** implement data loading logic/function
	# 	input_data = []
	# 	output_data = []
		
		
	# 	X_data_tensor = torch.tensor(input_data)
	# 	y_data_tensor = torch.tensor(output_data)

	X_data_tensor = torch.tensor(X_init)
	y_data_tensor = torch.tensor(y_init)


	# create Gaussian process model and perform initial training
	# *** depending on information on noise from instruments, the likelihood can be further tuned with noise parameters
	# likelihood = GaussianLikelihood()
	model = GPModel(X_data_tensor, y_data_tensor,
				#  likelihood
				 )
	optimizer_fit = make_optimizer(
		optim_class=optimizer_class, 
		params=model.parameters(), 
		**optimizer_kwargs
	)
	gp_info_dict["optimizer"] = optimizer_fit
	
	# train_GP(
	# 	model=model,
	# 	X_train=X_data_tensor,
	# 	y_train=y_data_tensor,
	# 	**gp_info_dict,
	# )
	
	# next_data_point, mean, sigma | None
	improvement_data, running = run_optimization(
		model=model,
		X_train=X_data_tensor,
		y_train=y_data_tensor,
		**gp_info_dict,
		**optimization_info_dict
	)

	# deconstruct if able
	# if improvement_data is not None:
	# 	next_data_point, mean, sigma = improvement_data
	# 	return next_data_point, mean.numpy(), sigma.numpy()
	# else:
	# 	return improvement_data

	return improvement_data, running
	
