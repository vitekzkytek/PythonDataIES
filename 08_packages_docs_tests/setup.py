from setuptools import setup, find_packages

setup(
    name='PackageName',
    version='0.1',
    author='YoursTruly',
    author_email='yourstruly@fsv.cuni.cz',
    packages= ["src"], #find_packages(),
    description='Exemplatory package.',
    #long_description=open('README.md').read(),
   install_requires=[
   "pytest",
   ],)