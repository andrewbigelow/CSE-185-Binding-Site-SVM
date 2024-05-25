import os

class MpileupParser:
    def __init__(self, mpileup_file):
        self.mpileup_file = mpileup_file

    def read_mpileup_file(self):
        """Reads the mpileup file and returns its content as a list of lines."""
        if not os.path.isfile(self.mpileup_file):
            raise FileNotFoundError(f"The mpileup file {self.mpileup_file} does not exist.")
        
        with open(self.mpileup_file, 'r') as file:
            lines = file.readlines()
        
        return lines

    def parse_line(self, line):
        """Parses a single line of the mpileup file."""
        columns = line.strip().split()
        if len(columns) < 5:
            raise ValueError(f"Invalid mpileup format in line: {line}")
        
        chromosome = columns[0]
        position = int(columns[1])
        ref_base = columns[2]
        depth = int(columns[3])
        reads = columns[4]
        return (chromosome, position, ref_base, depth, reads)