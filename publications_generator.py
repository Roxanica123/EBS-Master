import argparse
import json
import sys

from common import get_field_value, get_sub_config_file, read_json, write_result


def generate_publications(p_template, number):
    publications_list = []
    for i in range(number):
        publication = []
        for field in p_template:
            field_value = get_field_value[field["type"]](field)
            publication.append(field_value)
        publications_list.append(tuple(publication))
    return publications_list


def write_sub_config_file(p_template, file):
    if file is not None:
        with open(file, "w") as f:
            json.dump(get_sub_config_file(p_template), f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publications generation")
    parser.add_argument('--template', '-t', default="./template.json", help="Template file")
    parser.add_argument('--number', '-n', default=100, type=int, help="The number of publications to generate")
    parser.add_argument('--output', '-o', default="gen/publications.txt", help="Output file for generated publications")
    parser.add_argument('--sub_config_gen', '-sc_gen', default=None,
                        help="File name for generated subscriptions config file")
    args = parser.parse_args(sys.argv[1:])
    template = read_json(args.template)
    publications = generate_publications(template, args.number)
    write_result(publications, args.output)
    write_sub_config_file(template, args.sub_config_gen)
