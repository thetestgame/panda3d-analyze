try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = open('README.md').read()
setup(
    name='panda3d_analyze',
    description='Panda3D module that provides simplified stat collection and analysis',
    long_description=long_description,
    license='MIT',
    version='1.0.0',
    author='Jordan Maxwell',
    maintainer='Jordan Maxwell',
    url='https://github.com/NxtStudios/p3d-analyze',
    packages=['panda3d_analyze'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ])
