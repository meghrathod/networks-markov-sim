# NR Simulator

> This is a simulator for analysis of Handover mechanism in a wireless system with 5G NR(New Radio) technology and 4G
> LTE (Long Term Evolution Technology)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This is a simulator for analysis of Handover mechanism, its success and failure rate in a wireless system with 5G NR(New
Radio) technology and 4G LTE (Long Term Evolution Technology). The simulator is written in Python. The simulator is
designed to be modular and extensible. It is possible to add new handover algorithms and new mobility models.

## Installation

The simulator is written in Python and uses the following libraries:

- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [math](https://docs.python.org/3/library/math.html)
- [random](https://docs.python.org/3/library/random.html)
- [time](https://docs.python.org/3/library/time.html)

## Usage

The simulator is designed to be easy to use. The simulator is run by executing the following command:

```
python3 main.py
```

## Environment

The environment of the simulator is configurable with the environment.py file. The following parameters can be
configured:

- Frequency of base stations
- Number of base stations
- Time to trigger handover
- Input power of base stations
- Hysteresis

## Handover Algorithm : A3 Based

- This project has implemented a A3 based handover algorithm. This algorithm uses RSRP (Reference Signal Received Power)
  to determine the best base station to connect to. The base station with the highest RSRP is chosen.
- Project uses Random Waypoint Mobility Model to generate mobility of UE (User Equipment).
- Project uses a 1D line to simulate the environment.
- At every time tick, the UE measures the RSRP of all the base stations nearby and if the RSRP of the current base
  station is less than the RSRP of the best base station by a hysteresis amount for a minimum time to trigger, the UE
  will trigger a handover to the best base station.
- The simulator will run for a specified number of time ticks and will output the number of handovers that occurred, the
  number of successful handovers and the number of failed handovers.

## License

[GNU General Public License v3.0](./LICENSE)