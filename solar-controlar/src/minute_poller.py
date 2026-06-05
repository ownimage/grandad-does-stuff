import os

import requests

from common.json_store import JsonStore
from filenames import Filenames
from solarcontrolar.givenergyfactory import GivEnergyFactory


class MinutePoller:
    def __init__(self):
        self.givenergy = GivEnergyFactory(requests=requests, os=os).instance()
        self.store = JsonStore(Filenames.MINUTE_TOTALS_FILE.value)

    def run(self):
        data = self.store.read()
        date_str, time_str, solar, usage = self.givenergy.get_minute_data()

        if date_str not in data:
            data[date_str] = {}

        data[date_str][time_str] = {
            "solar": solar,
            "usage": usage
        }
        self.store.write(data)
        print(data)
        return data


if __name__ == "__main__":
    poller = MinutePoller()
    poller.run()
