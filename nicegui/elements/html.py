import justpy as jp
from .element import Element

class Html(Element):

    def __init__(self, content: str = ''):

        view = jp.Div()
        super().__init__(view, '')
        self.content = content

    @property
    def content(self):

        return self.content.inner_html

    @content.setter
    def content(self, content: any):

        self.set_content(content)

    def set_content(self, content: str):

        self.view.inner_html = content