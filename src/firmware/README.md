# MarkovBox

## Author

Oktawian Bieszke, Marcin Ptasiński, Mikołaj Domiński, Oliver Tyszko

## Description

MarkovBox - The self-composing synthesizer.

## Cloning

If you already cloned without submodules:

```sh
git submodule update --init --recursive
```

## Building

Requires the [ARM GCC toolchain](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm).

From `src/firmware` run:

```sh
make clean && make
```

## Flashing

Flashing over USB DFU (you must press `BOOT` + `RESET` buttons before flash):

```sh
make program-dfu
```

Or with an ST-Link connected:

```sh
make program
```
