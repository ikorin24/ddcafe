# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from ddcafe import __version__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='ddcafe',
    version=__version__,
    description='play "Daydraem cafe" on the terminal.',
    entry_points={
        "console_scripts": [
            "ddcafe = ddcafe.ddcafe:main"
        ]
    },
    long_description=readme,
    zip_safe=False,
    include_package_data=True,
    author='ikorin24',
    author_email='sunshinexxab@yahoo.co.jp',
    url='https://github.com/ikorin24/ddcafe',
    license=license_txt,
    packages=find_packages(exclude=('media', 'dev'))
)
