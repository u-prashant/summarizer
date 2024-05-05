import chardet
import pandas as pd
import numpy as np
from constants import Columns


class Reader:
    @staticmethod
    def read_csv(file):
        with open(file, 'rb') as f:
            enc = chardet.detect(f.read())
        print(file)
        return pd.read_csv(file, encoding=enc['encoding'])

    @staticmethod
    def read_excel(file):
        return pd.read_excel(file)


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
                df[Columns.BUCode] = np.nan
            dfs.append(df[RawFileReader.columns_to_read])
        return pd.concat(dfs)


class InfoFileReader:
    columns_to_read = [
        Columns.OCINumber,
        Columns.RELensName,
        Columns.LELensName,
        Columns.REIndex,
        Columns.LEIndex,
        Columns.REFocality,
        Columns.LEFocality,
        Columns.Coating
    ]

    @staticmethod
    def read(files):
        dfs = []
        for file in files:
            print('Reading {} file...'.format(file))
            df = Reader.read_excel(file)
            if 'Export OCI Number' in df.columns:
                df[Columns.OCINumber] = df['Export OCI Number']
            elif 'OCI number' in df.columns:
                df[Columns.OCINumber] = df['OCI number']
            dfs.append(df[InfoFileReader.columns_to_read])
        return pd.concat(dfs)
