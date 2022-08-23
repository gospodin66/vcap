# Makefile for python code
# 
# > make help
#
# The following commands can be used.
#
# init:  sets up environment and installs requirements
# install:  Installs development requirments
# format:  Formats the code with autopep8
# lint:  Runs flake8 on src, exit if critical rules are broken
# clean:  Remove build and cache files
# env:  Source venv and environment files for testing
# leave:  Cleanup and deactivate venv
# test:  Run pytest
# run:  Executes the logic

VENV_PATH='env/bin/activate'
ENVIRONMENT_VARIABLE_FILE='.env'


PHONY=all init install-upgrade wheels install package-dist package-local clean clean-upgrade enter leave

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)


init: ## sets up environment and installs requirements
init:
	pip install -r requirements.txt
	pipenv install -r requirements.txt

install-d: ## Installs development requirments
install-d:
	python -m pip install --upgrade pip
	pip install setuptools wheel pytest

install-e: ## Installs development requirments
install-e:
	pip install -r requirements.txt
	pip install -e .

install: ## Install
install:
	python -m pip install --upgrade pip
	python setup.py install
	python -m pip install --no-clean .

install-wheel: ## Install package wheel
install-wheel:
	pip install --no-clean --force-reinstall wheels/*.whl

get-wheels: ## Download wheels (*.whl)
get-wheels:
	pip wheel -r requirements.txt --wheel-dir ./wheels
	pip wheel . --wheel-dir ./wheels

wheels: ## Create binary wheel distro
wheels:
	python setup.py bdist_wheel

package-dist: # Create source (tarball) and wheel distribution
package-dist:
	python setup.py bdist_wheel
	python setup.py sdist --formats=zip,gztar,bztar,ztar,tar

package-local: ## Don't generate anything, just install locally
package-local:
	python setup.py develop

clean: ## Remove build and cache files
clean: clean-upgrade
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf tests
	rm -rf wheels
	rm -rf .pytest_cache
	rm -rf log
	rm -rf vcap-0.0.1
	rm -rf src/vcap/__pycache__
	find . -name \*.pyc -exec rm -v {}
	find . -name \*.egg-info -exec rm -vr {}
clean-upgrade: ## Installs development requirments
clean-upgrade:
	pip uninstall -y flake8 iniconfig pyparsing pyflakes pycodestyle py pluggy mccabe attrs packaging flake8
					 
enter: ## Cleanup and deactivate venv
enter: 
	. /home/cheki/.local/share/virtualenvs/pythonenv-IfSpZUPS/bin/activate
leave: ## Cleanup and deactivate venv
leave: clean
	deactivate

.PHONY: $(PHONY)