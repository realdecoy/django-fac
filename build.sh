# 1. Installing the virtual environment package
pip install --upgrade virtualenv

# 2. Creating and activating virtual environment
virtualenv venv
source venv/bin/activate

# 3. Installing packaging and deployment dependencies
pip install --upgrade  build setuptools twine

# 4. Building Python package
python3 -m build

# 5. Deploying python package
twine upload --verbose dist/*