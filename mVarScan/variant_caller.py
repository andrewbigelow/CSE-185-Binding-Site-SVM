def is_SNP(count, ) :
   print() 

# Parse mpileup data
def parse_mpileup_line(line):
    fields = line.strip().split()
    chrom = fields[0]
    pos = int(fields[1])
    ref_base = fields[2]
    coverages = fields[3::3]
    reads = fields[4::3]
    return chrom, pos, ref_base, coverages, reads


def process_mpileup(file_path, min_var_freq=0.2):
    with open(file_path, 'r') as file:
        for line in file:
            chrom, pos, ref_base, coverages, reads = parse_mpileup_line(line)
            for read in reads:
                counts = count_bases(read)
                total_reads = sum(counts.values())
                variant, var_base, freq = is_snp(counts, total_reads, min_var_freq)
                if variant:
                    print(f"SNP found at {chrom}:{pos} -> {ref_base} to {var_base} with frequency {freq:.2f}")
                