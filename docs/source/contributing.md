# Contributing

We welcome contributions and feedback from the community!

## Creating a custom scoring method
All scoring methods should inherit from the {class}`ScoringMethod <arthur_bench.scoring.scoring_method.ScoringMethod>` base class and provide a custom implementation of the `run_batch` method.

A scoring method can leverage any combination of input texts, context texts, and reference texts to score candidate generations. All computed scores must be float values where a higher value indicates a better score. If you have a scoring method that does not fit these constraints, please get in touch with the Arthur team.

**Steps for adding a custom scoring method:**
- Install bench from source, in development mode:
    ```
    pip install -e . 
    ```
- Add your ScoringMethod implementation in a new file in `arthur_bench/scoring`. For scoring methods that require prompt templating, we use the [LangChain](https://python.langchain.com/) library.
- Register your scoring method by adding it to the scoring method enum in `arthur_bench/models/models.py`

At this point, you should be able to create test suites with your new scoring method and test your implementation locally.

**Contributing your scoring method**:
- Fork the bench repository and create a pull request from your fork. This [Github guide](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) provides more in depth instructions.
- Your scoring method docstring should use [Sphinx format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format) for compatibility with documentation.
- Provide unit tests for the scoring method in a separate file in the `test` directory.

