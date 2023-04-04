from setuptools import setup, find_packages

setup(
    name='PackageName',
    version='0.1',
    author='YoursTruly',
    author_email='yourstruly@fsv.cuni.cz',
    packages= find_packages(),
    description='Exemplatory package.',
    #long_description=open('README.md').read(),
   install_requires=[
   "Django >= 1.1.1",
   "pytest",
   ],)