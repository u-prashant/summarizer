import pandas as pd
import numpy as np


class Writer:
    def __init__(self, file_path):
        self.writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    def write_group(self, sheet_name, df):
        df = df.apply(lambda x: x)
        df = df.reset_index(drop=True)
        df = df.replace(0, np.nan)
        df.to_excel(self.writer, sheet_name=sheet_name, index=False)

    def write(self, sheet_name, df):
        df.to_excel(self.writer, sheet_name=sheet_name, index=False)

    def save(self):
        self.writer.close()
