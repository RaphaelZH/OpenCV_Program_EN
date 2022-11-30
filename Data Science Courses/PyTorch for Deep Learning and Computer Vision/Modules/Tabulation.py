import re
from tabulate import tabulate
from termcolor import cprint

from .DataFrameGeneration import DataFrame_Generator
from .RandomColors import color_list_generator


class Form_Generator:
    def __init__(self):
        self.adjusted_width = 59

    def sign_adjuster(self, string):
        return string.replace("<", "⟨").replace(">", "⟩")

    def heading_printer(self, heading):
        self.heading = heading
        global font_colors_list
        try:
            font_colors_list
        except NameError:
            font_colors_list = color_list_generator()
        if font_colors_list == []:
            font_colors_list = color_list_generator()
        self.previous_color = font_colors_list.pop(0)
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

    def string_trimmer(self, string, expandtabs, width):
        printable_lines = []
        string = self.tabulator_replacement(string, expandtabs)
        printable_line = string
        indent = expandtabs
        if len(string) > width:
            printable_line = string
            while len(printable_line) > width:
                while printable_line.rfind(" ") > width:
                    printable_line = printable_line[: printable_line.rfind(" ")]
                printable_line = printable_line[: printable_line.rfind(" ")]
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


"""
    def dataframe_printer(self, df):
        cprint(df, self.previous_color, attrs=["bold"])
"""
