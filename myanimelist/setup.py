#!/usr/bin/env python

from distutils.core import setup

setup(name='malparser',
      version='0.2.6',
      description='Python package to access the MyAnimeList Anime',
      long_description=open('README.rst').read(),
      author='Anders Jensen',
      license='MIT',
      author_email='johndoee+malparser@tidalstream.org',
      url='https://github.com/JohnDoee/',
      packages=['malparser', 'malparser.test'],
      package_data={'malparser.test': ['testfiles/*/*.html']},
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

