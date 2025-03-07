from setuptools import setup, find_packages

setup(
    name="maimai-bot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'pymongo',
    ],
) 