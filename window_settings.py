
import flet as ft


TITLE = "Turing Machine simulator"
MIN_WIDTH = 850
MIN_HEIGHT = 500
V_ALIGNMENT = ft.MainAxisAlignment.CENTER
H_ALIGNMENT = ft.CrossAxisAlignment.CENTER
THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.INDIGO_300,
        secondary=ft.Colors.INDIGO_100,
    ),
)
THEME_MODE = "light"


def apply_settings(page : ft.Page):
    page.title = TITLE
    page.theme = THEME
    page.theme_mode = THEME_MODE

    page.scroll = ft.ScrollMode.AUTO
    page.expand = True