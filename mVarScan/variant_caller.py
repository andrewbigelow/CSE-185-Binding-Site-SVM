from mpileup_parser import MpileupParser
from file_parsing import args

def is_SNP(counts, total_reads, min_var_freq) :
    for base, count in counts.items() :
        if base != 'N' and base != 'del' :
            freq = count / total_reads
            if freq > min_var_freq :
                return True, base, freq
    return False, None, 0

def is_homozygous_nonreference_SNP(base, freq, min_homozygous_freq) :
    if freq > min_homozygous_freq :
        return True, base, freq
    return False, None, 0    print("hello")

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


def main() :
    # Populate variables from command line tool
    mpileup = args.mpileup
    min_var_frequency = 0.2
    if args.min_var_frequency != None :
        min_var_frequency = args.min_var_frequency
    
    min_frequency_for_hom = 0.8
    if args.min_frequency_for_hom != None :
        min_frequency_for_hom = args.min_frequency_for_hom