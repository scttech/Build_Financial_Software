from setuptools import setup, find_packages

setup(
    name="pylint_postgres_plugin",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "pylint.plugins": [
            "psycopg_import_checker = pylint_postgres_plugin.psycopg_import_checker:register",
        ],
    },
)
