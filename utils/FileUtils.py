from Config import *

class FileUtils:
    @classmethod
    def save_coverage(cls, depth, cov):
        file_name = cls.__get_cov_file_path()
        cls.__write_cov(file_name, depth, cov)

    @staticmethod
    def __get_cov_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        cov_file_name = "coverage.txt"
        return os.path.join(config_path, cov_file_name)

    @staticmethod
    def __write_cov(file_path:str, depth, cov):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        fw.write(f"{depth}:{cov}" + "\n")
        fw.close()


