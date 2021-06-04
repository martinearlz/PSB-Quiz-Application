# agiledev

## Testing
1. Create a new Python file under the tests folder, call it `test_{name}`. E.g, test_quiz.py

2. Put some test logic into it, take test_logic.py for reference, with proper Gherkin format and assets.

3. Go to .github/workflows, open test.yml

4. Include the new test to be executed, e.g:
`- name: Quiz testing unit testing
   run: pytest -v tests/test_quiz.py`

## Running Tests
1. `cd` to the `tests` folder.

2. Run `pytest -vv` to run all the tests. Make sure you install `pytest` beforehand, using `pip install -U pytest`.
