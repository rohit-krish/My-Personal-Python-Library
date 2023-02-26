from setuptools import find_packages, setup

setup(
    name='mylib',
    packages=find_packages(include=['mylib']),
    version='1.1.1',
    description='My Personal Libraries',
    author='Rohit Krishna',
    install_requires=['numpy', 'opencv-python', 'filterpy', 'scipy']
)
