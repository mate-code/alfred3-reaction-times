
from jinja2 import Environment
from jinja2 import PackageLoader

#: jinja Environment giving access to included jinja-templates.
jinja_env = Environment(loader=PackageLoader("alfred3_reaction_times", "templates"))
