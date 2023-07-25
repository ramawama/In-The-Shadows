from setuptools import setup


setup(
     name='intheshadows',
     version='1.0.0',
     packages=['intheshadows',],
     url='https://github.com/ramawama/In-The-Shadows',
     license='GPL 3',
     author='Carson Sobolewski',
     author_email='csobolewski@ufl.edu',
     description='Turn-based stealth game written in pygame!',
     install_requires=['pygame>=2.4.0', 'numpy>=1.25.0', 'igraph>=0.10.5', 'texttable>=1.6.7'],

     entry_points =
     {  "console_scripts":
             [
                 "intheshadows = intheshadows.main:main"
             ]
     },
    package_data = {
        '': ['assets/**/*', 'levels/**/*', 'libraries/*'],
    }
 )