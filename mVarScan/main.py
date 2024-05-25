from mVarScan import MpileupParser, VariantCaller, FileParsing
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "mVarScan",
        description = "Command-line python package to perform variant calling on sam or bam files"
    )

    parser.add_argument("mpileup", help="mpileup file", type=str, metavar="FILE")
    parser.add_argument("-o", "--out", help="Write output to file. ", metavar="FILE", type=str, required=False)
    parser.add_argument("-f", "--fasta-ref", help="indexed fasta reference genome file", type=str, metavar="FILE", required=False)
    parser.add_argument("-m", "--min-var-frequency", \
                        help="minumum frequency to call a non-reference a mutation. If not called: will auto to 0.2", \
                        type=float, required=False)
    parser.add_argument("-h", "--min-freq-for-hom", \
                        help="minumum frequency to call a non-reference a homozygous mutation. If not called: will auto to 0.8", \
                        type=float, required=False)

    args = parser.parse_args()
    
    # Populate variables from command line tool
    mpileup = args.mpileup
    min_var_frequency = 0.2
    if args.min_var_frequency != None :
        min_var_frequency = args.min_var_frequency
    
    min_frequency_for_hom = 0.8
    if args.min_frequency_for_hom != None :
        min_frequency_for_hom = args.min_frequency_for_hom

    mpileup_parser = MpileupParser(parser.mpileup)
    caller = VariantCaller(mpileup_parser)
    caller.process()