# Research: WAV File Format

**Related issue:** #34 <br>
**Time spent:** 2 h

## Question

How does a WAV file store the waveform and information about the sound?

## Findings

### Data Format

WAV is a container based on the **RIFF**. RIFF splits a file into chunks. Each chunk consists of:

- a 4-byte ASCII identifier (`"fmt "`, `"data"`)
- a 4-byte size of the chunk's content (not including the identifier and the size field itself)
- the content of the chunk

A WAV file is a single `RIFF` chunk containing the form type `"WAVE"` and at least two sub-chunks: `fmt ` and `data`.
All values inside a WAV file are stored little-endian.

### WAV file header

The header of a basic PCM WAV file is exactly 44 bytes.

| Byte offset | Field           | Size | Sample value | Description                                              |
| :---------- | :-------------- | :--- | :----------- | :------------------------------------------------------- |
| 0-3         | Chunk ID        | 4    | `"RIFF"`     | Marks the file as RIFF format                            |
| 4-7         | Chunk size      | 4    | `1024`       | File size minus 8 bytes (`"RIFF"` ID and this field)     |
| 8-11        | Format          | 4    | `"WAVE"`     | Identifies the RIFF form as WAV                          |
| 12-15       | Subchunk 1 ID   | 4    | `"fmt "`     | Format chunk marker                                      |
| 16-19       | Subchunk 1 size | 4    | `16`         | Size of the remaining format data                        |
| 20-21       | Audio format    | 2    | `1`          | Encoding type (`1` = PCM)                                |
| 22-23       | Channels        | 2    | `2`          | Number of channels (`1` = mono, `2` = stereo)            |
| 24-27       | Sample rate     | 4    | `44100`      | Samples per second, per channel                          |
| 28-31       | Byte rate       | 4    | `176400`     | `Sample rate * Channels * Bits per sample / 8`           |
| 32-33       | Block align     | 2    | `4`          | Bytes per sample frame: `Channels * Bits per sample / 8` |
| 34-35       | Bits per sample | 2    | `16`         | Bit depth of a single sample                             |
| 36-39       | Subchunk 2 ID   | 4    | `"data"`     | Data chunk marker                                        |
| 40-43       | Subchunk 2 size | 4    | `988`        | Size of the audio data in bytes (file size - 44)         |

### Data section

The `data` chunk starts right after the header and contains raw samples with no further structure.

- **Sample** - a single amplitude value of one channel at a given moment.
- **Sample frame** - one sample for each channel, taken at the same moment.

Layout for 16-bit stereo:

| Bytes 0-1          | Bytes 2-3         | Bytes 4-5         | Bytes 6-7         |
| :----------------- | :---------------- | :---------------- | :---------------- |
| sample 0 , frame 0 | sample 1, frame 0 | sample 0, frame 1 | sample 1, frame 1 |

Number encoding depends on bit depth:

| Bits per sample | Type             | Range             | Silence |
| :-------------- | :--------------- | :---------------- | :------ |
| 8               | unsigned integer | 0 - 255           | 128     |
| 16              | signed integer   | -32768 - 32767    | 0       |
| 24 / 32         | signed integer   | full signed range | 0       |

## Sources

- [WAV Wikipedia ](https://pl.wikipedia.org/wiki/WAV) - overview of the WAV format
- [WAV format)](http://soundfile.sapp.org/doc/WaveFormat/) - description of the 44-byte header
