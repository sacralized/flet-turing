
import flet as ft

from window_settings import apply_settings
import menu_panel as menu
import main_window as mw
import machine_window as machine_window
import json

from detail.style.style_settings import *

def main(page: ft.Page):
    apply_settings(page)

    menu.setup_menu(page)
    mw.setup_main_page(page)

    def open_main_menu():
        mw.show()
        if machine_window.Table_Layout:
            machine_window.destruct()

    def on_create_table(e):
        Alphabet = mw.Alphabet_TField.value
        StartingWord = mw.StartingWord_TField.value
        mw.hide()
        machine_window.setup_table_page(page, Alphabet, StartingWord)

    def on_decimal_increment_example(e):
        Alphabet = "0123456789"
        StartingWord = "1024"
        mw.hide()
        machine_window.setup_table_page(page, Alphabet, StartingWord)
        StateTable = {
            "q0" : ["0 R q0", "1 R q0", "2 R q0", "3 R q0", "4 R q0", "5 R q0", "6 R q0", "7 R q0", "8 R q0", "9 R q0", f"{BLANK_SYMBOL} L q1"],
            "q1" : ["1 N q2", "2 N q2", "3 N q2", "4 N q2", "5 N q2", "6 N q2", "7 N q2", "8 N q2", "9 N q2", "0 L q1", "1 N q2"],
            "q2" : ["0 L q2", "1 L q2", "2 L q2", "3 L q2", "4 L q2", "5 L q2", "6 L q2", "7 L q2", "8 L q2", "9 L q2", f"{BLANK_SYMBOL} R !"],
        }
        machine_window.state_table.__rebuild_from_dict__(StateTable)
        page.update()

    def on_binary_increment_example(e):
        Alphabet = "01"
        StartingWord = "100011"
        mw.hide()
        machine_window.setup_table_page(page, Alphabet, StartingWord)
        StateTable = {
            "q0" : ["0 R q0", "1 R q0", f"{BLANK_SYMBOL} L q1"],
            "q1" : ["1 N q2", "0 L q1", "1 N q2"],
            "q2" : ["0 L q2", "1 L q2", f"{BLANK_SYMBOL} R !"],
        }
        machine_window.state_table.__rebuild_from_dict__(StateTable)
        page.update()

    # Add loading from json
    def on_load_json_submit(e):
        page.close(mw.Script_BottomSheet)
        try:
            data = json.loads(mw.Script_TField.value)
            Alphabet : str = data["Alphabet"]
            StateTable : dict[str, list[str]] = data["StateTable"]
            StartingWord : str = data["StartingWord"]
            mw.hide()
            machine_window.setup_table_page(page, Alphabet, StartingWord)
            machine_window.state_table.__rebuild_from_dict__(StateTable)
            page.update()
        except:
            mw.ScriptError_Text.value = mw.INCORRECT_SCRIPT_ERROR
            mw.ScriptError_Text.visible = True
            page.update()

    mw.CreateTable_Button.on_click = on_create_table
    mw.DecimalIncrementExample_Button.on_click = on_decimal_increment_example
    mw.BinaryIncrementExample_Button.on_click = on_binary_increment_example
    mw.Script_TField.on_submit = on_load_json_submit
    
    def on_return_click(e):
        if mw.visible():
            # Clear textfields
            mw.Alphabet_TField.value = ""
            mw.StartingWord_TField.value = ""
            mw.ErrorHint_Text.visible = False
            mw.CreateTable_Button.disabled = True
            mw.Script_TField.value = ""
            page.update()
        else:
            open_main_menu()

    menu.Return_Button.on_click = on_return_click


ft.app(target=main, view=ft.WEB_BROWSER,)