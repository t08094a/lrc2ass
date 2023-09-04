import datetime
import pathlib
import re
from typing import List
import line


class Parser:
    def __init__(self, lcr_path: pathlib.Path, music_length: datetime.time):
        self._input_file = lcr_path
        self._music_length = music_length

        # noinspection RegExpRedundantEscape
        self._valid = re.compile(r'^\[[0-9][0-9]:[0-9.]+\]')
        # noinspection RegExpUnnecessaryNonCapturingGroup
        self._word_timestamp = re.compile(r'(.+?)(?:<(\d{2}:\d{2}.\d{3})>)')
        self._word_timestamp_length = len('<00:16.200>')

        self._lines = []

    def read(self):
        with open(self._input_file, 'r') as lcr:
            for line_content in lcr:
                line_obj = line.Line(line_content)

                if line_obj.is_valid:
                    self._lines.append(line_obj)

        item: line.Line
        for i, item in enumerate(self._lines):
            if i == len(self._lines) - 1:
                next_line = None
            else:
                next_line = self._lines[i + 1]

            if next_line is not None:
                item.end_time = next_line.start_time
            else:
                item.end_time = self._music_length

        return self

    @property
    def items(self) -> List[line.Line]:
        return self._lines
    