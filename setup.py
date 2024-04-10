from setuptools import setup, find_packages


setup(
    name='PFTL',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ["py4lab=pftl.start:start",]
        },
    install_requires=[
        'numpy',
        'pyqtgraph',
        'pyzmq',
        'pyqt5',
        'h5py',
        'pyserial',
        'pyvisa',
        'pyvisa-py',
        'opencv-python',
        'click',
        'pyyaml',
        ]
    )