from mpileup_parser import MpileupParser
from variant_caller import VariantCaller

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "mVarScan",
        description = "Command-line python package to perform variant calling on sam or bam files"
    )

    parser.add_argument("mpileup", help="mpileup file", type=str, metavar="FILE")
    parser.add_argument("-o", "--out", help="Write output to simple text file. ", metavar="FILE", type=str, required=False)
    parser.add_argument("-vcf", "--vcf", help="Write output to VCF format file. ", metavar="FILE", type=str, required=False)
    parser.add_argument("-m", "--min-var-frequency", \
                        help="minumum frequency to call a non-reference a mutation. If not called: will auto to 0.2", \
                        type=float, required=False)
    parser.add_argument("-a", "--min-freq-for-hom", \
                        help="minumum frequency to call a non-reference a homozygous mutation. If not called: will auto to 0.8", \
                        type=float, required=False)
    parser.add_argument("-p", "--pvalue", \
                        help="minumum frequency to call a non-reference a homozygous mutation. If not called: will auto to 0.99", \
                        type=float, required=False)
    parser.add_argument("-r2", "--min-reads2", help="Minimum supporting reads at a position to call variants. Default 2", \
                        type=int, required=False, default=2)
    parser.add_argument("-q", "--min-avg-qual", help="Minimum base quality at a position to count a read. Default 15", \
                        type=int, required=False, default=15)

    args = parser.parse_args()
    
    # Populate variables from command line tool
    mpileup = args.mpileup
    min_var_frequency = 0.2
    if args.min_var_frequency is not None :
        min_var_frequency = args.min_var_frequency
    
    min_frequency_for_hom = 0.8
    if args.min_freq_for_hom is not None :
        min_frequency_for_hom = args.min_frequency_for_hom

    pvalue = 0.99
    if args.pvalue is not None : 
        pvalue = args.pvalue
    
    if args.out is not None:
        output_file = args.out
    
    # TODO: implement VCF output
    if args.vcf is not None:
        vcf = args.vcf

    min_reads2 = 2
    if args.min_reads2 is not None:
        min_reads2 = args.min_reads2

    min_avg_qual = 15
    if args.min_avg_qual is not None:
        min_avg_qual = args.min_avg_qual
    
    # TODO: Include freqs for the variant caller
    mpileup_parser = MpileupParser(mpileup)
    caller = VariantCaller(mpileup_parser, min_var_frequency, min_frequency_for_hom, pvalue, \
                        output_file, min_reads2, min_avg_qual)
    caller.find_snps()