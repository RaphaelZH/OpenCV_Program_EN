import random
import re
from tabulate import tabulate
from termcolor import cprint


def list_head_checker(list_1, list_2):
    for i in range(len(list_2)):
        if list_1[-1] == list_2[0]:
            head, list_2 = list_2[0], list_2[1:]
            list_2.append(head)
        else:
            break
    return list_2


def list_connector(list_1, list_2):
    if list_1 != []:
        list_2 = list_head_checker(list_1, list_2)
    list_1 += list_2
    return list_1


def color_list_generator(n=100):
    termcolors = [
        'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    ]
    global font_colors_list
    font_colors_list = []
    for i in range(((n - 1) // 8 + 1)):
        if n <= 8:
            random_list = random.sample(termcolors, k=n)
            list_connector(font_colors_list, random_list)
        else:
            if i < ((n - 1) // 8):
                random_list = random.sample(termcolors, k=8)
                list_connector(font_colors_list, random_list)
            else:
                k = n % 8
                if k == 0:
                    random_list = random.sample(termcolors, k=8)
                    list_connector(font_colors_list, random_list)
                elif k == 1:
                    random_list = random.sample(termcolors, k=2)
                    font_colors_list = list_connector(font_colors_list,
                                                      random_list)[:-1]
                else:
                    random_list = random.sample(termcolors, k=k)
                    list_connector(font_colors_list, random_list)


def font_color_printer(string, *args, **kwargs):
    global adjusted_width, font_colors_list, previous_color
    try:
        font_colors_list
    except NameError:
        color_list_generator()
    if font_colors_list == []:
        color_list_generator()
    previous_color = font_colors_list.pop(0)
    adjusted_width = 59
    return cprint(string, previous_color, attrs=['underline'], end='\n\n')


def statement_generator(statements):
    global adjusted_width, previous_color
    table = [["Statement"]]
    for statement in statements:
        if len(statement) > adjusted_width:
            printable_statement = ""
            printable_line = statement
            while len(statement) > adjusted_width:
                while printable_line.rfind(' ') > adjusted_width:
                    printable_line = printable_line[:printable_line.rfind(' ')]
                else:
                    printable_line = printable_line[:printable_line.rfind(' ')]
                printable_statement += printable_line + "\n"
                statement = statement[len(printable_line) + 1:]
                printable_line = statement
            else:
                printable_statement += printable_line
                table.append([printable_statement])
        else:
            table.append([statement])
    table_list = tabulate(table,
                          headers='firstrow',
                          tablefmt='pretty',
                          colalign=('left', )).split('\n')
    for line in table_list:
        cprint('\t'.expandtabs(4) + line, previous_color, attrs=['bold'])


def definition_generator(definitions):
    global adjusted_width, previous_color
    table = [["Definition"]]
    for definition in definitions:
        printable_definition = ""
        for line in definition.strip().split("\n"):
            if len(line) > adjusted_width:
                printable_lines = ""
                printable_line = line
                while len(line) > adjusted_width:
                    while printable_line.rfind(' ') > adjusted_width:
                        printable_line = printable_line[:printable_line.rfind(' ')]
                    else:
                        printable_line = printable_line[:printable_line.rfind(' ')]
                    printable_lines += printable_line + "\n\t".expandtabs(8)
                    line = line[len(printable_line) + 1:]
                    printable_line = line
                else:
                    printable_lines += printable_line
                    printable_definition += printable_lines + "\n"
            else:
                printable_definition += line + "\n"
            table.append([printable_definition])
        else:
            table.append([definition])
    table_list = tabulate(table,
                          headers='firstrow',
                          tablefmt='pretty',
                          colalign=('left', )).split('\n')
    for line in table_list:
        cprint('\t'.expandtabs(4) + line, previous_color, attrs=['bold'])
        
        
    """
    
        if len(value) > remainder:
                for nested_string in string_list:
                    if len(nested_string) > remainder:
                        printable_string = ""
                        printable_line = nested_string
                        while len(nested_string) > remainder:
                            while printable_line.rfind(' ') > remainder:
                                printable_line = printable_line[:printable_line
                                                                .rfind(' ')]
                            else:
                                printable_line = printable_line[:printable_line
                                                                .rfind(' ')]
                            printable_string += printable_line + "\n"
                            nested_string = nested_string[len(printable_line) +
                                                          1:]
                            printable_line = nested_string
                        else:
                            printable_string += printable_line
                            printable_value += printable_string + "\n"
                    else:
                        printable_value += nested_string + "\n"
                table.append([variable, printable_value.strip("\n")])
            else:
                printable_value = ""
                printable_line = value
                while len(value) > remainder:
                    while printable_line.rfind(' ') > remainder:
                        printable_line = printable_line[:printable_line.
                                                        rfind(' ')]
                    else:
                        printable_line = printable_line[:printable_line.
                                                        rfind(' ')]
                    printable_value += printable_line + "\n"
                    value = value[len(printable_line) + 1:]
                    printable_line = value
                else:
                    printable_value += printable_line
                    table.append([variable, printable_value])
        else:
            table.append([variable, value])
    table_list = tabulate(table,
                          headers='firstrow',
                          tablefmt='pretty',
                          colalign=("left", "left")).split('\n')
    for line in table_list:
        cprint('\t'.expandtabs(4) + line, previous_color, attrs=['bold'])
    
    
    
    """
        

def variable_generator(variables, values):
    global adjusted_width, previous_color
    table = [["Variable", "Value"]]
    max_length = len(max(variables, key=len))
    if len("Variable") >= max_length:
        length_variable = len("Variable")
    else:
        length_variable = max_length
    remainder = adjusted_width - length_variable - 3
    for variable, value in zip(variables, values):
        if len(value) > remainder:
            if re.search(r'\n', str(value)):
                start = 0
                printable_value = ""
                string_list = []
                for match in re.finditer(r'\n', str(value)):
                    nested_string = str(value)[start:match.span()[0]]
                    string_list.append(nested_string)
                    start = match.span()[1]
                string_list.append(str(value)[start:])
                for nested_string in string_list:
                    if len(nested_string) > remainder:
                        printable_string = ""
                        printable_line = nested_string
                        while len(nested_string) > remainder:
                            while printable_line.rfind(' ') > remainder:
                                printable_line = printable_line[:printable_line
                                                                .rfind(' ')]
                            else:
                                printable_line = printable_line[:printable_line
                                                                .rfind(' ')]
                            printable_string += printable_line + "\n"
                            nested_string = nested_string[len(printable_line) +
                                                          1:]
                            printable_line = nested_string
                        else:
                            printable_string += printable_line
                            printable_value += printable_string + "\n"
                    else:
                        printable_value += nested_string + "\n"
                table.append([variable, printable_value.strip("\n")])
            else:
                printable_value = ""
                printable_line = value
                while len(value) > remainder:
                    while printable_line.rfind(' ') > remainder:
                        printable_line = printable_line[:printable_line.
                                                        rfind(' ')]
                    else:
                        printable_line = printable_line[:printable_line.
                                                        rfind(' ')]
                    printable_value += printable_line + "\n"
                    value = value[len(printable_line) + 1:]
                    printable_line = value
                else:
                    printable_value += printable_line
                    table.append([variable, printable_value])
        else:
            table.append([variable, value])
    table_list = tabulate(table,
                          headers='firstrow',
                          tablefmt='pretty',
                          colalign=("left", "left")).split('\n')
    for line in table_list:
        cprint('\t'.expandtabs(4) + line, previous_color, attrs=['bold'])


def expression_generator(expressions, results):
    global adjusted_width, previous_color
    table = [["Expression", "Result"]]
    max_length = len(max(expressions, key=len))
    if len("Expression") >= max_length:
        length_expression = len("Expression")
    else:
        length_expression = max_length
    remainder = adjusted_width - length_expression - 3
    for expression, result in zip(expressions, results):
        if len(result) > remainder:
            if re.search(r'\n', str(result)):
                start = 0
                printable_result = ""
                string_list = []
                for match in re.finditer(r'\n', str(result)):
                    nested_string = str(result)[start:match.span()[0]]
                    string_list.append(nested_string)
                    start = match.span()[1]
                string_list.append(str(result)[start:])
                for nested_string in string_list:
                    if len(nested_string) > remainder:
                        printable_string = ""
                        printable_line = nested_string
                        while len(nested_string) > remainder:
                            while printable_line.rfind(' ') > remainder:
                                printable_line = printable_line[:printable_line
                                                                .rfind(' ')]
                            else:
                                printable_line = printable_line[:printable_line
                                                                .rfind(' ')]
                            printable_string += printable_line + "\n"
                            nested_string = nested_string[len(printable_line) +
                                                          1:]
                            printable_line = nested_string
                        else:
                            printable_string += printable_line
                            printable_result += printable_string + "\n"
                    else:
                        printable_result += nested_string + "\n"
                table.append([expression, printable_result.strip("\n")])
            else:
                printable_result = ""
                printable_line = result
                while len(result) > remainder:
                    while printable_line.rfind(' ') > remainder:
                        printable_line = printable_line[:printable_line.
                                                        rfind(' ')]
                    else:
                        printable_line = printable_line[:printable_line.
                                                        rfind(' ')]
                    printable_result += printable_line + "\n"
                    result = result[len(printable_line) + 1:]
                    printable_line = result
                else:
                    printable_result += printable_line
                    table.append([expression, printable_result])
        else:
            table.append([expression, result])
    table_list = tabulate(table,
                          headers='firstrow',
                          tablefmt='pretty',
                          colalign=("left", "left")).split('\n')
    for line in table_list:
        cprint('\t'.expandtabs(4) + line, previous_color, attrs=['bold'])
