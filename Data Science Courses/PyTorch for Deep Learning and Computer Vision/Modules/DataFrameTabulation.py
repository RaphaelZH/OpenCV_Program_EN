from tabulate import tabulate


def df_tabulation(df, tablefmt):
    if tablefmt in ["outline", "pretty", "psql"]:
        table_lists = tabulate(df, headers="keys",tablefmt=tablefmt).split("\n")
        return table_lists
    exception = Exception("This table format is not supported.")
    raise exception


def replacement(string):
    return string.replace(string, " " * (len(string) - 1) + "…")


def display_restrictions(df, tablefmt):
    table_lists = df_tabulation(df, tablefmt=tablefmt)
    if len(table_lists) > 14:
        table_lists = table_lists[:9] + table_lists[-6:]
        replacement_target = table_lists[8].strip("|").split("|")
        for i in range(len(replacement_target)):
            replacement_target[i] = replacement(replacement_target[i])
        table_lists[8] = "|" + "|".join(replacement_target) + "|"
    return table_lists


def list_splitter(table_lists, i):
    global border_line, interval_line
    if i in [0, len(table_lists) - 1]:
        border_line = "+"
        interval_line = "+"
        return table_lists[i].strip("+").split("+")
    elif i == 2:
        if table_lists[i].strip("|").split("+") == "":
            border_line = "+"
            interval_line = "+"
            return table_lists[i].strip("+").split("+")
        else:
            border_line = "|"
            interval_line = "+"
            return table_lists[i].strip("|").split("+")
    else:
        border_line = "|"
        interval_line = "|"
        return table_lists[i].strip("|").split("|")


def list_splicer(table_lists, i):
    split_list = list_splitter(table_lists, i)
    new_string = border_line
    cumulative_length = len(new_string)
    reassembled_list = []
    reassembling = 0
    for i in range(len(split_list)):
        cumulative_length += (len(split_list[i]) + 1)
        if cumulative_length <= 63:
            if i == len(split_list) - 1:
                new_string += (split_list[i] + border_line)
            else:
                new_string += (split_list[i] + interval_line)
        else:
            reassembled_list.append(new_string)
            new_string = "… " + interval_line
            cumulative_length = len(new_string)
            reassembling += 1
    return reassembled_list


def table_rebuilder(df, tablefmt):
    global table_lists
    new_table = []
    table_lists = display_restrictions(df, tablefmt=tablefmt)
    for i in range(len(table_lists)):
        new_table.append(list_splicer(table_lists, i))
    return new_table


def table_converter(df, tablefmt="psql"):
    table = table_rebuilder(df, tablefmt=tablefmt)
    new_table = []
    for i in range(len(table[0])):
        for j in range(len(table)):
            new_table.append(table[j][i])
    return new_table
