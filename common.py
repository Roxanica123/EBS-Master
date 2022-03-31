import json
import random


def get_selection_field_value(field):
    field_name = field["name"]
    field_value = random.choice(field["values"])
    return field_name, field_value


def get_range_field_value(field):
    field_name = field["name"]
    field_value = random.uniform(field["min"], field["max"])
    if field["datatype"] == "int":
        field_value = int(field_value)
    return field_name, field_value


get_field_value = {
    "selection": get_selection_field_value,
    "range": get_range_field_value
}

allowed_comparison = {
    "selection": ["=", "!="],
    "range": ["=", "!=", "<", "<=", ">", ">="]
}


def read_json(file):
    return json.load(open(file))


def write_result(p_publications, output_file):
    with open(output_file, "w") as f:
        print(*p_publications, sep="\n", file=f)


def get_sub_config_file(p_template):
    config = {}
    for field in p_template:
        config[field["name"]] = {
            "frequency": None,
            "comparison_frequency": [{op: None} for op in allowed_comparison[field["type"]]]
        }

    return config
