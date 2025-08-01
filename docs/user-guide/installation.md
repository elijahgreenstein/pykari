---
title: Installation
---

Pykari depends on two plugin extensions for [Markdown-It-Py][mditpy]: [Heading, MD][headingmd] and [Highlight-It][hlit]. Follow the installation instructions for each plugin. Then, clone the [Pykari repository][pykari], change into the repository directory, and install Pykari with `pip`:

```bash
pip install .
```

`pip` will install Pykari, as well as the following additional dependencies (if not already installed):

- [Jinja][jinja]
- [Markdown-It-Py][mditpy]
- [Markdown-It-Py Plugin Extensions][mditpy-plugins]
- [PyYAML][pyyaml]

[headingmd]: https://github.com/elijahgreenstein/headingmd
[hlit]: https://github.com/elijahgreenstein/highlight-it
[jinja]: https://jinja.palletsprojects.com/en/stable/
[mditpy-plugins]: https://mdit-py-plugins.readthedocs.io/en/latest/
[mditpy]: https://markdown-it-py.readthedocs.io/en/latest/
[pygments]: https://pygments.org/
[pykari]: https://github.com/elijahgreenstein/pykari
[pyyaml]: https://pyyaml.org/

