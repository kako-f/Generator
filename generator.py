import sys
import platform
import datetime

from common.argumentParser import ArgumentParser as Ap
from common.commonFunc import CommonFunctions as Cf
from Analysis.random import RandomCreation as Rc

program_name = 'GenFetcher'
program_ver = '1.0.0'
system = platform.system()


def main_module(args):
    arguments = Ap(prog_version=program_ver, argv=args, program_name=program_name)

    start_time = datetime.datetime.now()
    print('\nStarted at: ', start_time)

    if arguments.return_arguments().dna is not None and arguments.return_arguments().dna is not False:
        print('Analyzing DNA sequences.\n')
        type_of_seq = 'dna'
    elif arguments.return_arguments().prot is not None and arguments.return_arguments().prot is not False:
        print('Analyzing Protein sequences. \n')
        type_of_seq = 'prot'
    elif arguments.return_arguments().rna is not None and arguments.return_arguments().rna is not False:
        print('Analyzing RNA sequences. \n')
        type_of_seq = 'rna'
    else:
        print('Analyzing DNA sequences.\n')
        type_of_seq = 'dna'

    if arguments.return_arguments().random is not None and arguments.return_arguments().random is not False:

        print("\nInput the directory where the files are located.")
        input_files = Cf().get_files(file_extensions=("*.fasta", "*.fna", '*.faa'))
        Cf().annotation_files(genomes_files=input_files)
        random_creation = Rc(av_cores=arguments.return_arguments().nuc,
                             files=input_files,
                             type_of_seq=type_of_seq)
        random_creation.initialize_rsc()
        random_creation.start_random_creation()
    else:
        pass

    end_time = datetime.datetime.now()
    print('Ended at: ', end_time)
    print('Total execution time: ', end_time - start_time)


if __name__ == '__main__':
    intro = '\n############################################\n' \
            '# {p} {v}                          #\n' \
            '# Create random genomes.    #\n' \
            '############################################'.format(v=program_ver, p=program_name)
    system_info = '\n########################\n' \
                  '# Platform : {plat}   #\n' \
                  '########################\n'.format(plat=system)

    print(intro)
    print(system_info)
    main_module(sys.argv[1:])

# print('\nInput a folder name where to save the analyzed random data.\n'
#       ' * If the folder doesn\'nt exist it will be created.\n'
#       ' * If there is any data created by the program in the specified folder, '
#       'this will be overwritten.\n')
# ran_db_folder = commonfunc.check_input()
# ran_db = Db.Database(db_folder=ran_db_folder)
#
# print("\nInput the directory where the files are located.")
# input_files = commonfunc.get_files(file_extensions=("*.fasta", "*.fna", "*.faa"))
# print('Starting the analysis on ' + str(len(input_files)) + ' file(s).')
# commonfunc.annotation_files(genomes_files=input_files)
#
# random_analysis = RanAnalysis(kmer_size=arguments.return_arguments().k,
#                               av_cores=arguments.return_arguments().nuc,
#                               database=ran_db,
#                               files=input_files,
#                               chunk_size=arguments.return_arguments().limit,
#                               multi_fasta=arguments.return_arguments().mfasta,
#                               type_of_seq=type_of_seq,
#                               masked=arguments.return_arguments().maskedregions,
#                               type_of_an=type_of_an)
# random_analysis.initialize_rsc()
# random_analysis.start_random_creation()
# random_analysis.start_analysis()
