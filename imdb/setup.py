#!/usr/bin/env python

from distutils.core import setup

def read_description():
    import os
    path = os.path.join(os.path.dirname(__file__), 'README.rst')
    try:
        with open(path) as f:
            return f.read()
    except:
        return 'No description found'


setup(
    name='imdbparser',
    version='1.0.0',
    description='Python package to access the IMDB Movies',
    long_description=read_description(),
    author='Anders Jensen',
    license='MIT',
    author_email='johndoee+malparser@tidalstream.org',
    url='https://github.com/JohnDoee/',
    packages=['imdbparser'],
    install_requires=['lxml'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
  ]
)

