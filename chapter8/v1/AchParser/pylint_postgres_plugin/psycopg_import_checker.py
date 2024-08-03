import os

from pylint.checkers import BaseChecker

ALLOWED_MODULES = ["ach_file_sql"]
ALLOWED_DIRECTORIES = ["ach_processor/database"]


class PsycopgImportChecker(BaseChecker):

    name = "psycopg-import-checker"
    msgs = {
        "E9999": (
            "psycopg usage only allowed in specific modules",
            "psycopg-disallowed-import",
            "Used when psycopg is imported outside designated modules.",
        ),
    }
    options = ()

    def visit_import(self, node):
        if any(modname == "psycopg" for modname, _ in node.names):
            self._check_psycopg_usage(node)
        elif any(modname.startswith("psycopg") for modname, _ in node.names):
            self._check_psycopg_usage(node)

    def visit_importfrom(self, node):
        if node.modname.startswith("psycopg"):
            self._check_psycopg_usage(node)

    def _check_psycopg_usage(self, node):
        module_name = node.root().name
        module_file = node.root().file
        if module_name in ALLOWED_MODULES:
            return

        for allowed_dir in ALLOWED_DIRECTORIES:
            allowed_path = os.path.normpath(allowed_dir)
            module_path = os.path.normpath(module_file)
            if allowed_path in module_path:
                return

        self.add_message("psycopg-disallowed-import", node=node)


def register(linter):
    linter.register_checker(PsycopgImportChecker(linter))
