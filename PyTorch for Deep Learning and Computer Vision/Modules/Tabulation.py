import itertools
import pandas as pd
import re
from tabulate import tabulate
from termcolor import cprint

from .RandomColors import color_list_generator


class Form_Generator:
    def __init__(self):
        self.adjusted_width = 59

    def sign_adjuster(self, string):
        regex_pattern = "\<[\s\S]*?\>"
        while re.search(regex_pattern, string):
            positions = re.search(regex_pattern, string).span()
            string = f"{string[:positions[0]]}⟨{string[positions[0] + 1:]}"
            string = f"{string[:positions[1] - 1]}⟩{string[positions[1]:]}"
        return string

    def color_selector(self):
        global font_colors_list
        try:
            font_colors_list
        except NameError:
            font_colors_list = color_list_generator()
        if font_colors_list == []:
            font_colors_list = color_list_generator()
        return font_colors_list

    def heading_printer(self, heading):
        global font_colors_list
        try:
            font_colors_list
        except NameError:
            font_colors_list = self.color_selector()
        if font_colors_list == []:
            font_colors_list = self.color_selector()
        self.previous_color = font_colors_list.pop(0)
        self.heading = heading
        cprint(
            self.sign_adjuster(self.heading),
            self.previous_color,
            attrs=["underline"],
            end="\n\n",
        )

    def tabulator_replacement(self, string, expandtabs):
        if len(re.findall(r"\t", string)) > 0:
            string = re.sub(r"\t", " " * expandtabs, string)
        return string

    def lookup_checker(self, string, target, type="r"):
        if string.find(target) == -1:
            return None
        else:
            return string.find(target) if type == "l" else string.rfind(target)

    def string_trimmer(self, string, expandtabs, width):
        printable_lines = []
        string = self.tabulator_replacement(string, expandtabs)
        printable_line = string
        indent = expandtabs
        exception = Exception(
            "The length of the consecutive string is longer than expected."
        )
        if True in (len(i) > (width - indent) for i in string.split(" ")):
            raise exception
        if len(string) > width:
            printable_line = string
            while len(printable_line) > width:
                while (
                    len(printable_line[: self.lookup_checker(printable_line, " ")])
                    > width
                ):
                    printable_line = printable_line[
                        : self.lookup_checker(printable_line, " ")
                    ]
                printable_line = printable_line[
                    : self.lookup_checker(printable_line, " ")
                ]
                printable_lines.append(printable_line)
                string = string[len(printable_line) + 1 :]
                printable_line = string
                width -= indent
                indent = 0
        printable_lines.append(printable_line)
        return printable_lines

    def definition_generator(self, definitions, expandtabs=4):
        table = [["Definition"]]
        for definition in definitions:
            printable_lines = [
                "\n\t".expandtabs(expandtabs).join(
                    self.string_trimmer(line, expandtabs, self.adjusted_width)
                )
                for line in definition.strip().split("\n")
            ]
            table.append(["\n".join(printable_lines)])
        table_list = tabulate(
            table, headers="firstrow", tablefmt="pretty", colalign=("left",)
        ).split("\n")
        for line in table_list:
            cprint(
                "\t".expandtabs(4) + self.sign_adjuster(line),
                self.previous_color,
                attrs=["bold"],
            )

    def statement_generator(self, statements, expandtabs=4):
        table = [["Statement"]]
        for statement in statements:
            printable_lines = [
                "\n\t".expandtabs(expandtabs).join(
                    self.string_trimmer(line, expandtabs, self.adjusted_width)
                )
                for line in statement.strip().split("\n")
            ]
            table.append(["\n".join(printable_lines)])
        table_list = tabulate(
            table, headers="firstrow", tablefmt="pretty", colalign=("left",)
        ).split("\n")
        for line in table_list:
            cprint(
                "\t".expandtabs(4) + self.sign_adjuster(line),
                self.previous_color,
                attrs=["bold"],
            )

    def variable_generator(self, variables, values, expandtabs=8):
        table = [["Variable", "Value"]]
        max_length = len(max(variables, key=len))
        length_variable = max(len("Variable"), max_length)
        remainder = self.adjusted_width - length_variable - 3
        for variable, value in zip(variables, values):
            printable_lines = [
                "\n\t".expandtabs(expandtabs).join(
                    self.string_trimmer(line, expandtabs, remainder)
                )
                for line in value.strip().split("\n")
            ]
            table.append([variable, "\n".join(printable_lines)])
        table_list = tabulate(
            table, headers="firstrow", tablefmt="pretty", colalign=("left", "left")
        ).split("\n")
        for line in table_list:
            cprint(
                "\t".expandtabs(4) + self.sign_adjuster(line),
                self.previous_color,
                attrs=["bold"],
            )

    def expression_generator(self, expressions, results, expandtabs=8):
        table = [["Expression", "Result"]]
        max_length = len(max(expressions, key=len))
        length_expression = max(len("Expression"), max_length)
        remainder = self.adjusted_width - length_expression - 3
        for expression, result in zip(expressions, results):
            printable_lines = [
                "\n\t".expandtabs(expandtabs).join(
                    self.string_trimmer(line, expandtabs, remainder)
                )
                for line in result.strip().split("\n")
            ]
            table.append([expression, "\n".join(printable_lines)])
        table_list = tabulate(
            table, headers="firstrow", tablefmt="pretty", colalign=("left", "left")
        ).split("\n")
        for line in table_list:
            cprint(
                "\t".expandtabs(4) + self.sign_adjuster(line),
                self.previous_color,
                attrs=["bold"],
            )

    def dataframe_generator(self, df_table):
        for line in df_table:
            cprint(
                "\t".expandtabs(4) + self.sign_adjuster(line),
                self.previous_color,
                attrs=["bold"],
            )


class DataFrame_Generator:
    def __init__(self, *args):
        self.col_name = []
        self.dict = {}
        for i in args:
            self.col_name.append(i)
            self.dict.update({str(i): []})

    def updater(self, *args):
        for i, j in zip(self.col_name, args):
            self.dict[i].append(j)

    def converter(self):
        return pd.DataFrame.from_dict(self.dict)

    def tabulation(self, tablefmt="psql"):
        return table_converter(self.converter(), tablefmt)


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
        if cumulative_length <= 63:
            if i == len(split_list) - 1:
                new_string += split_list[i] + border_line
                reassembled_list.append(new_string)
            else:
                new_string += split_list[i] + interval_line
        else:
            reassembled_list.append(new_string)
            if i == len(split_list) - 1:
                new_string = f"… {interval_line + split_list[i] + border_line}"
                reassembled_list.append(new_string)
            else:
                new_string = f"… {interval_line + split_list[i] + interval_line}"
                cumulative_length = len(new_string)
    return reassembled_list


def table_rebuilder(df, tablefmt):
    table_lists = display_restrictions(df, tablefmt=tablefmt)
    return [list_splicer(table_lists, i) for i in range(len(table_lists))]


def table_converter(df, tablefmt):
    table = table_rebuilder(df, tablefmt=tablefmt)
    return [
        table[j][i]
        for i, j in itertools.product(range(len(table[0])), range(len(table)))
    ]
