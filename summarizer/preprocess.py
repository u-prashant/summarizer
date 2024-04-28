import numpy as np
import pandas as pd
import datetime

from helper import get_lab
from constants import Columns


class Preprocessor:
    def __init__(self, department):
        self.department = department

    def preprocess(self, df):
        df = self.set_datatype(df)
        df = self.sort(df)
        df = self.add_production_date(df)
        df = self.add_department(df)
        df = self.add_building(df)
        df = self.group_by_oci(df)
        df = self.add_time(df)
        df = self.group_by_oci(df)
        df = self.add_stock_info(df)
        df = self.group_by_oci(df)
        return df

    @staticmethod
    def set_datatype(df):
        df[Columns.DateOfChange] = pd.to_datetime(df[Columns.DateOfChange], dayfirst=True).dt.date
        df[Columns.ChangeOfTime] = pd.to_datetime(df[Columns.ChangeOfTime], format='%H:%M:%S').dt.time
        return df

    def add_department(self, df):
        df[Columns.Department] = df[Columns.OrderStatus].apply(self.department.find)
        return df

    @staticmethod
    def sort(df):
        return df.sort_values([Columns.OCINumber, Columns.DateOfChange, Columns.ChangeOfTime])

    def add_production_date(self, df):
        columns_to_shift = [Columns.DateOfChange, Columns.ChangeOfTime]
        shifted_columns = ['DateOfChange X', 'ChangeOfTime X']
        df[shifted_columns] = df[columns_to_shift].shift(-1)
        df[Columns.ProductionDate] = df.apply(
            lambda x: self.get_date_based_on_7am_format(x[shifted_columns[0]], x[shifted_columns[1]]), axis=1)
        df = df.drop(columns=shifted_columns)
        return df

    def add_stock_info(self, df):
        return df.apply(self.check_if_stock_per_oci)

    @staticmethod
    def check_if_stock_per_oci(df):
        df[Columns.Stock] = not (
                df[Columns.Department].str.contains('TS').any() | df[Columns.Department].str.contains('DS').any())
        df[Columns.Stock] = df[Columns.Stock].apply(lambda x: 'Stock' if x is True else np.nan)
        return df

    def add_time(self, df):
        return df.apply(lambda x: self.calculate_time_diff(x))

    @staticmethod
    def calculate_time_diff(df):
        df['StartDate'] = df.apply(lambda x: datetime.datetime(
            x[Columns.DateOfChange].year,
            x[Columns.DateOfChange].month,
            x[Columns.DateOfChange].day,
            x[Columns.ChangeOfTime].hour,
            x[Columns.ChangeOfTime].minute,
            x[Columns.ChangeOfTime].second
        ), axis=1)

        df[Columns.Time] = df['StartDate'].shift(-1) - df['StartDate']
        df[Columns.Time] = df[Columns.Time].apply(lambda x: x.total_seconds())
        df[Columns.Time] = df[Columns.Time].fillna(0.0).astype(int)
        df = df.drop(columns=['StartDate'])
        return df

    @staticmethod
    def get_date_based_on_7am_format(date, time):
        if pd.isnull(date) or pd.isnull(time):
            return pd.NaT

        new_date = date
        if time.hour < 7:
            new_date = new_date - datetime.timedelta(days=1)
        return new_date

    @staticmethod
    def group_by_oci(df):
        return df.groupby([Columns.OCINumber], as_index=False)

    @staticmethod
    def add_building(df):
        df[Columns.LAB] = df[Columns.OrderStatus].apply(get_lab)
        return df
