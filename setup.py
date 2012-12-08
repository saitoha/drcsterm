# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from drcsterm import __version__, __license__, __author__

setup(name                  = 'drcsterm',
      version               = __version__,
      description           = 'UCS Private Area (Plain 16) -> DRCS conversion filter for terminal',
      long_description      = open("README.rst").read(),
      py_modules            = ['drcsterm'],
      eager_resources       = [],
      classifiers           = ['Development Status :: 4 - Beta',
                               'Topic :: Terminals',
                               'Environment :: Console',
                               'Intended Audience :: End Users/Desktop',
                               'License :: OSI Approved :: GNU General Public License (GPL)',
                               'Programming Language :: Python'
                               ],
      keywords              = 'DRCS terminal',
      author                = __author__,
      author_email          = 'user@zuse.jp',
      url                   = 'https://github.com/saitoha/drcsterm',
      license               = __license__,
      packages              = find_packages(exclude=[]),
      zip_safe              = True,
      include_package_data  = False,
#      install_requires      = ['tff >=0.0.9, <0.1.0'],
      install_requires      = [],
      entry_points          = """
                              [console_scripts]
                              drcsterm = drcsterm:main
                              """
      )

