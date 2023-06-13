from gendiff.make_parser import parser_func
from gendiff.some_code import stylish


def main():
    args = parser_func()
    return stylish(args.first_file, args.second_file, formatter='stylish')


if __name__ == '__main__':
    main()
