from typing import Dict, List


class MidiInput:
    def __init__(self, cfg: Dict):
        self._type = cfg['type']
        self._channel = cfg['channel']
        self._note = cfg['note']
        self._control = cfg['control']

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
