from typing import Optional, Type, TypeVar
import inspect

import torch
import gpytorch


def assign_pytorch_device(
    do_device_check: bool=True,
) -> torch.DeviceObjType:
    """
    Dynamically assign which hardware to use for model training.
    Supports CPU, Nvidia GPUs with CUDA, Intel GPUs with XPU, and AMD GPUs with ROCm.
    Intel and AMD GPUs require a special version of pytorch and specific drivers, described in the links provided.

    * Not possible to have all types of GPUs simultaneously available in the same environment; each requires a distinct Pytorch version
    that is incompatible with the others.

    CPU / Nvidia GPU:
        https://pytorch.org/get-started/locally/
    
    Intel GPU:
        https://docs.pytorch.org/docs/stable/notes/get_start_xpu.html
        https://intel.github.io/intel-extension-for-pytorch/
        https://www.intel.com/content/www/us/en/developer/articles/technical/introducing-intel-extension-for-pytorch-for-gpus.html
    
    AMD GPU:
        https://pytorch.org/blog/pytorch-for-amd-rocm-platform-now-available-as-python-package/
        https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html
        https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html

    """
    if torch.xpu.is_available():
        device_count = list(range(torch.xpu.device_count()))
        for device in device_count:
            print(f'Device name [{device}]:', torch.xpu.get_device_name(device))
        device_str: str = "xpu"
        gpu_package = torch.xpu
    elif torch.cuda.is_available(): # this checks for both Nvidia and AMD cards
        device_count = list(range(torch.cuda.device_count()))
        for device in device_count:
            print(f'Device name [{device}]:', torch.cuda.get_device_name(device))
        device_str: str = "cuda"
        gpu_package = torch.xpu
    else:
        device_str: str = "cpu"

    device = torch.device(device_str)

    if do_device_check:
        device_check(device)

    return device

D = TypeVar("D", torch.xpu, torch.cuda)

def device_check(
    device: torch.DeviceObjType,
    gpu_package: Optional[Type[D]]=None
):
    print(f"PyTorch version: {torch.__version__}")

    # test CPU/GPU computation
    x = torch.randn(1000, 1000, device=device)
    y = torch.randn(1000, 1000, device=device)
    result = torch.mm(x, y) # matrix multiplication test
    
    if gpu_package is not None:
        print(f"GPU memory allocated by Pytorch: {gpu_package.memory_allocated()}")
    print(f"Computation successful on: {result.device}")

    return None



# For more on optimizers see https://docs.pytorch.org/docs/stable/optim.html
T_Optim = TypeVar("T_Optim", bound=torch.optim.Optimizer) # LBFGS, Adam; LBFGS generally converges faster, but uses more memory; The reverse is true of Adam
DEFAULT_OPTIMIZERS = {
    torch.optim.Adam: {"lr": 1e-3},
    torch.optim.LBFGS: {"line_search_fn": "strong_wolfe"},
}

def get_optimizer_with_defaults(optim_class: Type[T_Optim], params, **kwargs) -> T_Optim:
    defaults = DEFAULT_OPTIMIZERS.get(optim_class, {})
    merged_kwargs = {**defaults, **kwargs}
    return make_optimizer(optim_class, params, **merged_kwargs)

def make_optimizer(
    optim_class: Type[T_Optim], 
    params, 
    **kwargs
) -> T_Optim:
    signature = inspect.signature(optim_class.__init__) # init signature of the optimizer
    filtered_kwargs = {key: value for key, value in kwargs.items() if key in signature.parameters} # only pass kwargs that are in the signature
    return optim_class(params, **filtered_kwargs)




### custom mean function, although using the ConstantMean() is considered best practice if little to no information is known about the surface being probed


# *** only expects 2 independent variables and 1 dependent variable output; can make more generalized to handle arbitrary dimension inputs/outputs later
class PolynomialMean(gpytorch.means.Mean):
	def __init__(self, input_size, batch_shape=torch.Size()):
		super().__init__()
		# coefficients for the quadratic terms
		self.register_parameter(
			name='quadratic_coeffs', 
			parameter=torch.nn.Parameter(torch.randn(*batch_shape, input_size)),
		)
		# bias term
		self.register_parameter(
			name='bias', 
			parameter=torch.nn.Parameter(torch.randn(*batch_shape, 1)),
		)

	def forward(self, x):
		quadratic_terms = (x.pow(2) * self.quadratic_coeffs)  # element-wise squaring and multiplication by coefficients
		tensor_sum = quadratic_terms.sum(dim=-1) + self.bias  # sum over feature dimension and add bias
		return tensor_sum