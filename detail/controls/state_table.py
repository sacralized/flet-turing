# State table control

import flet as ft
import numpy as np

from detail.style.style_settings import *

ACTIVE_CELL_COLOR = ft.Colors.INDIGO_200
ERROR_CELL_COLOR = ft.Colors.RED_200

class StateTable:
    def __init__(self, page : ft.Page, Alphabet : str, RowCount : int = 2):

        self.Page = page
        self.Alphabet = np.unique(list(Alphabet.upper()))      
        # Dictionary containing all state rows (name/row)      
        self.StateRows = dict()

        self.Table = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=CELL_SPACING,
            expand=True,
        )
        def add_staterow_click(e):
            self.create_new_state_row()
            self.Page.update()

        self.Add_StateRow_Button = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE_ROUNDED,
            icon_size=30,
            tooltip="Add new state row",
            on_click=add_staterow_click,
            width=STATE_TABLE_CELL_WIDTH,
            alignment=ft.alignment.top_center
        )
        self.Container = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=CELL_SPACING,
            expand=True,
            controls=[self.Table, self.Add_StateRow_Button],
        )
        # Create title row
        title_row = ft.Row(
            controls=[ft.Container(width=STATE_TABLE_CELL_WIDTH)],
            spacing=CELL_SPACING,
        )
        for i in Alphabet:
            title_row.controls.append(get_styled_text(i))
        blank_title = get_styled_text(BLANK_SYMBOL)
        blank_title.selectable = True
        title_row.controls.append(blank_title)
        title_row.controls.append(ft.Container(width=STATE_TABLE_CELL_WIDTH))
        self.Table.controls.append(title_row)
        
        for i in range(RowCount):
            self.create_new_state_row()
        # Active cell row and column
        self.ActiveCell = None
        

    # Get flet control
    def get_control(self):
        return self.Container
    

    def make_active(self, ActiveRow : str, ActiveColumn : int):
        # Make previous cell inactive
        if self.ActiveCell:
            self.ActiveCell.fill_color = ""
        active_row : ft.Row = self.StateRows.get(ActiveRow)
        self.ActiveCell : ft.TextField = active_row.controls[ActiveColumn]
        self.ActiveCell.fill_color = ACTIVE_CELL_COLOR

    
    # Return ValueToWrite, TapeAction, RowToJump
    def parse_cell(self, Cell : ft.TextField) -> tuple[str, str, str]:
        res = Cell.value.split(" ")
        if res.__len__() == 3:
            return res[0], res[1], res[2]
        elif res.__len__() == 1:
            return "", res[0], ""
        elif res.__len__() == 0:
            return "", "N", ""
        else:
            return "", "", ""
        

    def is_valid_action(self, ValueToWrite, TapeAction, RowToJump) -> bool:
        result = True
        if ValueToWrite != "" and ValueToWrite != BLANK_SYMBOL and not self.Alphabet.__contains__(ValueToWrite):
            result = False
        elif TapeAction != "R" and TapeAction != "N" and TapeAction != "L":
            result = False
        elif RowToJump != "" and RowToJump != "!" and (not RowToJump.startswith("q") or RowToJump.__len__() != 2):
            result = False
        return result


    def __generate_new_cell__(self) -> ft.TextField:
        def on_value_change(e):
            ValueToWrite, TapeAction, RowToJump = self.parse_cell(new_textfield)
            if self.is_valid_action(ValueToWrite, TapeAction, RowToJump):
                new_textfield.fill_color = ""
            else:
                new_textfield.fill_color = ERROR_CELL_COLOR
            self.Page.update()
            
        new_textfield = get_styled_textfield(regex_string=rf"^[0-9,a-z,а-я,{BLANK_SYMBOL}, ,!]*$")
        new_textfield.max_length = 6
        new_textfield.on_change = on_value_change
        return new_textfield


    # Rebuild Table from string dictionary
    def __rebuild_from_dict__(self, dict : dict[str, list[str]]):
        for key, row in self.StateRows.items():
            self.Table.controls.remove(row)
        self.StateRows.clear()
        for key, list in dict.items():
            self.create_new_state_row(key)
            for i, val in enumerate(list):
                row : ft.Row = self.StateRows.get(key)
                row.controls[i+1].value = val


    def create_new_state_row(self, RowName : str = ""):
        if RowName == "":
            RowIndex = 0
            RowName = "q" + str(RowIndex)
            while self.StateRows.__contains__(RowName):
                RowIndex += 1
                RowName = "q" + str(RowIndex)
        
        new_row = ft.Row(
            controls=[get_styled_text(RowName)],
            spacing=CELL_SPACING
        )
        # Alphabet columns
        for i in self.Alphabet:
            new_row.controls.append(self.__generate_new_cell__())
        # Blank symbol column
        new_row.controls.append(self.__generate_new_cell__())
        #Delete row button
        def delete_click(e):
            self.Table.controls.remove(new_row)
            self.StateRows.pop(RowName, None)
            self.Page.update()

        delete_row_btn = ft.IconButton(
            icon=ft.Icons.DELETE_FOREVER_ROUNDED,
            icon_size=30,
            tooltip="Delete state row",
            on_click=delete_click,
            width=STATE_TABLE_CELL_WIDTH,
        )
        new_row.controls.append(delete_row_btn)
        self.StateRows[RowName] = new_row
        self.Table.controls.append(new_row)
