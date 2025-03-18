from setuptools import setup, find_packages

setup(
    name="zehef-json",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["only_account_search_json_output"],
    entry_points={
        "console_scripts": [
            "zehef-json = only_account_search_json_output:main",
        ],
    },
    install_requires=[
        "requests",
        "bs4",
        "httpx",
        "requests",
        "email-validator",
    ],
    description="Output the Zehef result (only account search) in JSON format",
    url="https://github.com/zackey-heuristics/Zehef",
    license="GPLv3",
)