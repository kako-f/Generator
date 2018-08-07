import multiprocessing


class MpManager(object):
    def __init__(self, main_function, iterable_function, number_of_workers=None):
        """
        With this, the multiprocess routine is started, the given functions are initialized and
        distributed to the available or given cores.

        :param main_function: Main function to be distributed through the given cores (workers)
        :param iterable_function: Function to prepare the iterables to be distributed to the cores.
        :param number_of_workers: number of cores to work with.
        """
        self.main_function = main_function
        self.iterable_function = iterable_function
        self.pool_of_workers = multiprocessing.Pool(processes=number_of_workers)

    @staticmethod
    def return_thread_status():
        """
        TODO
        :return:
        """
        return multiprocessing.current_process()

    def random_genome_creation(self, files):
        """
        Each core handle the creation of a random sequence if it's needed.


        :param files: files from which the random sequences are created
        :return:
        """
        file = self.pool_of_workers.map(func=self.main_function, iterable=self.iterable_function(files))
        self.pool_of_workers.close()
        self.pool_of_workers.join()

        return file
