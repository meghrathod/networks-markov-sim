import environment


class Ticker:
    """This class defines the properties of a ticker, i.e. a timer that ticks at a certain interval."""

    def __init__(self):
        self.ticker_duration = environment.TICKER_INTERVAL
        self.time = 0

    def tick(self):
        self.time += self.ticker_duration

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time
