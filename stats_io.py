def clear_file(filename):
    with open(filename, 'w') as f:
        pass


def save_csv_from_list(data, filename):
    with open(filename, 'w') as f:
        for line in data:
            f.write(line)


def append_csv_from_list(data, filename):
    with open(filename, 'a') as f:
        for line in data:
            f.write(line)

