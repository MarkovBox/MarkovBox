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

@dataclass
class Track:
    idx: int
    notes: list[Note]

@dataclass
class Song:
    ticks_per_beat: int
    time_signature: tuple[int,int]
    key: tuple[int,int] #[number of sharps((-7) - 7),major(0) or minor(1)]
    notes: list[Track]

class MidiFile:
    format_type = -1
    number_of_tracks = -1
    ticks_per_beat = -1

    def __init__(self,filepath : str) -> None:
        with open(filepath,"rb") as f: #TODO: add error handling
            self.file_content = bytearray(f.read())

    def parse_header(self,header: bytearray) -> None:
        if header[:8] != bytes.fromhex("4D54686400000006"): #every midi file begins with MThd 0 0 0 6
            exit(1) #TODO: add error handling

        self.format_type = int.from_bytes(header[8:10], "big")
        self.number_of_tracks = int.from_bytes(header[10:12], "big")
        division = int.from_bytes(header[12:14], "big")

        if (self.format_type == 0 and (self.number_of_tracks != 1)) or self.format_type > 2:
            exit(1) #TODO: add error handling

        if division & 0x8000:
            # SMPTE
            pass # for now
        else:
            self.ticks_per_beat = division & 0x7FFF 

    def parse(self):
        self.parse_header(self.file_content[:14])
        print(self.ticks_per_beat,self.format_type,self.number_of_tracks)



#for testing
#will be removed later
if __name__ == "__main__":
    a = MidiFile("./midi_file.mid")
    a.parse()
