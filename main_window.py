
import flet as ft
from window_settings import *


EMPTY_ALPHABET_ERROR = "Alphabet must contain at least one character."
INCORRECT_STARTING_WORD_ERROR = "Alphabet doesn't contain character: "
INCORRECT_SCRIPT_ERROR = "Pasted script couldn't be parsed."


def setup_main_page(page: ft.Page):

    def on_alphabet_changed(e : ft.ControlEvent):
        value : str = e.control.value
        isEmpty : bool = value.__len__() == 0

        ErrorHint_Text.visible = isEmpty
        CreateTable_Button.disabled = isEmpty
        if isEmpty:
            ErrorHint_Text.value = EMPTY_ALPHABET_ERROR
        
        page.update()


    def on_starting_word_changed(e : ft.ControlEvent):
        StartingWord : str = e.control.value.upper()
        Alphabet : str = Alphabet_TField.value.upper()
        # Check if starting word contains only alphabet characters
        isIncorrect : bool = False
        IncorrectCh = ""
        for ch in StartingWord:
            if not Alphabet.__contains__(ch):
                isIncorrect = True
                IncorrectCh = ch
                break

        ErrorHint_Text.visible = isIncorrect
        CreateTable_Button.disabled = isIncorrect
        if isIncorrect:
            ErrorHint_Text.value = INCORRECT_STARTING_WORD_ERROR + IncorrectCh
        
        page.update()


    def on_alphabet_submit(e : ft.ControlEvent):
        isEmpty : bool = e.control.value.__len__() == 0

        if not isEmpty:
            StartingWord_TField.focus()
        else:
            Alphabet_TField.focus()
        page.update()


    def on_starting_word_submit(e : ft.ControlEvent):
        CreateTable_Button.on_click(e)
        page.update()

    Title_Text = ft.Text(
        value="Turing Machine simulator",
        weight=ft.FontWeight.W_500,
        size=20,
        text_align=ft.TextAlign.CENTER,
    )
    
    Welcome_Text = ft.Text(
        value="Enter alphabet and starting word for Turing Machine.",
        weight=ft.FontWeight.W_400,
        size=16,
        text_align=ft.TextAlign.CENTER,
    )
    

    global Alphabet_TField
    Alphabet_TField = ft.TextField(
        label="Alphabet",
        border_color=page.theme.color_scheme.secondary,
        hint_text="Enter characters",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9,a-z,A-Z,а-я,А-Я]*$", replacement_string=""),
        width=400,
        height=40,
        on_change=on_alphabet_changed,
        on_submit=on_alphabet_submit
    )


    global StartingWord_TField
    StartingWord_TField = ft.TextField(
        label="Starting word",
        border_color=page.theme.color_scheme.secondary,
        hint_text="Enter string or leave empty",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9,a-z,A-Z,а-я,А-Я]*$", replacement_string=""),
        width=400,
        height=40,
        on_change=on_starting_word_changed,
        on_submit=on_starting_word_submit,
    )

    # Contains error text
    global ErrorHint_Text
    ErrorHint_Text = ft.Text(
        size=14,
        color=ft.Colors.RED_ACCENT,
        theme_style=ft.TextThemeStyle.TITLE_SMALL,
        value=EMPTY_ALPHABET_ERROR,
        visible=False
    )
    

    global CreateTable_Button
    CreateTable_Button = ft.ElevatedButton(
        text="Create machine",
        width=400,
        height=40,
        disabled=True,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
    )

    global Script_TField
    Script_TField = ft.TextField(
        label="Script",
        border_color=page.theme.color_scheme.secondary,
        hint_text="Paste script and press enter",
        width=400,
        height=40,
    )

    def on_load_click(e):
        page.open(Script_BottomSheet)
        Script_TField.focus()


    LoadScript_Button = ft.ElevatedButton(
        text="Load from script",
        width=400,
        height=40,
        disabled=False,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
        on_click=on_load_click
    )

    global ScriptError_Text
    ScriptError_Text = ft.Text(
        size=14,
        color=ft.Colors.RED_ACCENT,
        theme_style=ft.TextThemeStyle.TITLE_SMALL,
        value=INCORRECT_SCRIPT_ERROR,
        visible=False
    )

    Example_Text = ft.Text(
        value="Examples:",
        weight=ft.FontWeight.W_400,
        size=16,
        text_align=ft.TextAlign.CENTER,
    )

    # Increment decimal ns button
    global DecimalIncrementExample_Button
    DecimalIncrementExample_Button = ft.ElevatedButton(
        text="Increment (decimal ns)",
        width=400,
        height=40,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
    )

    # Increment Binary ns button
    global BinaryIncrementExample_Button
    BinaryIncrementExample_Button = ft.ElevatedButton(
        text="Increment (binary ns)",
        width=400,
        height=40,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=16)
        ),
    )


    Title_Cont = ft.Container(
        content = Title_Text,
        alignment=ft.Alignment(0, 0),
    )

    Create_Label_Cont = ft.Container(
        content = Welcome_Text,
        alignment=ft.Alignment(0, 0),
    )

    CreateTable_Col = ft.Column(
        controls=[Alphabet_TField, StartingWord_TField, ErrorHint_Text, CreateTable_Button],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    Spacer = ft.Container(
        alignment=ft.Alignment(0, 0),
        height=100,
    )

    SmallSpacer = ft.Container(
        alignment=ft.Alignment(0, 0),
        height=50,
    )

    CreateTable_Cont = ft.Container(
        content = CreateTable_Col,
        alignment=ft.Alignment(0, 0),
    )

    ExampleText_Cont = ft.Container(
        content = Example_Text,
        alignment=ft.Alignment(0, 0),
    )

    DecimalIncrement_Button_Cont = ft.Container(
        content = DecimalIncrementExample_Button,
        alignment=ft.Alignment(0, 0),
    )

    BinaryIncrement_Button_Cont = ft.Container(
        content = BinaryIncrementExample_Button,
        alignment=ft.Alignment(0, 0),
    )

    Load_Script_Cont = ft.Container(
        content = ft.Text(
            value="Paste saved script and press enter.",
            weight=ft.FontWeight.W_400,
            size=16,
            text_align=ft.TextAlign.LEFT,
        ),
        alignment=ft.Alignment(0, 0),
    )

    Script_TField_Cont = ft.Container(
        content = Script_TField,
        alignment=ft.Alignment(0, 0),
    )

    global Script_BottomSheet
    Script_BottomSheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[Load_Script_Cont, Script_TField_Cont],
            ),
        ),
    )

    Script_Button_Cont = ft.Container(
        content = LoadScript_Button,
        alignment=ft.Alignment(0, 0),
    )

    Script_Error_Cont = ft.Container(
        content = ScriptError_Text,
        alignment=ft.Alignment(0, 0),
    )


    Content_Column = ft.Column(
        controls=[
        Title_Cont,
        Spacer,
        Create_Label_Cont,
        CreateTable_Cont,
        SmallSpacer,
        Script_Button_Cont,
        Script_Error_Cont,
        SmallSpacer,
        ExampleText_Cont,
        DecimalIncrement_Button_Cont,
        BinaryIncrement_Button_Cont
        ],
    )

    Main_Layout = ft.Container(
        content=Content_Column,
        expand=True,
        )

    page.add(
        Main_Layout
    )
    
    page.update()

    global hide
    def hide():
        Main_Layout.visible = False

    global show
    def show():
        Main_Layout.visible = True
        page.update()

    global visible
    def visible():
        return Main_Layout.visible
        