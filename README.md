# alfred-reaction-times
Alfred3 library for measurement of reaction times

## Installation

Please note, that the base package alfred3 must also be installed.

```cmd
$ pip install alfred3
```

Afterwards, you can install alfred3_reaction_times:

```cmd
$ pip install alfred3-reaction-times
```

## A "Hello world" experiment

```Python
import alfred3 as al
import alfred3_reaction_times as art
exp = al.Experiment()


exp += al.Page('Reacting to "Hello World"', name="hello_world")

exp.hello_world += al.Text('Please press any key when you see "Hello World')

exp.hello_world += art.ReactionTimes(
    art.Trial(
        art.Fixation(
            element=al.Text("X"), # any alfred3 element to be shown
            duration=5 # display duration in seconds
        ),
        art.Stimulus(
            al.Text("Hello world"), # any alfred3 element to be shown
            art.Reaction("any") # definition of the keys that are considered as the proper reaction
        )
    )
)

```

In this example, an "X" will be shown as a fixation stimulus, followed by the text 
"Hello World" after 5 seconds

On further information on how to write and run an alfred3 experiment,
please read the [alfred3 documentation](https://alfredo3.psych.bio.uni-goettingen.de/docs/)