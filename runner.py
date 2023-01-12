import environment
import main

TTT_range = [25, 50, 100, 200, 300, 400, 500]
HYSTERESIS_range = [0, 3, 5, 7, 10, 12, 15, 17, 20]

for TTT in TTT_range:
    for HYSTERESIS in HYSTERESIS_range:
        environment.TTT = TTT
        environment.HYSTERESIS = HYSTERESIS
        main.run_threads(TTT, HYSTERESIS)
