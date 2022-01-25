import importlib.resources

import alfred3 as al
from alfred3.element.core import Element

from . import js

from ._env import jinja_env

from .trial import Trial


class ReactionTimes(Element):

    element_template = jinja_env.get_template("ReactionTimes.html.j2")

    def __init__(
            self,
            *trials: Trial,
            **kwargs
    ):
        super().__init__(**kwargs)
        #self.trials = () if trials is None else trials
        self.trials = list(trials)

    def __iadd__(self, trial):
        self.trials.append(trial)
        return self

    def added_to_page(self, page):
        super().added_to_page(page)

        if not any([isinstance(el, ReactionTimes) for el in page.elements.values()]):
            with importlib.resources.path(js, "main.js") as filepath:
                page += al.JavaScript(path=str(filepath))

        for trial in self.trials:
            if trial is None:
                continue
            trial.display_standalone = False
            page += trial

    @property
    def template_data(self):
        d = super().template_data
        d["trials_html"] = "".join([s.web_widget for s in self.trials])
        return d
