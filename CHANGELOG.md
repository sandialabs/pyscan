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



