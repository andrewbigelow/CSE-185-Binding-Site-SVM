# VarScan
When running VarScan using the command:
```bash
time java -jar VarScan.jar mpileup2snp ~/downloads/trio.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0.8 --p-va
lue 0.01 --output-vcf 1 --variants snp > trio.vcf
```   
The total time it took running was:
```bash
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

real    0m24.796s
user    0m46.863s
sys     0m0.918s
```
Next Dataset:
```bash
time java -jar VarScan.jar mpileup2snp ~/downloads/NA12878_child.mpileup --min-var-frequency 0.2 --min-freq-for-hom 0
.8 --p-value 0.01 --output-vcf 1 --variants snp > trio.vcf
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

real    0m36.097s
user    0m52.578s
sys     0m1.494s
```
   
When running mVarScan on the same file with the same options used (excluding --variants snp because our program is only meant for SNPs) the output time was:
```bash
TIME
```
   
   
# VarScan output
To compare the actual accuracy of our tool we compared it to the output of VarScan. For the prior command, the output was:
```bash
Only SNPs will be reported
Min coverage:   8
Min reads2:     2
Min var freq:   0.2
Min avg qual:   15
P-value thresh: 0.01
Reading input from trio.mpileup
200002 bases in pileup file
53 variant positions (44 SNP, 9 indel)
3 were failed by the strand-filter
41 variant positions reported (41 SNP, 0 indel)
```
   
   
On our tool, the output was slighlty different just due to formating but we got:
```bash
OUTPUT
```
   
Overall the same SNPs were reported just in a different format meaning we had a very high accuracy (assuming VarScan is a ground truth).