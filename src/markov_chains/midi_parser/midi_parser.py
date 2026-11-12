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
        self.running_status = None
        self._active_notes: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self._current_notes: list[Note] = []
        self._current_track_idx = 0
        try:
            with open(filepath, "rb") as f:
                self.file_content = bytearray(f.read())
        except FileNotFoundError as e:
            print("Error:", e)

    def parse_header(self, header: bytearray) -> None:
        # every midi file begins with MThd 0 0 0 6
        if header[:4] != bytes.fromhex("4D546864"):  # magic number 'MThd'
            raise ValueError("Invalid Midi file(header)")
        if header[4:8] != bytes.fromhex("00000006"):  # length of the header
            raise ValueError("Invalid Midi header length")

        self.format_type = int.from_bytes(header[8:10], "big")
        self.number_of_tracks = int.from_bytes(header[10:12], "big")
        division = int.from_bytes(header[12:14], "big")

        if (self.format_type == 0 and (self.number_of_tracks != 1)) or self.format_type > 2:
            raise ValueError("Invalid midi format type or number of tracks")

        if division & 0x8000:
            # SMPTE
            raise NotImplemented("SMPTE not implemented")
        else:
            self.ticks_per_beat = division & 0x7FFF
            self.song = Song(self.ticks_per_beat, (0, 0), [])

    def parse_track_header(self, track_header: bytearray) -> int:
        # magic number 'MTrk'
        if track_header[:4] != bytes.fromhex("4D54726b"):
            raise ValueError("Invalid Midi file(track)")
        return int.from_bytes(track_header[4:8], "big")

    def note_on(self, channel, pitch, velocity, time):
        self._active_notes.setdefault(
            (channel, pitch), []).append((time, velocity))

    def note_off(self, channel, pitch, time):
        key = (channel, pitch)
        queue = self._active_notes.get(key)
        if not queue:
            return
        onset, velocity = queue.pop(0)
        self._current_notes.append(Note(
            pitch=pitch,
            onset=onset,
            duration=time - onset,
            velocity=velocity,
            channel=channel,
            track=self._current_track_idx))

    def meta_and_sysex(self, status, event, i, current_time):
        # meta
        if status == 0xFF:
            meta_type = event[i]
            i += 1
            j = 0
            length = 0
            while True:
                b = event[i]
                i += 1
                length = (length << 7) | (b & 0x7F)
                if (b & 0x80) and j > 3:
                    raise ValueError("Invalid variable length values")
                j += 1
                if not (b & 0x80):
                    break
            data = event[i:i + length]
            i += length

            if meta_type == 0x2F:                       # end of track
                return (i, current_time, True)
            if meta_type == 0x59 and length == 2:       # key signature
                self.song.key = (
                    int.from_bytes(data[0:1], "big", signed=True),
                    data[1],
                )
            return (i, current_time, False)

        # sysex
        if status in (0xF0, 0xF7):
            length = 0
            while True:
                b = event[i]
                i += 1
                length = (length << 7) | (b & 0x7F)
                if not (b & 0x80):
                    break
            i += length
            return (i, current_time, False)
        return (i, -1, False)

    def channel_events(self, status, event, i, current_time):
        event_type = status >> 4
        channel = status & 0x0F

        name, msg_length = None, 0
        for evt_name, (code, length) in EventTypes.items():
            if code == event_type:
                name, msg_length = evt_name, length
                break
        if name is None:
            raise ValueError(f"Unknown event type: 0x{status:02X}")

        if name == "noteon":
            pitch, velocity = event[i], event[i + 1]
            i += 2
            if velocity == 0:                          # Note On vel 0 == Note Off
                self.note_off(channel, pitch, current_time)
            else:
                self.note_on(channel, pitch, velocity, current_time)
        elif name == "noteoff":
            pitch = event[i]
            i += 2
            self.note_off(channel, pitch, current_time)
        elif name == "noteaftertouch":
            i += 2
        elif name == "channelaftertouch":
            i += 1
        else:
            i += msg_length - 1

        return i

    def close_unterminated_notes(self, end_time: int):
        for (channel, pitch), queue in self._active_notes.items():
            while queue:
                onset, velocity = queue.pop(0)
                self._current_notes.append(Note(
                    pitch=pitch,
                    onset=onset,
                    duration=end_time - onset,
                    velocity=velocity,
                    channel=channel,
                    track=self._current_track_idx))
        self._active_notes.clear()

    # [length,time,end of track]
    def parse_event(self, event: bytearray, previous_event_time: int) -> [int, int, bool]:
        i = 0
        delta_time = 0
        j = 0
        while True:
            b = event[i]
            i += 1
            delta_time = (delta_time << 7) | (b & 0x7F)
            if (b & 0x80) and j > 3:
                raise ValueError("Invalid variable length values")
            j += 1
            if not (b & 0x80):
                break
        current_time = previous_event_time + delta_time

        # status byte
        status = event[i]
        if status < 0x80:
            if self.running_status is None:
                raise ValueError("Running status without previous status")
            status = self.running_status
        else:
            i += 1
            self.running_status = status if status < 0xF0 else None

        # meta and sysex events handling
        mns_ret_val = self.meta_and_sysex(status, event, i, current_time)
        if mns_ret_val[1] != -1:
            return mns_ret_val
        i = mns_ret_val[0]

        i = self.channel_events(status, event, i, current_time)

        return (i, current_time, False)

    def parse_track(self, track: bytearray, size: int):
        self._active_notes = {}
        self._current_notes = []
        self._current_track_idx = len(self.song.tracks)
        self.running_status = None

        location, time = 0, 0
        while location < size:
            consumed, time, eot = self.parse_event(track[location:], time)
            location += consumed
            if eot:
                break
        self.close_unterminated_notes(time)

        self.song.tracks.append(
            Track(self._current_track_idx, self._current_notes))

    def parse(self):
        self.parse_header(self.file_content[:14])
        location = 14
        for _ in range(self.number_of_tracks):
            length_of_chunk = self.parse_track_header(
                self.file_content[location:location+8])
            location += 8
            self.parse_track(
                self.file_content[location:location+length_of_chunk], length_of_chunk)
            location += length_of_chunk


if __name__ == "__main__":
    # usage
    a = MidiFile("./Super Mario 64 - Medley.mid")
    a.parse()
