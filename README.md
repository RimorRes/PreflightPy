# PreFlight

[![PyPI](https://img.shields.io/pypi/v/preflightpy?color=blue)](https://pypi.org/project/preflightpy/)
[![GitHub](https://img.shields.io/github/license/Oxyde2/Preflight?color=yellow)](LICENSE)

[![Coverage Status](https://coveralls.io/repos/github/Oxyde2/Preflight/badge.svg?branch=master)](https://coveralls.io/github/Oxyde2/Preflight?branch=master)
[![Build Status](https://travis-ci.com/Oxyde2/Preflight.svg?branch=master)](https://travis-ci.com/Oxyde2/Preflight)

[![Gitmoji](https://img.shields.io/badge/gitmoji-%20%F0%9F%98%9C%20%F0%9F%98%8D-FFDD67.svg?)](https://gitmoji.carloscuesta.me/)

Python module for **S**imulation and **O**ptimization of **R**ocket **T**rajectories, [**SORT**](https://www.nasa.gov/pdf/140648main_ESAS_17a.pdf) for short.
- Altitude prediction
- State prediction
- Flight trajectory optimization
- Flight plan optimization

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


## Installation

You can get Preflight from pip via `pip install preflight`. To contribute
to the package, check out our [contribution guidelines](CONTRIBUTING.md) and preform the following steps.

### Contribuitng

#### Cloning

 1. Cloning
    Through the command line, get to the directory you wish to clone the repository into then run the following command.
    ```
    git clone https://github.com/Oxyde2/Preflight.git
    ```

2. Downloading the ZIP
    Download the compressed files and unzip them.

#### Prerequisites

To install the required python modules just run the following command in the command line at the root of the repository.

```
pip install -r requirements.txt
```

Once you have successfully obtained your local copy and the dependencies, open the project folder in your desired IDE or text editor.

**PreFlight requires Python 3.6+ and is not compatible with
Python 2.x.**

## Built With

* [Matplotlib](https://matplotlib.org/) - To draw the graphs
* [PyInstaller](https://pyinstaller.readthedocs.io/) - To build executable files.
* [PIP](https://pip.pypa.io/) - Python dependency manager.

## Versioning

The versioning is formatted to Semantic Versioning 2.0.0 standards. [SemVer](https://semver.org/).
The changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
For available versions, see the [releases of this project](https://github.com/Oxyde2/Preflight/releases).

## Authors

* **Maxime Djomby** - *Initial work* - [Oxyde2](https://github.com/Oxyde2/)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Early development of Preflight was supported by [Mix_42](https://github.com/42mix).
The website [Rocket & Space Technology](http://www.braeunig.us/space/), written by Robert A. Braeunig, was used for pressure, density and temperature formulas for the atmospheric model.
