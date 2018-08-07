import sys
import glob
import os
import fnmatch
from shutil import copy2


class CommonFunctions(object):
    def __init__(self):
        """
        Set of common function used by the program itself.
        Refer to each function for details
        """
        pass

    def get_files(self, file_extensions, directory=None):
        """

        :param file_extensions:
        :param directory:
        :return:
        """
        if directory is None:
            while True:
                try:
                    directory = self.check_input()
                    files_in_directory = []
                    if os.path.exists(path=directory):
                        for ext in file_extensions:
                            if sys.version_info[0] > 3 and sys.version_info[1] >= 5:
                                files_in_directory.extend(
                                    glob.glob(os.path.normpath(os.path.join(directory, ext)), recursive=True))
                            else:
                                for root, dirnames, filenames in os.walk(directory):
                                    for filename in fnmatch.filter(filenames, ext):
                                        files_in_directory.append(os.path.normpath(os.path.join(root, filename)))
                    else:
                        raise TypeError()
                except TypeError:
                    print('Could\'nt find any usable files in the given directory or does\'nt exists.\n')
                else:
                    break
        else:
            while True:
                try:
                    files_in_directory = []
                    if os.path.exists(path=directory):
                        for ext in file_extensions:
                            if sys.version_info[0] > 3 and sys.version_info[1] >= 5:
                                files_in_directory.extend(
                                    glob.glob(os.path.normpath(os.path.join(directory, ext)), recursive=True))
                            else:
                                for root, dirnames, filenames in os.walk(directory):
                                    for filename in fnmatch.filter(filenames, ext):
                                        files_in_directory.append(os.path.normpath(os.path.join(root, filename)))
                    else:
                        raise TypeError()
                except TypeError:
                    print('Could\'nt find any usable files in the given directory or does\'nt exists.\n')
                else:
                    break
        return files_in_directory

    @staticmethod
    def check_input():
        """

        Function to check if the input typed it's a valid one or not.

        :return: return input.
        """
        while True:
            try:
                typed_input = input("Please type your input : ")
                if not typed_input:
                    raise TypeError()
                else:
                    print("\n* Using \" %s \" * \n" % typed_input)
            except TypeError:
                print('Please enter a valid input.')
            else:
                break

        return typed_input

    @staticmethod
    def query_yes_no(question, default="yes"):
        """
        Ask a yes/no question via input() and return their answer.

        :param question: is a string that is presented to the user.
        :param default: is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).
        :return: The "answer" return value is True for "yes" or False for "no".

        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            choice = input(question + prompt)
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

    @staticmethod
    def create_file_folder(file, basepath=None):
        """
        function to create specified file folders.
        Choose between creating folder for the normal databases or the random ones.

        :param file:
        :param basepath:
        :return: path of the created folder
        """
        file_path = os.path.dirname(file)
        if basepath is None:
            basepath = os.path.basename(os.path.dirname(file_path))
        else:
            pass
        lastpath = os.path.basename(os.path.normpath(file_path))
        newpath = os.path.normpath(os.path.join(basepath, lastpath + '_random'))

        return newpath

    def annotation_files(self, genomes_files):
        """
        The main purpose of this function is to copy the annotation files of the sequence files to the directory where
        the random genomes are stored.
        Because the random sequence created it's essentially the same sequence with his content scrambled, the
        annotation file could be the same for obtaining the same basic information.


        :param genomes_files: genome files in directory
        :param temp_files: If more random files are created, we copy the same annotation files to a temp folder
        :return: Nothing
        """
        annotation_file_list = {}
        genome_file_list = {}

        file_path = os.path.dirname(genomes_files[0])

        newpath = self.create_file_folder(genomes_files[0])

        ann_file = self.get_files(file_extensions=("*.gbff", "*.gbk", "*.gb"), directory=file_path)

        if not os.path.exists(newpath):
            os.makedirs(newpath)
        else:
            pass
        for file in ann_file:
            name, ext = os.path.splitext(file)
            annotation_file_list[name] = ext
        for file in genomes_files:
            name, ext = os.path.splitext(file)
            genome_file_list[name] = ext

        intersection_list = set(annotation_file_list).intersection(genome_file_list)

        print('Creating annotation files for random sequence in ' + newpath + '.')

        for file in intersection_list:
            new_annotation_file = os.path.normpath(
                os.path.join(newpath, os.path.basename(file) + '_random' + annotation_file_list[file]))
            copy2(file + annotation_file_list[file], new_annotation_file)
