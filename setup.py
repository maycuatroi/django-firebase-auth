import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-firebase-auth',
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'firebase-admin',
        'djangorestframework'
    ],
    include_package_data=True,
    license='MIT License',
    description='Django authentication middle ware using Firebase Authentication Service',
    long_description=long_description,
    author='Nguyen Anh Binh',
    author_email='sometimesocrazy@gmail.com',
)
