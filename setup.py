from setuptools import setup, find_packages

setup(
    name="liveconfig",
    version="0.1.2-beta.post1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "liveconfig.interfaces.web.frontend": ['/templates/*.html', '/static/*.css'],
    },
    author="Fergus Gault",
    author_email="gaultfergus@gmail.com",
    description="Python package for developers which allows the live editing of class instance attributes to ease development of large python programs. LiveConfig will allow you to interact with values during program execution through an interface of your choice. Values can be saved, and loaded on startup.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=[
        "prompt_toolkit",
        "flask"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    license="MIT",
    url="https://github.com/Fergus-Gault/LiveConfig",
)