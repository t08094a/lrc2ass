import argparse
import pathlib
import converter
import lrc
import parser
import os


def main():
    arg_parser = argparse.ArgumentParser(prog="lrc2ass", usage='%(prog) lrc mp3',
                                         description='parses the input lyrics file LRC and converts it to an ASS file')
    arg_parser.add_argument("lrc", help="The LRC lyrics file to convert.", type=pathlib.Path)
    arg_parser.add_argument("mp3", help="The mp3 file to determine the music length.", type=pathlib.Path)
    args = arg_parser.parse_args()

    lrc_file = pathlib.Path(args.lrc)
    mp3_file = pathlib.Path(args.mp3)
    output_file = pathlib.Path(os.path.splitext(mp3_file.resolve())[0] + ".ass")

    music_length = lrc.get_music_length(mp3_file)

    lines = parser.Parser(lrc_file, music_length).read().items
    converter.Converter(lines).convert_to_ass_format(output_file)


if __name__ == '__main__':
    main()
