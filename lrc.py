import pathlib
import re
import datetime
import subprocess
# from typing import List
# import timed_words


def parse_lrc_time_to_timestamp(lrc_time: str) -> datetime.time | None:
    if lrc_time is None or type(lrc_time) is datetime.time:
        return lrc_time

    lrc_time_regex = re.compile(r'\[?(?P<minutes>\d{2}):(?P<seconds>\d{2})\.(?P<microseconds>\d{3})\]?')
    match = lrc_time_regex.match(lrc_time)
    if match:
        return datetime.time(0, int(match['minutes']), int(match['seconds']), int(match['microseconds'])*1000)
    else:
        return None


def get_music_length(mp3_file: pathlib.Path) -> datetime.time:
    # we need to call ffprobe to get the exact ending
    # time for ass file
    cmd = (f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '
           f'-sexagesimal \'{mp3_file.resolve()}\'')
    ending = subprocess.getoutput(cmd)

    return datetime.datetime.strptime(ending, '%H:%M:%S.%f').time()


def convert_timed_words_to_string(words) -> str:  # : List[timed_words.TimedWords]
    result = ''

    for item in words:
        millis = str(item.time_delta.microseconds)
        result += f'{{\k{millis}}} {item.content}'

    return result
