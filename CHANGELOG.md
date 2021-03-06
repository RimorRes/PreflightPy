# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning: [SemVer](https://semver.org/).

## [Unreleased]
### Additions
- Implementation of earth gravity/radius latitude model
- Unit tests for said models

## [0.6.2] - 2020-2-18
### Added
- Gravity now changes according to altitude

### Fixed
- Unit tests to accept deviations under threshold

## [0.6.1] - 2020-2-17
### Added
- Unit tests for density heterosphere model

### Fixed
- Density calculation in `env.py`

## [0.6.0] - 2019-11-2
### Added
- Unit tests for heterosphere model
- Unit tests for `params.py`
- Linting using `flake8`

### Changed
- `env.py` for 86km - 1000km support

## [0.5.0] - 2019-11-1
### Added
- `env.py` for the `Environment` class
- `case.json` for input
- `.json` input file support
- `.csv` output file support
- `.gitignore` file
- Unit tests
- Travis CI and Coveralls

### Changed
- `params.py` for `.json` input support
- `system.py` for `.csv` output support
- REQUIREMENTS.txt

### Fixed
- Environment model

## [0.4.0] - 2019-10-23
### Added
- `LICENSE.md`
- `Requirements.txt` for PIP

### Changed
- Restructured repo using [Repository Structure and Python](https://www.kennethreitz.org/essays/repository-structure-and-python)

### Removed
- `/Core` folder
- `ConsoleClass.py`

## [0.3.1] - 2019-09-28
**Development is no longer discontinued! :tada:**
### Changed
- README.md
- Moved repo GitLab→ GitHub

## [0.3.0] - 2019-02-20
### Added
- "--graph" option in "run" command to display graphs

## [0.2.0] - 2019-02-19
### Added
- Full implementation of console-like inputs

## [0.1.0] - 2019-02-15
### Added
- Progress bar using ascii graphics


## [0.0.0] - 2019-02-13
### Added
- This CHANGELOG file
- README file
- Progress from RFTE version 3.6
