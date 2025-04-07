from setuptools import setup, find_packages

setup(
    name="liveconfig",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "liveconfig.interfaces.web.frontend": ['/templates/*.html', '/static/*.css'],
    },
    author="Fergus Gault",
    author_email="gaultfergus@gmail.com",
    description="Python package for developers which allows the live editing of variables, classes, and functions to ease development of large python programs. LiveConfig will allow you to interact with values during program execution through an interface of your choice. Values can be saved, and loaded on startup.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=[
        "prompt_toolkit",
        "flask"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    url="https://github.com/Fergus-Gault/LiveConfig",
)