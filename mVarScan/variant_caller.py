from mpileup_parser import MpileupParser

def is_SNP(count, ):
    print("hello")

def count_bases(self, read_bases):
    counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0, 'del': 0}
    for base in read_bases:
        if(base in counts):
            counts[base] += 1
        elif(base.upper() in counts):
            counts[base.upper()] += 1
        elif(base == '*' | base == '-'):
            counts['del'] += 1
    return counts
