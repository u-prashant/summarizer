from abc import ABC, abstractmethod

import pandas as pd

from constants import Sheets, Buildings, Columns
import numpy as np


class Summarizer(ABC):
    def __init__(self, department_sequence):
        self.d = department_sequence

        self.buildings = [
            Buildings.A2,
            Buildings.A14,
            Buildings.A15,
        ]

        self.common_columns = [
            Columns.OCINumber,
            Columns.CustomerName,
            Columns.CustomerCode,
            Columns.BUCode,
            Columns.OCIQty,
            Columns.OrderDate,
        ]

        self.final_column_sequence = self.get_final_sequence()

    def get_final_sequence(self):
        final_column_sequence = []
        final_column_sequence.extend(self.common_columns)
        final_column_sequence.extend(self.d.departments_sequence)
        return final_column_sequence

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def get_sheet(self):
        pass

    @abstractmethod
    def summary(self, df):
        pass


class TimeCalculator(Summarizer):
    def __init__(self, department_sequence):
        super(TimeCalculator, self).__init__(department_sequence)
        self.final_column_sequence.append(Columns.Time)

    def name(self):
        return 'Time Computer'

    def get_sheet(self):
        return Sheets.TIME_DATA

    def summary(self, df):
        df = self.compute_time(df)
        df = df[self.final_column_sequence]
        df = df.apply(lambda x: x)
        df = df.reset_index(drop=True)
        df = df.replace(0, np.nan)
        return df

    def compute_time(self, df):
        df = df.apply(self.get_time_per_oci)
        return df

    def get_time_per_oci(self, df):
        row = df.iloc[[0], [df.columns.get_loc(c) for c in self.common_columns]]
        for dept in self.d.departments:
            for building in self.buildings:
                if building in self.d.departments_name[dept]:
                    column = self.d.departments_name[dept][building]
                    row[column] = df[(df[Columns.Department] == dept) & (df[Columns.LAB] == building)][
                        Columns.Time].sum()
        row[Columns.Time] = df[Columns.Time].sum()
        return row


class DeptCounter(Summarizer):
    def __init__(self, department_sequence):
        super(DeptCounter, self).__init__(department_sequence)

    def name(self):
        return 'DeptCounter'

    def get_sheet(self):
        return Sheets.COUNT_DATA

    def summary(self, df):
        df = self.count_dept(df)

        # flatten df
        df = df[self.final_column_sequence]
        df = df.apply(lambda x: x)
        df = df.reset_index(drop=True)
        df = df.replace(0, np.nan)

        df = self.get_single_count(df)
        df = self.get_total_count(df)

        df = df.replace(0, np.nan)

        return df

    def count_dept(self, df):
        df = df.apply(self.get_count_per_oci)
        return df

    def get_count_per_oci(self, df):
        row = df.iloc[[0], [df.columns.get_loc(c) for c in self.common_columns]]
        for dept in self.d.departments:
            for building in self.buildings:
                if building in self.d.departments_name[dept]:
                    column = self.d.departments_name[dept][building]
                    row[column] = len(df[(df[Columns.Department] == dept) & (df[Columns.LAB] == building)])
        return row

    def get_single_count(self, df):
        row = df.iloc[[0], [df.columns.get_loc(c) for c in self.common_columns]]
        for column in self.common_columns:
            row[column] = np.nan
        row[Columns.CustomerName] = 'Single Count'
        for dept in self.d.departments:
            for building in self.buildings:
                if building in self.d.departments_name[dept]:
                    column = self.d.departments_name[dept][building]
                    row[column] = len(df[(df[column] == 1)])
        return pd.concat([df, row])

    def get_total_count(self, df):
        row = df.iloc[[0], [df.columns.get_loc(c) for c in self.common_columns]]
        for column in self.common_columns:
            row[column] = np.nan

        row[Columns.OCINumber] = df.iloc[:-1][Columns.OCINumber].count()
        row[Columns.CustomerName] = 'Total Count'
        row[Columns.CustomerCode] = df.iloc[:-1][Columns.CustomerCode].count()
        row[Columns.BUCode] = df.iloc[:-1][Columns.BUCode].count()
        row[Columns.OCIQty] = df.iloc[:-1][Columns.OCIQty].sum()

        for dept in self.d.departments:
            for building in self.buildings:
                if building in self.d.departments_name[dept]:
                    column = self.d.departments_name[dept][building]
                    row[column] = df.iloc[:-1][column].count()
        return pd.concat([df, row])
