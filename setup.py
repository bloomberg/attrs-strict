from setuptools import setup

with open("README.md") as fp:
    readme = fp.read()

long_description = "".join(
    [
        section.split("<!-- end -->")[0]
        for section in readme.split("<!-- begin -->")
        if "<!-- end -->" in section
    ]
)

setup(long_description=long_description)
