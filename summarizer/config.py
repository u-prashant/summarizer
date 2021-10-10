import os
import pickle
from constants import Errors


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.source_dir = '/'
        self.target_dir = '/'
        self.read()

    def read(self):
        try:
            with open(self.config_file, 'rb') as f:
                self.source_dir, self.target_dir = pickle.load(f)
        except:
            print(Errors.ConfigurationFileNotFound)

    def write(self):
        with open(self.config_file, 'wb') as f:
            pickle.dump([self.source_dir, self.target_dir], f)

    def set_source_dir(self, path):
        self.source_dir = self.get_directory(path)

    def set_target_dir(self, directory):
        self.target_dir = directory

    @staticmethod
    def get_directory(text):
        paths = text.split('\n')
        if not os.path.exists(paths[0]):
            return '/'
        return os.path.split(paths[0])[0]
