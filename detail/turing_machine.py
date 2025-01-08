# Turing machine simulation class

from detail.controls.tape import Tape
from detail.controls.state_table import StateTable
from detail.style.style_settings import *

import numpy as np
import json
import threading


MAX_ITER_COUNT = 1000
class TuringMachine():
    def __init__(self, Tape : Tape, StateTable : StateTable):
        self.Tape = Tape
        self.StateTable = StateTable
        self.IterCount : int = 0
        self.ResultText = get_styled_text("")
        self.ResultText.width = 300
        self.End = True
        self.CurrentRow = ""
        self.Lock = threading.Lock()


    # Get flet Text control, containing result
    def get_result_text(self):
        return self.ResultText
    

    def __set_result_text__(self, value : str):
        self.ResultText.value = value
        self.StateTable.Page.update()


    def __append_result_text__(self, value : str):
        self.ResultText.value += value
        self.StateTable.Page.update()


    def set_current_row(self, CurrentRow : str):
        self.CurrentRow = CurrentRow
    
    def set_current_row_to_start(self):
        if self.StateTable.StateRows.__len__() > 0:
            self.CurrentRow : str = list(self.StateTable.StateRows.keys())[0]
        else:
            self.CurrentRow : str = "q0"

    # Make one step
    def make_step(self):
        with self.Lock:
            if self.End:
                self.__start_programm__()
                return

            if self.StateTable.StateRows.keys().__len__() == 0:
                self.__append_result_text__(f"Error: There is no state table!\n")
                self.__error_encountered__()
                return
            elif not self.StateTable.StateRows.keys().__contains__(self.CurrentRow):
                self.__append_result_text__(f"Error: There is no state row named \"{self.CurrentRow}\"!\n")
                self.__error_encountered__()
                return
            row : ft.Row = self.StateTable.StateRows[self.CurrentRow]
            value = self.Tape.read_value()
            # find element in alphabet
            index = self.Tape.Alphabet.__len__()
            for i, c in enumerate(self.Tape.Alphabet):
                if value == c:
                    index = i
                    break
            # Index + 1 because each row contain text block in the beggining
            self.StateTable.make_active(self.CurrentRow, index + 1)
            ValueToWrite, TapeAction, RowToJump = self.StateTable.parse_cell(self.StateTable.ActiveCell)
            # Parse all actions
            if not self.StateTable.is_valid_action(ValueToWrite, TapeAction, RowToJump):
                self.__append_result_text__(f"Error: Incorrect input in cell [{self.CurrentRow}, {index + 1}]!\n")
                self.__error_encountered__()
                return
            if ValueToWrite != "":
                self.Tape.write_value(ValueToWrite)
                if value != ValueToWrite:
                    self.__append_result_text__(f"Replace {value} -> {ValueToWrite}.\n")

            if TapeAction == "R":
                self.Tape.move_right()
                self.__append_result_text__(f"Move tape right.\n")
            elif TapeAction == "L":
                self.Tape.move_left()
                self.__append_result_text__(f"Move tape left.\n")

            if RowToJump != "" and RowToJump != " " and self.StateTable.StateRows.__contains__(RowToJump):
                self.CurrentRow = RowToJump
            elif RowToJump == "!":
                # End of programm
                self.__end_of_programm__()
            
            self.IterCount += 1
            if self.IterCount >= MAX_ITER_COUNT:
                self.__append_result_text__(f"Error: Reached iteration count of {self.IterCount}!\n")
                self.__error_encountered__()
                return
    

    def __start_programm__(self):
        self.End = False
        self.__set_result_text__("Begin!\n")
        self.set_current_row_to_start()
    
    def __error_encountered__(self):
        self.End = True
        self.IterCount = 0
        self.__append_result_text__("Error was encountered!")

    def __end_of_programm__(self):
        self.IterCount = 0
        self.End = True
        self.__append_result_text__("End!\n")
    
    # Make steps until program end or MAX_ITER_COUNT reached
    def run_until_end(self):
        if self.End:
            self.make_step()
        while not self.End:
            self.make_step()


    def serialize_to_json(self):
        state_table : dict[str, list[str]] = dict()
        for key, row in self.StateTable.StateRows.items():
            state_table[key] = list[str]()
            for i in row.controls:
                if type(i) is ft.TextField:
                    state_table[key].append(i.value)
        Alphabet = ""
        for ch in self.StateTable.Alphabet:
            Alphabet += ch
        StartingWord = ""
        WordSpotted = False
        for i in self.Tape.cell_row.controls:
            if type(i) is ft.TextField:
                if i.value == "" and WordSpotted:
                    break
                elif i.value == BLANK_SYMBOL and WordSpotted:
                    break
                elif i.value != BLANK_SYMBOL and i.value != "":
                    WordSpotted = True
                    StartingWord += i.value
        data = {
            'Alphabet': Alphabet,
            'StateTable': state_table,
            'StartingWord': StartingWord
        }
        string = json.dumps(data)
        return string
