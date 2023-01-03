import os
from typing import List

import openpyxl

# Import the values from the environment.py file
from environment import (
    TTT,
    HYSTERESIS,
    A3_OFFSET)


class Result:
    total = 0

    def __init__(self, success: List[int], failure: List[int]):
        self.success = success
        self.failure = failure
        self.total = sum(success) + sum(failure)

    def get_total_success(self):
        return sum(self.success)

    def get_success(self):
        return self.success

    def get_failure(self):
        return self.failure

    def get_total_failure(self):
        return sum(self.failure)

    def save_to_file(self, file_name: str):
        # Check if the file exists
        file_name = os.path.join(os.path.dirname(__file__), file_name)
        if not os.path.exists(file_name):
            print("File does not exist, creating new file")
            # Create a new workbook and add a header row
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.cell(row=1, column=1).value = "Success [lte2lte]"
            sheet.cell(row=1, column=2).value = "Success [lte2nr]"
            sheet.cell(row=1, column=3).value = "Success [nr2lte]"
            sheet.cell(row=1, column=4).value = "Success [nr2nr]"
            sheet.cell(row=1, column=5).value = "Failure [lte2lte]"
            sheet.cell(row=1, column=6).value = "Failure [lte2nr]"
            sheet.cell(row=1, column=7).value = "Failure [nr2lte]"
            sheet.cell(row=1, column=8).value = "Failure [nr2nr]"
            sheet.cell(row=1, column=9).value = "Failed HOs"
            sheet.cell(row=1, column=10).value = "Successful HOs"
            sheet.cell(row=1, column=11).value = "Total HOs"
            sheet.cell(row=1, column=12).value = "Time To Trigger"
            sheet.cell(row=1, column=13).value = "Hysteresis"
            sheet.cell(row=1, column=14).value = "A3 Offset"
        else:
            # Load the existing workbook
            workbook = openpyxl.load_workbook(file_name)
            sheet = workbook.active

        # Get the next available row on the sheet
        next_row = sheet.max_row + 1

        # Write the elements of self.success to separate cells
        for i, element in enumerate(self.success):
            sheet.cell(row=next_row, column=i + 1).value = element

        # Write the elements of self.failure to separate cells
        for i, element in enumerate(self.failure):
            sheet.cell(row=next_row, column=i + 5).value = element

        # Write the total success and total failure to the sheet
        sheet.cell(row=next_row, column=9).value = str(self.get_total_failure())
        sheet.cell(row=next_row, column=10).value = str(self.get_total_success())
        sheet.cell(row=next_row, column=11).value = str(self.get_total_ho())

        # Write the TTT and HYSTERESIS to the sheet
        sheet.cell(row=next_row, column=12).value = TTT
        sheet.cell(row=next_row, column=13).value = HYSTERESIS
        sheet.cell(row=next_row, column=14).value = A3_OFFSET

        # Save the workbook
        workbook.save(file_name)

    def get_total_ho(self):
        return self.total
