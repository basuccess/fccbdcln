from setuptools import setup, find_packages

setup(
    name='tabblockln',
    version='0.1.0',
    author='Tony Houweling',
    author_email='tony.houweling@gmail.com',
    description='A project to organize fcc bdc files and creat symbolic links in preparation for catfccbdc.py to merge the broadband service location data with the US census blocks for GIS analysis.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'os',
        're',
        'shutil',
        'zipfile',
        'logging',
        'argparse',
        'datetime'
    ],
    entry_points={
        'console_scripts': [
            'tabblockln=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
