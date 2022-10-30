# README - Executive summary and app presentation #

### Purpose of the repository ###

This repository hosts a Python-based application for threat modelling, which enables to visualise the attack 
tree/graph by running the `app.py` file and to add values to the nodes (in the `json` file/s under the `src/configs` 
folder) that the application aggregates to form an overall value impact to the business of any threats identified, which 
is shown on the first node of the attack tree at the centre of it, as illustrated on the screenshots under the 
`docs/evidence_of_testing/attack_trees` folder.

### Setup ###

* Update conda

Update conda by executing the following command:

`conda update -n base -c defaults conda`

* Create the virtual environment

Create a conda virtual environment named `threat_modelling` and install the required dependencies/libraries
(listed in the `environment.yml` file) by executing the following command: 

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

The repository's structure follows a Python package-like structure with a `setup.py`, `setup.cfg`, and `pyproject.toml` 
files, along with an `environment.yml` with all required dependencies. Instructions to install them are provided above.
As expected, the `tests` folder follows the structure of the codes laid out under the `src` folder. 

The solution implemented leverages two main libraries in Python, as follows:
- `networkx` to build an attack tree of nodes and edges, inspired by the library's 'weighted graph' (NetworkX, 2022) 
as it is important to show the monetary amount and probability associated with each node, 
where each node represents a security threat and each edge captures the relationship between the threats identified 
pre- and post-digitalisation. To optimise the utilisation of space of the image canvas, instead of drawing it as 
a top-down tree, which would have been otherwise hard to read, the attack tree was designed such that the node at the 
centre is the starting point of the tree, which displays the total monetary amount and overall probability of 
occurrence that were respectively computed as the sum of the monetary amounts and the average of the child 
nodes' probabilities (Hess _et al_., 2007). The child nodes' probabilities were obtained by multiplying any probabilities 
of the threats represented under them as children of such child nodes, thus considered as independent events 
(Bertsekas & Tsitsiklis, 2008).
- `matplotlib` to visualise the above-mentioned attack tree and save it to an .svg image file, which enables to view it 
and zoom on it without losing its resolution.

Two `json` files were created and stored/versioned under the `src/threat_modelling/configs` folder, as follows:
- the `pre_digitalisation.json` file with the threats identified prior to the suggested digitalisation, including the 
monetary amount and probability of occurrence for each security threat on each leaf node;
- the `post_digitalisation.json` file with the threats identified further to the suggested digitalisation, including the 
monetary amount and probability of occurrence for each business threat on each leaf node.

Three main Python files were created as follows:
- the `app.py` that implements the function `visualise_and_save_attack_tree` to view and save an attack tree given the 
path to a json file with the specifications of the attack tree as mentioned above and the chosen output image file name;
- the `utils.py` that has the following utility-based functions:
  - `extract_threats_dict_from_json` that extracts a dictionary of security threats from a json file;
  - `format_text_on_node` that formats the textual description shown on each node of the attack tree, which outlines 
    the security threat it represents, along with its associated monetary amount and probability of occurrence.
  - `get_list_of_probs_and_monet_amounts_from_children_dict` that extracts the list of probabilities and monetary 
    amounts from a list of dictionaries of children nodes of an attack tree. 
- the `constants.py` has the key constants used throughout the application for ease of maintainability and reusability.

### Instruction to execute the solution ###

Run the `app.py` after inputting the `path_to_json` and `output_file_name` in the function 
`visualise_and_save_attack_tree` at lines 196 and 197 of the `app.py` file respectively, which 
will have the path of the json file to read the configuration of the attack tree considered and the 
name of the output image file to save this attack tree after visualising it.

In particular:
- To visualise and output the attack tree **pre-digitalisation**, please pass the constants 
`PATH_TO_PRE_DIGITAL_JSON` and `OUTPUT_FILE_ATTACK_TREE` (defined in the `src/threat_modelling/constants.py` file) 
to the argument `path_to_json` of the function `visualise_and_save_attack_tree` at the bottom of the `app.py` file.
Thereafter, run the `app.py` file.
- To visualise and output the attack tree **post-digitalisation**, please pass the constants 
`PATH_TO_POST_DIGITAL_JSON` and `OUTPUT_FILE_ATTACK_TREE_POST_DIGITAL` (defined in the 
`src/threat_modelling/constants.py` file) to the argument `path_to_json` of the function 
`visualise_and_save_attack_tree` at the bottom of the `app.py` file. Thereafter, run the `app.py` file.

### Testing methodology ###

Functional testing was performed throughout the development and the results showing the successful operation or 
execution of the application were saved to cover both cases considered (pre- and post-digitalisation) as per the 
sub-section below named `Evidence of testing`.

The required unit tests were implemented in the file `tests/threat_modelling/test_utils.py`, which makes use of the 
`dummy_lists.py` file to import a rather long list for the required unit testing.

Furthermore, linting was performed as per the sub-section named `Linting` below.

### Running the tests and evidence of testing ###

Evidence of functional testing (by running the `app.py` file) was provided as screenshots under 
the `docs/evidence_of_testing/successful_operation` folder into two sub-folders (`pre_digitalisation` and 
`post_digitalisation`); the related attack trees generated as a result of running the application are stored 
under the `docs/evidence_of_testing/attack_trees` folder.

To run the unit tests, please run the file `tests/threat_modelling/test_utils.py`. Evidence that the unit tests 
passed is provided under the `docs/evidence_of_testing/unit_tests_passed_output` folder 
via the screenshot on the file `unit_tests_passed.png`.

Linting was also performed as per the sub-section named `Linting` below and evidence of running the linters `flake8` and 
`pylint` (before and after linting the codes) is provided under the folder `linting_outputs`, which via `pylint` quantifies 
the score before linting on the screenshot at 
`docs/evidence_of_testing/linting_outputs/before_linting/pylint_report/pylint_before_linting_2.png` as `3.37/10` and 
after linting on the screenshot at 
`docs/evidence_of_testing/linting_outputs/after_linting/pylint_report/pylint_after_linting_improved.png` as `7.89/10` 
(improved, as expected).

Furthermore, a security vulnerability scan was performed by running `safety check` (via the `safety` library); 
three security vulnerabilities were identified due to the outdated version of the library `numpy` used 
(version `1.21.5`) in Python `3.7.10`; thus, Python had to be upgraded to `3.8.1` to be able to upgrade `numpy` to 
the version `1.22.2` (as per the `environment.yml` file) that includes the fix to the vulnerabilities detected. 
Evidence of the security vulnerabilities scans performed before and after upgrading Python and numpy is stored 
under the `docs/evidence_of_testing/security_vulnerability_scans` folder.

### Linting ###

Both `flake8` and `pylint` were leveraged for linting the codes (by running `flake8 src` and `pylint src`) and, 
based on their initial reports, the codes were enhanced accordingly and follow-up/improved reports were generated.

For linting to ensure a consistent ordering of imports, the `isort` library was used to enforce it automatically 
throughout the codebase by running the following commands: 

- `isort src` for the source codes, and 
- `isort tests` for the unit tests-related codes.

For linting to ensure adherence of the Python codes to PEP-8 (Van Rossum _et al_., 2001), besides leveraging the 
'Problems' tab at the bottom of the PyCharm IDE throughout the development, the `autopep8` library was leveraged 
to enforce it automatically throughout the codebase by running the following command: 

`autopep8 --in-place --recursive .`

### References ###

- Bertsekas, D., & Tsitsiklis, J. N. (2008) _Introduction to probability_. Vol. 1. Athena Scientific.
- Hess, R. O., Holt, C. A., & Smith, A. M. (2007) Coordination of strategic responses to security threats: 
Laboratory evidence. _Experimental Economics_ 10(3): 235-250.
- NetworkX (2022) Weighted Graph. 
Retrieved from https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html on October 25th, 2022.
- Van Rossum, G., Warsaw, B., & Coghlan, N. (2001) PEP-8 - style guide for Python code. _Python.org_ 1565.