from Config import *

class FileUtils:
    @classmethod
    def save_coverage(cls, depth, a, b):
        file_name = cls.__get_cov_file_path()
        cls.__write_cov(file_name, depth, a, b)

    @staticmethod
    def __get_cov_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        cov_file_name = "coverage.txt"
        return os.path.join(config_path, cov_file_name)

    @staticmethod
    def __write_cov(file_path:str, depth, a, b):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        cov = a/b
        fw.write(f"{depth}:{a}/{b}={cov}" + "\n")
        fw.close()


