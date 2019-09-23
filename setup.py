from setuptools import find_packages, setup

setup(
    name='hmmviz',
    version='0.0.1',
    author='Benjamin Russell',
    description='A package for visualizing state transition graphs that often arise in hidden Markov models.',
    url='https://github.com/benrussell80/hmmviz',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)