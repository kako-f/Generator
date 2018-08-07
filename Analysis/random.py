import numpy
import os

from Bio.SeqIO.FastaIO import FastaIterator
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq as BioPythonSeq
from Bio import SeqIO

from common.commonFunc import CommonFunctions as Cf
from MpManager.MpClass import MpManager as Mpm


class RandomCreation(object):
    def __init__(self, av_cores, files, type_of_seq):
        self.av_cores = av_cores
        self.files = files
        self.change_length = False
        self.new_length = 0
        self.content_weights = None
        self.type_of_seq = type_of_seq
        self.final_files = ''
        if type_of_seq == 'dna':
            self.content_weights = {'A': 0.0, 'C': 0.0, 'T': 0.0, 'G': 0.0, 'R': 0.0, 'Y': 0.0, 'N': 0.0, 'a': 0.0,
                                    'c': 0.0, 't': 0.0, 'g': 0.0}
        elif type_of_seq == 'rna':
            self.content_weights = {'A': 0.0, 'C': 0.0, 'T': 0.0, 'G': 0.0, 'R': 0.0, 'Y': 0.0, 'N': 0.0, 'a': 0.0,
                                    'c': 0.0, 't': 0.0, 'g': 0.0}
        elif type_of_seq == 'prot':
            self.content_weights = {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 0.0, 'F': 0.0, 'G': 0.0, 'H': 0.0,
                                    'I': 0.0, 'J': 0.0, 'K': 0.0, 'L': 0.0, 'M': 0.0, 'N': 0.0, 'O': 0.0, 'P': 0.0,
                                    'Q': 0.0, 'R': 0.0, 'S': 0.0, 'T': 0.0, 'U': 0.0, 'V': 0.0, 'W': 0.0, 'Y': 0.0,
                                    '*': 0.0}

    @staticmethod
    def read_files(files):
        """
        TODO
        :param files:
        :return:
        """
        for file in files:
            yield file

    @staticmethod
    def count_bases(sequence, bases):
        """
        Class to count "genomic" data (prot, dna, rna, etc)

        :param sequence: Sequence to analyze
        :param bases: allowed bases (nucleotides, aminoacids, etc.)
        :return: key and value
        """

        content_weights = {}
        allowed_bases = []

        if bases is 'dna':
            allowed_bases = ['A', 'C', 'G', 'T', 'U', 'R', 'Y', 'K', 'M', 'S', 'W', 'B', 'D', 'H', 'V', 'N', '-', 'a',
                             'c', 'g', 't']
        elif bases is 'prot':
            allowed_bases = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                             'S', 'T', 'U', 'V', 'W', 'Y', '*']
        elif bases is 'rna':
            allowed_bases = ['A', 'C', 'G', 'T', 'U', 'R', 'Y', 'K', 'M', 'S', 'W', 'B', 'D', 'H', 'V', 'N', '-', 'a',
                             'c', 'g', 't']

        for base in allowed_bases:
            content_weights[base] = sequence.count(base) / len(sequence)

        return list(content_weights.keys()), list(content_weights.values())

    def initialize_rsc(self):
        """
        TODO
        :return:
        """
        question_choice = Cf().query_yes_no("\nYou can choose the weight of the nucleotides of the random "
                                            "sequences to be created.\nIf you choose to not specify the "
                                            "weight of the nucleotides the biological values will be used "
                                            "instead.\n"
                                            "Want to proceed?")
        question_length = Cf().query_yes_no(
            "Want to input a length for the sequence or use the biological one?")
        if question_choice:
            print('Content: ' + str(self.content_weights.keys()))
            for key in self.content_weights.keys():
                while True:
                    try:
                        new_weight = float(input('Enter value for ' + key + ': '))
                        if not (0.0 <= new_weight < 1):
                            raise ValueError()
                        else:
                            if sum(self.content_weights.values()) + new_weight <= 1:
                                self.content_weights[key] = new_weight
                            else:
                                raise TypeError()
                    except ValueError:
                        print('Invalid input, please input float numbers between [0 and 1)')
                    except TypeError:
                        print('The sum of all the weights can\'t be greater than 1.')
                    else:
                        break
        else:
            pass

        if question_length:
            self.change_length = True
            while True:
                try:
                    self.new_length = int(input('Enter new length value: '))
                except ValueError:
                    print('Invalid input, please input integers.')
                else:
                    break
        else:
            pass

    def generate_rs(self, sequence):
        """
        TODO
        :param sequence:
        :return:
        """
        keys, weights = None, None
        if self.type_of_seq == 'dna':
            keys, weights = self.count_bases(sequence=sequence, bases='dna')
        elif self.type_of_seq == 'rna':
            keys, weights = self.count_bases(sequence=sequence, bases='rna')
        elif self.type_of_seq == 'prot':
            keys, weights = self.count_bases(sequence=sequence, bases='prot')

        print(keys, weights, sum(weights))

        if sum(self.content_weights.values()) == 0.0:
            if self.change_length:
                ran_sequence = numpy.random.choice(keys, self.new_length, p=weights)
                return "".join(x for x in ran_sequence)
            else:
                ran_sequence = numpy.random.choice(keys, len(sequence), p=weights)
                return "".join(x for x in ran_sequence)
        else:
            if self.change_length:
                final_random_sequence = numpy.random.choice(list(self.content_weights.keys()), self.new_length,
                                                            p=list(self.content_weights.values()))
            else:
                final_random_sequence = numpy.random.choice(list(self.content_weights.keys()), len(sequence),
                                                            p=list(self.content_weights.values()))
            return ''.join(x for x in final_random_sequence)

    def create_rs(self, file):

        newpath = Cf().create_file_folder(file=file)
        filename, extension = os.path.splitext(os.path.basename(file))
        random_genome_file = os.path.join(newpath, os.path.normpath(os.path.join(filename + '_random' + extension)))
        with open(file, 'rU') as GenomeFile:
            with open(random_genome_file, 'w') as RgFile:
                for record in FastaIterator(handle=GenomeFile):
                    print('Creating random record for: ' + record.id)
                    created_random_seq = self.generate_rs(str(record.seq))
                    random_record = SeqRecord(BioPythonSeq(created_random_seq),
                                              id=record.id + '_random_',
                                              name=record.name + '_random_',
                                              description=record.description + '_random_')
                    SeqIO.write(random_record, RgFile, 'fasta')
            RgFile.close()

        return random_genome_file

    def start_random_creation(self):
        """
        TODO
        :return:
        """
        mp_ran_gen_creation_task = Mpm(main_function=self.create_rs, iterable_function=self.read_files,
                                       number_of_workers=self.av_cores)
        file = mp_ran_gen_creation_task.random_genome_creation(files=self.files)
        self.final_files = file
        mp_ran_gen_creation_task.pool_of_workers.terminate()
