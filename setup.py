from setuptools import setup
import setuptools
import pip
import os
import re
from pip._internal.req import parse_requirements
from pathlib import Path

this_directory = Path(__file__).parent

# Load version
VERSIONFILE="step_by_step_ks/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

links = []
requires = []

requirements = parse_requirements('requirements.txt', session='hack')
requirements = list(requirements) 
try:
    requirements = [str(ir.req) for ir in requirements]
except:
    requirements = [str(ir.requirement) for ir in requirements]

setup(name='step_by_step_ks',
			version=verstr,
			description='A package to perform a 2-sample Kolmogorov-Smirnov test step by step.',
			long_description=(this_directory / "README.md").read_text(),
			#long_description=open('README.rst',encoding="utf8").read(),
			long_description_content_type='text/markdown',
			url='http://github.com/remyeltorro/step_by_step_ks',
			author='Rémy Torro',
			author_email='remy.torro@gmail.fr',
			license='MIT',
			packages=setuptools.find_packages(),
			zip_safe=False,
			install_requires = requirements,
			)

