import alfred3 as al
from alfred3.element.core import Element
from alfred3.exceptions import AlfredError
from alfred3._helper import inherit_kwargs

from ._env import jinja_env
from .keycodes import keycodes

from .hidden_input import HiddenInput


class SequencePart(Element):
    """
    SequencePart baseclass, providing basic functionality for all sequence parts

    Args:
        element (Element): Alfred3 element you want to display when this part
            is shown during the execution of the trial
        duration (float): Duration of display in seconds. For Stimulus parts, this
            duration will be the maximum display time before the stimulus presentation
            is considered to be a timeout. Leave it blank or 0 to disable this behavior.

    See Also:
        * See :class:`.ReactionTimes` and
          :class:`.Trial` for code examples on how to use sequence parts.

    """
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
    """
    Used for adding a possible keypress as a reaction to a stimulus part.

    Args:
        key (str): The key the user can press to trigger a reaction

    See Also:
        * See :class:`.ReactionTimes` and
          :class:`.Trial` for code examples on how to use reactions with Stimulus objects.

    Notes:
        Possible keycodes are stored in art.keycodes::

            keycodes = {{
                "any": 0,
                "backspace": 8,
                "tab": 9,
                "enter": 13,
                "shift": 16,
                "ctrl": 17,
                "alt": 18,
                "pause/break": 19,
                "caps lock": 20,
                "escape": 27,
                "page up": 33,
                "space": 32,
                "page down": 34,
                "end": 35,
                "home": 36,
                "arrow left": 37,
                "arrow up": 38,
                "arrow right": 39,
                "arrow down": 40,
                "print screen": 44,
                "insert": 45,
                "delete": 46,
                "0": 48,
                "1": 49,
                "2": 50,
                "3": 51,
                "4": 52,
                "5": 53,
                "6": 54,
                "7": 55,
                "8": 56,
                "9": 57,
                "a": 65,
                "b": 66,
                "c": 67,
                "d": 68,
                "e": 69,
                "f": 70,
                "g": 71,
                "h": 72,
                "i": 73,
                "j": 74,
                "k": 75,
                "l": 76,
                "m": 77,
                "n": 78,
                "o": 79,
                "p": 80,
                "q": 81,
                "r": 82,
                "s": 83,
                "t": 84,
                "u": 85,
                "v": 86,
                "w": 87,
                "x": 88,
                "y": 89,
                "z": 90,
                "left window key": 91,
                "right window key": 92,
                "select key": 93,
                "numpad 0": 96,
                "numpad 1": 97,
                "numpad 2": 98,
                "numpad 3": 99,
                "numpad 4": 100,
                "numpad 5": 101,
                "numpad 6": 102,
                "numpad 7": 103,
                "numpad 8": 104,
                "numpad 9": 105,
                "multiply": 106,
                "add": 107,
                "subtract": 109,
                "decimal point": 110,
                "divide": 111,
                "f1": 112,
                "f2": 113,
                "f3": 114,
                "f4": 115,
                "f5": 116,
                "f6": 117,
                "f7": 118,
                "f8": 119,
                "f9": 120,
                "f10": 121,
                "f11": 122,
                "f12": 123,
                "num lock": 144,
                "scroll lock": 145,
                "My Computer (multimedia keyboard)": 182,
                "My Calculator (multimedia keyboard)": 183,
                "semicolon": 186,
                "equal sign": 187,
                "comma": 188,
                "dash": 189,
                "period": 190,
                "forward slash": 191,
                "open bracket": 219,
                "backslash": 220,
                "close bracket": 221,
                "single quote": 222,
            }}

    """
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

        if "name" in kwargs and kwargs["name"] == "--TIMEOUT--":
            raise AlfredError("Forbidden name --TIMEOUT--")

    @property
    def template_data(self):
        d = super().template_data
        d["key"] = self.key
        return d


@inherit_kwargs
class Pause(SequencePart):
    """
    Blank part to add a pause to the trials execution

    Args:
        duration (float): Duration of the pause in seconds
        {kwargs}

    See Also:
        * See :class:`.ReactionTimes` and
          :class:`.Trial` for code examples on how to use sequence parts.

    """
    type = "pause"

    def __init__(
            self,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(duration=duration, **kwargs)


@inherit_kwargs
class Fixation(SequencePart):
    """
    Fixation to show right before a stimulus

    Args:
        element (Element): Alfred3 element you want to display as a fixation
        duration (float): Duration of the fixation in seconds
        {kwargs}

    See Also:
        * See :class:`.ReactionTimes` and
          :class:`.Trial` for code examples on how to use sequence parts.

    """
    type = "fixation"

    def __init__(
            self,
            element: Element,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(element=element, duration=duration, **kwargs)


@inherit_kwargs
class Stimulus(SequencePart):
    """
    Stimulus to show to the user

    Args:
        element (Element): Alfred3 element you want to display as a stimulus
        *reactions (Reaction): Possible reactions the user can show to trigger
            reaction time measurement and continue the execution
        {kwargs}

    See Also:
        * See :class:`.ReactionTimes` and
          :class:`.Trial` for code examples on how to use sequence parts.

    """
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


@inherit_kwargs
class Feedback(SequencePart):
    """
    Feedback to show after a reaction has been measured

    Args:
        element (Element): Alfred3 element you want to display as a feedback
        duration (float): Duration of the feedback in seconds
        {kwargs}

    See Also:
        * See :class:`.ReactionTimes` and
          :class:`.Trial` for code examples on how to use sequence parts.

    """
    type = "feedback"

    def __init__(
            self,
            element: Element,
            duration: float = 0,
            **kwargs
    ):
        super().__init__(element=element, duration=duration, **kwargs)
