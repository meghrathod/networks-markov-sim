import random

import environment


class UE:
    """
    Defines user entity in the environment
    """

    velocity = environment.VELOCITY
    direction = 1  # 0 - Towards 0, 1 - Away from
    nearby_bs = []
    HO_success = 0
    HO_failure = 0
    associated_eNB = None

    def __init__(self, x):
        self.x = x
        self.id = random.randint(0, 1000)

    def set_eNB(self, associated_eNB):
        self.associated_eNB = associated_eNB

    def get_eNB(self):
        return self.associated_eNB

    def get_id(self):
        return self.id

    def get_location(self):
        return self.x

    def set_location(self, x):
        self.x = x

    def set_nearby_bs(self, nearby_bs):
        self.nearby_bs = nearby_bs

    def set_direction(self, direction):
        self.direction = direction

    def set_velocity(self, velocity):
        self.velocity = velocity

    def __str__(self):
        return "UE located at %s" % self.x

    def move(self):  # Move the UE in the environment per millisecond
        if self.direction == 0:
            self.x = self.x + self.velocity / 1000
        else:
            self.x = self.x - self.velocity / 1000

    def generate_random_motion(self, constant):
        if constant == 'v':
            self.set_direction(random.randint(0, 1))
            self.move()
        if constant == 'd':
            self.set_velocity(random.randint(0, 100))
            self.move()
        if constant == 'vd':
            self.move()

    def getRSSI(self, bs):
        return bs.calc_received_power(self.x, environment.FREQ)

    def detect_HO(self):
        pass
