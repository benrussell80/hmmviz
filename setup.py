from setuptools import find_packages, setup
import os


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='hmmviz',
    version='0.0.7',
    author='Benjamin Russell',
    description='A package for visualizing state transition graphs from hidden Markov models or other models.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/benrussell80/hmmviz',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    install_requires=[
        'hmmlearn>=0.2',
        'matplotlib>=3.1.0',
        'numpy>=1.16',
        'pandas>=0.24.2',
    ]
)

"""
Publish to PyPI:
----------------
python3 setup.py sdist bdist_wheel
twine upload dist/*

"""