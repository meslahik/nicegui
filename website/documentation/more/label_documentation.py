from nicegui import ui

from ..tools import text_demo


def main_demo() -> None:
    ui.label('some label')


def more() -> None:
    @text_demo('Change Appearance Depending on the Content', '''
        You can overwrite the `_handle_text_change` method to update other attributes of a label depending on its content. 
        This technique also works for bindings as shown in the example below.
    ''')
    def status():
        class status_label(ui.label):
            def _handle_text_change(self, text: str) -> None:
                super()._handle_text_change(text)
                if text == 'ok':
                    self.classes(replace='text-positive')
                else:
                    self.classes(replace='text-negative')

        model = {'status': 'error'}
        status_label().bind_text_from(model, 'status')
        ui.switch(on_change=lambda e: model.update(status='ok' if e.value else 'error'))
