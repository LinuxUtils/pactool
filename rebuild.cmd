rm -rf build dist pactool.egg-info pactool_linuxutils.egg-info
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*