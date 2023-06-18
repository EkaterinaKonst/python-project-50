### Hexlet tests and linter status:
[![Actions Status](https://github.com/EkaterinaKonst/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/EkaterinaKonst/python-project-50/actions)

[![CI check](https://github.com/EkaterinaKonst/python-project-50/actions/workflows/main.yml/badge.svg)](https://github.com/EkaterinaKonst/python-project-50/actions/workflows/maim.yml)

<a href="https://codeclimate.com/github/EkaterinaKonst/python-project-50/maintainability"><img src="https://api.codeclimate.com/v1/badges/fde8d5dda619fc18d29c/maintainability" /></a>

<a href="https://codeclimate.com/github/EkaterinaKonst/python-project-50/test_coverage"><img src="https://api.codeclimate.com/v1/badges/fde8d5dda619fc18d29c/test_coverage" /></a>

# **Gendiff** - compare two json and/or yaml files

## **About**
You can get a comparison of two json/yaml files - different formats can be compared too!


The output type depends on the selected format:
- **stylish** - is selected by default
- **plain**
- **json**

## Help
```bash
gendiff -h

usage: gendiff [-h] [-f [{stylish,plain,json}]] [first_file] [second_file]

Compares two configuration files and shows a difference.

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f [{stylish,plain,json}], --format [{stylish,plain,json}]
                        set format of output
```

# Installation

### You can install by using following commands:
    git clone
    cd python-project-50
    make install
    make build
    make package-install


[![asciicast](https://asciinema.org/a/C246BEASVsR7ivLi32ibVFc0J)](https://asciinema.org/a/C246BEASVsR7ivLi32ibVFc0J)

