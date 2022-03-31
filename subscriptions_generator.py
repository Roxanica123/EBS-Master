import argparse
import random
import sys

from common import read_json, get_sub_config_file, write_result, get_field_value


def get_wanted_field_frequencies(p_config, number):
    wanted_fields_freq = {}
    for field in p_config:
        if p_config[field]["frequency"] is not None:
            wanted_fields_freq[field] = p_config[field]["frequency"] * number // 100
    return wanted_fields_freq


def clean_available_fields(available_fields, fields_freq):
    for field in available_fields:
        if field in fields_freq and fields_freq[field] == 0:
            available_fields.remove(field)
            fields_freq.pop(field)


def get_field_from_template(field_name, p_template):
    for field in p_template:
        if field["name"] == field_name:
            return field


def generate_subscription(p_template, available_fields, fields_freq, remaining_sub):
    subscription = []
    options = available_fields[:]
    min = 1
    max = None
    if fields_freq != {}:
        field_name = random.choice(list(fields_freq.keys()))
        field = get_field_from_template(field_name, p_template)
        subscription.append(get_field_value[field["type"]](field))
        options = [f for f in available_fields if f != field_name]
        min = 0
        max = len(available_fields) - len(list(fields_freq.keys()))
    fields_to_add = random.sample(options, k=round(random.uniform(min, len(options) if max is None else max)))
    for field_name in fields_to_add:
        field = get_field_from_template(field_name, p_template)
        subscription.append(get_field_value[field["type"]](field))
    for field in subscription:
        if field[0] in fields_freq:
            fields_freq[field[0]] -= 1
    return subscription


def get_op_freq(p_config, gen_subscriptions):
    fields_number = {}
    for sub in gen_subscriptions:
        for pair in sub:
            if pair[0] not in fields_number:
                fields_number[pair[0]] = 0
            fields_number[pair[0]] += 1

    for field in p_config:
        with_freq = []
        others = []
        for op in p_config[field]["comparison_frequency"]:
            key = list(op.keys())[0]
            if op[key] is not None:
                with_freq.append([key, round(op[key] * fields_number[field] / 100)])
            else:
                others.append(key)
        for i, sub in enumerate(gen_subscriptions):
            for j, pair in enumerate(sub):
                if pair[0] == field:
                    if len(with_freq) != 0 and with_freq[0][1] != 0:
                        op = with_freq[0][0]
                        gen_subscriptions[i][j] = (pair[0], op, pair[1])
                        with_freq[0][1] -= 1
                        if with_freq[0][1] == 0:
                            del with_freq[0]
                    else:
                        gen_subscriptions[i][j] = (pair[0], random.choice(others), pair[1])
    print(fields_number)


def add_operators(gen_subscriptions, p_template, p_config):
    op_freq = get_op_freq(p_config, gen_subscriptions)


def generate_subscriptions(p_template, p_config, number):
    available_fields = [field for field in p_config]
    fields_freq = get_wanted_field_frequencies(p_config, number)
    gen_subscriptions = []
    for i in range(number):
        clean_available_fields(available_fields, fields_freq)
        gen_subscriptions.append(generate_subscription(p_template, available_fields, fields_freq, number - i - 1))
    add_operators(gen_subscriptions, p_template, p_config)
    random.shuffle(gen_subscriptions)
    return gen_subscriptions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publications generation")
    parser.add_argument('--template', '-t', default="./template.json", help="Template file")
    parser.add_argument('--number', '-n', default=100, type=int, help="The number of subscriptions to generate")
    parser.add_argument('--config', '-c', default="./config.json", help="Path to config file")
    parser.add_argument('--output', '-o', default="gen/subscriptions.txt",
                        help="Output file for generated publications")
    args = parser.parse_args(sys.argv[1:])
    template = read_json(args.template)
    config = get_sub_config_file(template) if args.config is None else read_json(args.config)
    subscriptions = generate_subscriptions(template, config, args.number)
    write_result(subscriptions, args.output)
