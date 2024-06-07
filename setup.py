from setuptools import setup

setup(
    name='mVarScan',
    version='0.1.10',    
    description='An implementation of the existing VarScan tool (specifically mpileup2snp option). Used to find SNPs given a .mpileup file',
    url='https://github.com/andrewbigelow/mVarScan/tree/main',
    author='Andrew Bigelow, Numaan Formoli, Aditya Parmar',
    author_email='abigelow@ucsd.edu',
    license='Proprietary',
    packages=['mVarScan'],
    install_requires=[
        'mpi4py>=3.0',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'mvarscan=mVarScan.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
