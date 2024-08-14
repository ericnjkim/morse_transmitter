from dataclasses import dataclass
import time

@dataclass
class MorseTransmissionTimer:

    recorded_time = 0
    start_time = 0
    bpm = 0
    dot_length = 0
    dash_length = 0

    def __init__(self, bpm: int=60):
        self.bpm = bpm
        self.dash_length = 60/self.bpm
        self.dot_length = self.dash_length/3
        self.space_length = self.dot_length * 7

    def start_timer(self):
        self.start_time = time.perf_counter()

    def end_timer(self):
        self.recorded_time = time.perf_counter() - self.start_time

    def current_time(self) -> float:
        return time.perf_counter() - self.start_time

    def transmission(self):
        if self.recorded_time:
            if self.recorded_time <= self.dot_length:
                return "."
            elif self.dot_length <= self.recorded_time <= self.space_length:
                return "_"
            else:
                return "/"

    def reset(self):
        self.recorded_time = 0
        self.start_time = 0
