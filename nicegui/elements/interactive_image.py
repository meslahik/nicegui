from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, List, Optional, Union, cast

from PIL.Image import Image as PIL_Image

from ..events import GenericEventArguments, MouseEventArguments, handle_event
from .image import pil_to_base64
from .mixins.content_element import ContentElement
from .mixins.source_element import SourceElement


class InteractiveImage(SourceElement, ContentElement, component='interactive_image.js'):
    CONTENT_PROP = 'content'
    PIL_CONVERT_FORMAT = 'PNG'

    def __init__(self,
                 source: Union[str, Path] = '', *,
                 content: str = '',
                 on_mouse: Optional[Callable[..., Any]] = None,
                 events: List[str] = ['click'],
                 cross: bool = False,
                 ) -> None:
        """Interactive Image

        Create an image with an SVG overlay that handles mouse events and yields image coordinates.
        It is also the best choice for non-flickering image updates.
        If the source URL changes faster than images can be loaded by the browser, some images are simply skipped.
        Thereby repeatedly updating the image source will automatically adapt to the available bandwidth.
        See `OpenCV Webcam <https://github.com/zauberzeug/nicegui/tree/main/examples/opencv_webcam/main.py>`_ for an example.

        :param source: the source of the image; can be an URL, local file path or a base64 string
        :param content: SVG content which should be overlaid; viewport has the same dimensions as the image
        :param on_mouse: callback for mouse events (yields `type`, `image_x` and `image_y`)
        :param events: list of JavaScript events to subscribe to (default: `['click']`)
        :param cross: whether to show crosshairs (default: `False`)
        """
        super().__init__(source=source, content=content)
        self._props['events'] = events
        self._props['cross'] = cross

        def handle_mouse(e: GenericEventArguments) -> None:
            if on_mouse is None:
                return
            args = cast(dict, e.args)
            arguments = MouseEventArguments(
                sender=self,
                client=self.client,
                type=args.get('mouse_event_type', ''),
                image_x=args.get('image_x', 0.0),
                image_y=args.get('image_y', 0.0),
                button=args.get('button', 0),
                buttons=args.get('buttons', 0),
                alt=args.get('alt', False),
                ctrl=args.get('ctrl', False),
                meta=args.get('meta', False),
                shift=args.get('shift', False),
            )
            handle_event(on_mouse, arguments)
        self.on('mouse', handle_mouse)

    def _set_props(self, source: Union[str, Path]) -> None:
        if isinstance(source, PIL_Image):
            source = pil_to_base64(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(source)

    def force_reload(self) -> None:
        """Force the image to reload from the source."""
        self._props['t'] = time.time()
        self.update()
