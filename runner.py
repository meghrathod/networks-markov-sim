import environment
import main

TTT_range = [50]
HYSTERESIS_range = [5, 7, 10, 12, 14, 16, 18, 20]
VELOCITY_range = ((0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8))

for TTT in TTT_range:
    for HYSTERESIS in HYSTERESIS_range:
        for VELOCITY in VELOCITY_range:
            environment.TTT = TTT
            environment.HYSTERESIS = HYSTERESIS
            environment.MAX_SPEED = VELOCITY[0]
            environment.MIN_SPEED = VELOCITY[1]
            main.run_threads(TTT, HYSTERESIS, VELOCITY[0], VELOCITY[1])
