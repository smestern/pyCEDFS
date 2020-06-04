from setuptools import setup


setup(
    name='pyCEDFS',
    version='0.1.3',
    author='Smestern',
    author_email='n/a',
    packages=['pyCEDFS'],
    url='https://github.com/smestern',
    license='MIT License',
    platforms='https://github.com/smestern',
    description='',
    long_description='',
    install_requires=[	
       'matplotlib>=2.1.0',
       'numpy>=1.17',
	'importlib>=3.7',
	],
	include_package_data=True,
	package_data={
        
        "": ["*.dll"]},
)
