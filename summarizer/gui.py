import sys

from manager import Manager
from constants import Options, Files, APP, Colors
from tkinter import filedialog, ttk
from tkinter import *
from helper import get_summary_file_location


class GUI:
    def __init__(self, config):
        self.config = config
        self.launch()

    def launch(self):
        window = self.set_window()
        source = SourceGUI(window, self.config.source_dir)
        target = TargetGUI(window, self.config.target_dir)
        raw_checkbox = CheckboxGUI(window, APP.PREPROCESS_CHECKBOX)
        time_checkbox = CheckboxGUI(window, APP.TIME_CHECKBOX)
        count_checkbox = CheckboxGUI(window, APP.COUNT_CHECKBOX)
        generate = GenerateReportGUI(window, self.config, source, target, raw_checkbox, time_checkbox, count_checkbox)
        exit_btn = ExitGUI(window)

        source.label_static.grid(column=1, row=1, padx=15, pady=13, sticky='W')
        source.button_browse.grid(column=4, row=1, padx=15, pady=13, sticky='EW')
        source.label_dynamic.grid(column=1, row=2, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=3, columnspan=4, sticky='ew')

        target.label_static.grid(column=1, row=7, padx=15, pady=13, sticky='W')
        target.button_browse.grid(column=4, row=7, padx=15, pady=13, sticky='EW')
        target.label_dynamic.grid(column=1, row=8, columnspan=4, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=9, columnspan=4, sticky='ew')

        raw_checkbox.checkbox.grid(column=2, row=10, columnspan=2, padx=15, pady=13, sticky='EW')
        time_checkbox.checkbox.grid(column=2, row=11, columnspan=2, padx=15, pady=13, sticky='EW')
        count_checkbox.checkbox.grid(column=2, row=12, columnspan=2, padx=15, pady=13, sticky='EW')

        ttk.Separator(window, orient='horizontal').grid(column=1, row=13, columnspan=4, sticky='ew')

        generate.button.grid(column=2, row=14, columnspan=2, padx=15, pady=13, sticky='EW')
        exit_btn.button.grid(column=2, row=15, columnspan=2, padx=15, pady=13, sticky='EW')

        window.mainloop()

    @staticmethod
    def set_window():
        window = Tk()
        window.title(APP.NAME)
        window.config(background=Colors.AZURE3)
        return window


class SourceGUI:
    def __init__(self, window, source_dir):
        self.window = window
        self.source_dir = source_dir
        self.label_static = self.get_label_static()
        self.label_dynamic = self.get_label_dynamic()
        self.button_browse = self.get_button_browse()

    def get_label_static(self):
        return Label(self.window, text=APP.SOURCE_STATIC_LABEL, width=30, pady=7, bg=Colors.AZURE3)

    def get_label_dynamic(self):
        return Label(self.window, text=APP.NO_FILES_SELECTED, width=70, height=4, fg=Colors.BLUE)

    def get_button_browse(self):
        return Button(self.window, text=APP.BROWSE, width=20, command=self.browse_files, bg=Colors.AZURE4,
                      fg=Colors.WHITE)

    def browse_files(self):
        file_types = [('Excel files', '.xlsx .xls .csv'), ('all files', '.*')]
        files = filedialog.askopenfilenames(initialdir=self.source_dir, title=APP.SELECT_RAW_FILES,
                                            filetypes=file_types)

        text = '\n'.join(list(files))
        if text == "":
            text = APP.NO_FILES_SELECTED
        self.label_dynamic.configure(text=text)


class TargetGUI:
    def __init__(self, window, target_dir):
        self.window = window
        self.target_dir = target_dir
        self.label_static = self.get_label_static()
        self.label_dynamic = self.get_label_dynamic()
        self.button_browse = self.get_button_browse()

    def get_label_static(self):
        return Label(self.window, text=APP.TARGET_STATIC_LABEL, width=30, pady=7, bg=Colors.AZURE3)

    def get_label_dynamic(self):
        text = APP.NO_DIR_SELECTED
        if self.target_dir != '/':
            text = self.target_dir
        return Label(self.window, text=text, width=70, height=4, fg=Colors.BLUE)

    def get_button_browse(self):
        return Button(self.window, text=APP.BROWSE, width=20, command=self.browse_folder, bg=Colors.AZURE4,
                      fg=Colors.WHITE)

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.target_dir, title=APP.SELECT_DESTINATION_FOLDER)
        if folder == '':
            folder = APP.NO_DIR_SELECTED
        self.label_dynamic.configure(text=folder)


class CheckboxGUI:
    def __init__(self, window, text):
        self.window = window
        self.var = IntVar()
        self.checkbox = self.get_checkbox(text)

    def get_checkbox(self, text):
        return Checkbutton(self.window, text=text, variable=self.var, bg=Colors.AZURE3)


class GenerateReportGUI:
    def __init__(self, window, config, source_ui, target_ui, raw_checkbox, time_checkbox, counter_checkbox):
        self.config = config
        self.window = window
        self.source_ui = source_ui
        self.target_ui = target_ui
        self.raw_checkbox = raw_checkbox
        self.time_checkbox = time_checkbox
        self.counter_checkbox = counter_checkbox
        self.button = self.get_button()

    def get_button(self):
        return Button(self.window, text=APP.GENERATE_REPORT, bg=Colors.GRAY25, fg=Colors.WHITE, width=30,
                      command=self.generate_report)

    def generate_report(self):
        raw_files = self.source_ui.label_dynamic.cget('text')
        target_dir = self.target_ui.label_dynamic.cget('text')
        self.config.set_source_dir(raw_files)
        self.config.set_target_dir(target_dir)
        self.config.write()

        files = {
            Files.RAW_FILES: raw_files.split('\n'),
            Files.ORDER_STATUS_TO_DEPT_FILE: './data/order_status_to_department.csv',
            Files.DEPT_SEQUENCE_FILE: './data/department_sequence.csv',
            Files.CATEGORY_FILE: './data/category.csv',
            Files.OUTPUT_FILE: get_summary_file_location(target_dir)
        }
        options = {
            Options.WRITE_PREPROCESS_DATA: self.raw_checkbox.var.get() == 1,
            Options.COMPUTE_TIME_DATA: self.time_checkbox.var.get() == 1,
            Options.COMPUTE_COUNT_DATA: self.counter_checkbox.var.get() == 1
        }
        Manager.manage(files, options)


class ExitGUI:
    def __init__(self, window):
        self.window = window
        self.button = self.get_button()

    def get_button(self):
        return Button(self.window, text=APP.EXIT, width=30, command=sys.exit)
