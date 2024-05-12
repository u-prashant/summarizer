from constants import Columns


class CoatingToCoatingGroup:
    def __init__(self, df):
        self.coating_to_coating_group_map = self.get_map(df)

    @staticmethod
    def get_map(df):
        return dict(zip(df[Columns.CoatingList], df[Columns.CoatingGroupName]))
