---
title: How to Write a Template
---

# Setup

Create a Pykari project with the command line interface:

```bash
pykari --setup mytemplate
```

Pykari will create a default template, `default.html`, in `mytemplate/_templates`, as well as an empty style sheet, `styles.css`, in `mytemplate/_static`.

# Default Template

Open `mytemplate/_templates/default.html`. It contains a very basic template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <link rel="stylesheet" href="{{ ROOT }}/_static/styles.css">
</head>
<body>
{{ BODY }}
</body>
</html>
```

The template includes a `title` variable set within double curly braces, `{{ title }}`, which [Jinja uses to represent expressions][jinja-expr]. Pykari will look for a value for `title` in the metadata of each Markdown source file. All Markdown documents that use this template **must**, therefore, include `title` in the [metadata block](../user-guide/markdown.html#metadata). For example:

```
---
title: Creative Anecdote
---
```

Note that the template also includes [two variables](../user-guide/static.html#variables) that Pykari creates each time it processes a Markdown source file:

`ROOT`
: Pykari will replace `{{ ROOT }}` with the relative path from the Markdown file to the source directory. In the HTML, this will correspond to the relative path from the HTML file to the build directory. Use the `ROOT` variable to ensure that links in the template work for all project pages, regardless of their location relative to the source/build directory.

`BODY`
: Pykari will replace `{{ BODY }}` with the content of a Markdown file, converted to HTML.

# Custom Template

## Create a New Template

Change into the project directory and copy the contents of the default template into a new template, `great.html`:

```bash
cat _templates/default.html > _templates/great.html
```

Open `_templates/great.html` and check that the contents are the same as `_templates/default.html`.

## Link to Home Page

Use the `ROOT` variable to add links to other project pages in the template. For example, add an anchor element to `_templates/great.html` to include a link to the home page (`index.html`) on every page:

```html
<body>
<a href="{{ ROOT }}/index.html">Home</a>
{{ BODY }}
</body>
```

## Title and Date

Use variables to include values from source file metadata, such as `title` and `date`:

```html
<body>
<a href="{{ ROOT }}/index.html">Home</a>
<h1 id="title">{{ title }}</h1>
{% if date %}
<p id="date">{{ date }}</p>
{% endif %}
{{ BODY }}
</body>
```

Note the use of a [Jinja `if` statement][jinja-if] around the `date` variable. The `date` paragraph will only appear in the rendered HTML page if the Markdown source file contains `date` in its metadata. Optionally include a `date` in source file metadata as follows:

```
---
title: Creative Anecdote
date: 2025-07-31
---
```

## Static Files

Add link elements to templates to link to additional CSS style sheets. For example, create a new style sheet in `_static`:

```bash
touch _static/great.css
```

Open `_static/great.css` and add the following:

```css
#title {
  color: orange;
  font-family: sans-serif;
}
```

Close `_static/great_styles.css` and open `_templates/great.html`. Use the `ROOT` variable again to link to the style sheet in the HTML `head` element:

```html
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <link rel="stylesheet" href="{{ ROOT }}/_static/styles.css">
  <link rel="stylesheet" href="{{ ROOT }}/_static/great.css">
</head>
```

Pages rendered from the `great.html` template will now have an orange, sans-serif title.

## Use a Custom Template

By default, Pykari uses `_templates/default.html` to render HTML pages. To use a different template, add a `template` variable to the metadata of the source Markdown file:

```
---
title: Creative Anecdote
date: 2025-07-31
template: great
---
```

Note that the template name, `great`, is the name of the template file, `great.html`, without the `.html` extension.

## Final Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <link rel="stylesheet" href="{{ ROOT }}/_static/styles.css">
  <link rel="stylesheet" href="{{ ROOT }}/_static/great.css">
</head>
<body>
<a href="{{ ROOT }}/index.html">Home</a>
<h1 id="title">{{ title }}</h1>
{% if date %}
<p id="date">{{ date }}</p>
{% endif %}
{{ BODY }}
</body>
</html>
```

[jinja-expr]: https://jinja.palletsprojects.com/en/stable/templates/#expressions
[jinja-if]: https://jinja.palletsprojects.com/en/stable/templates/#if
[pygments-gen-styles]: https://pygments.org/docs/cmdline/#generating-styles

