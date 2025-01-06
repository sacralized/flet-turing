
import flet as ft
import numpy as np

from detail.controls.tape import *
from detail.controls.state_table import *
from detail.turing_machine import *



# Constructor
def setup_table_page(page: ft.Page, Alphabet : str, StartingWord_ : str):

    # Format Alphabet label
    Help_String = "Alphabet: "
    for ch in np.unique(list(Alphabet.upper())):
        Help_String += f"{ch} "
    Help_String += "\n"
    Help_String += f"Blank symbol: {BLANK_SYMBOL} (Copyable)\nAction examples: \"L\", \"R\", \"{BLANK_SYMBOL} N q0\""

    Help_Label = ft.Text(
        value=Help_String,
        weight=ft.FontWeight.W_400,
        size=16,
        text_align=ft.TextAlign.LEFT,
        selectable=True,
    )
    
    Spacer = ft.Container(
        alignment=ft.Alignment(0, 0),
        height=50,
    )

    Table_Column = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            Help_Label,
            Spacer,
        ],
    )

    # Create tape line
    tape = Tape(page, Alphabet, StartingWord_)
    Table_Column.controls.append(tape.get_control())

    Table_Column.controls.append(Spacer)

    # Create State Table
    global state_table
    state_table = StateTable(page, Alphabet)
    Table_Column.controls.append(state_table.get_control())

    # Add make step button
    def make_step_click(e):
        machine.make_step()
        page.update()

    MakeStep_Button = ft.ElevatedButton(
        text="Make step",
        width=350,
        height=40,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
        on_click=make_step_click
    )
    Table_Column.controls.append(MakeStep_Button)

    # Add Spacer
    Table_Column.controls.append(ft.Container(height=20))

    # Add Run Button
    def run_click(e):
        machine.run_until_end()
        page.update()

    Run_Button = ft.ElevatedButton(
        text="Run",
        width=300,
        height=40,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
        on_click=run_click
    )
    Table_Column.controls.append(Run_Button)

    # Add copy script button
    def on_copy_click(e):
        page.set_clipboard(machine.serialize_to_json())
        page.snack_bar = ft.SnackBar(ft.Text("Copied!"))
        page.snack_bar.open = True
        page.update()
        pass

    Copy_Button = ft.ElevatedButton(
        text="Copy script",
        width=250,
        height=40,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
        on_click=on_copy_click
    )
    Table_Column.controls.append(ft.Container(height=20))
    Table_Column.controls.append(Copy_Button)

    # Add Spacer
    Table_Column.controls.append(ft.Container(height=20))

    # Add machine class and result text to the view
    machine = TuringMachine(Tape=tape, StateTable=state_table)
    Table_Column.controls.append(machine.get_result_text())

    Table = ft.Container(
    #Table_Layout = ft.Container(
        content=ft.Row(controls=[Table_Column], scroll=ft.ScrollMode.AUTO, 
                       vertical_alignment=ft.CrossAxisAlignment.START, 
                       #alignment=ft.alignment.top_center
        ),
        alignment=ft.alignment.top_center
    )


    global Table_Layout
    Table_Layout = ft.Column(
        controls=[Table],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        Table_Layout
    )

    tape.scroll_to_head()

    page.update()

    global destruct
    def destruct():
        page.remove(Table_Layout)
        
