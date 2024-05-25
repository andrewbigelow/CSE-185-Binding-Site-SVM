from mVarScan import MpileupParser

# TODO: Make sure we initialize min_var_freq as well as min_homozygous_freq
# TODO: Need to add min_homozygous_freq
class VariantCaller:
    def __init__(self, parser, min_var_frequency, min_frequency_for_hom):
        self.parser = parser
        self.min_var_freq = min_var_frequency
        self.min_frequency_for_hom = min_frequency_for_hom

    def is_SNP(self, counts, total_reads) :
        for base, count in counts.items() :
            if base != 'N' and base != 'del' :
                freq = count / total_reads
                if freq > self.min_var_freq :
                    return True, base, freq
        return False, None, 0

    def is_homozygous_nonreference_SNP(base, freq, min_homozygous_freq) :
        if freq > min_homozygous_freq :
            return True, base, freq
        return False, None, 0

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
    
    # TODO: Check if total reads is correct
    def process(self):
        file =  open(self.parser.mpileup_file, 'r')
        for line in file:
            chrom, pos, ref_base, coverages, reads = self.parser.parse_line(line)
            for read in reads:
                counts = self.count_bases(read)
                total_reads = sum(counts.values())
                is_variant, variant_base, freq = self.is_snp(counts, total_reads)
                if is_variant:
                        print(f"SNP found at {chrom}:{pos} -> {ref_base} to {variant_base} with frequency {freq:.2f}")
