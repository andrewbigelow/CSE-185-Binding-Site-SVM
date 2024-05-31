from mpileup_parser import MpileupParser
from scipy.stats import fisher_exact 

# TODO: Make sure we initialize min_var_freq as well as min_homozygous_freq
# TODO: Need to add min_homozygous_freq
class VariantCaller:
    def __init__(self, parser, min_var_frequency, min_frequency_for_hom, pvalue, output_file):
        self.parser = parser
        self.min_var_freq = min_var_frequency
        self.min_frequency_for_hom = min_frequency_for_hom
        self.pvalue = pvalue
        self.output_file = output_file

    def is_SNP(self, counts, total_reads) :
        for base, count in counts.items() :
            if base != 'N' and base != 'del' and base != '.' and base != ',':
                freq = count / total_reads
                if freq > self.min_var_freq :
                    return True, base, freq
        return False, None, 0


    # Call if is_SNP() returns true
    def is_homozygous_nonreference_SNP(self, base, freq) :
        if freq > self.min_frequency_for_hom :
            return True, base, freq
        return False, None, 0

    def count_bases(self, read_bases):
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0, 'del': 0, '.': 0, ',': 0}
        for base in read_bases:
            if(base in counts):
                counts[base] += 1
            elif(base.upper() in counts):
                counts[base.upper()] += 1
            elif(base == '*' or base == '-'):
                counts['del'] += 1
        return counts
    
    def get_pval(self, counts):
        ref_count = 0
        alt_count = 0
        total_count = 0

        for count in counts:
            if count == '.' or count == ',' :
                ref_count += counts[count]
                total_count += counts[count]
            elif count == 'del' :
                continue
            else :
                alt_count += counts[count]
                total_count += counts[count]
        
        table = [[ref_count, alt_count], [total_count - ref_count, total_count - alt_count]]
        odds_ratio, p_value = fisher_exact(table)

        return odds_ratio, p_value
    
    # TODO: Check if total reads is correct
    def find_snps(self):
        file =  self.parser.read_mpileup_file()
        results = []
        for line in file:
            chrom, pos, ref_base, coverages, reads = self.parser.parse_line(line)
            for read in reads:
                counts = self.count_bases(read)
                total_reads = sum(counts.values())
                is_variant, variant_base, freq = self.is_SNP(counts, total_reads)
                if is_variant:
                    odds_ratio, pval = self.get_pval(counts)
                    is_homo, homo_base, homo_freq = self.is_homozygous_nonreference_SNP(counts, total_reads)
                    if (is_homo and pval < self.pvalue) :
                        result = f"Homozygous SNP found at {chrom}:{pos} -> {ref_base} to {variant_base} with frequency {freq:.2f} and p value {pval} and Odds ratio {odds_ratio}"
                    elif (pval < self.pvalue):
                        result = f"SNP found at {chrom}:{pos} -> {ref_base} to {variant_base} with frequency {freq:.2f} and p value {pval} and Odds ratio {odds_ratio}"
                    else:
                            result = None
                    
                    if result:
                        if self.output_file:
                            results.append(result)
                        else:
                            print(result)    

        # Output to a file
        if self.output_file is not None:
            with open(self.output_file, 'w') as f:
                for result in results:
                    f.write(result + '\n')
                print("Results of mVarScan output to " + self.output_file)

        # TODO: add VCF and CSV TSV options