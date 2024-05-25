from mpileup_parser import MpileupParser

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
    return False, None, 0

def count_bases(self, read_bases):