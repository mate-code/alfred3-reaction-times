import alfred3 as al
from alfred3.element.core import Element

from ._env import jinja_env


class SequencePart(Element):
    element_template = jinja_env.get_template("SequencePart.html.j2")

    def __init__(
            self,
            element=None,
            duration: float = 0,
            **kwargs
    ):
        super(SequencePart, self).__init__(**kwargs)
        self.duration = duration
        self.element = element

    type = "sequence-part"

    def added_to_page(self, page):
        super().added_to_page(page)
        if self.element is not None:
            self.element.display_standalone = False
            page += self.element

    @property
    def template_data(self):
        d = super().template_data
        d["duration"] = self.duration
        e = self.element
        d["type"] = self.type

        try:
            d["element_html"] = e.web_widget
        except AttributeError:
            d["element_html"] = e if e is not None else ""

        return d


class Reaction(Element):

    keycodes = {
        "n": 78,
        "y": 89,
    }

    def __init__(
            self,
            key,
            **kwargs
    ):
        super().__init__(**kwargs)
        if key not in self.keycodes.keys():
            raise KeyError("Unknown key " + key)
        self.key = self.keycodes[key]

    @property
    def template_data(self):
        d = super().template_data
        d["key"] = self.key
        return d


class Pause(SequencePart):
    type = "pause"

    def __init__(
            self,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(duration=duration, **kwargs)


class Fixation(SequencePart):
    type = "fixation"

    def __init__(
            self,
            element: Element,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(element=element, duration=duration, **kwargs)


class Stimulus(SequencePart):
    type = "stimulus"

    def __init__(
            self,
            element: Element,
            *reactions: Reaction,
            timeout: float = 0,
            **kwargs
    ):
        super().__init__(element=element, duration=timeout, **kwargs)
        self.reactions = reactions


class Feedback(SequencePart):
    type = "feedback"

    def __init__(
            self,
            element: Element,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(element=element, duration=duration, **kwargs)
