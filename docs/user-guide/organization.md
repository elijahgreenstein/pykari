---
title: Project Organization
---

The organization of a Pykari project is loosely based on [Sphinx][sphinx]. When you use the [command line tools](cli.html) to set up a Pykari project, the setup tool creates the following files and subdirectories in the project directory:

```
myproject/
    _build/
    _pykari.yaml
    _static/
        styles.css
    _templates/
        default.html
    index.md
    Makefile
```

`_build`
: The build directory. Pykari will write site files here.

`_pykari.yaml`
: The [configuration file](configuration.html) for a Pykari project.

`_static`
: The directory for static files (e.g. CSS style sheets).

  `styles.css` is an empty CSS style sheet for users to customize.

`_templates`
: The directory for HTML templates. Pykari will use these templates to build complete HTML pages from Markdown source files.

  `default.html` is a basic, default template for users to customize.

`Makefile`
: Use `make` to generate the website from source; use `make clean` to clean up the build directory.

[sphinx]: https://www.sphinx-doc.org/en/master/index.html

