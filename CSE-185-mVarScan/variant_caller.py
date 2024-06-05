from mpileup_parser import MpileupParser
from scipy.stats import fisher_exact 

# TODO: Make sure we initialize min_var_freq as well as min_homozygous_freq
# TODO: Need to add min_homozygous_freq
class VariantCaller:
    '''
    varient_caller object used to call mVarScan in main
    populated with command line arguments
    '''
    def __init__(self, parser, min_var_frequency, min_freq_for_hom, pvalue, output_file, min_reads2, min_coverage, min_avg_qual, tab):
        self.parser = parser
        self.min_var_freq = min_var_frequency
        self.min_freq_for_hom = min_freq_for_hom
        self.pvalue = pvalue
        self.output_file = output_file
        self.min_reads2 = min_reads2
        self.min_coverage = min_coverage
        self.min_avg_qual = min_avg_qual
        self.tab = tab
    
    '''
    DESCRIPTION:
        iterates over the mpileup data for a given base and compares the frequency
        of alternate bases to the reference bases and based on input min frequency
        will return True if the alternate freq is higher (SNP)

    PARAMETERS:
        counts: a dictionary representing the 5th file of the mpileup data
                which represents the reads compared to the reference base

        total_reads: total number of reads for any given base
    
    RETURNS:
        if given read is an SNP: returns True, the alternate base itself, and the frequency of that base
        otherwise returns False, None for the base, and 0 for the frequency
    '''
    def is_SNP(self, counts, total_reads) :
        if(total_reads == 0):
            return False, None, 0
        for base, count in counts.items() :
            if base not in ['N', 'del', '.', ',', 'ins']:
                freq = count / total_reads
                if freq > self.min_var_freq and count >= self.min_reads2:
                    return True, base, freq
        return False, None, 0

    '''
    USAGE: 
        call only if is_SNP() returns True

    PARAMETERS:
        base: alternate base from is_SNP()
        freq: frequency of alternate base from is_SNP()

    RETURNS:
        True as well as the base and freq given the frequency is greater than the input min_homo
    '''
    def is_homozygous_nonreference_SNP(self, freq) :
        if freq > self.min_freq_for_hom :
            return True
        return False

    # TODO: Remove N
    def count_bases(self, read_bases):
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0, 'del': 0, 'ins': 0, '.': 0, ',': 0}
        i = 0
        while i < len(read_bases):
            base = read_bases[i]
            # Skip the next character which is the mapping quality
            if base == '^':
                # Move past the '^' and the following quality character
                i += 2
            # End of a read segment, move past
            elif base == '$':
                i += 1
            # Check for matches and mismatches
            elif base in counts:
                counts[base] += 1
                i += 1
            # Handle case for mismatches on reverse strand
            elif base.upper() in counts:
                counts[base.upper()] += 1
                i += 1
            # Deletion of the reference base
            elif base == '*' or base == '#':
                counts['del'] += 1
                i += 1
            # Insertion or deletion
            elif base == '+' or base == '-':
                # Move past the '+' or '-'
                i += 1
                number = ''
                while i < len(read_bases) and read_bases[i].isdigit():
                    number += read_bases[i]
                    i += 1
                # Length of the insertion/deletion
                length = int(number) 
                # Skip the actual inserted/deleted bases
                i += length
                if base == '+':
                    # Count each inserted base
                    counts['ins'] += length
                else:
                    # Count each deleted base
                    counts['del'] += length 
            else:
                # Move past any unexpected characters
                i += 1
        return counts

    
    def get_pval(self, counts):
        ref_count = 0
        alt_count = 0
        total_count = 0

        for count in counts:
            if count == '.' or count == ',' :
                ref_count += counts[count]
                total_count += counts[count]
            elif count in ['del', 'N', 'ins'] :
                continue
            else :
                alt_count += counts[count]
                total_count += counts[count]
        table = [[ref_count, alt_count], [total_count - ref_count, total_count - alt_count]]
        odds_ratio, p_value = fisher_exact(table)

        return p_value

    def find_snps(self):
        file = self.parser.read_mpileup_file()
        results = []
        total_snps = 0
        chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(file[1])
        if(len(coverages) == 1):
            if(self.tab == '1'):
                header = "#CHROM\tPOS\tREF\tALT\tSAMPLE\t"
                results.append(header)
                for line in file:
                    chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
                    # zip() helps pairwise iteration over reads and base_qualities
                    for coverage, read, base_quality in zip(coverages, reads, base_qualities):
                        avg_qual = sum(ord(q) - 33 for q in base_quality) / len(base_quality)
                        # if average base quality is less than the minimum, do not parse the read
                        if avg_qual < self.min_avg_qual:
                            continue
                    counts = self.count_bases(read)
                    if int(coverage) < self.min_coverage:
                        continue
                    # print("read = ",read)
                    is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
                    homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                    # is variant and reads are more than or equal to threshold (min_reads)
                    if is_variant:
                        if (self.pvalue != 0.99) :
                            pval = self.get_pval(counts)
                        else:
                            pval = 0.98
                        if pval <= self.pvalue:
                            result = (f"{chrom}\t{pos}\t{ref_base}\t{variant_base}\t{homo_status}:{counts.get(variant_base, 0)},{coverage}:"
                                    f"{avg_qual}:{freq}:{pval}")
                        else:
                            result = None

                        if result:
                            total_snps += 1
                            results.append(result)
            else:
                for line in file:
                    chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
                    # zip() helps pairwise iteration over reads and base_qualities
                    for coverage, read, base_quality in zip(coverages, reads, base_qualities):
                        avg_qual = sum(ord(q) - 33 for q in base_quality) / len(base_quality)
                        # if average base quality is less than the minimum, do not parse the read
                        if avg_qual < self.min_avg_qual:
                            continue
                    counts = self.count_bases(read)
                    if int(coverage) < self.min_coverage:
                        continue
                    # print("read = ",read)
                    is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
                    homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                    # is variant and reads are more than or equal to threshold (min_reads)
                    if is_variant:
                        if (self.pvalue != 0.99) :
                            pval = self.get_pval(counts)
                        else:
                            pval = 0.98
                        is_homo = self.is_homozygous_nonreference_SNP(freq)
                        if pval <= self.pvalue:
                            result = (f"Sample | {homo_status} | {ref_base} -> {variant_base} |"
                                    f" frequency {freq:.2f} | p-value {pval} |"
                                    f" reads {counts.get(variant_base, 0)},{coverage} | avg base quality {avg_qual}| ")
                        else:
                            result = None

                        if result:
                            total_snps += 1
                            results.append(result)
        else:
            if(self.tab == '1'):
                num_samples = len(coverages)
                header_base = "#CHROM\tPOS\tREF\tALT"
                samples_header = "\t".join(f"SAMPLE_{i+1}" for i in range(num_samples))
                header = f"{header_base}\t{samples_header}\t"
                results.append(header)

                for line in file:
                    chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
                    any_sample_variant = False
                    snp_found = f"{chrom}\t{pos}\t"

                    zipped_data = zip(coverages, reads, base_qualities)
                    snp_info_list = []                
                    for coverage, read, base_quality in zipped_data:
                        counts = self.count_bases(read)
                        pval = self.get_pval(counts) if self.pvalue != 0.99 else 0.98

                        is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
                        homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                        
                        # Calculate average base quality
                        avg_qual = sum(ord(q) - 33 for q in base_quality) / len(base_quality)

                        # Format SNP string
                        sample_snp = (f"{homo_status}:{counts.get(variant_base, 0)},{coverage}:"
                                    f"{avg_qual}:{freq}:{pval}")

                        snp_info_list.append(sample_snp)

                        # Determine if any of the reads in the line pass the SNP conditions
                        if is_variant and pval <= self.pvalue and avg_qual >= self.min_avg_qual and int(coverage) >= self.min_coverage:
                            if(not any_sample_variant):
                                snp_found += f"{ref_base}\t{variant_base}\t"
                            any_sample_variant = True
                    if any_sample_variant:
                        total_snps += 1
                        snp_found += "\t".join(snp_info_list)
                        results.append(snp_found)
            else:
                for line in file:
                    chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
                    any_sample_variant = False
                    sample_num = 0
                    snp_found = f"{chrom}:{pos} | "

                    zipped_data = zip(coverages, reads, base_qualities)
                    snp_info_list = []                
                    for coverage, read, base_quality in zipped_data:
                        sample_num += 1
                        counts = self.count_bases(read)
                        pval = self.get_pval(counts) if self.pvalue != 0.99 else 0.98

                        is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
                        homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                        
                        # Calculate average base quality
                        avg_qual = sum(ord(q) - 33 for q in base_quality) / len(base_quality)

                        # Format SNP string
                        sample_snp = (f"Sample {sample_num} | {homo_status} | {ref_base} -> {variant_base} |"
                                    f" frequency {freq:.2f} | p-value {pval} |"
                                    f" reads {counts.get(variant_base, 0)},{coverage} | avg base quality {avg_qual}| ")

                        snp_info_list.append(sample_snp)

                        # Determine if any of the reads in the line pass the SNP conditions
                        if is_variant and pval <= self.pvalue and avg_qual >= self.min_avg_qual and int(coverage) >= self.min_coverage:
                            any_sample_variant = True

                    if any_sample_variant:
                        total_snps += 1
                        snp_found += " ".join(snp_info_list)
                        results.append(snp_found)

        # Output the results either to the console or a file
        if self.output_file:
            with open(self.output_file, 'w') as f:
                f.writelines(f"{result}\n" for result in results)
            print("Results of mVarScan output to: " + self.output_file)
        else:
            for result in results:
                print(result)

        print("Total number of SNPs found: " + str(total_snps) + '\n')

    # def find_snps(self):
    #         file = self.parser.read_mpileup_file()
    #         results = []
    #         total_snps = 0
    #         chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(file[1])
    #         if(len(coverages) == 1):
                
    #         if(self.vcf == '1'):
    #             num_samples = len(coverages)
    #             header_base = "#CHROM\tPOS\tREF\tALT"
    #             samples_header = "\t".join(f"SAMPLE_{i+1}" for i in range(num_samples))
    #             header = f"{header_base}\t{samples_header}\t"
    #             results.append(header)

    #             for line in file:
    #                 chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
    #                 any_sample_variant = False
    #                 snp_found = f"{chrom}\t{pos}\t"

    #                 zipped_data = zip(coverages, reads, base_qualities)
    #                 snp_info_list = []                
    #                 for coverage, read, base_quality in zipped_data:
    #                     counts = self.count_bases(read)
    #                     pval = self.get_pval(counts) if self.pvalue != 0.99 else 0.98

    #                     is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
    #                     homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                        
    #                     # Calculate average base quality
    #                     avg_qual = sum(ord(q) - 33 for q in base_quality) / len(base_quality)

    #                     # Format SNP string
    #                     sample_snp = (f"{homo_status}:{counts.get(variant_base, 0)},{coverage}:"
    #                                 f"{avg_qual}:{freq}:{pval}")

    #                     snp_info_list.append(sample_snp)

    #                     # Determine if any of the reads in the line pass the SNP conditions
    #                     if is_variant and pval <= self.pvalue and avg_qual >= self.min_avg_qual and int(coverage) >= self.min_coverage:
    #                         if(not any_sample_variant):
    #                             snp_found += f"{ref_base}\t{variant_base}\t"
    #                         any_sample_variant = True
    #                 if any_sample_variant:
    #                     total_snps += 1
    #                     snp_found += "\t".join(snp_info_list)
    #                     results.append(snp_found)
    #         else:
    #             for line in file:
    #                 chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
    #                 any_sample_variant = False
    #                 sample_num = 0
    #                 snp_found = f"{chrom}:{pos} | "

    #                 zipped_data = zip(coverages, reads, base_qualities)
    #                 snp_info_list = []                
    #                 for coverage, read, base_quality in zipped_data:
    #                     sample_num += 1
    #                     counts = self.count_bases(read)
    #                     pval = self.get_pval(counts) if self.pvalue != 0.99 else 0.98

    #                     is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
    #                     homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                        
    #                     # Calculate average base quality
    #                     avg_qual = sum(ord(q) - 33 for q in base_quality) / len(base_quality)

    #                     # Format SNP string
    #                     sample_snp = (f"Sample {sample_num} | {homo_status} | {ref_base} -> {variant_base} |"
    #                                 f" frequency {freq:.2f} | p-value {pval} |"
    #                                 f" reads {counts.get(variant_base, 0)},{coverage} | avg base quality {avg_qual}| ")

    #                     snp_info_list.append(sample_snp)

    #                     # Determine if any of the reads in the line pass the SNP conditions
    #                     if is_variant and pval <= self.pvalue and avg_qual >= self.min_avg_qual and int(coverage) >= self.min_coverage:
    #                         any_sample_variant = True

    #                 if any_sample_variant:
    #                     total_snps += 1
    #                     snp_found += " ".join(snp_info_list)
    #                     results.append(snp_found)

    #         # Output the results either to the console or a file
    #         if self.output_file:
    #             with open(self.output_file, 'w') as f:
    #                 f.writelines(f"{result}\n" for result in results)
    #             print("Results of mVarScan output to: " + self.output_file)
    #         else:
    #             for result in results:
    #                 print(result)

    #         print("Total number of SNPs found: " + str(total_snps) + '\n')