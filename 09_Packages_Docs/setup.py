from setuptools import setup

setup(
    name='PackageName',
    version='0.1',
    author='YoursTruly',
    author_email='yourstruly@fsv.cuni.cz',
    packages=['package_name','package_name.test'],
    url='',
    license='LICENSE.txt',
    description='Exemplatory package.',
    long_description=open('README.md').read(),
   install_requires=[
   "Django >= 1.1.1",
   "pytest",
   ],)