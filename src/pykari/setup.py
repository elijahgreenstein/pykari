"""Set up Pykari static site."""

from pathlib import Path

import yaml


def setup(dirname: Path) -> None:
    """Set up Pykari project.

    :param dirname: Name of the project directory.

    .. note::

        This function makes the project directory first, and then the project
        contents; it will raise an error if the directory already exists.
    """
    print("\033[94mSetting up Pykari site ...\033[0m")
    dirname.mkdir()
    print(f"- Made project directory `{dirname}`")
    files = {
        "_pykari.yaml": yaml.dump(
            {
                "source": ".",
                "build": "_build",
                "ignore": ["_build"],
                "static_ext": [".css", ".js", ".jpg", ".png"],
            }
        ),
        "Makefile": "\n".join(
            [
                "# Default Pykari Makefile",
                "",
                "BLD := _build",
                "",
                ".PHONY: generate",
                "generate:",
                "\tpykari",
                "",
                ".PHONY: clean",
                "clean:",
                "\trm -rf $(BLD)",
            ]
        ),
        "index.md": "---\ntitle: Index page\n---\n\n# Your Pykari site\n",
        "_templates/default.html": "\n".join(
            [
                "<!DOCTYPE html>",
                '<html lang="en">',
                "<head>",
                '  <meta charset="UTF-8">',
                "  <title>{{ title }}</title>",
                '  <link rel="stylesheet" href="{{ ROOT }}/_static/styles.css">',
                "</head>",
                "<body>",
                "{{ BODY }}",
                "</body>",
                "</html>",
            ]
        ),
        "_static/styles.css": "/* Pykari site CSS */",
    }
    for subdir in ["_build", "_static", "_templates"]:
        (dirname / subdir).mkdir()
        print(f"- Made subdirectory `{dirname / subdir}`")
    for name, content in files.items():
        with open(dirname / name, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"- Created `{dirname / name}`")
    print("\033[94m... \033[93mDone!\033[0m")
