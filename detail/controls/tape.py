# Two-directional tape control

import flet as ft
import numpy as np
from detail.style.style_settings import *

INITIAL_LENGTH = 40
SCROLL_DURATION = 300
HEAD_CELL_COLOR = ft.Colors.INDIGO_200


class Tape:
    def __init__(self, page : ft.Page, Alphabet : str, StartingWord : str):
        
        self.Alphabet = np.unique(list(Alphabet.upper()))
        #self.Alphabet = Alphabet
        self.Page = page
        StartingWord = list(StartingWord.upper())

        def on_scroll_left_click(e):
            self.cell_row.scroll_to(delta=-TAPE_CELL_WIDTH, duration=SCROLL_DURATION)

        def on_scroll_right_click(e):
            self.cell_row.scroll_to(delta=TAPE_CELL_WIDTH, duration=SCROLL_DURATION)

        def on_page_resize(e):
             self.cell_row.width=page.width-page.width/5
             page.update()
            
        # Row for cells
        self.cell_row = ft.Row(
            spacing=CELL_SPACING,
            scroll=ft.ScrollMode.AUTO,
            #offset=ft.transform.Offset(0.1, 0.1),
            width=page.width-page.width/5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.on_resize=on_page_resize
        self.scroll_left_button = ft.IconButton(
            icon=ft.Icons.ARROW_LEFT_ROUNDED,
            icon_size=50,
            tooltip="Scroll left",
            on_click=on_scroll_left_click,
        )
        self.scroll_right_button = ft.IconButton(
            icon=ft.Icons.ARROW_RIGHT_ROUNDED,
            icon_size=50,
            tooltip="Scroll right",
            on_click=on_scroll_right_click,
        )
        self.row = ft.Row(
            controls=[self.scroll_left_button, self.cell_row, self.scroll_right_button],
            spacing=CELL_SPACING,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.head_index : int = int(INITIAL_LENGTH / 2)
        for i in range(INITIAL_LENGTH):
            self.__append_new_cell__()
        self.place_word(StartingWord)

    # Get flet control
    def get_control(self):
        return self.row
    
    def __append_new_cell__(self):
        Alphabet = ""
        for ch in self.Alphabet:
            Alphabet += ch
        new_cell = get_styled_textfield(BLANK_SYMBOL, regex_string=rf"^[{Alphabet},{BLANK_SYMBOL}]*$")
        new_cell.key=str(self.cell_row.controls.__len__())
        new_cell.max_length = 1
        new_cell.capitalization = ft.TextCapitalization.CHARACTERS
        new_cell.width = TAPE_CELL_WIDTH
        self.cell_row.controls.append(new_cell)
    
    # Clear Tape and place word in the middle of the tape
    def place_word(self, Word : str):
        for cell in self.cell_row.controls:
            cell.value = ""
        old_index = self.head_index
        self.head_index = int(self.cell_row.controls.__len__() / 2)
        self.__change_selection__(old_index)
        for i, ch in enumerate(Word):
            # Add some empty space after word
            while self.cell_row.controls.__len__() < self.head_index + int(INITIAL_LENGTH / 2):
                self.__append_new_cell__()
            self.cell_row.controls[self.head_index + i].value = ch
    

    def __change_selection__(self, old_index : int):
        self.cell_row.controls[old_index].fill_color = ""
        self.cell_row.controls[self.head_index].fill_color = HEAD_CELL_COLOR


    def scroll_to_head(self):
        cell_count_on_screen = int(self.cell_row.width / TAPE_CELL_WIDTH)
        scroll_offset = int(cell_count_on_screen/2)
        index_scroll_to = self.head_index - scroll_offset
        index_scroll_to = max(0, index_scroll_to)
        cell_scroll_to = self.cell_row.controls[index_scroll_to]
        self.cell_row.scroll_to(key=cell_scroll_to.key, duration=SCROLL_DURATION)
        
    # Not thread-safe
    def move_left(self):
        old_index = self.head_index
        if self.head_index == 0:
            self.cell_row.controls.insert(0, get_styled_textfield(BLANK_SYMBOL))
        else:
            self.head_index -= 1
        self.__change_selection__(old_index)
        
    # Not thread-safe
    def move_right(self):
        old_index = self.head_index
        self.head_index += 1
        while self.cell_row.controls.__len__() <= self.head_index:
            self.cell_row.controls.append(get_styled_textfield(BLANK_SYMBOL))
        self.__change_selection__(old_index)
        

    def read_value(self) -> str:
        return self.cell_row.controls[self.head_index].value
    
    
    def write_value(self, value : str):
        self.cell_row.controls[self.head_index].value = value