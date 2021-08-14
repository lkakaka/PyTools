import os

CONFIG_FILE = os.path.dirname(__file__) + "/../config.txt"


class Config:

    @staticmethod
    def read_config():
        print("read config******")
        with open(CONFIG_FILE) as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#"):
                    continue
                arr = line.split("=")
                print("{0}={1}".format(arr[0], arr[1]))
                setattr(Config, arr[0], arr[1])

    @staticmethod
    def get_config_str(key):
        return Config.__dict__.get(key)


Config.read_config()
