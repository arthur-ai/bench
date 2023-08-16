# Contributing

We welcome contributions and feedback from the community!

## Creating a custom scorer
All scorers should inherit from the {class}`Scorer <arthur_bench.scoring.scorer.Scorer>` base class and provide a custom implementation of the `run_batch` method.

A scorer can leverage any combination of input texts, context texts, and reference texts to score candidate generations. All computed scores must be float values where a higher value indicates a better score. If you have a scorer that does not fit these constraints, please get in touch with the Arthur team.

**Steps for adding a custom scorer:**
- Install bench from source, in development mode:
    ```
    pip install -e . 
    ```
- Add your Scorer implementation in a new file in `arthur_bench/scoring`. For scorers that require prompt templating, we use the [LangChain](https://python.langchain.com/) library.
- Register your scorer by adding it to the scorer enum in `arthur_bench/models/models.py`

At this point, you should be able to create test suites with your new scorer and test your implementation locally.

**Contributing your scorer**:
- Fork the bench repository and create a pull request from your fork. This [Github guide](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) provides more in depth instructions.
- Your scorer docstring should use [Sphinx format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format) for compatibility with documentation.
- Provide unit tests for the scorer in a separate file in the `test` directory.

