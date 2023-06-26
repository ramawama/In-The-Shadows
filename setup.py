from setuptools import setup, Extension


module = Extension('library',
                   sources = ['libraries/library.cpp'],
                   extra_compile_args=["-fPIC"])

setup(
     name='intheshadows',
     version='0.1.0',
     packages=['intheshadows',],
     url='https://github.com/ramawama/In-The-Shadows',
     license='GPL 3',
     author='Carson Sobolewski',
     author_email='csobolewski@ufl.edu',
     description='Turn-based stealth game written in pygame!',
     install_requires=['pygame>=2.4.0', 'numpy'],
     ext_modules=[module],

     entry_points =
     {  "console_scripts":
             [
                 "intheshadows = intheshadows.main:main"
             ]
     },
    package_data = {
        '': ['assets/**/*', 'levels/**/*'],
    }
 )