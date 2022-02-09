import importlib.resources

import alfred3 as al
from alfred3.element.core import Element

from . import js
from . import css

from ._env import jinja_env

from .trial import Trial


class ReactionTimes(Element):
    """
        The basic reaction times element.

        Args:
            *trials (Trial): List of trials to iterate through
                during execution.

            {kwargs}

        Notes:

            .. note:: You can also add the trials later. For a larger number
                of trials with similar layout, the usage of loops is recommended.

        Examples:

            Basic example for adding reaction times measurement with multiple trials::

                import alfred3 as al
                import alfred3_reaction_times as art
                exp = al.Experiment()


                @exp.member
                class Demo(al.Page):

                    def on_exp_access(self):
                        self += art.ReactionTimes(
                            art.Trial(...),
                            art.Trial(...),
                            art.Trial(...),
                        )


            Example for adding reaction times measurement with complete trials
            using a loop:

                import alfred3 as al
                import alfred3_reaction_times as art
                exp = al.Experiment()


                @exp.member
                class Demo(al.Page):

                    def on_exp_access(self):
                        reactions = art.ReactionTimes()
                        stimuli = ("A", "B", "C", "D", "E", "F", "G")

                        for stimulus in stimuli:
                            trial = art.Trial()
                            trial += art.Pause(
                                duration=1
                            )
                            trial += art.Fixation(
                                element=al.Text("X"),
                                duration=1
                            )
                            trial += art.Stimulus(
                                al.Text(stimulus),
                                art.Reaction("any", name=f"reaction_{stimulus}"),
                                name=f"stimulus_{stimulus}",
                                duration=3
                            )
                            reactions += trial

                        self += reactions

        """

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
            with importlib.resources.path(js, "main.js") as js_filepath:
                page += al.JavaScript(path=str(js_filepath))

            with importlib.resources.path(css, "layout.css") as css_filepath:
                page += al.Style(path=str(css_filepath))

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
