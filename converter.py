from typing import List
import line
import pathlib
import lrc


class Converter:
    def __init__(self, lines: List[line.Line]):
        self._lines = lines

    def convert_to_ass_format(self, output_file: pathlib.Path):

        with open(output_file.resolve(), 'w') as af:
            af.write('[Script Info]\n')
            af.write('\n')
            af.write('[Aegisub Project]\n')
            af.write(f'Active Line: {len(self._lines)}\n')
            af.write('\n')

            af.write("""
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
    """)
            af.write('\n')

            af.write('[Events]\n')
            af.write('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')

            for current_line in self._lines:
                af.write('Dialogue: 0,')
                af.write(current_line.start_time.strftime('%H:%M:%S.%f'))
                af.write(',')
                af.write(current_line.end_time.strftime('%H:%M:%S.%f'))
                af.write(',Default,,0,0,0,,')
                af.write(lrc.convert_timed_words_to_string(current_line.items))
                af.write('\n')

            # write the last line.
            # af.write("Dialogue: 0,")
            # af.write(self._lines[len(self._lines) - 1][0])
            # af.write(",")
            # af.write(ending)
            # af.write(",Default,,0,0,0,,")
            # af.write(self._lines[len(self._lines) - 1][1])
            # af.write("\n")
