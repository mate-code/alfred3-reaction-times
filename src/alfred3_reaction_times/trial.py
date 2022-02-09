import alfred3 as al
from alfred3.element.core import Element

from ._env import jinja_env

from .sequence_part import SequencePart


class Trial(Element):
    """
    The basic reaction times element.

        Args:
            *sequence (SequencePart): List of sequence parts to iterate through
                during execution. Default SequencePart objects are: Pause, Fixation,
                Stimulus and Feedback, but custom ones can be created extending the
                SequencePart object

            {kwargs}

        Notes:

            .. note:: You can also add the sequence parts later.

        Examples:

            Basic example for adding trials:

                import alfred3 as al
                import alfred3_reaction_times as art
                exp = al.Experiment()


                @exp.member
                class Demo(al.Page):

                    def on_exp_access(self):
                        self += art.ReactionTimes(
                            art.Trial(
                                art.Pause(duration=1),
                                art.Stimulus(
                                    al.Text("A"),
                                    art.Reaction("any", name="reaction_A"),
                                    name="stimulus_A",
                                    duration=3
                                )
                            ),
                            art.Trial(
                                art.Pause(duration=1),
                                art.Stimulus(
                                    al.Text("B"),
                                    art.Reaction("any", name="reaction_B"),
                                    name="stimulus_B",
                                    duration=3
                                )
                            ),
                        )


            Example for adding trials with complete trials
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
                            trial += art.Stimulus(
                                al.Text(stimulus),
                                art.Reaction("any", name=f"reaction_{stimulus}"),
                                name=f"stimulus_{stimulus}",
                                duration=3
                            )
                            reactions += trial

                        self += reactions

    """

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
        d["sequence_html"] = "".join([s.web_widget for s in self.sequence])  # list comprehension
        return d



