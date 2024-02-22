import requests
import json
import mido
from abc import ABC, abstractmethod
from typing import Dict

LEDFX_HOST = "http://localhost:8888"


class ApiCall(ABC):
    def __init__(self, host: str):
        self._host = host

    @abstractmethod
    def process(self, midi_msg):
        raise NotImplementedError("Please Implement this method")


class OneShot(ApiCall):
    def __init__(self, host, virtual, color):
        super().__init__(host)
        self._virtual = virtual
        self._api = host + "/api/virtuals_tools/" + virtual
        self._put_json = {
            "tool": "oneshot",
            "color": color,
            "ramp": 10,
            "hold": 0,
            "fade": 200
        }

    def process(self, midi_msg):
        requests.put(self._api, json=self._put_json)


class MidiInput:
    def __init__(self, midi_type: str, channel: int, note: int, control: int):
        self._type = midi_type
        self._channel = channel
        self._note = note
        self._control = control

    def match(self, msg) -> bool:
        if self._type is not None and msg.type != self._type:
            return False
        if self._control is not None and msg.control != self._control:
            return False
        if self._note is not None and msg.note != self._note:
            return False
        if self._channel is not None and msg.channel != self._channel:
            return False
        return True


class InputProcessor:
    def __init__(self, midi_port: str):
        self._midi_port: str = midi_port
        self._midi_triggers: Dict[MidiInput, ApiCall] = {}

    def add_midi_trigger(self, midi_input: MidiInput, api_call: ApiCall):
        self._midi_triggers[midi_input] = api_call

    def run(self):
        with mido.open_input(self._midi_port) as in_port:
            for msg in in_port:
                for midi_input, api_call in self._midi_triggers.items():
                    if midi_input.match(msg):
                        api_call.process(msg)
                        continue


def main():
    api_url = "http://localhost:8888/api/virtuals"
    response = requests.get(api_url)
    print(json.dumps(response.json(), sort_keys=True, indent=2))
    api_url = "http://localhost:8888/api/virtuals/tester/effects"
    response = requests.get(api_url)
    print(json.dumps(response.json(), sort_keys=True, indent=2))
    # todo = {"config": {"brightness": 1.0}, "type": "blade_power_plus"}
    # response = requests.post(api_url, json=todo)
    # print(json.dumps(response.json(), sort_keys=True, indent=2))
    with mido.open_input('Arturia MiniLab mkII MIDI 1') as inport:
        for msg in inport:
            print(msg)
            # response = requests.get(api_url)
            # todo = response.json()['effect']
            # todo['config']['brightness'] = msg.value/127.0
            # requests.post(api_url, json=todo)
            if msg.type == 'note_on' and msg.note == 48:
                oneshot_api = "http://localhost:8888/api/virtuals_tools"
                todo = {
                    "tool": "oneshot",
                    "color": "red",
                    "ramp": 10,
                    "hold": 0,
                    "fade": 200
                }
                response = requests.put(oneshot_api, json=todo)
                print(response)
                # print(json.dumps(response.json(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
