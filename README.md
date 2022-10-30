# README #

### Purpose of the repository ###

This repository hosts a Python-based application for threat modelling, which enables to visualise the attack tree/graph and to add values to the nodes that the application aggregates to form an overall value impact to the business of any threats identified.

### Setup ###

* Update conda

Update conda by executing the following command:

`conda update -n base -c defaults conda`

* Create the virtual environment

Create a conda virtual environment named `threat_modelling` and install the required dependencies by executing the 
following command: 

`conda env create --name threat_modelling --file environment.yml`

* Activate and deactivate the conda environment

To activate this environment, execute the following command:

`conda activate threat_modelling`

To deactivate the environment, execute the following command:

`conda deactivate`

To install the project as a package in non-editable (standard) mode:

`pip install .`

To install the project as a package in editable (development) mode:

`pip install -e .`

### Description of the solution implemented ###

### Instruction to execute the solution ###

### Testing methodology ###

### Running the tests ###

#### Evidence of testing ####

### Linting ###

For linting to ensure a consistent ordering of imports, the `isort` library was leveraged to enforce it automatically 
throughout the codebase by running the following commands: 

- `isort src` for the source codes, and 
- `isort tests` for the unit tests-related codes.

For linting to ensure adherence of the Python codes to PEP-8, besides leveraging the 'Problems' tab at the bottom of the 
PyCharm IDE throughout the development, the `autopep8` library was leveraged to enforce it automatically throughout the 
codebase by running the following command: 

`autopep8 --in-place --recursive .`

### Future work ###

### References ###
