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

