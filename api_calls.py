from abc import ABC, abstractmethod
from typing import Dict
import requests


class ApiCall(ABC):
    def __init__(self, host: str):
        self._host = host

    @abstractmethod
    def process(self, midi_msg):
        raise NotImplementedError("Please Implement this method")


class OneShot(ApiCall):
    def __init__(self, cfg: Dict):
        super().__init__(cfg['host'])
        self._virtual = cfg['virtual_id']
        self._api = self._host + "/api/virtuals_tools/" + self._virtual
        self._put_json = {
            "tool": "oneshot",
            "color": cfg['color'],
            "ramp": 10,
            "hold": 0,
            "fade": 200
        }

    def process(self, midi_msg):
        requests.put(self._api, json=self._put_json)


class AdjustBrightness(ApiCall):
    def __init__(self, cfg: Dict):
        super().__init__(cfg['host'])
        self._virtual = cfg['virtual_id']
        self._api = self._host + '/api/virtuals/' + self._virtual + '/effects'
        self._max_control_value = 127.0

        # The knob polling frequency is too large, so we only trigger on the Nth one.
        self._counter = 1
        self._skip = 4

    def process(self, midi_msg):
        self._counter += 1
        if self._counter % self._skip == 0:
            response = requests.get(self._api)
            todo = response.json()['effect']
            todo['config']['brightness'] = midi_msg.value / self._max_control_value
            requests.post(self._api, json=todo)
            self._counter = 0
