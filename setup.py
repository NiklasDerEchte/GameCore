from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

setup(
    name="GameCore",
    version="0.1.4",
    description="GameCore is a nice runtime structure for pygame ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Niklas Wockenfuß",
    url="https://github.com/NiklasDerEchte/GameCore",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.5",
    install_requires=parse_requirements("requirements.txt"),
)