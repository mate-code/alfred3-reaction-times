from alfred3.element.core import InputElement
from ._env import jinja_env


# @inherit_kwargs
class HiddenInput(InputElement):
    """
    Provides a hidden entry field.

    Args:
        {kwargs}

    Examples:
        ::

            import alfred3 as al
            exp = al.Experiment()

            @exp.member
            class Demo(al.Page):
                name = "demo"

                def on_exp_access(self):
                    self += al.HiddenInput(name="hi1", default="fixed")

    """

    base_template = jinja_env.get_template("EmptyBaseElement.html.j2")
    element_template = jinja_env.get_template("HiddenInput.html.j2")

