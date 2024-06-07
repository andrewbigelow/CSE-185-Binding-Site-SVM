from scipy.stats import fisher_exact 

# TODO: Make sure we initialize min_var_freq as well as min_homozygous_freq
# TODO: Need to add min_homozygous_freq
class VariantCaller:
    """
    A class to call variants from mpileup data using specific thresholds and statistical testing.

    Attributes:
        parser (MpileupParser): An instance of MpileupParser to read and parse mpileup data.
        min_var_freq (float): Minimum variant allele frequency threshold for calling a variant.
        min_freq_for_hom (float): Minimum frequency to consider a variant as homozygous non-reference.
        pvalue (float): P-value threshold for calling a variant based on Fisher's exact test.
        output_file (str): Path to the output file where results will be saved.
        min_reads2 (int): Minimum read count supporting a variant to be considered for analysis.
        min_coverage (int): Minimum coverage required to consider a position for analysis.
        min_avg_qual (float): Minimum average base quality required to consider reads at a position.
        tab (str): Format selector for output, influences how output data is structured.

    Methods:
        is_SNP: Evaluates if a position in the genome is a SNP based on read data.
        is_homozygous_nonreference_SNP: Determines if a SNP is homozygous for the non-reference allele.
        count_bases: Counts occurrences of each base in the read data.
        get_pval: Calculates the p-value for the observed allele frequency distribution using Fisher's exact test.
        find_snps: Processes mpileup data to find SNPs according to the specified thresholds and parameters.
    """

    def __init__(self, parser, min_var_frequency, min_freq_for_hom, pvalue, output_file, min_reads2, min_coverage, min_avg_qual, tab):
        """Initializes the VariantCaller with required parameters for variant calling.
        
        Args:
            mpileup_file (str): Path to the mpileup file.
        """
        self.parser = parser
        self.min_var_freq = min_var_frequency
        self.min_freq_for_hom = min_freq_for_hom
        self.pvalue = pvalue
        self.output_file = output_file
        self.min_reads2 = min_reads2
        self.min_coverage = min_coverage
        self.min_avg_qual = min_avg_qual
        self.tab = tab
    
    def is_SNP(self, counts, total_reads) :
        """
        Determines if the observed allele frequencies at a position indicate a SNP.

        Args:
            counts (dict): A dictionary of base counts at a position.
            total_reads (int): Total number of reads covering the position.

        Returns:
            tuple: (bool, str or None, float), where the boolean indicates if a SNP was found,
                   the string (if present) is the variant base, and the float is the frequency of the variant base.

        Raises:
            ValueError: If the total reads are zero, which would lead to division by zero.
        """

        if(total_reads == 0):
            return False, None, 0
        for base, count in counts.items() :
            if base not in ['N', 'del', '.', ',', 'ins']:
                freq = count / total_reads
                if freq > self.min_var_freq and count >= self.min_reads2:
                    return True, base, freq
        return False, None, 0

    def is_homozygous_nonreference_SNP(self, freq) :
        """
        Checks if the frequency of the alternate allele is high enough to consider it as homozygous nonreference.

        Args:
            freq (float): The frequency of the alternate allele.

        Returns:
            bool: True if the frequency is above the threshold for homozygous nonreference, False otherwise.
        """

        if freq > self.min_freq_for_hom :
            return True
        return False
    
    def count_bases(self, read_bases):
        """
        Counts each type of base from the read data, considering special cases like insertions and deletions.

        Args:
            read_bases (str): String representing the bases read at a position.

        Returns:
            dict: A dictionary with keys as base types and values as counts.
        """

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
        """
        Calculates the p-value from a contingency table of reference and alternate allele counts using Fisher's exact test.

        Args:
            counts (dict): Dictionary with base counts including reference and alternate alleles.

        Returns:
            float: P-value calculated using Fisher's exact test to assess the significance of the observed variant.
        """

        ref_count = 0
        alt_count = 0
        total_count = 0

        for count in counts:

            # If reference base
            if count == '.' or count == ',' :
                ref_count += counts[count]
                total_count += counts[count]
            elif count in ['del', 'N', 'ins'] :
                continue

            # If alternative base
            else :
                alt_count += counts[count]
                total_count += counts[count]
        table = [[ref_count, alt_count], [total_count - ref_count, total_count - alt_count]]
        odds_ratio, p_value = fisher_exact(table)

        return p_value

    def find_snps(self):
        """
        Processes the mpileup data to identify SNPs based on set thresholds and outputs results to a file or stdout.

        This method integrates various checks and calculations to identify and report SNPs.
        """

        print(f"Min coverage:\t{self.min_coverage}")
        print(f"Min reads2::\t{self.min_reads2}")
        print(f"Min var freq:\t{self.min_var_freq}")
        print(f"Min avg qual:\t{self.min_avg_qual}")
        print(f"P-value thresh:\t{self.pvalue}")

        print(f"Reading input from {self.parser.mpileup_file}")

        file = self.parser.read_mpileup_file()
        results = []
        total_snps = 0
        chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(file[1])

        # Check if its only one sample
        if(len(coverages) == 1):
            # Check if output is tab format
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
                        # if coverage is less than the minimum, do not parse read
                        if int(coverage) < self.min_coverage:
                            continue
                        is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
                        homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                        # get p-value
                        if is_variant:
                            if (self.pvalue != 0.99) :
                                pval = self.get_pval(counts)
                            else:
                                pval = 0.98
                            # if p-value is less than or equal to minimum p-value, record snp
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
                        # if coverage is less than the minimum, do not parse the read
                        if int(coverage) < self.min_coverage:
                            continue
                        is_variant, variant_base, freq = self.is_SNP(counts, int(coverage))
                        homo_status = "1/1" if self.is_homozygous_nonreference_SNP(freq) else "0/1"
                        if is_variant:
                            # get p-value
                            if (self.pvalue != 0.99) :
                                pval = self.get_pval(counts)
                            else:
                                pval = 0.98
                            is_homo = self.is_homozygous_nonreference_SNP(freq)
                            # if p-value is less than or equal to minimum p-value, record snp
                            if pval <= self.pvalue:
                                result = (f"{chrom}:{pos} | Sample | {homo_status} | {ref_base} -> {variant_base} |"
                                        f" frequency {freq:.2f} | p-value {pval} |"
                                        f" reads {counts.get(variant_base, 0)},{coverage} | avg base quality {avg_qual}| ")
                            else:
                                result = None
                            if result:
                                total_snps += 1
                                results.append(result)
        else:
            # Check if output is tab format
            if(self.tab == '1'):
                # Ensure header has extra columns for extra samples
                num_samples = len(coverages)
                header_base = "#CHROM\tPOS\tREF\tALT"
                samples_header = "\t".join(f"SAMPLE_{i+1}" for i in range(num_samples))
                header = f"{header_base}\t{samples_header}\t"
                results.append(header)

                for line in file:
                    chrom, pos, ref_base, coverages, reads, base_qualities = self.parser.parse_line(line)
                    any_sample_variant = False
                    snp_found = f"{chrom}\t{pos}\t"
                    snp_info_list = []      

                    for coverage, read, base_quality in zip(coverages, reads, base_qualities):
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
                            # if this is the first read, attach the ref_base and variant base to snp record
                            if(not any_sample_variant):
                                snp_found += f"{ref_base}\t{variant_base}\t"
                            any_sample_variant = True

                    # if any of the reads were a variant, record snp to results
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
                    snp_info_list = []      

                    for coverage, read, base_quality in zip(coverages, reads, base_qualities):
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
                            
                    # if any of the reads were a variant, record snp to results
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