# Research: Midi File Format

**Related issue:** #25 <br>
**Time spent:** 2 h

## Question

How do midi files save data and what parts of a midi file should be saved for training?

## Findings

### Data Format

Most values inside a MIDI file are stored big-endian.
Delta times (and a few other values) use a variable-length format instead, where the lower 7 bits of each byte hold data and the top bit signals that another byte follows, up to a 4 bytes or 0x0FFFFFFF.

### Header Chunk

First 14 bytes of a midi file is a header chunk.
First 4 bytes of the header are always the same (0x4D546864) so it can be used for checking if the midi file is valid.
Next 4 bytes should be equal 6 as it is the length of the chunk. After the 8-byte Mthd + chunk length the remaining 6 bytes of the header need to be saved as it is format type (2 bytes need to be a number between 0 and 2), number of tracks (2 bytes a number from 1-65535 for format 1 and 2 and 1 for format 0) and time division (2 bytes either ticks per quarter-note (msb = 0) or frames per second (msb = 1)).

### Track Chunk

Than the file is divided into track chunks ( the number of them is given in the header ).
First 4 bytes are always the same (0x4D54726B). Next 4 bytes specify the length of the track in bytes. After that its just a stream of midi events.

### MIDI Events

Each event starts with a variable-length delta time relative to the previous event in the track, then the event data. Its either a channel event (0x8–0xE), meta event (0xFF) or sysex (0xF0/0xF7).
Running status applies: a data byte where a status is expected reuses the previous status, cleared by any meta or sysex event. Note On with velocity 0 is Note Off, and pairs must be matched per (channel, pitch) in order.

### Needed Elements

For training only the notes are needed not the full event stream.
From the header the time division has to be kept and the format and track count are keept for orientation while parsing.
From the events only Note On and Note Off are needed, accumulated into absolute ticks and stored as pitch, onset, duration, velocity, channel and track index.
Song-level information such as key signature, time signature and track indexes need to be stored.
Tempo, controllers and sysex can all be skipped, because they dont change the note sequence.
Files whose time division has the top bit set use SMPTE timing, have no musical grid, and should either be converted or skipped.

## Sources

- [Official Midi File Format](https://midi.org/summary-of-midi-1-0-messages) - specifications of a midi file by midi organisation
- [Midi File Format](https://web.archive.org/web/20141126200842/https://sonicspot.com/guide/midifiles.html) - specifications of a midi file
- [Midi Format More Info](https://www.fileformat.info/format/midi/corion.htm) - more specifications of a midi file
