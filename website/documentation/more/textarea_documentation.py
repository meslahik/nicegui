from nicegui import ui

from ..tools import text_demo


def main_demo() -> None:
    ui.textarea(label='Text', placeholder='start typing',
                on_change=lambda e: result.set_text('you typed: ' + e.value))
    result = ui.label()


def more() -> None:

    @text_demo('Clearable', '''
        The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.    
    ''')
    def clearable():
        i = ui.textarea(value='some text').props('clearable')
        ui.label().bind_text_from(i, 'value')
