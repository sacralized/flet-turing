
import flet as ft



def setup_menu(page : ft.Page):
    global Return_Button
    Return_Button = ft.FloatingActionButton(
        icon=ft.Icons.ARROW_BACK_ROUNDED, 
        bgcolor=page.theme.color_scheme.secondary,
        text="Return",
    )

    global Source_Button
    Source_Button = ft.FloatingActionButton(
        icon=ft.Icons.OPEN_IN_NEW_ROUNDED,
        bgcolor=page.theme.color_scheme.secondary,
        text="GitHub",
    )

    Ret_Btn_Cont = ft.Container(
        content=ft.Row(
            controls=[Return_Button, Source_Button],
            spacing=10
            ),
        alignment=ft.Alignment(-0.9, -0.9),
    )

    page.add(Ret_Btn_Cont)