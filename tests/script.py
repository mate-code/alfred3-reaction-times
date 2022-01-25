import alfred3 as al

import alfred3_reaction_times
import alfred3_reaction_times as art

exp = al.Experiment()


@exp.member
class Demo(al.Page):

    def on_exp_access(self):
        self += al.Text("Reaction Times Test")

        self += art.ReactionTimes(
            art.Trial(
                art.Stimulus(
                    al.Text("To start, press any key"),
                    name="start"
                ),
            ),
            art.Trial(
                art.Fixation(
                    element=al.Text("X"),
                    duration=2
                ),
                art.Stimulus(
                    al.Text("Hello Stimulus 1")
                ),
                art.Pause(2.5),
            ),
            art.Trial(
                art.Fixation(
                    element=al.Text("X"),
                    duration=2
                ),
                art.Stimulus(
                    al.Text("Hello Stimulus 2")
                ),
                art.Pause(2.5),
            ),
            art.Trial(
                art.Fixation(
                    element=al.Text("X"),
                    duration=2
                ),
                art.Stimulus(
                    al.Text("Hello Stimulus 3")
                ),
                art.Pause(2.5),
            ),
        )

        # reactions = art.ReactionTimes()
        # stimuli = ("A", "B", "C", "D", "E", "F", "G")
        #
        # for stimulus in stimuli:
        #     trial = art.Trial()
        #     trial += art.Fixation(
        #         element=al.Text("X"),
        #         duration=2
        #     )
        #     trial += art.Stimulus(
        #         art.Reaction("y", name="reaction_yes"),
        #         art.Reaction("n", name="reaction_no"),
        #         element=al.Text(stimulus),
        #         duration=2
        #     )
        #     trial += art.Feedback(
        #         element=al.Text("Timeout"),
        #         duration=2,
        #         showif={
        #             "Stimulus": {"time": ">2"}
        #         }
        #     )
        #     trial += art.Pause(
        #         duration=2
        #     )
        #     reactions += trial
        #
        # self += reactions
        #
        # self += al.Text("End")


if __name__ == "__main__":
    exp.run()
