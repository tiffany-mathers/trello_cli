from setuptools import setup, find_packages

setup(
    name="my_cli_program",
    version="0.1",
    packages=find_packages(),
    py_modules=['trello'],
    entry_points={
        'console_scripts': [
            'trello = trello:main',
        ],
    },
)