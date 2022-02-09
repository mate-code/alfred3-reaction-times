import alfred3 as al
from alfred3.element.core import Element
from alfred3.exceptions import AlfredError

from ._env import jinja_env
from .keycodes import keycodes

from .hidden_input import HiddenInput


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

    base_template = jinja_env.get_template("EmptyBaseElement.html.j2")
    element_template = jinja_env.get_template("Reaction.html.j2")

    def __init__(
            self,
            key: str = "any",
            **kwargs
    ):
        super().__init__(**kwargs)
        # Python style?
        if key in keycodes.keys():
            self.key = keycodes[key]
        elif key in keycodes.values():
            self.key = key
        else:
            raise KeyError("Unknown key " + key)

        if kwargs["name"] == "--TIMEOUT--":
            raise AlfredError("Forbidden name --TIMEOUT--")

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
    element_template = jinja_env.get_template("Stimulus.html.j2")

    input_time = None
    input_reaction = None

    def __init__(
            self,
            element: Element,
            *reactions: Reaction,
            **kwargs
    ):
        super().__init__(element=element, **kwargs)
        self.reactions = reactions

    def added_to_page(self, page):
        super().added_to_page(page)

        self.input_time = HiddenInput(name=self.name + "_time")
        self.input_time.display_standalone = False
        page += self.input_time

        self.input_reaction = HiddenInput(name=self.name + "_reaction")
        self.input_reaction.display_standalone = False
        page += self.input_reaction

        for reaction in self.reactions:
            if reaction is None:
                continue
            reaction.display_standalone = False
            page += reaction

    @property
    def template_data(self):
        d = super().template_data
        d["reaction_html"] = "".join([r.web_widget for r in self.reactions])
        d["input_time_html"] = self.input_time.web_widget
        d["input_time_name"] = self.input_time.name
        d["input_reaction_html"] = self.input_reaction.web_widget
        d["input_reaction_name"] = self.input_reaction.name
        return d


class Feedback(SequencePart):
    type = "feedback"

    def __init__(
            self,
            element: Element,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(element=element, duration=duration, **kwargs)
