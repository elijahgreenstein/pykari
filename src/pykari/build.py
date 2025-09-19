"""Build site from source."""

from pathlib import Path
import shutil
import sys
import traceback
from typing import Any

from headingmd import headingmd_plugin
from highlight_it import highlight_plugin
import jinja2
import yaml
from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin


CONFIGURATION = Path("_pykari.yaml")


def is_updated(source: Path, build: Path) -> bool:
    """Check if build file is up-to-date.

    :param source: Path to source file.
    :param build: Path to build file.
    :returns: True if build file exists and is up to date; otherwise False.

    This function checks that the build file exists and then compares the time
    of last modification of the source file to that of the build file. The
    function returns ``True`` if the build file exists and the time of last
    modification is later than the time of last modification of the source file;
    otherwise, the function returns ``False``.
    """
    return build.is_file() and (source.stat().st_mtime < build.stat().st_mtime)


def handle_exc(msg: str, details: str | None, tb: str | None = None) -> None:
    """Handle exceptions.

    :param msg: Top-level error/warning message.
    :param tb: Optional traceback
    :param details: Optional details about the error.
    """
    print(f"\033[91mERROR: {msg}\033[0m\n")
    if details:
        print(details)
        print()
    if tb:
        print("Traceback:\n")
        for line in tb.splitlines():
            print(f"    {line}")
        print()
    sys.exit(1)


def get_config(path: Path) -> dict[str, str] | None:
    """Get configuration file.

    :param path: Path to configuration file.
    :returns: Configuration dictionary.
    """
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f.read())
    except FileNotFoundError:
        msg = f"Unable to find configuration file `{path}`."
        details = "> Did you set up a Pykari project?\n"
        details += "    - Usage: $ pykari --setup <PROJECT-NAME>\n"
        details += "> Check that you are in the root project directory."
        tb = traceback.format_exc()
        handle_exc(msg, details, tb)
        return None


def get_env(tpl_dir: Path) -> jinja2.Environment:
    """Load Jinja environment.

    :param tpl_dir: Path to directory of templates.
    :returns: Jinja environment configured with ``DictLoader``.

    This function reads all of the HTML files in the given directory and creates
    a Jinja environment with a ``DictLoader`` environment that pairs the file
    name (without extension) to the file contents.
    """
    tpl_dict = {}
    for tpl in tpl_dir.glob("*.html"):
        with open(tpl, encoding="utf-8") as f:
            tpl_dict[tpl.stem] = f.read()
    return jinja2.Environment(
        loader=jinja2.DictLoader(tpl_dict),
    )


def check_build_dir(path: Path) -> None:
    """Make build directory, if necessary.

    :param path: Build directory.
    """
    if not path.is_dir():
        path.mkdir()
        print(f"- Made build directory: {path}")


def check_build_subdir(path: Path) -> None:
    """Make build subdirectory from file path, if necessary.

    :param path: File path.
    """
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True)
        print(f"- Made subdirectory: {path.parent}")


def check_copy(file: Path, src: Path, bld: Path) -> bool:
    """Copy from source, if necessary.

    :param file: File path, relative to source directory.
    :param src: Source directory.
    :param bld: Build directory.
    :returns: True if build file updated/created from source; otherwise False.

    This function copies the source file to the build directory under any of the
    following conditions:

    1. There is no build file.
    2. The time of last modification of the source file is *later than* the time
    of last modification of the build file.
    """
    if is_updated(src / file, bld / file):
        return False
    check_build_subdir(bld / file)
    shutil.copyfile(src / file, bld / file)
    print(f"- Copied {src / file} to {bld / file}")
    return True


def get_paths(file: Path, src: Path, bld: Path) -> tuple[Path, Path]:
    """Get Markdown source file and HTML build file paths.

    :param file: File path, relative to source directory.
    :param src: Source directory.
    :param bld: Build directory.
    :returns: Tuple of path to Markdown source file, HTML build file.
    """
    md = src / file
    html = bld / file.with_suffix(".html")
    return md, html


def check_build(
    md: Path, html: Path, src: Path, env: jinja2.Environment, tpl_dir: Path
) -> bool:
    """Build from source, if necessary.

    :param md: Path to Markdown source file.
    :param html: Path to HTML build file.
    :param src: Source directory.
    :param env: Jinja environment configured with ``DictLoader``.
    :param tpl_dir: Template directory path.
    :returns: True if build file updated/created from source; otherwise False.

    This function builds from source under any of the following conditions:

    1. There is no build file.
    2. The time of last modification of the source file is *later than* the time
    of last modification of the build file.
    3. The time of last modification of the template file is *later than* the
    time of last modification of the build file.
    """
    # Load data
    data = md2html(md, src)
    # Set template name to "default" or user-designated name
    tpl_name = "default"
    if "template" in data:
        tpl_name = data["template"]
    # Check build against source and against template
    if is_updated(md, html) and is_updated(tpl_dir / (tpl_name + ".html"), html):
        return False
    # Load template
    tpl = env.get_template(tpl_name)
    # Create directories as needed
    check_build_subdir(html)
    # Render HTML from template and write file
    rendered = tpl.render(data)
    with open(html, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"- Built {html} from {md}")
    return True


def get_relative_root(file: Path, src: Path) -> Path:
    """Get a relative path to the root directory from the given file.

    :param path: File path.
    :param src: Source directory.
    :returns: Relative path to the root directory.

    Example: if the file path, relative to the source directory, is
    ``path/to/file.txt``, this function returns the path ``../..``. This
    relative path can be inserted into HTML templates to create links to other
    files on the website. For example, if the website menu contains a link to
    ``menu/item/link.txt``, the relative path from ``path/to/file.txt`` will be
    ``../../menu/item/link.txt``. Pykari automatically passes a ``ROOT``
    variable to the Jinja template keyed to the path returned from this
    function. Hence, use the path ``{{ ROOT }}/menu/item/link.txt`` to
    ensure that template links can be accessed from any page in the site.
    """
    level_down = len(file.relative_to(src).parts) - 1
    relative = Path("/".join([".."] * level_down))
    return relative if relative else Path(".")


def md2html(md: Path, src: Path) -> dict[Any, Any]:
    """Load metadata and body text from Markdown file.

    :param md: Path to source Markdown file.
    :param src: Source directory.
    :returns: Dictionary of data from source file.

    .. note::

        The Markdown file **must** contain a complete YAML metadata block.
    """
    mdit = (
        MarkdownIt("commonmark", options_update={"typographer": True})
        .enable(["replacements", "smartquotes", "table", "strikethrough"])
        .use(anchors_plugin, max_level=3)
        .use(deflist_plugin)
        .use(front_matter_plugin)
        .use(attrs_plugin)
        .use(headingmd_plugin, shift=1)
        .use(highlight_plugin)
    )
    with open(md, encoding="utf-8") as f:
        text = f.read()
    tokens = mdit.parse(text)
    if tokens[0].type == "front_matter":
        data = yaml.safe_load(tokens[0].content)
        data["BODY"] = mdit.renderer.render(tokens, mdit.options, env=None).strip()
        data["ROOT"] = get_relative_root(md, src)
        return data
    raise ValueError(f"{md} does not begin with complete YAML metadata.")


def generate() -> None:
    """Generate static site."""
    conf = get_config(CONFIGURATION)
    print("\033[94mChecking for updates ...\033[0m")
    src = Path(conf["source"])
    bld = Path(conf["build"])
    static_ext = conf["static_ext"]
    check_build_dir(bld)
    tpl_dir = src / "_templates"
    env = get_env(tpl_dir)
    updates = False
    for extension in static_ext:
        for file in (src / "_static").glob(f"**/*{extension}"):
            updates = check_copy(file.relative_to(src), src, bld) or updates
    for file in src.glob("**/*.md"):
        if conf["ignore"] and file.parts[0] in conf["ignore"]:
            continue
        md, html = get_paths(file.relative_to(src), src, bld)
        updates = check_build(md, html, src, env, tpl_dir) or updates
    if updates:
        print("\033[94m... \033[93mBuild complete!\033[0m\n")
    else:
        print("\033[94m... no updates to build.\033[0m\n")
