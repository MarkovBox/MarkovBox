from dataclasses import dataclass
EventTypes = { # [code,length (in bytes)]
    "noteoff" : [0x8,3],
    "noteon" : [0x9,3],
    "noteaftertouch" : [0xA,3],
    "controller" : [0xB,3],
    "programchange" : [0xC,2],
    "channelaftertouch" : [0xD,2],
    "pitchbend" : [0xE,3]
}

@dataclass
class Note:
    pitch: int
    onset: int
    duration: int
    velocity: int
    channel: int
    track: int

class MidiFile:
    _file_content = None
    def __init__(self,filepath : str) -> None:
        with open(filepath,"rb") as f:
            _file_content = f.read()
