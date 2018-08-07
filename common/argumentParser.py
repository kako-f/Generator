import argparse


class ArgumentParser(object):
    def __init__(self, prog_version, argv, program_name):
        """

        :param prog_version:
        :param argv:
        :param program_name:
        """
        self.def_cores = 2
        self.program_v = prog_version
        self.arguments = argv
        self.ap = argparse.ArgumentParser(description=program_name + " is a program writen in Python3 to find "
                                                                     "create random genomic sequences."
                                                                     "Written by Camilo Fuentes Beals."
                                                                     "\n Program version: " + self.program_v)

        self.ap.add_argument('-n', '--nuc', nargs='?', default=self.def_cores, type=int,
                             help='Number of cpu cores to use. Default = ' + str(self.def_cores))
        self.ap.add_argument('-ran', '--random', action='store_true', default=False,
                             help='Create random sequences from biological files')

        sequence_type = self.ap.add_mutually_exclusive_group(required=True)
        sequence_type.add_argument('-dna', action='store_true', help='Analyze DNA sequence')
        sequence_type.add_argument('-rna', action='store_true', help='Analyze RNA sequence')
        sequence_type.add_argument('-prot', action='store_true', help='Analyze protein sequence')

    def return_arguments(self):
        """

        :return: Processed arguments.
        """
        return self.ap.parse_args(self.arguments)
