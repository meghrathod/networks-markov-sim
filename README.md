# NR Simulator

> This is a simulator for performance analysis of the Handover mechanism in a wireless system with 5G NR(New Radio) technology and 4G
> LTE (Long Term Evolution Technology)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This is a simulator for analysis of the fast conditional handover using a novel Markov Model. The simulator is written in Python. The simulator is
designed to be modular and extensible. It is possible to add new handover algorithms and new mobility models.

## Installation

The simulator is written in Python and uses the following libraries governed by their respective licenses:

- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [math](https://docs.python.org/3/library/math.html)
- [random](https://docs.python.org/3/library/random.html)
- [time](https://docs.python.org/3/library/time.html)

## Usage

The simulator is designed to be easy to use. The simulator is run after configuring `markov-runner.py`.

## Environment

The environment of the simulator is configurable with the environment.py file. The following parameters can be
configured:

- Frequency of base stations
- Number of base stations
- Time to trigger handover
- Input power of base stations
- Hysteresis
- Tprep and Texec
- Preparation and Execution offsets
- Velocity of user
- Bandwidth of base stations
- RLF Threshold
And a few other configurable properties can be extended by modifying `Simulate_UE.py`.

## License

[GNU General Public License v3.0](./LICENSE)
