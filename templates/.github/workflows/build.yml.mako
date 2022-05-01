<%!
    import config.python
    import pydmt.helpers.python
%>name: build
on: [push, pull_request, workflow_dispatch]
jobs:
  build:
    runs-on: ${"${{ matrix.os }}"}
    strategy:
      matrix:
        os: ${pydmt.helpers.python.get_list_unquoted(config.python.test_os)}
        python-version: ${pydmt.helpers.python.get_list_unquoted(config.python.test_python)}
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${"${{ matrix.python-version }}"}
      uses: actions/setup-python@v3
      with:
        python-version: ${"${{ matrix.python-version }}"}
    - name: Install python dependencies
      run: python -m pip install -r requirements.txt
    - name: Build
      run: pymakehelper run_make
