import pickle
import os

class SavedInstanceUtils:
    @staticmethod
    def dump_pickle(instance, file_path = "./SavedRuntimeContent/a.pickle"):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        f = open(file_path, "wb")
        pickle.dump(instance, f)
        f.close()

    @staticmethod
    def load_pickle(file_path = "./SavedRuntimeContent/a.pickle"):
        if not os.path.exists(file_path):
            raise Exception
        f = open(file_path, "rb")
        instance = pickle.load(f)
        f.close()
        return instance

