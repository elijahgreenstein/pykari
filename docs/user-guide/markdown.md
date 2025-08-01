---
title: Markdown
---

Pykari generates HTML webpages in the build directory from Markdown files in the source directory. Add Markdown files with the extension `.md` to the source directory to add new pages to your website.

When you use the [Pykari command line tools](cli.html) to generate your website, Pykari will look for all files with the extension `.md` in the source directory, convert the contents to HTML, and write corresponding HTML files in the build directory.

# CommonMark

Pykari uses the [Markdown-It-Py][mditpy] Markdown parser to convert Markdown to HTML. The Pykari parser is configured with the [default CommonMark settings][mditpy-commonmark], and you can follow [CommonMark][commonmark] conventions to format source documents.

# Additional Markdown Settings

The Pykari parser also uses several additional settings and [Markdown-It-Py plugins][mditpy-plugins] to extend the CommonMark syntax.

## Typography

The [Markdown-It-Py typographic settings][mditpy-typography] are enabled. Single and double quotes will be replaced with opening and closing quotes, and certain character patterns will be replaced (e.g. `...` will be replaced with the `…` character).

## Tables

The core [Markdown-It-Py table plugin][mditpy-core-plugins] is enabled. Follow [GitHub Markdown conventions][gh-tables] to create tables:

```markdown
| Column A Header      | Column B Header      |
| -------------------- | -------------------- |
| Column A, Row 1 Cell | Column B, Row 1 Cell |
| Column A, Row 2 Cell | Column B, Row 2 Cell |
```

## Strikethrough Text

The core [Markdown-It-Py strikethrough plugin][mditpy-core-plugins] is enabled. Use `~~` characters for strikethrough text:

```markdown
~~This text is stricken.~~
```

## Definition Lists

The Markdown-It-Py [definition list plugin][mditpy-deflist] is enabled:

```markdown
Item 1
: Definition, first paragraph.

  Definition, second paragraph.

Item 2
~ Compact definition, first paragraph.
~ Compact definition, second paragraph.
```

# Links

To link to other files in a Pykari project, use the relative path from the source file to the other file, but change the extension to `.html`. Use two full stop characters (`..`) to represent the parent directory of the directory containing the file.

Here is an example project:

```
myproject/
    index.md
    posts/
        technical/
            essay.md
        personal/
            travel.md
```

To link to the `essay` page from the `travel` page, write the following in `travel.md`:

```markdown
A [link](../technical/essay.html) to the technical essay.
```

Note that `travel.md` is in the `personal` directory. The two full stop characters (`..`) represent the parent directory of `personal`: `posts`.

To link to the `index` page from the `travel` page, write the following in `travel.md`:

```markdown
A [link](../../index.html) to the index page.
```

# Metadata

Every Markdown file **must** begin with a metadata block; Pykari will raise an error if no metadata is found. Include metadata for each file in a [YAML-formatted][yaml] block at the top of the Markdown file, preceded and followed by at lines containing at least three hyphen characters (`---`). For example:

```
---
title: Insightful Essay
date: 2025-07-31
---

# First Section
```

Pykari will use the metadata to render [templates](static.html#templates). Include variables in a [Jinja][jinja]-formatted template to indicate where metadata should appear in a document. For example:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
</head>
<body>
<h1 id="title">{{ title }}</h1>
<div id="date">{{ date }}</div>
{{ BODY }}
</body>
</html>
```

The `{{ title }}` and `{{ date }}` [Jinja expressions][jinja-expr] will be replaced with the corresponding values from the metadata.

Note that the example above uses the default `BODY` variable to indicate where the body content of the Markdown file should appear in [the template](static.html#templates). Refer to the [guide to writing Pykari templates](../howto/howto-template.html) for details about how to create a custom template.

# Headings

## Levels

It is recommended that the HTML `<h1>` tag be reserved for the title. Include the title in the metadata, and add an `<h1>` tag with the `{{ title }}` expression to your HTML templates. Markdown headings can be used for section levels beneath `<h1>`. Pykari uses the [Heading, MD][headingmd] extension to Markdown-It-Py to shift HTML headings down one level from Markdown heading levels in the source file.

Here is an example of Markdown headings:

```
# First Section

## First Subsection
```

Pykari will render the above into HTML as:

```html
<h2 id="first-section">First Section</h2>
<h3 id="first-subsection">First Subsection</h2>
```

Note that the level-one Markdown heading, `# First Section`, is rendered with a level-two HTML tag (`<h2>`).

In short:

- Use a `title` variable in the metadata for the top-level `<h1>` section title.
- Use Markdown headings from levels one to five for subsequent section levels (HTML levels `<h2>` to `<h6>`).

## Heading Anchors

The [heading anchors plugin][mditpy-anchors] is enabled with `max_level` set to `3`. Level-one and two Markdown headings (which Pykari renders as `<h2>` and `<h3>` HTML headings) will automatically be assigned an `id` attribute based on the heading text. As seen in the previous example, the heading `# First Section` is rendered into HTML with the attribute `id="first-section"`.

## Syntax Highlighting

Pykari uses the [Highlight-It][hlit] extension to Markdown-It-Py to configure syntax highlighting with [Pygments][pygments]. To highlight a block of code, include the [Pygments short name][pygments-names] for the programming language immediately after the first code-block fence:

``````markdown
```python
def hello(x):
    print("Hello," x)
```
``````

Note that highlighting styles will not be included in the output HTML file. To set up syntax highlighting, follow the [Pygments instructions to generate a CSS style sheet][pygments-gen-styles] and write the file to the `_static` directory. For example:

```bash
pygmentize -f html -S default -a .highlight > _static/highlight.css
```

Then, include a link to the style sheet in your HTML templates:

```html
<link rel="stylesheet" href="{{ ROOT }}/_static/highlight.css">
```

Note that the example above uses the default `ROOT` variable to indicate the relative path to the source directory from the file. Refer to the [guide to writing Pykari templates](../howto/howto-template.html) for details about how to create a custom template.

[commonmark]: https://commonmark.org/
[gh-tables]: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables
[headingmd]: https://github.com/elijahgreenstein/headingmd
[hlit]: https://github.com/elijahgreenstein/highlight-it
[jinja]: https://jinja.palletsprojects.com/en/stable/
[jinja-expr]: https://jinja.palletsprojects.com/en/stable/templates/#expressions
[mditpy-anchors]: https://mdit-py-plugins.readthedocs.io/en/latest/#heading-anchors
[mditpy-commonmark]: https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser
[mditpy-core-plugins]: https://markdown-it-py.readthedocs.io/en/latest/plugins.html
[mditpy-deflist]: https://mdit-py-plugins.readthedocs.io/en/latest/#definition-lists
[mditpy-footnote]: https://mdit-py-plugins.readthedocs.io/en/latest/#footnotes
[mditpy-frontmatter]: https://mdit-py-plugins.readthedocs.io/en/latest/#front-matter
[mditpy-plugins]: https://mdit-py-plugins.readthedocs.io/en/latest/
[mditpy-typography]: https://markdown-it-py.readthedocs.io/en/latest/using.html#typographic-components
[mditpy]: https://markdown-it-py.readthedocs.io/en/latest/
[pygments]: https://pygments.org/
[pygments-gen-styles]: https://pygments.org/docs/cmdline/#generating-styles
[pygments-names]: https://pygments.org/languages/
[pykari]: https://github.com/elijahgreenstein/pykari
[yaml]: https://yaml.org/
