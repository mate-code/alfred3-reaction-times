import alfred3 as al
from alfred3.element.core import Element

from ._env import jinja_env

from .sequence_part import SequencePart


class Trial(Element):

    element_template = jinja_env.get_template("Trial.html.j2")

    def __init__(
            self,
            *sequence: SequencePart,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.sequence = list(sequence)

    def __iadd__(self, other):
        self.sequence.append(other)
        return self

    def added_to_page(self, page):
        super().added_to_page(page)
        for sequence_part in self.sequence:
            if sequence_part is None:
                continue
            sequence_part.display_standalone = False
            page += sequence_part

    @property
    def template_data(self):
        d = super().template_data
        # {s.name: s.web_widget for s in self.sequence} # dict comprehension
        d["sequence_html"] = "".join([s.web_widget for s in self.sequence]) # list comprehension
        return d



