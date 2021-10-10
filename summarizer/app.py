from config import Config
from constants import Files
from gui import GUI


def main(files: dict):
    config = Config(files[Files.CONFIG_FILE])
    GUI(config)


if __name__ == '__main__':
    files_map = {
        Files.CONFIG_FILE: 'data/config.pkl'
    }
    main(files_map)
