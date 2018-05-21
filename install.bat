
python -m pip uninstall tec
::python setup.py install
python setup.py sdist
python -m pip install dist/tec-2.0.7.tar.gz 
pause