# [0.5.0](https://github.com/rsbrost/test_pyscan_versioning/compare/v0.1.0...v0.5.0) (2024-05-07)


### Bug Fixes

* added line at end of drivers/testing/init file to satisfy flake8 req ([57821cb](https://github.com/rsbrost/test_pyscan_versioning/commit/57821cb008084b9c8d6b7526ce914bc1051f4548))
* added uses: actions/checkout@v3 to try and fix issue. ([bca0865](https://github.com/rsbrost/test_pyscan_versioning/commit/bca0865fda6a132745c477e950577d355dacc813))
* Added wiki link to contributors in README and docs index ([5a17be4](https://github.com/rsbrost/test_pyscan_versioning/commit/5a17be4b768d106ea8d162cfb42776e769dc5b8a))
* Added wiki link to contributors in README and docs index (Jasmine's commit pre revert) ([76faaca](https://github.com/rsbrost/test_pyscan_versioning/commit/76faaca2843ce90eb5bc99dc00f050591a438167))
* corrected comment with version_when_pushed.yml ([09e4ac5](https://github.com/rsbrost/test_pyscan_versioning/commit/09e4ac5573ad5053dac942420e7616d81b60890a))
* deleted new_release.yml since it is not running on push. Will replace with two separate workflows. ([04ac6e2](https://github.com/rsbrost/test_pyscan_versioning/commit/04ac6e206311d02cdaf03200014a8e2150baee0c))
* Fixed formatting in README and docs index ([1f080fe](https://github.com/rsbrost/test_pyscan_versioning/commit/1f080fecc8d43346b50a917e7defb340417dad02))
* Fixed formatting in README and docs index (Jasmine's commit pre-revert) ([baa32a6](https://github.com/rsbrost/test_pyscan_versioning/commit/baa32a663b1c7744a48488b58709d4c220d5f9a0))
* fixed type so that all ymls are not running on push. ([15a1e1f](https://github.com/rsbrost/test_pyscan_versioning/commit/15a1e1f12a2c24819fe41af311ad1ad48c8345f4))
* fixed type so that all ymls are not running on push. ([2c0322d](https://github.com/rsbrost/test_pyscan_versioning/commit/2c0322d19171a37ca1cc827f03771e8c51b6f15a))
* fixing missing permissions in python-app.yml ([13d8a6c](https://github.com/rsbrost/test_pyscan_versioning/commit/13d8a6cfc7bc2d00e6b147876e527f37bc028125))
* fixing new_release.yml workflow to have proper permissions for auto versioning. ([d434314](https://github.com/rsbrost/test_pyscan_versioning/commit/d434314c2df54acb8c34a9f33f14ae141b67e025))
* giving permissions to python-app.yml for autoversioning. ([4654a91](https://github.com/rsbrost/test_pyscan_versioning/commit/4654a914d1ebe254e410ae4764e1fd7ab716c590))
* python-app.yml updates to try and capture versioning automatically. ([f213e64](https://github.com/rsbrost/test_pyscan_versioning/commit/f213e6468da3208f7a9c06ed4fee84d6b5c3a32a))
* Renamed workflow to temp versioning for testing. ([2ef638a](https://github.com/rsbrost/test_pyscan_versioning/commit/2ef638a9d29726419412bb4e49b3ea6d635668d2))
* restoring __init__.py to drivers/testing/ folder which may be helpful for building docs and or installing pyscan. ([b94895e](https://github.com/rsbrost/test_pyscan_versioning/commit/b94895e4e26925d91240215cf59a1468e5d709c1))
* trying to correct python-app.yml missing token error. ([d0b25c2](https://github.com/rsbrost/test_pyscan_versioning/commit/d0b25c2f08026dadb4ad83ebb7665c95fba42fec))
* updated manual_versioning.yml to enable workflow run on main. ([08b7401](https://github.com/rsbrost/test_pyscan_versioning/commit/08b7401ebd8f5d0eab1fbff399bb746474fdd0d4))
* updated new_release.yml syntax to try and fix not running on push to main. ([71b3bba](https://github.com/rsbrost/test_pyscan_versioning/commit/71b3bba9ce1c0395e8469294e62a0d1831dcbc1d))
* updated new_release.yml to only auto version on pull request approval to main or dev. ([358f65e](https://github.com/rsbrost/test_pyscan_versioning/commit/358f65e5ec0b875595bbf5a6d14fabe35c3195b4))
* updated new_release.yml to only auto version on pull request approval to main or dev. ([5ab2722](https://github.com/rsbrost/test_pyscan_versioning/commit/5ab272271bf833f013105c837aff3d096b5a661e))
* updated python-app.yml to only perform versioning and update changelog after the build passes all tests. ([c4d2ed1](https://github.com/rsbrost/test_pyscan_versioning/commit/c4d2ed16852f347957b4e800d7364b869d763fbd))
* updated python-app.yml to only perform versioning and update changelog after the build passes all tests. ([1a47452](https://github.com/rsbrost/test_pyscan_versioning/commit/1a47452e0e73a32f0e5a83dac3cf27ef1b442ac0))
* updated workflow permissions for versioning files. ([4b9da2e](https://github.com/rsbrost/test_pyscan_versioning/commit/4b9da2efae19774653529ef348ea2786e17c600c))
* updated workflows to now only auto-version on merge from pull request or push to main and not dev. ([90f50d2](https://github.com/rsbrost/test_pyscan_versioning/commit/90f50d2b464f9b3358e6679e134ba305bf8de2e4))
* updating, trying new things. ([4359dec](https://github.com/rsbrost/test_pyscan_versioning/commit/4359decff896c42ab3fabed3c19c2c31aca3f61b))


### Features

* added 2 workflows, one to auto version on merge from pull request, and one to auto version on push to main. ([a679f12](https://github.com/rsbrost/test_pyscan_versioning/commit/a679f12b3051824ca0f4d4fa9a9c31a359ad3848))
* added and updated workflows for more refined control in addition to auto versioning. ([2928899](https://github.com/rsbrost/test_pyscan_versioning/commit/2928899afe7c27579183ad53c5340ebe6cb168bb))
* added and updated workflows for more refined control in addition to auto versioning. ([7cc1541](https://github.com/rsbrost/test_pyscan_versioning/commit/7cc1541e6c4357a21bfad7198a8a151affa2dbff))
* added basic_build.yml to ensure install success on every build. ([a2555b6](https://github.com/rsbrost/test_pyscan_versioning/commit/a2555b6ab5d2fc4415cb49f3a3be082a0afcf6de))
* added new workflow for testing versioning temporarily. ([2fdd155](https://github.com/rsbrost/test_pyscan_versioning/commit/2fdd155d3eb90dff372467fe025b7ffdd08852d8))
* added workflow dispatch for ultimate versioning solution to temporarily test. ([842fecd](https://github.com/rsbrost/test_pyscan_versioning/commit/842fecd446a443cfdcc023d95ccd1e8260b8c361))
* run_info.py and setup.py now load version from package.json and store as attributes when run. ([1dea934](https://github.com/rsbrost/test_pyscan_versioning/commit/1dea9342215d391ef43417657e8fc6674b227738))



# [0.1.0](https://github.com/rsbrost/test_pyscan_versioning/compare/v0.0.1...v0.1.0) (2024-04-18)


### Bug Fixes

* fixing missing permissions in python-app.yml ([ff4018b](https://github.com/rsbrost/test_pyscan_versioning/commit/ff4018bb059f422445164bf1472cc1b84b143337))
* giving permissions to python-app.yml for autoversioning. ([4984c3e](https://github.com/rsbrost/test_pyscan_versioning/commit/4984c3ec6b5c558b445f4024542ef5a848104e75))
* python-app.yml updates to try and capture versioning automatically. ([b4ad18b](https://github.com/rsbrost/test_pyscan_versioning/commit/b4ad18b3c1e805d6a3ecbdddddb5a55a0fcd1502))
* trying to correct python-app.yml missing token error. ([73350bd](https://github.com/rsbrost/test_pyscan_versioning/commit/73350bdf3caaadb0b10c74d074d591e6ed5c5d55))


### Features

* added basic_build.yml to ensure install success on every build. ([3e791fb](https://github.com/rsbrost/test_pyscan_versioning/commit/3e791fb93146d5d0e16c1a269d6feb80fac142eb))



## 0.0.1 (2023-11-28)



