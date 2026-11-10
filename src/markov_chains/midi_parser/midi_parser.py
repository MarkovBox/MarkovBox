from dataclasses import dataclass
EventTypes = {  # [code,length (in bytes)]
    "noteoff": [0x8, 3],
    "noteon": [0x9, 3],
    "noteaftertouch": [0xA, 3],
    "controller": [0xB, 3],
    "programchange": [0xC, 2],
    "channelaftertouch": [0xD, 2],
    "pitchbend": [0xE, 3]
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
    # time_signature: tuple[int, int]
    key: tuple[int, int]  # [number of sharps((-7) - 7),major(0) or minor(1)]
    tracks: list[Track]


class MidiFile:
    format_type = -1
    number_of_tracks = -1
    ticks_per_beat = -1
    song = None

    def __init__(self, filepath: str) -> None:
        with open(filepath, "rb") as f:  # TODO: add error handling
            self.file_content = bytearray(f.read())

    def parse_header(self, header: bytearray) -> None:
        # every midi file begins with MThd 0 0 0 6
        if header[:4] != bytes.fromhex("4D546864"):  # magic number 'MThd'
            exit(1)  # TODO: add error handling
        if header[4:8] != bytes.fromhex("00000006"):  # length of the header
            exit(1)  # TODO: add error handling

        self.format_type = int.from_bytes(header[8:10], "big")
        self.number_of_tracks = int.from_bytes(header[10:12], "big")
        division = int.from_bytes(header[12:14], "big")

        if (self.format_type == 0 and (self.number_of_tracks != 1)) or self.format_type > 2:
            exit(1)  # TODO: add error handling

        if division & 0x8000:
            # SMPTE
            pass  # for now
        else:
            self.ticks_per_beat = division & 0x7FFF
            self.song = Song(self.ticks_per_beat, None, None)

    def parse_track_header(self, track_header: bytearray) -> int:
        # magic number 'MTrk'
        print(track_header)
        if track_header[:4] != bytes.fromhex("4D54726b"):
            exit(1)  # TODO: add error handling
        return int.from_bytes(track_header[4:8], "big")

    def parse_event(self, event: bytearray) -> int:
        pass

    def parse_track(self, track: bytearray, size: int):
        location = 0
        while location < size:
            location += self.parse_event(track[location:])

    def parse(self):
        self.parse_header(self.file_content[:14])
        location = 14
        for i in range(self.number_of_tracks):
            length_of_chunk = self.parse_track_header(
                self.file_content[location:location+8])
            location += 8
            self.parse_track(
                self.file_content[location:location+length_of_chunk], length_of_chunk)
            location += length_of_chunk
        print(self.ticks_per_beat, self.format_type, self.number_of_tracks)


# for testing
# will be removed later
if __name__ == "__main__":
    a = MidiFile("./midi_file.mid")
    a.parse()
