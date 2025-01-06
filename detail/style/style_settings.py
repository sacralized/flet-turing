
import flet as ft

TAPE_CELL_WIDTH = 60
STATE_TABLE_CELL_WIDTH = 80
CELL_SPACING = 0
FONT_SIZE = 15

BLANK_SYMBOL = "☐"

def get_styled_text(value : str):
    return ft.Text(
            value=value,
            size=FONT_SIZE,
            width=STATE_TABLE_CELL_WIDTH,
            text_align=ft.TextAlign.CENTER,
        )

def get_styled_textfield(hint : str = "N", regex_string = r"^[0-9,a-z,а-я]*$", case_senstivie : bool = False):
    return ft.TextField(
            value="",
            hint_text=hint,
            input_filter=ft.InputFilter(allow=True, regex_string=regex_string, replacement_string="", case_sensitive=case_senstivie),
            width=STATE_TABLE_CELL_WIDTH,
            border=ft.InputBorder.NONE,
            filled=True,
            text_align=ft.TextAlign.CENTER,
        )