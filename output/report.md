# Repository Analysis Report - python_stat_tests_visualisation

This report provides a detailed analysis of the repository [python_stat_tests_visualisation](https://github.com/sofiapopp/python_stat_tests_visualisation).

## Repository Overview

The repository **python_stat_tests_visualisation** contains the Python package `RR_PROJECT_BULATOVA_POPP` (referred to as `rr_project_bulatova_popp` in the source code). It is designed to perform automated statistical hypothesis testing and data visualization. The package automatically selects the appropriate parametric or non-parametric test based on the distribution (normality) and variance (homoscedasticity) properties of the input data, providing integrated visual representations of the results.

## Project Structure

The project has the following directory structure:

- **`rr_project_bulatova_popp/`**: The core package directory containing:
  - `__init__.py`: Package initialization exposing key test classes.
  - `ABCTest.py`: Defines the `StatisticalTest` abstract base class.
  - `PairedTestClass.py`: Implements the `PairedTtest` class for paired samples.
  - `IndependentTestClass.py`: Implements the `IndependentTtest` class for independent samples.
  - `AnovaTestClass.py`: Implements the `MultiGroupTest` class for multiple group comparisons.
- **`example/`**: Contains `usage_example.ipynb`, a Jupyter Notebook showcasing library usage.
- **`images/`**: Contains images for the README documentation.
- **`build/` & `RR_PROJECT_BULATOVA_POPP.egg-info/`**: Build artifacts generated during compilation/packaging.
- **`setup.py`**: Package installation script.
- **`.gitignore`**: Version control exclusion file.
- **`LICENSE`**: MIT license file.
- **`README.md`**: Project documentation.

## Technologies

The project is built on the following technologies:

- **Programming Language**: Python 3.x
- **Data Science & Manipulation**: `pandas`, `numpy`
- **Scientific Computing & Statistics**: `scipy` (`scipy.stats` for Shapiro-Wilk, D'Agostino-Pearson, ANOVA, Wilcoxon, Mann-Whitney U, Alexander-Govern, Bartlett, and T-tests)
- **Visualization**: `matplotlib`, `seaborn`, `joypy` (for joyplots)
- **Packaging/Build Tools**: `setuptools`

## Strengths

- **Object-Oriented Design**: Utilizes an abstract base class (`StatisticalTest`) to enforce a consistent API across different test types.
- **Automated Test Selection**: Automates the statistical workflow by running pre-requisite assumption checks (normality, variance homogeneity) and choosing the correct statistical test dynamically.
- **Built-in Visualizations**: Bundles analytical results with visualizations (QQ plots, KDE overlays, Joyplots, Boxplots) that enhance interpretability.
- **Strong Input Checking**: Concrete class constructors validate dataframe types, check for missing columns, ensure data values are numeric and finite, and verify sample size constraints.

## Potential Issues

- **Committed Build Artifacts**: The `build/` and `.egg-info/` directories are committed to version control. This can lead to conflicts and bloat in the git history.
- **Redundant/Duplicate Code**: The file `build/lib/rr_project_bulatova_popp/module1.py` is committed. It duplicates much of the class code in a single module and contains outdated method naming (e.g., `run_multi_group_test` instead of `run_test`).
- **SciPy Mode Compatibility Issue**: In `ABCTest.py` line 38, calling `st.mode(arr)` stores the complete `ModeResult` object in the dataframe. In modern SciPy versions, this returns a tuple (mode array, count array) rather than a scalar, which can cause formatting errors downstream.
- **Spelling Typos**:
  - `not_lurge_length` in `AnovaTestClass.py` and `IndependentTestClass.py` (should be `not_large_length`).
  - `lenght` in `PairedTestClass.py` (should be `length`).
- **Matplotlib Blocking**: Visualizations call `plt.show()` inside the library classes, blocking execution and preventing the user from customizing, saving, or embedding the generated figures in custom layouts.
- **Windows-Specific Paths**: The README contains Windows-specific paths like `'..\\Datasets\\dataset_1.csv'`.
- **Incomplete Automations**:
  - `AnovaTestClass.py`'s `run_test()` has a `check_variance` parameter defaulting to `False`. If `False`, it runs standard ANOVA without testing homoscedasticity, violating assumption-checking flow.
  - `IndependentTestClass.py` lacks an automated check for homoscedasticity to decide between Student's T-Test and Welch's T-Test.

## Recommendations

1. **Clean Up Version Control**: Remove `build/` and `RR_PROJECT_BULATOVA_POPP.egg-info/` folders from git and add them to `.gitignore`.
2. **Remove Outdated Code**: Remove the `module1.py` file to avoid confusion.
3. **Fix SciPy Mode Usage**: Update `st.mode(arr)` in `ABCTest.py` to extract the mode value safely (e.g., `st.mode(arr, keepdims=True).mode[0]`).
4. **Fix Typos**: Rename `not_lurge_length` to `not_large_length` and `lenght` to `length`.
5. **Decouple Plotting**: Modify plot functions to return the Matplotlib `fig` and `ax` objects instead of calling `plt.show()` directly.
6. **Improve Independent T-Test selection**: Implement an automated homoscedasticity test (e.g., Levene's test) in `IndependentTtest.run_test()` to automatically toggle `equal_var`.
7. **Ensure Path Portability**: Use `os.path` or `pathlib` for file paths in example code and documentation.
