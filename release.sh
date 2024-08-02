rm -rf ./build ./dist ./pyhurl.egg-info
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*