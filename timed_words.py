from datetime import timedelta, time, datetime, date
import lrc


class TimedWords:
    def __init__(self, chunk: ()):
        self._content = chunk[0]
        self._end_time = lrc.parse_lrc_time_to_timestamp(chunk[1])
        self._start_time: time | None = None

    def __str__(self):
        if self.time_delta is not None:
            return f'[Δ {self.time_delta.microseconds} ms] {self._content}'
        if self._end_time is None:
            return f'[{self._start_time.strftime("%M:%S.%f")} : - ] {self._content}'
        if self._start_time is None:
            return f'[- : {self._end_time.strftime("%M:%S.%f")}] {self._content}'
        return self._content

    @property
    def content(self) -> str:
        return self._content

    @property
    def start_time(self) -> time:
        return self._start_time

    @start_time.setter
    def start_time(self, value: time):
        self._start_time = value

    @property
    def end_time(self) -> time:
        return self._end_time

    @end_time.setter
    def end_time(self, value: time):
        self._end_time = value

    @property
    def time_delta(self) -> timedelta | None:
        if self._start_time is None or self._end_time is None:
            return None

        duration = datetime.combine(datetime.min, self._end_time) - datetime.combine(datetime.min, self._start_time)
        return duration
