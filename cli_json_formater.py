import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action")
parser.add_argument("-fn", "--filename")
parser.add_argument("-fi", "--field")
parser.add_argument("-v", "--value")
parser.add_argument("-o", "--output")


def open_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        file_to_return = json.load(file)

    return file_to_return


def save_json(output, json_to_save):
    with open(output, "w", encoding="utf-8") as file:
        json.dump(json_to_save, file, ensure_ascii=False)


def add_field_to_json(filename, field, value):
    with open(filename, "r", encoding="utf-8") as file:
        json_to_modify = json.load(file)
        for elem in json_to_modify:
            elem[field] = value

    return json_to_modify


def main():
    args = parser.parse_args()
    if args.action == "add":
        json_to_save = add_field_to_json(args.filename, args.field, args.value)
        save_json(args.output, json_to_save)


if __name__ == "__main__":
    main()
