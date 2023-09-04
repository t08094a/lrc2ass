import re
from datetime import time, datetime, timedelta
from typing import List
import timed_words
import lrc


class LineIterator(type):
    def __iter__(self):
        return self.classiter()


class Line:
    __metaclass__ = LineIterator

    def __init__(self, line_content: str):
        self._line_content = line_content
        self._is_valid = False
        self._start_time: datetime.time | None = None
        self._end_time: datetime.time | None = None
        self._word_chunks: List[timed_words.TimedWords] = []
        self.__parse_line()

    def __str__(self):
        if len(self._word_chunks) == 0:
            if self.time_delta is not None:
                return f'[Δ {self.time_delta.microseconds} ms] {self._content}'
            if self._end_time is None:
                return f'[{self._start_time.strftime("%M:%S.%f")} : - ] {self._content}'
            if self._start_time is None:
                return f'[- : {self._end_time.strftime("%M:%S.%f")}] {self._content}'
            return self._content

        iterable = iter(map(lambda x: str(x), self._word_chunks))
        return ''.join(iterable)

    def __parse_line(self):
        valid = re.compile(r'^\[(?P<time>[0-9][0-9]:[0-9.]+)\]\s*(?P<content>[\s\S]+)$')
        word_timestamp = re.compile(r'(.+?)(?:<(\d{2}:\d{2}.\d{3})>)')
        word_timestamp_length = len('<00:16.200>')

        line_match = valid.match(self._line_content)
        self._is_valid = line_match is not None

        if not line_match:
            return

        self.start_time = lrc.parse_lrc_time_to_timestamp(line_match['time'])
        text = line_match['content'].strip()

        if word_timestamp.search(text):
            chunks = word_timestamp.findall(text)

            for chunk in chunks:
                self._word_chunks.append(timed_words.TimedWords(chunk))

            last_timestamp = chunks[-1][1]
            index = text.index(last_timestamp)
            last_text_chunk = text[index + word_timestamp_length:]

            self._word_chunks.append(timed_words.TimedWords((last_text_chunk, None)))

            # adjust times
            self._word_chunks[0].start_time = self.start_time
            it = iter(self._word_chunks[1:])

            prev = self._word_chunks[0]
            x: timed_words.TimedWords

            for x in it:
                x.start_time = prev.end_time
                prev = x
        else:
            x = timed_words.TimedWords((text, None))
            x.start_time = self.start_time

            self._word_chunks.append(x)

    @property
    def is_valid(self) -> bool:
        return self._is_valid

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

        if len(self._word_chunks) > 0:
            self._word_chunks[-1].end_time = value

    @property
    def time_delta(self) -> timedelta | None:
        if self._start_time is None or self._end_time is None:
            return None

        duration = datetime.combine(datetime.min, self._end_time) - datetime.combine(datetime.min, self._start_time)
        return duration

    @property
    def items(self):
        return self._word_chunks

    # noinspection SpellCheckingInspection
    @classmethod
    def classiter(cls):
        return iter(cls.word_chunks)
