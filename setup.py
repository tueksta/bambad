from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2"]

setup(
    name="bambad",
    version="1.0.0",
    author="Andreas Beer",
    author_email="andreas.beer+bambad@gmail.com",
    description="A command line tool for finding, downloading, unpacking and launching Bamboo artifacts for Mac, Windows, and iOS on a Bamboo server via the Bamboo API(s)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/tuexss/bambad/homepage/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
