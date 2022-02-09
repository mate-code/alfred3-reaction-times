import alfred3 as al

import alfred3_reaction_times as art

exp = al.Experiment()


@exp.member
class Demo(al.Page):

    def on_exp_access(self):
        self += al.Text("Reaction Times Test")

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
                art.Reaction("y", name="reaction_" + stimulus + "_yes"),
                art.Reaction("n", name="reaction_" + stimulus + "_no"),
                name="stimulus_" + stimulus,
                duration=3
            )
            trial += art.Feedback(
                element=al.Text("Yes!"),
                duration=2,
                showif={
                    "stimulus_" + stimulus + "_reaction": "reaction_" + stimulus + "_yes"
                }
            )
            trial += art.Feedback(
                element=al.Text("No!"),
                duration=2,
                showif={
                    "stimulus_" + stimulus + "_reaction": "reaction_" + stimulus + "_no"
                }
            )
            reactions += trial

        self += reactions

        self += al.Text("End")


@exp.member
class InputCheck(al.Page):

    def on_each_show(self):
        print(self.exp.values)


if __name__ == "__main__":
    exp.run()
