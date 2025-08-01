# Pykari: Static Sites in a Flash

Pykari is a simple static site generator written in Python. The name comes from the Japanese word "pikari" (ピカリ), meaning a "flash of light."

## Installation

Pykari depends on two plugin extensions for [Markdown-It-Py][mditpy]: [Heading, MD][headingmd] and [Highlight-it][hlit]. Follow the installation instructions on the pages for each plugin. Then, clone this repository, change into the repository directory, and install Pykari with `pip`:

```bash
pip install .
```

## Basic Usage

Pykari comes with a command line tool, `pykari`, to set up projects and generate static site files. Type the following command and press enter to set up a new project in `myproject`:

```bash
pykari --setup myproject
```

Pykari project organization is loosely based on [Sphinx][sphinx]. Edit the CSS stylesheet in `_static` and the HTML template in `_templates` to customize the look of your site. Edit `index.md` and/or add other Markdown files to add pages to your site. Once you are ready to generate your site, change into the project directory, type `pykari`, and press enter. Pykari will create the static site in `_build`.

## Next Steps

Refer to the [Pykari documentation][pykari-docs] for more detailed instructions. 

[headingmd]: https://github.com/elijahgreenstein/headingmd
[hlit]: https://github.com/elijahgreenstein/highlight-it
[jinja]: https://jinja.palletsprojects.com/en/stable/
[mditpy]: https://markdown-it-py.readthedocs.io/en/latest/
[pykari-docs]: https://elijahgreenstein.github.io/pykari/
[sphinx]: https://www.sphinx-doc.org/en/master/

