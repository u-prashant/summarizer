import pandas as pd

from constants import Columns, Buildings


class OrderStatusToDepartment:
    def __init__(self, df):
        self.order_status_to_dept_map = self.get_map(df)

    @staticmethod
    def get_map(df):
        return dict(zip(df[Columns.OrderStatus], df[Columns.Department]))

    def find(self, order_status):
        if '-KOL' in order_status:
            return ''

        if order_status in self.order_status_to_dept_map:
            return self.order_status_to_dept_map[order_status]

        print('Department Not Found for OrderStatus {}'.format(order_status))
        return ''


class DepartmentSequence:
    def __init__(self, df):
        self.departments_sequence = DepartmentSequence.get_sequence(df)
        self.departments_name = DepartmentSequence.get_departments_name(df)
        self.departments = list(df[Columns.Department])

    @staticmethod
    def get_sequence(df):
        sequence = []
        for index, row in df.iterrows():
            for building in [Buildings.A2, Buildings.A14, Buildings.A15]:
                if not pd.isna(row[building]):
                    row[building] = row[building].strip()
                    if row[building] != '':
                        sequence.append(row[building])
        return sequence

    @staticmethod
    def get_departments_name(df):
        name_map = {}
        for index, row in df.iterrows():
            name_map[row[Columns.Department]] = {}
            for building in [Buildings.A2, Buildings.A14, Buildings.A15]:
                val = row[building]
                if not pd.isna(val):
                    name_map[row[Columns.Department]][building] = val.strip()
        return name_map
