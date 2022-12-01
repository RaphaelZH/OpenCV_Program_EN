import itertools
from tabulate import tabulate


def dataframe_tabulation(df, tablefmt):
    if tablefmt in ["outline", "pretty", "psql"]:
        return tabulate(df, headers="keys", tablefmt=tablefmt).split("\n")
    exception = Exception("This table format is not supported.")
    raise exception


def replacement(string):
    return string.replace(string, " " * (len(string) - 1) + "…")


def display_restrictions(df, tablefmt):
    table_lists = dataframe_tabulation(df, tablefmt=tablefmt)
    if len(table_lists) > 14:
        table_lists = table_lists[:9] + table_lists[-6:]
        replacement_target = table_lists[8].strip("|").split("|")
        for i in range(len(replacement_target)):
            replacement_target[i] = replacement(replacement_target[i])
        table_lists[8] = "|" + "|".join(replacement_target) + "|"
    return table_lists


def list_splitter(arg0, arg1, table_lists, i):
    global border_line, interval_line
    border_line = arg0
    interval_line = arg1
    return table_lists[i].strip(arg0).split(arg1)


def row_selector(table_lists, i):
    if i in [0, len(table_lists) - 1]:
        return list_splitter("+", "+", table_lists, i)
    elif i == 2:
        if table_lists[i].strip("|").split("+")[0] == "":
            return list_splitter("+", "+", table_lists, i)
        else:
            return list_splitter("|", "+", table_lists, i)
    else:
        return list_splitter("|", "|", table_lists, i)


def list_splicer(table_lists, i):
    split_list = row_selector(table_lists, i)
    new_string = border_line
    cumulative_length = len(new_string)
    reassembled_list = []
    for i in range(len(split_list)):
        cumulative_length += len(split_list[i]) + 1
        if cumulative_length <= 62:
            if i == len(split_list) - 1:
                new_string += split_list[i] + border_line
                reassembled_list.append(new_string)
            else:
                new_string += split_list[i] + interval_line
        else:
            reassembled_list.append(new_string)
            new_string = f"… {interval_line + split_list[i] + interval_line}"
            cumulative_length = len(new_string)
    return reassembled_list


def table_rebuilder(df, tablefmt):
    global table_lists
    table_lists = display_restrictions(df, tablefmt=tablefmt)
    return [list_splicer(table_lists, i) for i in range(len(table_lists))]


def table_converter(df, tablefmt):
    table = table_rebuilder(df, tablefmt=tablefmt)
    return [
        table[j][i]
        for i, j in itertools.product(range(len(table[0])), range(len(table)))
    ]
