from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as file:
        requirements = []
        for line in file:
            if line.strip() and not line.startswith("#"):
                requirements.append(line.strip())
            else:
                if line.strip() and "<setup-skip>" in line.strip():
                    return requirements
        return requirements

setup(
    name="GameCore",
    version="0.1.5.2",
    description="GameCore is a nice runtime structure for pygame ",
    long_description=open("README.md", encoding="utf-8").read(),
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
