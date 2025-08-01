---
title: Command Line Interface
---

Pykari comes with a command line tool, `pykari`, to set up and build projects. Type the following command and press enter to set up a new project in `myproject`:

```bash
pykari --setup myproject
```

Pykari will create several [project files and subdirectories](organization.html) in `myproject`.

To generate a static site, change into the project directory, type the following command, and press enter:

```bash
pykari
```

Pykari will generate files for the static site in the build directory (`_build`, under the default project [configuration](configuration.html)).
