import random
from math import fabs
from typing import List

import environment
from eNB import eNB
from utils.Ticker import Ticker


# random.seed(42)


class UE:
    """Defines user entity in the environment"""

    def __init__(self, x, pause=100):
        self.direction = 1  # 0 - Towards 0, 1 - Away from
        self.nearby_bs = []
        self.HO_total = 0
        self.HO_success = [0, 0, 0, 0]
        self.HO_failure = [0, 0, 0, 0]
        self.associated_eNB = None
        self.upcoming_eNB = None
        self.velocity = 0
        self.time_at_destination = 0
        self.location = x
        self.id = random.randint(0, 1000)
        self.pause_time = pause
        self.waypoint = x
        self.destinations = []

    def set_eNB(self, associated_eNB):
        self.associated_eNB = associated_eNB

    def get_eNB(self) -> eNB:
        return self.associated_eNB

    def get_upcoming_eNB(self) -> eNB:
        return self.upcoming_eNB

    def set_upcoming_eNB(self, upcoming_eNB):
        self.upcoming_eNB = upcoming_eNB

    def get_id(self):
        return self.id

    def get_location(self):
        return self.location

    def set_location(self, x):
        self.location = x

    def set_nearby_bs(self, nearby_bs: List[eNB]):
        self.nearby_bs = nearby_bs

    def get_nearby_bs(self):
        return self.nearby_bs

    def set_direction(self, direction):
        self.direction = direction

    def set_HO_success(self, type_ho):
        self.HO_total += 1
        if type_ho == 0:
            self.HO_success[0] += 1
        elif type_ho == 1:
            self.HO_success[1] += 1
        elif type_ho == 2:
            self.HO_success[2] += 1
        elif type_ho == 3:
            self.HO_success[3] += 1

    def get_HO_success(self):
        return self.HO_success

    def get_HO_failure(self):
        return self.HO_failure

    def get_HO_total(self):
        return self.HO_total

    def set_HO_failure(self, type_ho):
        self.HO_total += 1
        if type_ho == 0:
            self.HO_failure[0] += 1
        elif type_ho == 1:
            self.HO_failure[1] += 1
        elif type_ho == 2:
            self.HO_failure[2] += 1
        elif type_ho == 3:
            self.HO_failure[3] += 1

    def set_velocity(self, velocity):
        self.velocity = velocity

    def __str__(self):
        return "UE located at %s" % self.location

    def move(
            self,
            ticker):  # Move the UE in the environment per millisecond(default)
        self.location += self.direction * self.velocity * ticker.ticker_duration
        ticker.tick()

    # def find_closest_bs(self):
    #     return min(
    #         self.nearby_bs,
    #         key=lambda bs: math.fabs(self.get_location() - bs.get_location()),
    #     )

    # def generate_random_motion(self, constant=None):
    #     if constant is None:
    #         self.set_velocity(random.randint(0, 100))
    #         self.set_direction(random.randint(-1, 1))
    #         self.move()
    #     if constant == "v":
    #         self.set_direction(random.randint(-1, 1))
    #         self.move()
    #     if constant == "d":
    #         self.set_velocity(random.randint(-1, 100))
    #         self.move()
    #     if constant == "vd":
    #         self.move()

    def get_min_max_bounds(self):
        """
        This function returns the minimum and maximum bounds on the destination selection for waypoint mobility
        """
        if self.location < 1000:
            min_bound = 0
            max_bound = self.location + 1000
        elif self.location > 49000:
            max_bound = 50000
            min_bound = self.location - 1000
        else:
            min_bound = self.location - 1000
            max_bound = self.location + 1000

        return min_bound, max_bound

    def get_handover_type(self):
        if (self.get_upcoming_eNB().get_type() == "lte"
                and self.get_eNB().get_type() == "lte"):
            return 0
        if (self.get_upcoming_eNB().get_type() == "lte"
                and self.get_eNB().get_type() == "nr"):
            return 1
        if (self.get_upcoming_eNB().get_type() == "nr"
                and self.get_eNB().get_type() == "lte"):
            return 2
        if (self.get_upcoming_eNB().get_type() == "nr"
                and self.get_eNB().get_type() == "nr"):
            return 3

    def update_UE_location(self, ticker: Ticker):
        """
        This function is responsible for random motion of the UE using the random waypoint model
        """
        # If it is time for the UE to start moving to the next destination, choose a new destination
        if (fabs(self.location) >= fabs(self.waypoint) and self.direction == 1) or \
                (fabs(self.location) <= fabs(self.waypoint) and self.direction == -1):
            # Choose a new destination between 0 and 50000 meters
            self.waypoint = random.uniform((self.get_min_max_bounds()[0]),
                                           self.get_min_max_bounds()[1])
            # Set the time at which the UE will start moving to the next destination
            self.pause_time = random.randint(environment.MIN_PAUSE, environment.MAX_PAUSE)
            # ticker.time = ticker.time + self.pause_time
            # Choose a new random speed between 10 and 50 meters per second (m/s) equivalent to 0.01 and 0.05 m/ms
            self.velocity = random.uniform(environment.MIN_SPEED, environment.MAX_SPEED)
            # Choose a new direction of movement based on the relative positions of the current location and the
            # destination
            if self.waypoint > self.location:
                self.direction = 1  # Move forwards
            else:
                self.direction = -1  # Move backwards
        # Update the UE's location based on its speed, direction, and the elapsed time
        self.move(ticker)
