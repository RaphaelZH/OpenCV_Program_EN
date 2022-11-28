import pandas as pd
from termcolor import cprint


from .DataFrameTabulation import table_converter


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
        self.df = pd.DataFrame.from_dict(self.dict)
        return self.df

    def tabulation(self):
        return table_converter(self.converter())
