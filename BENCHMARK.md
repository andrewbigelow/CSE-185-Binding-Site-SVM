# VarScan
When running VarScan using the command:
```bash
time java -jar VarScan.jar mpileup2snp path/to/file/trio.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --p-va
lue 0.01 --output-vcf 1 --variants snp > trio.vcf
Only SNPs will be reported
Min coverage:   8
Min reads2:     2
Min var freq:   0.2
Min avg qual:   15
P-value thresh: 0.01
Reading input from pathway/to/file/trio.mpileup
200002 bases in pileup file
53 variant positions (44 SNP, 9 indel)
3 were failed by the strand-filter
41 variant positions reported (41 SNP, 0 indel)

real    0m33.833s
user    0m55.287s
sys     0m0.866s
```
Next Dataset:
```bash
time java -jar VarScan.jar mpileup2snp path/to/file/NA12878_child.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --p-value 0.01 --output-vcf 1 --variants snp > trio.vcf
Only SNPs will be reported
Min coverage:   8
Min reads2:     2
Min var freq:   0.2
Min avg qual:   15
P-value thresh: 0.01
Reading input from path/to/file/NA12878_child.mpileup
200002 bases in pileup file
45 variant positions (38 SNP, 7 indel)
1 were failed by the strand-filter
37 variant positions reported (37 SNP, 0 indel)

real    0m18.368s
user    0m28.894s
sys     0m0.567s
```
   
When running mVarScan on the same file with the same options used (excluding --variants snp because our program is only meant for SNPs) the output time was:
```bash
time python3 path/to/file/main.py path/to/file/trio.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --pvalue 0.01 --out output.txt
Results of mVarScan output to: output.txt
Total number of SNPs found: 21


real    16m39.268s
user    16m29.433s
sys     0m3.013s
```
Next Dataset:
```bash
time python3 path/to/file/main.py path/to/file/NA12878_child.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --pvalue 0.01 --out output.vcf
Results of mVarScan output to: output.txt
Total number of SNPs found: 11


real    6m1.881s
user    5m44.120s
sys     0m2.627s
```
  
  
# Time
In terms of time our function runs noticably slowler than VarScan. We believe this is for a few reasons being:   
* Language (Java vs Python)
* VarScan implements their own Fisher's Exact Test when we use scipy's built in function
* VarScan uses different data structures as a way to speed up parsing through the files

  
# Results
For VarScan's function, it reported 41 SNPs on the trio file and 37 SNPs on the child file. Our output however had much fewer results with only 21 SNPs on the trio and 11 SNPs on the child file. All of the found SNPs within our function are found in the VarScan outputs as well. Our p-values are significantly bigger: for the child file chr6:128602796 was found to have a p-value of 0.0036911, but VarScan found it to have a p-value of 2.7841E-7. Interestingly, p-values that are very low in our function are very close to VarScans calculated p-value: we found chr6:128414945 in the chid file has a p-value of 7.619E-26 and VarScan caluclated a p-value of 3.8097E-26. While still off, it was within the same log_10 value.   
We believe the difference in these outputs (number of found SNPs and p-values) has to due with VarScan doing their own version of a Fisher's Exact Test, when we use scipy's built in test.
