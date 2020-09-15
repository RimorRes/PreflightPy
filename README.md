<div align="center"><img src="https://user-images.githubusercontent.com/53187347/77073741-01b61880-69f0-11ea-9e3f-0c3eb92718b7.png" width="600"/></div>

# PreflightPy

[![PyPI](https://img.shields.io/pypi/v/preflightpy?color=blue)](https://pypi.org/project/preflightpy/)
[![GitHub](https://img.shields.io/github/license/Oxyde2/Preflight?color=yellow)](LICENSE)

[![Coverage Status](https://coveralls.io/repos/github/Oxyde2/Preflight/badge.svg?branch=master)](https://coveralls.io/github/Oxyde2/Preflight?branch=master)
[![Build Status](https://travis-ci.com/RimorRes/Preflight.svg?branch=master)](https://travis-ci.com/RimorRes/Preflight)

[![Gitmoji](https://img.shields.io/badge/gitmoji-%20%F0%9F%98%9C%20%F0%9F%98%8D-FFDD67.svg?)](https://gitmoji.carloscuesta.me/)
[![Documentation Status](https://readthedocs.org/projects/preflight/badge/?version=latest)](https://preflight.readthedocs.io/en/latest/?badge=latest)

Python module for **S**imulation and **O**ptimization of **R**ocket **T**rajectories, [**SORT**](https://www.nasa.gov/pdf/140648main_ESAS_17a.pdf#page=19) for short.
- Altitude prediction
- State prediction
- Flight trajectory optimization
- Flight plan optimization

## Quick Start :vertical_traffic_light:

Before we get started, please note that PreflightPy was built with **Python 3.x** in mind and might not be compatible with older versions.

### Installation

Getting yourself your very own copy of this module is super simple!
You can get Preflight from pip using your terminal via the following command:

  ```bash
  pip install preflight
  ```

That's it you're set!

### Usage

Here's an example of typical usage of this package:

  ```python
  # Importing the module
  import preflightpy as pre

  # The 'Parameters' class collects info about the rocket and environmental conditions etc. from the input file.
  params = pre.Parameters("path/to/input/file.json")  

  #  The 'Environment' takes care of computing conditions (e.g. atmosphere, gravity) at various altitudes.
  env = pre.Environment(params.env_variables)

  # Specify the burn time of your engine in seconds.
  burn_time = 10

  # The 'System', the core of this module, it takes care of the main simulation and output.
  s = pre.System(params, env, burn_time)  

  s.launch()  # Blast off! Launches the simulation.

  # The results are outputted in .csv and .log formats and are located in the output folder specified by input file
  ```

The following is the format you'll have to use in your `.json` input files:

  ```json
  {
    "Engine" : {
      "Type" : "Liquid",
      "Specific impulse (s)" : 318,
      "Thrust (N)" : 500
    },
    "Fuel" : {
      "Oxidizer/fuel mixture ratio" : 15,
      "Fuel reserve (%)" : 5
    },
    "Mass" : {
      "Dry Mass (kg)" : 10
    },
    "Aerodynamics" : {
      "Drag coefficient" : 0.0556,
      "Cross-section (m2)" : 0.0255364
    },
    "Environment" : {
      "Elevation (m)" : 113,
      "Simulation step (s)" : 0.01,
      "Standard gravity (m/s2)" : 9.80665,
      "Air molar mass (kg/mol)" : 0.02896968,
      "Gas constant (J/(K.mol))" : 8.314462618,
      "Air heat capacity ratio" : 1.4,
      "Standard atmospheric pressure @SL (Pa)" : 101325
    },
    "Output" : {
      ".log file" : "Flight.log",
      ".csv file" : "Flight.csv"
    }
  }
  ```

## Documentation :pencil:

Visit our [documentation](https://preflight.readthedocs.io/en/latest/) to learn how to use `PreflightPy` in depth.

## Contribuitng :earth_americas:

If you want to contribute to this project, this set of instructions will get a copy up and running on your local machine for development and testing purposes! Once you're done, check out our [contribution guidelines](CONTRIBUTING.md) before you get started.

### Installation

To get a copy of the repository you'll have to clone it.
Through the command line, get to the directory you wish to clone the repository into then run the following command.

  ```bash
  git clone https://github.com/Oxyde2/Preflight.git
  ```

### Prerequisites

We're almost done, next step is to fetch our dependencies.
To install the required python modules just run the following command in the command line at the root of the repository folder.

  ```bash
  pip install -r requirements.txt
  ```

### Conclusion

Congratulations, you have successfully obtained your local copy and the dependencies!
Now open the project folder in your desired IDE or text editor and get crackin'!



## Built With :construction_worker:

* [Matplotlib](https://matplotlib.org/) - To draw the graphs.

## Versioning :bookmark:

The versioning is formatted to Semantic Versioning 2.0.0 standards. [SemVer](https://semver.org/).
The changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
For available versions, see the [releases of this project](https://github.com/Oxyde2/Preflight/releases).

## Authors :floppy_disk:

* **Maxime Djomby** - *Initial work* - [Oxyde2](https://github.com/Oxyde2/)

## License :page_with_curl:

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments :trumpet:

Early development of Preflight was supported by [Mix_42](https://github.com/42mix).
The website [Rocket & Space Technology](http://www.braeunig.us/space/), written by Robert A. Braeunig, was used for pressure, density and temperature formulas for the atmospheric model.
