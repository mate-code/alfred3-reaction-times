import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Parse version from _version.py in package directory
# See https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
version = {}
with open("src/alfred3_reaction_times/_version.py") as f:
    exec(f.read(), version)

setuptools.setup(
    name="alfred3_reaction_times",
    version=version["__version__"],
    author="Marius Teller",
    author_email="marius.teller@psych.uni-goettingen.de",
    description="Alfred3 library for measurement of reaction times.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mate-code/alfred-reaction-times",
    packages=setuptools.find_packages("src"),
    package_data={
        "alfred3_reaction_times": [
            "templates/*",
        ]
    },
    package_dir={"": "src"},
    install_requires=[
        "alfred3>=2.3.1",
        "jinja2>=2.11",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)