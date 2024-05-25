# README

This project is for CSE 185. It implements a subset of "VarScan" and finds SNPs within a given alligned genome in the form of a mpileup file.

## REQUIREMENTS:
- ensure that you have python 3.10 and above

## INSTALLATION:
    - fork and clone the git repository or download the code locally


## BASIC USAGE:
    path/to/file/main.py [mpileup]

## OPTIONAL:
    -o --out  FILENAME (file to output contents to)
    -f --fasta FILENAME (indexed fasta reference genome file)
    -m --min-var-frequency FREQUENCY (minumum frequency to call a non-reference a mutation. If not called: will auto to 0.2)
    -h --min-homo-frequency FREQUENCY (minumum frequency to call a non-reference a homozygous mutation. If not called: will auto to 0.8)

## The output will be specific chromosome positions as well as the alternative allele frequency
