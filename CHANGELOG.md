## [0.4.1](https://github.com/sandialabs/pyscan/compare/v0.4.0...v0.4.1) (2024-04-23)


### Bug Fixes

* corrected comment with version_when_pushed.yml ([09e4ac5](https://github.com/sandialabs/pyscan/commit/09e4ac5573ad5053dac942420e7616d81b60890a))
* updating, trying new things. ([4359dec](https://github.com/sandialabs/pyscan/commit/4359decff896c42ab3fabed3c19c2c31aca3f61b))



# [0.4.0](https://github.com/sandialabs/pyscan/compare/v0.3.0...v0.4.0) (2024-04-23)


### Bug Fixes

* deleted new_release.yml since it is not running on push. Will replace with two separate workflows. ([04ac6e2](https://github.com/sandialabs/pyscan/commit/04ac6e206311d02cdaf03200014a8e2150baee0c))
* fixing new_release.yml workflow to have proper permissions for auto versioning. ([d434314](https://github.com/sandialabs/pyscan/commit/d434314c2df54acb8c34a9f33f14ae141b67e025))
* updated manual_versioning.yml to enable workflow run on main. ([08b7401](https://github.com/sandialabs/pyscan/commit/08b7401ebd8f5d0eab1fbff399bb746474fdd0d4))
* updated new_release.yml syntax to try and fix not running on push to main. ([71b3bba](https://github.com/sandialabs/pyscan/commit/71b3bba9ce1c0395e8469294e62a0d1831dcbc1d))
* updated workflow permissions for versioning files. ([4b9da2e](https://github.com/sandialabs/pyscan/commit/4b9da2efae19774653529ef348ea2786e17c600c))


### Features

* added 2 workflows, one to auto version on merge from pull request, and one to auto version on push to main. ([a679f12](https://github.com/sandialabs/pyscan/commit/a679f12b3051824ca0f4d4fa9a9c31a359ad3848))



# [0.3.0](https://github.com/sandialabs/pyscan/compare/v0.2.1...v0.3.0) (2024-04-23)


### Bug Fixes

* added uses: actions/checkout@v3 to try and fix issue. ([bca0865](https://github.com/sandialabs/pyscan/commit/bca0865fda6a132745c477e950577d355dacc813))
* Added wiki link to contributors in README and docs index ([5a17be4](https://github.com/sandialabs/pyscan/commit/5a17be4b768d106ea8d162cfb42776e769dc5b8a))
* Fixed formatting in README and docs index ([1f080fe](https://github.com/sandialabs/pyscan/commit/1f080fecc8d43346b50a917e7defb340417dad02))
* fixed type so that all ymls are not running on push. ([15a1e1f](https://github.com/sandialabs/pyscan/commit/15a1e1f12a2c24819fe41af311ad1ad48c8345f4))
* fixed type so that all ymls are not running on push. ([2c0322d](https://github.com/sandialabs/pyscan/commit/2c0322d19171a37ca1cc827f03771e8c51b6f15a))
* fixing missing permissions in python-app.yml ([13d8a6c](https://github.com/sandialabs/pyscan/commit/13d8a6cfc7bc2d00e6b147876e527f37bc028125))
* giving permissions to python-app.yml for autoversioning. ([4654a91](https://github.com/sandialabs/pyscan/commit/4654a914d1ebe254e410ae4764e1fd7ab716c590))
* python-app.yml updates to try and capture versioning automatically. ([f213e64](https://github.com/sandialabs/pyscan/commit/f213e6468da3208f7a9c06ed4fee84d6b5c3a32a))
* Renamed workflow to temp versioning for testing. ([2ef638a](https://github.com/sandialabs/pyscan/commit/2ef638a9d29726419412bb4e49b3ea6d635668d2))
* trying to correct python-app.yml missing token error. ([d0b25c2](https://github.com/sandialabs/pyscan/commit/d0b25c2f08026dadb4ad83ebb7665c95fba42fec))
* updated new_release.yml to only auto version on pull request approval to main or dev. ([358f65e](https://github.com/sandialabs/pyscan/commit/358f65e5ec0b875595bbf5a6d14fabe35c3195b4))
* updated python-app.yml to only perform versioning and update changelog after the build passes all tests. ([c4d2ed1](https://github.com/sandialabs/pyscan/commit/c4d2ed16852f347957b4e800d7364b869d763fbd))
* updated workflows to now only auto-version on merge from pull request or push to main and not dev. ([90f50d2](https://github.com/sandialabs/pyscan/commit/90f50d2b464f9b3358e6679e134ba305bf8de2e4))


### Features

* added and updated workflows for more refined control in addition to auto versioning. ([2928899](https://github.com/sandialabs/pyscan/commit/2928899afe7c27579183ad53c5340ebe6cb168bb))
* added basic_build.yml to ensure install success on every build. ([a2555b6](https://github.com/sandialabs/pyscan/commit/a2555b6ab5d2fc4415cb49f3a3be082a0afcf6de))
* added new workflow for testing versioning temporarily. ([2fdd155](https://github.com/sandialabs/pyscan/commit/2fdd155d3eb90dff372467fe025b7ffdd08852d8))
* added workflow dispatch for ultimate versioning solution to temporarily test. ([842fecd](https://github.com/sandialabs/pyscan/commit/842fecd446a443cfdcc023d95ccd1e8260b8c361))



## [0.2.1](https://github.com/sandialabs/pyscan/compare/v0.2.0...v0.2.1) (2024-04-18)


### Bug Fixes

* updated new_release.yml to only auto version on pull request approval to main or dev. ([5ab2722](https://github.com/sandialabs/pyscan/commit/5ab272271bf833f013105c837aff3d096b5a661e))



# [0.2.0](https://github.com/sandialabs/pyscan/compare/v0.1.0...v0.2.0) (2024-04-18)


### Bug Fixes

* updated python-app.yml to only perform versioning and update changelog after the build passes all tests. ([1a47452](https://github.com/sandialabs/pyscan/commit/1a47452e0e73a32f0e5a83dac3cf27ef1b442ac0))


### Features

* added and updated workflows for more refined control in addition to auto versioning. ([7cc1541](https://github.com/sandialabs/pyscan/commit/7cc1541e6c4357a21bfad7198a8a151affa2dbff))



