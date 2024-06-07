from .mpileup_parser import MpileupParser
from .variant_caller import VariantCaller

def main(args) :
    # Populate variables from command line tool
    mpileup = args.mpileup
    min_var_frequency = 0.2
    if args.min_var_frequency is not None :
        min_var_frequency = args.min_var_frequency
    
    min_freq_for_hom = 0.8
    if args.min_freq_for_hom is not None :
        min_freq_for_hom = args.min_freq_for_hom

    pvalue = 0.99
    
    if args.pvalue is not None : 
        pvalue = args.pvalue
    
    output_file = None
    if args.out is not None:
        output_file = args.out
    
    # TODO: implement VCF output
    tab = 0
    if args.tab is not None:
        tab = args.tab

    min_reads2 = 2
    if args.min_reads2 is not None:
        min_reads2 = args.min_reads2

    min_coverage = 8
    if args.min_coverage is not None:
        min_coverage = args.min_coverage

    min_avg_qual = 15
    if args.min_avg_qual is not None:
        min_avg_qual = args.min_avg_qual
    
    mpileup_parser = MpileupParser(mpileup)
    caller = VariantCaller(mpileup_parser, min_var_frequency, min_freq_for_hom, pvalue, \
                        output_file, min_reads2, min_coverage, min_avg_qual, tab)
    caller.find_snps()


if __name__ == '__main__':
    pass