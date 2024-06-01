# mVarScan

This project is for CSE 185. It implements a subset of "VarScan" and finds SNPs within a given aligned genome in the form of a mpileup file.

### REQUIREMENTS:
- Ensure that you have Python 3.10 and above

### INSTALLATION:
- Clone the git repository or download the code locally as a ZIP

### BASIC USAGE:
    python path/to/file/main.py [mpileup]

### OPTIONAL:
    -o --out FILENAME (file to output contents to)
    -m --min-var-frequency FREQUENCY (minimum frequency to call a non-reference mutation, default: 0.2)
    -h --min-homo-frequency FREQUENCY (minimum frequency to call a non-reference homozygous mutation, default: 0.8)
    -p --pvalue FLOAT (p-value threshold to output SNP, default: 0.99)
    -r2 --min-reads2 INT (minimum supporting reads at a position to call variants, default: 2)

### OUTPUT:
The output will specify chromosome positions and the alternative allele frequency.
