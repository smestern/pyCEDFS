from setuptools import setup
import os
# load the descripntion
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.abspath(PATH_HERE+"/README.md"), encoding='utf-8') as f:
    long_description = f.read()
    print("loaded description: (%s lines)" % (long_description.count("\n")))

setup(
    name='pyCEDFS',
    version='0.1.6.3',
    author='Smestern',
    author_email='smestern@gmail.com',
    packages=['pyCEDFS'],
    url='https://github.com/smestern',
    license='MIT License',
    platforms='https://github.com/smestern',
    description='A python package to read data from CFS files generated by the signal software from CED systems',
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url = '',
    install_requires=[	
       'matplotlib>=2.1.0',
       'numpy>=1.17',
       'pynwb==1.4.0',
       'python_dateutil==2.8.1',
       'x_to_nwb==0.2.2'
	],
	include_package_data=True,
	package_data={
        
        "": ["*.dll"]},
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development ',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
         ],
)
