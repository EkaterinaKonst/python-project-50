from gendiff.make_parser import parser
from gendiff.some_code import *


def main():
    args = parser()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()