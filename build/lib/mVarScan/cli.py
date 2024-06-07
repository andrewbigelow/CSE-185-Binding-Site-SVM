from .main import main
import argparse

def parse_arguments() :
    parser = argparse.ArgumentParser(
        prog = "mVarScan",
        description = "Command-line python package to perform variant calling on sam or bam files"
    )

    parser.add_argument("mpileup", help="mpileup file", type=str, metavar="FILE")
    parser.add_argument("-o", "--out", help="Write output to simple text file. ", metavar="FILE", type=str, required=False)
    parser.add_argument("-t", "--tab", help="Write output to TAB format file. 1 for yes", metavar="FILE", type=str, required=False)
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
    parser.add_argument("-c", "--min-coverage", help="Minimum read depth at a position to make a call. Default 8", \
                        type=int, required=False, default=8)
    parser.add_argument("-q", "--min-avg-qual", help="Minimum base quality at a position to count a read (Phred). Default 15", \
                        type=int, required=False, default=15)
    return parser.parse_args()

def cli():
    args = parse_arguments()
    main(args)  # Call the main function from main.py with parsed arguments

if __name__ == "__main__":
    cli()