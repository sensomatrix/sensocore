# SensoMatrix

SensoMatrix, is a software platform which will take the data from different portable biosensors as input, automate the pre-processing, plot the data, display basic metrics and give the user the ability to run the signal processing operations commonly used in the analysis of electrophysiological signals. A combination of digital signal processing (DSP) techniques and statistical methods will be used to implement features such as signal classification, correlation between different signals and outlier detection. Methods pertaining to specific types of electro-physiological signals such as electroencephalography (EEG) and electrocardiogram (ECG) will also be implemented to facilitate their analysis.

## Prerequisites

### Python 3.5.4

#### Windows
Please install the version [Python 3.5.4](https://www.python.org/downloads/windows/)

#### Mac OS X
Please install the version [Python 3.5.4](https://www.python.org/downloads/mac-osx/)

#### Linux
Please follow [these](https://github.com/pyenv/pyenv-installer) instructions to install **pyenv**

Once pyenv has been downloaded, install Python 3.5.4 using the following commands
```bash
pyenv install 3.5.4
```

### ECG Classification Model
Please this [link](https://drive.google.com/open?id=1GcKqrWzMDVoEnCCxFmA8SPq_rGzPrij1)

Once downloaded, make sure that the path of this file is in sensobox folder


## Installation
Once you have installed Python follow the instructions below making sure that you are at the root folder
```bash
# Install the python packages
pip install pipenv

pipenv install --python 3.5.4
pipenv shell
```

## Running
To run the application simply type the following in command line
```bash
# Activating virtual environment if not already have
pipenv shell

python main.py
```

## Documentation
More information about documentation can be found [here](https://sensomatrix.readthedocs.io/en/latest/index.html)
