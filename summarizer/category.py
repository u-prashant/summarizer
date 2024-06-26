from constants import Columns


class CategoryManager:
    def __init__(self, df):
        self.category_to_dept_sequence = self.get_category_to_dept_seq(df)
        self.DEFAULT_CATEGORY = 'Others'

    @staticmethod
    def get_category_to_dept_seq(df):
        category_list = []
        for _, row in df.iterrows():
            category_list.append([row[Columns.Category], row[Columns.DepartmentSequence].split("|")])
        return category_list

    def get_category_for_oci(self, df):
        for item in self.category_to_dept_sequence:
            dept_seq = item[1]
            state_machine_ptr = 0
            for _, row in df.iterrows():
                departments = dept_seq[state_machine_ptr].split(":")
                for dept in departments:
                    if dept == row[Columns.Department]:
                        state_machine_ptr += 1
                        if state_machine_ptr == len(dept_seq):
                            return item[0]
                        break
        return self.DEFAULT_CATEGORY
