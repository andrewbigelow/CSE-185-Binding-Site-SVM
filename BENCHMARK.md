# VarScan
When running VarScan using the command:
```bash
time java -jar VarScan.jar mpileup2snp ~/downloads/trio.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --p-va
lue 0.01 --output-vcf 1 --variants snp > trio.vcf
Only SNPs will be reported
Min coverage:   8
Min reads2:     2
Min var freq:   0.2
Min avg qual:   15
P-value thresh: 0.01
Reading input from /Users/andrewbigelow/downloads/trio.mpileup
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
time java -jar VarScan.jar mpileup2snp ~/downloads/NA12878_child.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --p-value 0.01 --output-vcf 1 --variants snp > trio.vcf
Only SNPs will be reported
Min coverage:   8
Min reads2:     2
Min var freq:   0.2
Min avg qual:   15
P-value thresh: 0.01
Reading input from /Users/andrewbigelow/downloads/NA12878_child.mpileup
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
time python3 /Users/andrewbigelow/Documents/GitHub/CSE-185-Binding-Site-SVM//CSE-185-mVarScan/main.py ~/downloads/trio.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --pvalue 0.01 --out output.txt
Results of mVarScan output to: output.txt
Total number of SNPs found: 37


real    0m32.106s
user    0m30.379s
sys     0m0.609s
```
Next Dataset:
```bash
time python3 /Users/andrewbigelow/Documents/GitHub/CSE-185-Binding-Site-SVM//CSE-185-mVarScan/main.py ~/downloads/NA12878_child.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --pvalue 0.01 --out output.txt
Results of mVarScan output to: output.txt
Total number of SNPs found: 11


real    0m5.454s
user    0m5.504s
sys     0m0.228s
```