# PreFlight

Python programs for rocket flight emulation.
- Altitude prediction
- State prediction
- Flight trajectory optimization
- Flight plan optimization

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python3.x for running the `.py` files.

To install the required python modules just run the following command in the command line.

```
pip install -r requirements.txt
```

### Installing

 1. Cloning
    Through the command line, get to the directory you wish to clone the repository into then run the following command.
    ```
    git clone https://github.com/Oxyde2/Preflight.git
    ```

2. Downloading the ZIP
    Download the compressed files and unzip them.

Once you have successfully obtained your local copy open the project folder in your desired IDE or text editor.

Great! You're all set now!

### Launch the program!

1. Running the `.exe` file **Unvailable in versions inferior to 0.5.0**

    - Navigate through the command-line:
      ```bash
      cd dist/PreFlight
      ./PreFlight.exe
      ```
    - Or find the file through the file explorer.

2. Running the `.py` file **Unavailable in version 0.5.0-alpha.1**

    **You need to have Python3.x installed and have it's paths in the PATH environmental variable**

    - Navigate from the PreFlight folder:
      ```bash
      cd dist/PreFlight
      python PreFlight.py
      ```
    - Or find the file through the file explorer.

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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Mix_42](https://github.com/42mix)
