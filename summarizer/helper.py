from constants import Buildings
import os
from datetime import datetime


def get_lab(value):
    lab = Buildings.A15
    if Buildings.A2 in value:
        lab = Buildings.A2
    elif Buildings.A14 in value:
        lab = Buildings.A14
    return lab


def get_summary_file_location(directory):
    current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    return os.path.join(directory, 'production_summary_{}.xlsx'.format(current_time))
