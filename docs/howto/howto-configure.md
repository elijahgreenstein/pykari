---
title: How to Configure Your Pykari Project
---

# Setup

Create a Pykari project with the command line interface:

```bash
pykari --setup reorg
```

Pykari will create a configuration file, `reorg/_pykari.yaml`.

# Default Settings

Open `reorg/_pykari.yaml`. It contains the following settings:

```yaml
build: _build
ignore:
- _build
source: .
static_ext:
- .css
- .js
- .jpg
- .png
```

Details about each setting are available in the [configuration guide](../user-guide/configuration.html).

# Separate Source and Build Directories

By default, Pykari organizes the root project directory ("`.`") as the `source` directory and places the `build` directory, `_build`, inside the root/`source` directory. To separate the source and build directories, change the value for `source` from `.` to `source`. For consistency, change the value for `build` from `_build` to `build`.

The `ignore` setting instructs Pykari to ignore files in the listed subdirectories of the source directory. Since the build directory is no longer located inside of the source directory, change the value for `ignore` from `- _build` to `null`.

Next, open the project `Makefile`. Change the value of the `BLD` variable from `_build` to `build`:

```make
BLD := build
```

Finally, from the command line, change into the project directory, type the following commands, and press enter:

```bash
mkdir source
mv _static _templates index.md source
mv _build build
```

The above commands make a new directory named `source`, move source files and subdirectories into `source`, and rename `_build` as `build`. The project directory now contains the following files and subdirectories:

```
myproject/
    _pykari.yaml
    build/
    source/
        _static/
            styles.css
        _templates/
            default.html
        index.md
    Makefile
```

Note that the `_static` and `_templates` directories **must** remain in the `source` directory. 

# Works in Progress

Use the `ignore` setting to instruct Pykari to ignore files in particular subdirectories in the source directory. For example, type the following and press enter to make `drafts` and `working` subdirectories in `source`:

```bash
mkdir source/drafts source/working
```

Open `_pykari.yaml` and change the value for `ignore` from `null` to a list containing `drafts` and `working`:

```yaml
ignore:
- drafts
- working
```

Pykari will now ignore any files in `source/drafts` or `source/working` when generating a static site.

# Static Files

By default, Pykari copies CSS style sheets, JavaScript scripts, and JPG and PNG images from `source/_static` to `build/_static`. Add extensions to the `static_ext` list in `_pykari.yaml` to instruct Pykari to copy additional static files. For example, to use TIFF files in a website, open `_pykari.yaml` and add `.tiff` to the list:

```yaml
static_ext:
- .css
- .js
- .jpg
- .png
- .tiff
```

# Final Configuration

## `_pykari.yaml`

```yaml
build: build
ignore:
- drafts
- working
source: source
static_ext:
- .css
- .js
- .jpg
- .png
- .tiff
```

## `Makefile`

```make
# Default Pykari Makefile

BLD := site

.PHONY: generate
generate:
	pykari

.PHONY: clean
clean:
	rm -rf $(BLD)
```

