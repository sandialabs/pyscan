## [0.8.7](https://github.com/sandialabs/pyscan/compare/v0.8.6...v0.8.7) (2025-02-05)


### Bug Fixes

* **keysite driver:** Added new exception for keysite SD1 loading, rem… ([#244](https://github.com/sandialabs/pyscan/issues/244)) ([ee281ae](https://github.com/sandialabs/pyscan/commit/ee281ae7cb2e773072d03131da585c8f8bef5ebd))



## [0.8.6](https://github.com/sandialabs/pyscan/compare/v0.8.5...v0.8.6) (2024-12-17)


### Bug Fixes

* **driver:** doc string if not found returns blank.  If multiple, takes first ([f723504](https://github.com/sandialabs/pyscan/commit/f723504bc09b1b912a0d4b281a4bb905eecf7264))
* **drivers:** fixed doc string detection exit ([80aefe5](https://github.com/sandialabs/pyscan/commit/80aefe5de6e6907fb68634e7246e4a3b302e4841))



## [0.8.5](https://github.com/sandialabs/pyscan/compare/v0.8.4...v0.8.5) (2024-10-29)


### Bug Fixes

* **driver:** fixed the stanford 860 auto test end removed some unneeded properties ([35bc923](https://github.com/sandialabs/pyscan/commit/35bc923bee85bb3104d3234bccb9b1d5ed0a5bff))



## [0.8.4](https://github.com/sandialabs/pyscan/compare/v0.8.3...v0.8.4) (2024-10-18)


### Bug Fixes

* **drivers:** fixed driver import exceptions and names ([37f8160](https://github.com/sandialabs/pyscan/commit/37f816059524ce04fcbeeb9da739b3e1e81ab4da))



## [0.8.3](https://github.com/sandialabs/pyscan/compare/v0.8.2...v0.8.3) (2024-10-04)


### Bug Fixes

* **driver:** fixed flake8 errors and a few other imports ([140fda3](https://github.com/sandialabs/pyscan/commit/140fda3ac28a3394fb60a8a6e40134474adcb125))
* **driver:** fixed ocean optics, attocube, and keysightsd1 import messages ([145b8b7](https://github.com/sandialabs/pyscan/commit/145b8b796aaf61ee5e2151de416dab4e521c135a))
* **drivers:** fixed thorlabs and pulseblaster to not thor import errors ([2505ba9](https://github.com/sandialabs/pyscan/commit/2505ba948aff24aa96d6e3ad98c18a30e3fea97d))



## [0.8.2](https://github.com/sandialabs/pyscan/compare/v0.8.1...v0.8.2) (2024-10-04)


### Bug Fixes

* **driver:** fixed flake8 errors and a few other imports ([922316d](https://github.com/sandialabs/pyscan/commit/922316d697e41eb1cc5fa4d6457a3cecee071850))
* **driver:** fixed flake8 errors and a few other imports [skip ci] ([b82cf44](https://github.com/sandialabs/pyscan/commit/b82cf443ab3a38a1b0558eefe52c7a72914608cc))
* **driver:** fixed ocean optics, attocube, and keysightsd1 import messages ([cbfd373](https://github.com/sandialabs/pyscan/commit/cbfd373828b736497b47b7a25896f20e68ad5dd1))
* **drivers:** fixed thorlabs and pulseblaster to not thor import errors ([3483a34](https://github.com/sandialabs/pyscan/commit/3483a344da9740d5e6e22fbe3646be63b10c8880))



## [0.8.1](https://github.com/sandialabs/pyscan/compare/v0.8.0...v0.8.1) (2024-10-03)


### Bug Fixes

* **driver Stanford830:** learned to spell, fixed test notebook bug ([be9b137](https://github.com/sandialabs/pyscan/commit/be9b1376fb895486fd799050d483886951432723))
* **driver:** black listed stanford830 sensitivity for autotesting, depends on time constant ([0f8cedd](https://github.com/sandialabs/pyscan/commit/0f8cedda52b4b5d04598536205bb5d860ce5b31d))
* **driver:** fixed srs830 snap and offset_expand bugs ([4170268](https://github.com/sandialabs/pyscan/commit/4170268604b56ae86b059168c88ab2b4f0e38b35))
* **driver:** fixed Stanford830 buffer points as read only, complete driver? ([dc2a5be](https://github.com/sandialabs/pyscan/commit/dc2a5be3ece234081c51384ea714ed99190df741))
* **test)(driver:** fixed both test cases and srs830 driver so it is now passing the test cases. A debug setting is included to debug the test_driver() function; however, this will bypass the test log. An updated error message is included to point to setting the debug parameter to true for debugging purposes. ([74c835d](https://github.com/sandialabs/pyscan/commit/74c835d8329d82b28fb0260d8db6b7e21302d011))



# [0.8.0](https://github.com/sandialabs/pyscan/compare/v0.7.4...v0.8.0) (2024-10-01)


### Bug Fixes

* tried updating killswitch example notebook to skip last cell on nbmake workflow. ([cd2b930](https://github.com/sandialabs/pyscan/commit/cd2b930214923d5f1ff0304b6e45a59829c7903f))


### Features

* Added live_multi_plot function ([3502a7d](https://github.com/sandialabs/pyscan/commit/3502a7df2bf5e1e397e79c9dff983bc4e3b178d4))


### Reverts

* **general:** restoring main version of get_pyscan_version. ([b341479](https://github.com/sandialabs/pyscan/commit/b341479300ca90be17e98a5f6bd0d7c19ddb8a2a))
* **measurement:** restoring main version of run_info.py. ([9d3558e](https://github.com/sandialabs/pyscan/commit/9d3558efe5053e927314bf78213034eb46322ba2))



## [0.7.4](https://github.com/sandialabs/pyscan/compare/v0.7.3...v0.7.4) (2024-10-01)


### Bug Fixes

* **measurement:** fixed sparse experiment to use scan naming convention rather than loop. ([423ce39](https://github.com/sandialabs/pyscan/commit/423ce39cb05f751a09a313682c46c2254cc6472e))
* **measurement:** fixed sparse experiment to use scan naming convention rather than loop. [skip ci] ([ea71d69](https://github.com/sandialabs/pyscan/commit/ea71d6908264d88dc005d64d723f2dadb042850c))
* **plotting:** updating loop nomenclature to scan in plot_generator. ([af27aa6](https://github.com/sandialabs/pyscan/commit/af27aa626df4cf0bc3b78f8cb6847ca9a5ec9c49))



## [0.7.3](https://github.com/sandialabs/pyscan/compare/v0.7.2...v0.7.3) (2024-09-24)


### Bug Fixes

* fixing pyscan init to install more robustly. ([63fe2b1](https://github.com/sandialabs/pyscan/commit/63fe2b1adf8d6ae57da2d8741f182f6e839445e2))



## [0.7.2](https://github.com/sandialabs/pyscan/compare/v0.7.1...v0.7.2) (2024-09-17)


### Bug Fixes

* **install:** now install without -e will work since version file moved to pyscan folder. Version workflow set to track accordingly. Install and runinfo will now fail if version not detected. ([62bd629](https://github.com/sandialabs/pyscan/commit/62bd6291857490b6738b7f85e05f035bb1d06467))
* **install:** updating complete.yml to run jobs in parallel, and updated setup.py to explicity include pyscan/VERSION.json when using pip install . ([84a1982](https://github.com/sandialabs/pyscan/commit/84a198212d433b23600ef5d9ce13adf099789f43))
* **install:** updating complete.yml to run jobs in parallel, and updated setup.py to explicity include pyscan/VERSION.json when using pip install . [skip ci] ([d8f0974](https://github.com/sandialabs/pyscan/commit/d8f0974d4cc2c6564bb969b96182dbdcd644ff14))
* **measurement:** Update run_info.py ([68f0df2](https://github.com/sandialabs/pyscan/commit/68f0df2e06eab5e2021945fb8b6715b16022fa50))
* **workflows:** updating complete.yml to ensure the job complete2 does not have race condition, conflict, or other unwanted interaction with the job complete. ([acac485](https://github.com/sandialabs/pyscan/commit/acac485c89cf4e4b3bf3ed46712a0c95e86cca94))



## [0.7.1](https://github.com/sandialabs/pyscan/compare/v0.7.0...v0.7.1) (2024-09-13)


### Bug Fixes

* **core:** fixing ability for empty property scans inbetween used scans. Now adding a check to block this. Scans must be populated in sequential order. ([91b7c41](https://github.com/sandialabs/pyscan/commit/91b7c41df565755cb744bb216ca43066b90214f3))



# [0.7.0](https://github.com/sandialabs/pyscan/compare/v0.6.0...v0.7.0) (2024-07-16)


### Bug Fixes

* **test:** fixed test_test_instrument_driver.py to account for read_only and write_only properties added to test_instrument_driver.py. This now solves the issue with auto_test_driver not failing with read and write only properties and ensures they are auto tested for future compatibility. ([f4554cd](https://github.com/sandialabs/pyscan/commit/f4554cd9869d6f950f8965e470ee1209c802e017))


### Features

* **drivers:** adding a built in get_resources function that can return a list of available resources along with their names, and capture a target resource for initializing drivers. ([02971f6](https://github.com/sandialabs/pyscan/commit/02971f63888f95ec430873f90e21fe6c0a2df68f))



# [0.6.0](https://github.com/sandialabs/pyscan/compare/v0.5.4...v0.6.0) (2024-07-09)


### Bug Fixes

* **core:** fixed json decoder to now be standard decoder that converts dictionaries into ItemAttributes while still being generalizable. ([09210a9](https://github.com/sandialabs/pyscan/commit/09210a9d2ff03a6a047701b23440ec85b35ba22c))
* **core:** fixed JSON encoder to fully remove recursive_to_dict and be entirely independent. Seems to be working and passing all test cases; however, a saved expt file should be evaluated to confirm this is working before pulling these changes. ([2d94b8e](https://github.com/sandialabs/pyscan/commit/2d94b8ead48f63552d31350f2f437899437b2e4c))


### Features

* **general): measured function now fully saved as runinfo metadata. chore(general:** fixed json encoder again, this time it is using native functions more and only accounting for unsupported data types. ([2547d43](https://github.com/sandialabs/pyscan/commit/2547d43af38bbe967721b7d97c58aa441e5ae32e))



## [0.5.4](https://github.com/sandialabs/pyscan/compare/v0.5.3...v0.5.4) (2024-07-09)


### Bug Fixes

* **core:** added a json converter class in json_encoder.py to pyscan/general. This is now implemented in the save_metadata method of abstract_experiment.py which enables numpy values to be used as data inputs before saving. The converter changes the numpy values to standard python values and no longer throws the same type error as before. ([c2c2b8f](https://github.com/sandialabs/pyscan/commit/c2c2b8ffb3f8d1860f6dc6612b2c83eddc21a28f))
* **core:** added working json converter for runinfo and devices metadata now implemented in abstract experiment's save_metadata method. ([11f43a3](https://github.com/sandialabs/pyscan/commit/11f43a3c247dd4294d079ffd20b360572ffc3ed8))
* **core:** corrected the issue plesiopterys identified with saving numpy data types and consolidated the json converter added in the last commit to the pre existing recursive_to_dict function which can now handle numpy data types for saving. ([fb66ad8](https://github.com/sandialabs/pyscan/commit/fb66ad8727acfd33b6f59feef6b7a68d023d052f))
* **core:** fixed issue causing multiple experiments run with the same runinfo to fail. These sequential experiments would improperly double runinfo.measured by appending the same values to it more than once. Then when data was tried to be preallocated in abstract expt it would fail. ([cb093a2](https://github.com/sandialabs/pyscan/commit/cb093a25c5e86edb62b2a22ed7eab91fa73a1956))
* **core:** Fixed the issue with saving if experiments are run 'too fast'. Will now handle ultra fast experiments (up to a micro second or more) which was tested with demo nb 1 using a dt of 0.000000001 and consecutive experiments. ([bba1bca](https://github.com/sandialabs/pyscan/commit/bba1bcac7561a8f9e03083d3b12951223ccba4d4))
* **core:** updated experiment.py to reinitialize runinfo.measured as an empty list before populating at the beginning of every experiment run. This was causing issues with running subsequent experiments with the same runinfo, and is necessary to prevent runinfo.measured from being reused if runinfo.measure_function changed between runs. ([bbc1be8](https://github.com/sandialabs/pyscan/commit/bbc1be8958081385c4cfe3d23f5ab6eae83b8c82))


### Reverts

* Revert "fix(core): added a json converter class in json_encoder.py to pyscan/general. This is now implemented in the save_metadata method of abstract_experiment.py which enables numpy values to be used as data inputs before saving. The converter changes the numpy values to standard python values and no longer throws the same type error as before." ([30dbdd5](https://github.com/sandialabs/pyscan/commit/30dbdd5c25186ee3278894588b9a9121a354d7eb))
* Revert "fix(core): corrected the issue plesiopterys identified with saving numpy data types and consolidated the json converter added in the last commit to the pre existing recursive_to_dict function which can now handle numpy data types for saving." ([30c601d](https://github.com/sandialabs/pyscan/commit/30c601d6b2db2f3a8aa66debedbcbc5b2a1e7f70))
* Revert "chore(core): removed old import from abstract_experiment." ([9d7a10b](https://github.com/sandialabs/pyscan/commit/9d7a10bc51932f65bc8bcdba3a35af651f681dbd))
* Revert "chore(core): fix: fixed misuse of np.array n recursive_to_dict that was causing a type error." ([a56704d](https://github.com/sandialabs/pyscan/commit/a56704d650242ca73d9b3b988e50d64806fbb572))
* Revert "fix(core): added working json converter for runinfo and devices metadata now implemented in abstract experiment's save_metadata method." ([0d122b0](https://github.com/sandialabs/pyscan/commit/0d122b0d20b999797e136728ca792c092a06adeb))
* Revert "docs(general): added doc string to json_encoder.py CustomJSONEncoder class." ([1224b06](https://github.com/sandialabs/pyscan/commit/1224b06b573e94347e983ba7fa4156d6b27d97c7))
* Revert "chore(core): removed no longer used recursive_to_dict import from abstract expt." ([7d5b6e9](https://github.com/sandialabs/pyscan/commit/7d5b6e91487a310b8ef15a8000b9bcabb38cdbae))
* Revert "refactor(general): replaced recursive_to_item_attribute with json decoder item_attribute_object_hook." ([6dcfdc1](https://github.com/sandialabs/pyscan/commit/6dcfdc1b01811f81fc5e969addce0fb479595521))
* Revert "chore(general): updated the general __init__.py to account for the file changes from previous commits and import successfully with a new order since itemattribute is used in other pyscan/general modules now." ([27ae91c](https://github.com/sandialabs/pyscan/commit/27ae91c7a1495e05e7887897972ae94ddef886c9))
* Revert "chore(general): fixed improper spelling in the json_decoder." ([205c33a](https://github.com/sandialabs/pyscan/commit/205c33ac3071adfd3c942c7a65258054baf4d67a))
* Revert "chore(general): fixed improper spelling in the json_decoder." ([6e5b788](https://github.com/sandialabs/pyscan/commit/6e5b788fe880b43df8fe30ec9e637e6af8b6f3e0))
* Revert "chore(general): fixed error breaking pytests with decoder referencing np.float_ which was removed in numpy 2.0." ([0886669](https://github.com/sandialabs/pyscan/commit/0886669c34b46721029ed4c810ea9fc2a04c8342))
* Revert "chore(general): fixed error breaking pytests with decoder referencing np.float_ which was removed in numpy 2.0." ([a32e84d](https://github.com/sandialabs/pyscan/commit/a32e84d3a5c5524d53e7b79aa7d48085e160ada2))



## [0.5.3](https://github.com/sandialabs/pyscan/compare/v0.5.2...v0.5.3) (2024-06-18)


### Bug Fixes

* **core:** added a json converter class in json_encoder.py to pyscan/general. This is now implemented in the save_metadata method of abstract_experiment.py which enables numpy values to be used as data inputs before saving. The converter changes the numpy values to standard python values and no longer throws the same type error as before. ([09ebcde](https://github.com/sandialabs/pyscan/commit/09ebcdee8c09966ea18e4754ff99f4bb5bc2c692))
* **core:** added working json converter for runinfo and devices metadata now implemented in abstract experiment's save_metadata method. ([c7e17ce](https://github.com/sandialabs/pyscan/commit/c7e17ce765f0357b609860bf265f9f3a35fa594a))
* **core:** corrected the issue plesiopterys identified with saving numpy data types and consolidated the json converter added in the last commit to the pre existing recursive_to_dict function which can now handle numpy data types for saving. ([18c4baf](https://github.com/sandialabs/pyscan/commit/18c4baffbb5298539e342fedf872dc19b85b3234))



## [0.5.2](https://github.com/sandialabs/pyscan/compare/v0.5.1...v0.5.2) (2024-06-11)


### Bug Fixes

* **driver:** removed smoothing from keithley2260b, added __del__ ([30feab6](https://github.com/sandialabs/pyscan/commit/30feab624e89f77641e15185becde39eedb1ff55))



## [0.5.1](https://github.com/sandialabs/pyscan/compare/v0.5.0...v0.5.1) (2024-06-11)


### Bug Fixes

* **build:** replaced ipykernel with jupyter in setup.py so that all packages required to run jupyter notebooks are automatically installed when pyscan is. ([aa06263](https://github.com/sandialabs/pyscan/commit/aa06263d9fbb5ab6a3cf0f227b7b4cd699ec087f))
* **build:** replaced ipykernel with jupyter in setup.py so that all packages required to run jupyter notebooks are automatically installed when pyscan is. [skip ci] ([17704b5](https://github.com/sandialabs/pyscan/commit/17704b599114a7f9b42b3df2726d3b50c5bcb7d6))



# [0.5.0](https://github.com/sandialabs/pyscan/compare/v0.4.0...v0.5.0) (2024-06-06)


### Bug Fixes

* fixed issues with keithley2260b and Stanford830 preventing them from passing test cases. ([fadae52](https://github.com/sandialabs/pyscan/commit/fadae5204fc1e6d7caac10bf045417bf6f0160b0))


### Features

* completed solution for tracking driver versions and last date tested. ([45e0589](https://github.com/sandialabs/pyscan/commit/45e05894a6580d95686eadb4768fc7c8c251d414))



# [0.4.0](https://github.com/sandialabs/pyscan/compare/v0.2.0...v0.4.0) (2024-05-30)


### Features

* Auto versioning, change log, and release ([a2cea93](https://github.com/sandialabs/pyscan/commit/a2cea93e6143d79e9d99c15970fe9f1bc53d3576))



# [0.2.0](https://github.com/sandialabs/pyscan/compare/v0.1.0...v0.2.0) (2024-05-17)


### Bug Fixes

* added line at end of drivers/testing/init file to satisfy flake8 req ([57821cb](https://github.com/sandialabs/pyscan/commit/57821cb008084b9c8d6b7526ce914bc1051f4548))
* added uses: actions/checkout@v3 to try and fix issue. ([bca0865](https://github.com/sandialabs/pyscan/commit/bca0865fda6a132745c477e950577d355dacc813))
* Added wiki link to contributors in README and docs index ([5a17be4](https://github.com/sandialabs/pyscan/commit/5a17be4b768d106ea8d162cfb42776e769dc5b8a))
* Added wiki link to contributors in README and docs index (Jasmine's commit pre revert) ([76faaca](https://github.com/sandialabs/pyscan/commit/76faaca2843ce90eb5bc99dc00f050591a438167))
* corrected comment with version_when_pushed.yml ([09e4ac5](https://github.com/sandialabs/pyscan/commit/09e4ac5573ad5053dac942420e7616d81b60890a))
* corrected error in versioning workflow. ([f4d4a8a](https://github.com/sandialabs/pyscan/commit/f4d4a8ab7b360c0e406c4b4befdfc8393ba6a1a3))
* corrected errors causing driver's test notebooks to fail. ([e5c620b](https://github.com/sandialabs/pyscan/commit/e5c620bc103877766dd03780de6ea4c3c98a67fd))
* deleted new_release.yml since it is not running on push. Will replace with two separate workflows. ([04ac6e2](https://github.com/sandialabs/pyscan/commit/04ac6e206311d02cdaf03200014a8e2150baee0c))
* Fixed formatting in README and docs index ([1f080fe](https://github.com/sandialabs/pyscan/commit/1f080fecc8d43346b50a917e7defb340417dad02))
* Fixed formatting in README and docs index (Jasmine's commit pre-revert) ([baa32a6](https://github.com/sandialabs/pyscan/commit/baa32a663b1c7744a48488b58709d4c220d5f9a0))
* fixed type so that all ymls are not running on push. ([15a1e1f](https://github.com/sandialabs/pyscan/commit/15a1e1f12a2c24819fe41af311ad1ad48c8345f4))
* fixed type so that all ymls are not running on push. ([2c0322d](https://github.com/sandialabs/pyscan/commit/2c0322d19171a37ca1cc827f03771e8c51b6f15a))
* fixing missing permissions in python-app.yml ([13d8a6c](https://github.com/sandialabs/pyscan/commit/13d8a6cfc7bc2d00e6b147876e527f37bc028125))
* fixing new_release.yml workflow to have proper permissions for auto versioning. ([d434314](https://github.com/sandialabs/pyscan/commit/d434314c2df54acb8c34a9f33f14ae141b67e025))
* giving permissions to python-app.yml for autoversioning. ([4654a91](https://github.com/sandialabs/pyscan/commit/4654a914d1ebe254e410ae4764e1fd7ab716c590))
* now allocating the right branch to push the version and changelog changes with. ([1a0c53e](https://github.com/sandialabs/pyscan/commit/1a0c53e77390859490c735921c08dd30ba3242f5))
* python-app.yml updates to try and capture versioning automatically. ([f213e64](https://github.com/sandialabs/pyscan/commit/f213e6468da3208f7a9c06ed4fee84d6b5c3a32a))
* Removed gain from stanford830. ([41b1717](https://github.com/sandialabs/pyscan/commit/41b171743170a912ad814b2aae0d2e5941f1579d))
* Renamed workflow to temp versioning for testing. ([2ef638a](https://github.com/sandialabs/pyscan/commit/2ef638a9d29726419412bb4e49b3ea6d635668d2))
* restoring __init__.py to drivers/testing/ folder which may be helpful for building docs and or installing pyscan. ([b94895e](https://github.com/sandialabs/pyscan/commit/b94895e4e26925d91240215cf59a1468e5d709c1))
* runinfo now implements version correctly without setter only getter. ([65e83ce](https://github.com/sandialabs/pyscan/commit/65e83ce4f650fbae5935a724bd58f6fae003bc00))
* trying to correct python-app.yml missing token error. ([d0b25c2](https://github.com/sandialabs/pyscan/commit/d0b25c2f08026dadb4ad83ebb7665c95fba42fec))
* updated manual_versioning.yml to enable workflow run on main. ([08b7401](https://github.com/sandialabs/pyscan/commit/08b7401ebd8f5d0eab1fbff399bb746474fdd0d4))
* updated new_release.yml syntax to try and fix not running on push to main. ([71b3bba](https://github.com/sandialabs/pyscan/commit/71b3bba9ce1c0395e8469294e62a0d1831dcbc1d))
* updated new_release.yml to only auto version on pull request approval to main or dev. ([358f65e](https://github.com/sandialabs/pyscan/commit/358f65e5ec0b875595bbf5a6d14fabe35c3195b4))
* updated new_release.yml to only auto version on pull request approval to main or dev. ([5ab2722](https://github.com/sandialabs/pyscan/commit/5ab272271bf833f013105c837aff3d096b5a661e))
* updated python-app.yml to only perform versioning and update changelog after the build passes all tests. ([c4d2ed1](https://github.com/sandialabs/pyscan/commit/c4d2ed16852f347957b4e800d7364b869d763fbd))
* updated python-app.yml to only perform versioning and update changelog after the build passes all tests. ([1a47452](https://github.com/sandialabs/pyscan/commit/1a47452e0e73a32f0e5a83dac3cf27ef1b442ac0))
* updated release.yml to address potential bugs and problems in advance. ([0c8bef7](https://github.com/sandialabs/pyscan/commit/0c8bef778e0c8a5fe66434278c9f950b74a98eaf))
* updated setup.py to fix build issue. ([4f6fd99](https://github.com/sandialabs/pyscan/commit/4f6fd99417ed22be9a73ee48fe93e71efbd97d35))
* updated workflow permissions for versioning files. ([4b9da2e](https://github.com/sandialabs/pyscan/commit/4b9da2efae19774653529ef348ea2786e17c600c))
* updated workflows to now only auto-version on merge from pull request or push to main and not dev. ([90f50d2](https://github.com/sandialabs/pyscan/commit/90f50d2b464f9b3358e6679e134ba305bf8de2e4))
* updating version.yml to pull from main first each time. ([4620432](https://github.com/sandialabs/pyscan/commit/4620432b024afc234551df58d3088fb238f0c6fd))
* updating, trying new things. ([4359dec](https://github.com/sandialabs/pyscan/commit/4359decff896c42ab3fabed3c19c2c31aca3f61b))


### Features

* added 2 workflows, one to auto version on merge from pull request, and one to auto version on push to main. ([a679f12](https://github.com/sandialabs/pyscan/commit/a679f12b3051824ca0f4d4fa9a9c31a359ad3848))
* added and updated workflows for more refined control in addition to auto versioning. ([2928899](https://github.com/sandialabs/pyscan/commit/2928899afe7c27579183ad53c5340ebe6cb168bb))
* added and updated workflows for more refined control in addition to auto versioning. ([7cc1541](https://github.com/sandialabs/pyscan/commit/7cc1541e6c4357a21bfad7198a8a151affa2dbff))
* added basic_build.yml to ensure install success on every build. ([a2555b6](https://github.com/sandialabs/pyscan/commit/a2555b6ab5d2fc4415cb49f3a3be082a0afcf6de))
* added get_version function to pyscan/general, implemented it in runfinfo, and also created a basic test file to ensure it works as expected. ([0e9fd49](https://github.com/sandialabs/pyscan/commit/0e9fd49e3720c392368e9efa44c1a6f9d7ba85f8))
* added new workflow for testing versioning temporarily. ([2fdd155](https://github.com/sandialabs/pyscan/commit/2fdd155d3eb90dff372467fe025b7ffdd08852d8))
* added workflow dispatch for ultimate versioning solution to temporarily test. ([842fecd](https://github.com/sandialabs/pyscan/commit/842fecd446a443cfdcc023d95ccd1e8260b8c361))
* Update VERSION.json ([91677f8](https://github.com/sandialabs/pyscan/commit/91677f8d0f51821dfdea19d9941ca2f275a11914))



# [0.1.0](https://github.com/sandialabs/pyscan/compare/v0.0.1...v0.1.0) (2024-04-18)


### Bug Fixes

* fixing missing permissions in python-app.yml ([ff4018b](https://github.com/sandialabs/pyscan/commit/ff4018bb059f422445164bf1472cc1b84b143337))
* giving permissions to python-app.yml for autoversioning. ([4984c3e](https://github.com/sandialabs/pyscan/commit/4984c3ec6b5c558b445f4024542ef5a848104e75))
* python-app.yml updates to try and capture versioning automatically. ([b4ad18b](https://github.com/sandialabs/pyscan/commit/b4ad18b3c1e805d6a3ecbdddddb5a55a0fcd1502))
* trying to correct python-app.yml missing token error. ([73350bd](https://github.com/sandialabs/pyscan/commit/73350bdf3caaadb0b10c74d074d591e6ed5c5d55))


### Features

* added basic_build.yml to ensure install success on every build. ([3e791fb](https://github.com/sandialabs/pyscan/commit/3e791fb93146d5d0e16c1a269d6feb80fac142eb))



## 0.0.1 (2023-11-28)



