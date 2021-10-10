import pandas as pd
from constants import Columns


class Reader:
    @staticmethod
    def read_csv(file):
        print(file)
        return pd.read_csv(file)


class RawFileReader:
    columns_to_read = [
        Columns.OCINumber,
        Columns.CustomerName,
        Columns.CustomerCode,
        Columns.BUCode,
        Columns.OCIQty,
        Columns.OrderStatus,
        Columns.OrderDate,
        Columns.DateOfChange,
        Columns.ChangeOfTime
    ]

    @staticmethod
    def read(files):
        dfs = []
        for file in files:
            print('Reading {} file...'.format(file))
            df = Reader.read_csv(file)
            if Columns.BUCode not in df.columns:
                df[Columns.BUCode] = ''
            dfs.append(df[RawFileReader.columns_to_read])
        return pd.concat(dfs)
