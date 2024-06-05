from setuptools import setup

setup(
    name='mVarScan',
    version='0.1.0',    
    description='An implementation of the existing VarScan tool (specifically mpileup2snp option). Used to find SNPs given a .mpileup file',
    url='https://github.com/andrewbigelow/mVarScan/tree/main',
    author='Andrew Bigelow, Numaan Formoli, Aditya Parmar',
    author_email='abigelow@ucsd.edu, nformoli@ucsd.edu, atparmar@ucsd.edu',
    license='N/A',
    packages=['mVarScan'],
    install_requires=['mpi4py>=3.0',
                      'scipy.stats',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: N/A',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)