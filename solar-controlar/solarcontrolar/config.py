import json
import copy


class Config:

    def __init__(self, filename="config.json", data=None):
        self.filename = filename;

        if data is None:
            with open("config.json", "r") as file:
                self.__data = json.load(file)

    def get_data(self):
        return copy.deepcopy(self.__data)

    def with_data(self, data):
        value = Config(self.filename)
        value.__data = self.get_data()
        return value

    def save(self):
        with open(self.filename, "w") as file:
            json.dump(self.__data, file, indent=4)
