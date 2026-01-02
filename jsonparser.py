import json

data_processed = [
    {
        "name": "Лунтик",
        "age": 1,
        "friends": [{"name": "Вупсень", "age": 3}, {"name": "Пупсень", "age": 23}],
    }
]

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data_processed, file, ensure_ascii=False)


def remove_friends_older_ten(elems_to_filter):
    new_elems = []
    for elem in elems_to_filter:
        new_elem = elem.copy()
        new_elem["friends"] = [
            friend for friend in elem["friends"] if friend["age"] <= 10
        ]
        new_elems.append(new_elem)
    return new_elems


with open("data.json", "r", encoding="utf-8") as input_file:
    data = json.load(input_file)
    filtered_data = remove_friends_older_ten(data)

    with open("data_filtered.json", "w", encoding="utf-8") as output_file:
        json.dump(filtered_data, output_file, ensure_ascii=False)
