import os
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-firebase-auth",
    version="1.0.9",
    packages=find_packages(),
    install_requires=["firebase-admin", "djangorestframework"],
    url="https://github.com/maycuatroi/django-firebase-auth",
    include_package_data=True,
    license="MIT License",
    description="Django authentication middle ware using Firebase Authentication Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nguyen Anh Binh",
    author_email="sometimesocrazy@gmail.com",
)
