import os

class MpileupParser:
    """A parser for handling mpileup files.

    Attributes:
        mpileup_file (str): Path to the mpileup file to be parsed.
    """

    def __init__(self, mpileup_file):
        """Initialize the MpileupParser with the path to the mpileup file.

        Args:
            mpileup_file (str): Path to the mpileup file.
        """
        
        self.mpileup_file = mpileup_file

    def read_mpileup_file(self):
        """Read and load the content of the mpileup file.

        Raises:
            FileNotFoundError: Raised if the mpileup file does not exist at the specified path.

        Returns:
            list: A list of strings, where each string represents a line from the mpileup file.
        """

        if not os.path.isfile(self.mpileup_file):
            raise FileNotFoundError(f"The mpileup file {self.mpileup_file} does not exist.")
        
        with open(self.mpileup_file, 'r') as file:
            lines = file.readlines()
        
        return lines

    def parse_line(self, line):
        """Parse a single line from the mpileup file into its constituent components.

        Args:
            line (str): A line from the mpileup file.

        Raises:
            ValueError: If the line does not contain at least six expected fields.

        Returns:
            tuple: A tuple containing:
                - chromosome (str): The chromosome name.
                - position (int): The position on the chromosome.
                - ref_base (str): The reference base at the position.
                - depth (list): List of depth coverages.
                - read_bases (list): List of read bases at the position.
                - read_quality (list): List of quality scores for the reads.
        """
        
        columns = line.strip().split()
        if len(columns) < 6:
            raise ValueError(f"Invalid mpileup format in line: {line}")
        
        chromosome = columns[0]
        position = int(columns[1])
        ref_base = columns[2]
        depth = columns[3::3]
        read_bases = columns[4::3]
        read_quality = columns[5::3]
        
        return (chromosome, position, ref_base, depth, read_bases, read_quality)