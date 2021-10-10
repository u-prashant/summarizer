from constants import Files, Errors, Sheets, Options
from timer import Timer
from reader import Reader, RawFileReader
from preprocess import Preprocessor
from department import OrderStatusToDepartment, DepartmentSequence
from summarizer import TimeCalculator, DeptCounter
from writer import Writer


class Manager:
    @staticmethod
    def manage(files: dict, options: dict):
        total_timer = Timer('Total Time: ')
        total_timer.start()

        try:
            Manager.validate_files(files)
        except Exception as e:
            print(e)
            raise e

        # read order status to department
        order_status_to_department_df = Reader.read_csv(files[Files.ORDER_STATUS_TO_DEPT_FILE])
        o = OrderStatusToDepartment(order_status_to_department_df)

        # read department sequence
        department_sequence_df = Reader.read_csv(files[Files.DEPT_SEQUENCE_FILE])
        d = DepartmentSequence(department_sequence_df)

        # read raw file
        raw_file_df = RawFileReader.read(files[Files.RAW_FILES])

        w = Writer(files[Files.OUTPUT_FILE])

        # preprocessing raw file
        p = Preprocessor(o)
        preprocessed_df = p.preprocess(raw_file_df)
        if options[Options.WRITE_PREPROCESS_DATA]:
            w.write_group(Sheets.RAW_DATA, preprocessed_df)

        # running summarizers
        summarizers = []
        if options[Options.COMPUTE_TIME_DATA]:
            summarizers.append(TimeCalculator(d))
        if options[Options.COMPUTE_COUNT_DATA]:
            summarizers.append(DeptCounter(d))

        for summarizer in summarizers:
            print('Running {} ...'.format(summarizer.name()))
            t = Timer(summarizer.name())
            t.start()
            df = summarizer.summary(preprocessed_df)
            w.write(summarizer.get_sheet(), df)
            t.stop()

        w.save()
        total_timer.stop()

    @staticmethod
    def validate_files(files: dict):
        if Files.RAW_FILES not in files:
            raise Errors(Errors.RawFileNotProvided)

        if Files.ORDER_STATUS_TO_DEPT_FILE not in files:
            raise Errors(Errors.OrderStatusToDeptFileNotProvided)

        if Files.DEPT_SEQUENCE_FILE not in files:
            raise Errors(Errors.DeptSequenceFileNotProvided)

        if Files.OUTPUT_FILE not in files:
            raise Errors(Errors.OutputFileNotProvided)


if __name__ == '__main__':
    files_path = {
        Files.ORDER_STATUS_TO_DEPT_FILE: './data/order_status_to_department.csv',
        Files.DEPT_SEQUENCE_FILE: './data/department_sequence.csv',
        Files.RAW_FILES: ['./tmp/Ex_2109_copy.csv'],
        Files.OUTPUT_FILE: './tmp/abc.xlsx'
    }
    summarizer_options = {
        Options.WRITE_PREPROCESS_DATA: True,
        Options.COMPUTE_COUNT_DATA: True,
        Options.COMPUTE_TIME_DATA: True
    }
    Manager.manage(files_path, summarizer_options)
