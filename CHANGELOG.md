# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Default OPRF asset repo changed from "NikolaiVChr/OpRedFlag" to "Op-RedFlag/OpRedFlag"

## [0.10] - 2024-10-14

### Changed
- Updated py-opredflag to v0.3.0
- Updated runner to use python 3.12

## [0.9.1] - 2024-10-14

### Fixed

- Fixed system-wide install on Ubuntu 24.04 LTS by pinning python to v3.11

## [0.9] - 2023-12-07

### Added
- Added full support for semver spec including pre-releases and build metadata
- Added new "none" choice for compatibility parameter
- Added a new branch input to configure which branch the action should run on

### Changed

- Updated py-opredflag to v0.2.0

## [0.8] - 2023-09-30

### Changed

- Changed default commit message
- Updated py-opredflag to v0.1.0

### Fixed

- Update pip before installation
- Set default commit message if blank

## [0.7] - 2023-09-28

### Added

- Added commit_message parameter

## [0.6] - 2023-09-27

### Fixed

- Fixed workflow expression syntax issue
- Fixed python version incompatibility

## [0.5] - 2023-09-27

### Added

- Added new "compatibility" parameter

### Removed

- Removed "major" parameter in favor of "compatibility" parameter

### Fixed

- Set commit author if scheduled

## [0.4] - 2023-09-21

### Added

- Added multi-keys (multiple copies of one file)

## [0.3] - 2023-09-21

### Added

- Added "strict" parameter

### Fixed

- Fixed bug where "major" parameter was always set to "true"

## [0.2.1] - 2023-09-21

No major changes

## [0.2] - 2023-09-21

### Changed

- Default OPRF asset repo changed from "BobDotCom/OpRedFlag" to "NikolaiVChr/OpRedFlag"

## [0.1] - 2023-09-21

### Added

- Initial version


[unreleased]: https://github.com/BobDotCom/oprf-asset-updater/compare/v0.10...HEAD
[0.10]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.10
[0.9.1]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.9.1
[0.9]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.9
[0.8]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.8
[0.7]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.7
[0.6]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.6
[0.5]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.5
[0.4]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.4
[0.3]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.3
[0.2.1]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.2.1
[0.2]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.2
[0.1]: https://github.com/BobDotCom/oprf-asset-updater/releases/tag/v0.1
