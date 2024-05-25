import argparse

def main():
    parser = argparse.ArgumentParser(
        prog = "mVarScan",
        description = "Command-line python package to perform variant calling on sam or bam files"
    )

    parser.add_argument("bam", help="Indexed BAM files", type=str)
    parser.add_argument("-o", "--out", help="Write output to file. ", metavar="FILE", type=str, required=False)
    parser.add_argument("-f", "--fasta-ref", help="indexed fasta reference genome file", type=str, metavar="FILE", required=False)
    
    parser.add_argument("-m", "--min-var-frequency", \
                        help="minumum frequency to call a non-reference a mutation. If not called: will auto to 0.2", \
                        type=float, required=False)
    parser.add_argument("-h", "--min-freq-for-hom", \
                        help="minumum frequency to call a non-reference a homozygous mutation. If not called: will auto to 0.8", \
                        type=float, required=False)

    args = parser.parse_args()
