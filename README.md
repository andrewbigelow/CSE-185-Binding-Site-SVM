# mVarScan

This project is for CSE 185. It implements a subset of `mpileup2snp` and finds SNPs within a given aligned genome in the form of a mpileup file. See [VarScan](https://varscan.sourceforge.net/using-varscan.html) for more details

[REQUIREMENTS](#requirements) | [INSTALLATION](#installation) | [BASIC USAGE](#usage) | [OPTIONAL](#optional) | [File formats](#formats) | [Miro board](#miro)

<a name="requirements"></a>
## REQUIREMENTS:
- Ensure that you have Python 3.10 and above
- scipy.stats

These packages can be installed with `pip`:
```
pip install scipy.stats
```
Note: If you do not have root access, you can run the command above with additional options to install locally:
```
pip install --user scipy.stats
```

<a name="installation"></a>
## INSTALLATION:
```
git clone https://github.com/andrewbigelow/mVarScan.git
cd 
```

<a name="usage"></a>
## BASIC USAGE:
The basic usage of `mVarScan` is:
```
python path/to/file/CSE-185-mVarScan/main.py [options] [mpileup]
```

<a name="optional"></a>
## OPTIONAL:
    -o --out FILENAME (file to output contents to)
    -t --tab (1 for yes) (output using TAB formating, default: 0)
    -m --min-var-frequency FREQUENCY (minimum frequency to call a non-reference mutation, default: 0.2)
    -h --min-freq-for-hom FREQUENCY (minimum frequency to call a non-reference homozygous mutation, default: 0.8)
    -p --pvalue FLOAT (p-value threshold to output SNP, default: 0.99)
    -r2 --min-reads2 INT (minimum supporting reads at a position to call variants, default: 2)
    -c --min-coverage INT (Minimum read depth at a position to make a call. Default 8)
    -q --min-avg-qual INT (minimum average base quality at a position to count a read, default: 15)


<a name="output"></a>
## OUTPUT:
The output will specify chromosome positions and the alternative allele frequency.

<a name="notes"></a>
### NOTES:
- The `--min-avg-qual` option sets the minimum average Phred quality score for bases to be considered in variant calling. Phred quality scores are a common metric in sequencing data quality control, indicating the probability of a base call being incorrect. For more information about Phred scores, refer to [this link](https://drive5.com/usearch/manual10/quality_score.html).
