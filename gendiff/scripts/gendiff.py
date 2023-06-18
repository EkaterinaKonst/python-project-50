from gendiff.make_parser import parser_func
from gendiff.some_code import generate_diff


def main():
    args = parser_func()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
