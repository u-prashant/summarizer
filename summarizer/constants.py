class APP:
    NAME = 'TAT'
    SOURCE_STATIC_LABEL = 'Raw Files'
    TARGET_STATIC_LABEL = 'Destination Folder'
    SELECT_RAW_FILES = 'Select Raw Files'
    SELECT_DESTINATION_FOLDER = 'Select Destination Folder'
    NO_FILES_SELECTED = 'No Files Selected'
    NO_DIR_SELECTED = 'No Directory Selected'
    BROWSE = 'Browse'
    EXIT = 'Exit'
    GENERATE_REPORT = 'Generate Report'
    PREPROCESS_CHECKBOX = 'Raw Data'
    TIME_CHECKBOX = 'Time Data'
    COUNT_CHECKBOX = 'Count Data'


class Files:
    ORDER_STATUS_TO_DEPT_FILE = 'order_status_to_dept_file_path'
    DEPT_SEQUENCE_FILE = 'dept_sequence_file_path'
    CATEGORY_FILE = 'category_file_path'
    RAW_FILES = 'raw_files_path'
    OUTPUT_FILE = 'output_file_path'
    CONFIG_FILE = 'config_file_path'


class Options:
    WRITE_PREPROCESS_DATA = 0
    COMPUTE_COUNT_DATA = 1
    COMPUTE_TIME_DATA = 2


class Sheets:
    RAW_DATA = 'raw_data'
    TIME_DATA = 'time_data'
    COUNT_DATA = 'count_data'


class Buildings:
    A2 = 'A2'
    A14 = 'A14'
    A15 = 'A15'


class Columns:
    OCINumber = 'OCINumber'
    DateOfChange = 'DateOfChange'
    ChangeOfTime = 'ChangeOfTime'
    ProductionDate = 'ProductionDate'
    LAB = 'LAB'
    OrderStatus = 'OrderStatus'
    Department = 'Department'
    BUCode = 'BUCode'
    CustomerName = 'CustomerName'
    CustomerCode = 'CustomerCode'
    OCIQty = 'OCIQty'
    OrderDate = 'OrderDate'
    Time = 'Time'
    Stock = 'Stock'
    Category = 'Category'
    DepartmentSequence = 'Department Sequence'


class Errors(Exception):
    RawFileNotProvided = 'Raw File Path not provided'
    OrderStatusToDeptFileNotProvided = 'Order Status to Dept File Path not provided'
    DeptSequenceFileNotProvided = 'Dept Sequence File not provided'
    CategoryFileNotProvided = 'Category File not provided'
    OutputFileNotProvided = 'Output File Path not provided'
    ConfigurationFileNotFound = 'Config File not provided'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Colors:
    AZURE3 = 'azure3'
    AZURE4 = 'azure4'
    BLUE = 'blue'
    WHITE = 'white'
    GRAY25 = 'gray25'
