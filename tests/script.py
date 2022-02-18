import random

import alfred3 as al
import alfred3_reaction_times as art
exp = al.Experiment()

feelings = [
    # positive
    "beeindruckt",
    "dankbar",
    "ermutigt",
    "freudig",
    "gluecklich",
    "lebhaft",
    "zufrieden",
    # negative
    "aggressiv",
    "bedrueckt",
    "deprimiert",
    "empoert",
    "gehaessig",
    "panisch",
    "veraengstigt",
]

sci_fi = [
    # Star Wars
    "Yoda",
    "Obi Wan",
    "Skywalker",
    "Leia",
    "Han Solo",
    "Ewoks",
    "Lightsaber",
    # Star Trek
    "Kirk",
    "Spock",
    "McCoy",
    "Uhura",
    "Sulu",
    "Vulcans",
    "Phaser",
]


@exp.member
class AttributeDiscrimination(al.Page):

    def on_exp_access(self):
        self += al.Row(
            al.Text(
"""
**Positiv**

A drücken
""",
                render_markdown=True,
                align="left"
            ),
            al.Text(
"""
**Negativ**

L drücken
""",
                render_markdown=True,
                align="right"
            ),
        )

        reactions = art.ReactionTimes()
        rand_feelings = random.sample(feelings, len(feelings))
        i = 0
        while i < len(rand_feelings):
            feeling = rand_feelings[i]
            trial = art.Trial(name=f"attribute_discrimination_trial_{i}")
            # Pause between 1 and 2 seconds
            trial += art.Pause(
                duration=1 + random.random()
            )
            trial += art.Stimulus(
                al.Text(feeling, align="center"),
                art.Reaction("a", name=f"attribute_discrimination_{feeling}_positive"),
                art.Reaction("l", name=f"attribute_discrimination_{feeling}_negative"),
                name=f"attribute_discrimination_{feeling}",
                duration=3
            )
            reactions += trial
            i = i+1

        self += reactions


@exp.member
class DemoImageLoading(al.Page):

    def on_exp_access(self):
        self += al.Text("Test start")

        reactions = art.ReactionTimes()
        stimuli = range(1, 50)

        for stimulus in stimuli:
            trial = art.Trial()
            trial += art.Stimulus(
                al.Image(url=f"https://dummyimage.com/4096x2304/222/ccc.png&text=Image+{stimulus}"),
                art.Reaction("y", name=f"reaction_{stimulus}_yes"),
                art.Reaction("n", name=f"reaction_{stimulus}_no"),
                name=f"stimulus_{stimulus}",
                duration=3
            )
            reactions += trial

        self += reactions

        self += al.Text("Test end")


@exp.member
class Demo(al.Page):

    def on_exp_access(self):
        self += al.Text("Test start")

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
                art.Reaction("y", name=f"reaction_{stimulus}_yes"),
                art.Reaction("n", name=f"reaction_{stimulus}_no"),
                name="stimulus_" + stimulus,
                duration=3
            )
            trial += art.Feedback(
                element=al.Text("Yes!"),
                duration=2,
                showif={
                    f"stimulus_{stimulus}_reaction": f"reaction_{stimulus}_yes"
                }
            )
            trial += art.Feedback(
                element=al.Text("No!"),
                duration=2,
                showif={
                    f"stimulus_{stimulus}_reaction": f"reaction_{stimulus}_no"
                }
            )
            reactions += trial

        self += reactions

        self += al.Text("Test end")


@exp.member
class InputCheck(al.Page):

    def on_each_show(self):
        print(self.exp.values)


if __name__ == "__main__":
    exp.run()
