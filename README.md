# safe-sports-streams

[![Build Status](https://travis-ci.com/hudson-ayers/safe-sports-streams.svg?branch=master)](https://travis-ci.com/hudson-ayers/safe-sports-streams)
[![Coverage Status](https://coveralls.io/repos/github/hudson-ayers/safe-sports-streams/badge.svg?branch=master)](https://coveralls.io/github/hudson-ayers/safe-sports-streams?branch=master)

## For Developers

### Virtual Environment
We suggest using a [virtualenv][venv], which will allow you to install this
package and its dependencies in an isolated Python environment. Once you have
Python 3 installed on your machine, you can create a virtual environment called
`.venv` by running:

```
$ virtualenv -p python3 .venv
```

Once the virtual environment is created, activate it by running:

```
$ source .venv/bin/activate
```

Any Python libraries installed will not be contained within this virtual
environment. To deactivate the environment, run:

```
$ deactivate
```

### Installing Development Environment
To work on code and test changes in the package, install it in [editable
mode][e-mode] locally in your virtualenv by running:

```
$ make dev
```

This will also install our pre-commit hooks and local packages needed for style
checks.

### Testing

We use [pytest][pytest] to run our tests. Our tests are located in the `tests/`
directory in the repo and should be run _after_ installing the package locally.
Tests can be run by calling:

```
$ pytest tests/
```

[venv]: https://virtualenv.pypa.io/en/stable/
[e-mode]: https://packaging.python.org/tutorials/distributing-packages/#working-in-development-mode
[pytest]: https://docs.pytest.org/en/latest/
