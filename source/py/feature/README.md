# Maple Mono Feature Module

A utility module for managing OpenType font features like stylistic sets, character variants, and ligatures.

## Why

Most open-source font projects manage OpenType feature files manually. While fonttools' `ast` module enables feature file automation, the lack of documentation made implementation challenging. This module reimplements the `ast` functionality to generate `.fea` files and integrate them during builds.

## Overview

The `feature/` module uses an AST approach to programmatically define OpenType features.

### Key Components

- **`ast.py`**: Core utilities for defining OpenType features.
- **`regular.py`**: Entry file for regular features.
- **`italic.py`**: Entry file for italic features.
- **`base/`**: Foundational classes and features (e.g., numbers, cases, localized forms).
- **`calt/`**: Default ligatures.
- **`cv/`**: Character variants.
- **`ss/`**: Stylistic sets.

## Usage

### Custom Tags

Create custom tags using utilities in `calt/tag.py`.

The font includes built-in tags with full-round borders. Use `subst_liga` to customize trigger text:

```py
subst_liga(
    source="TODO:",
    target="tag_todo.liga",
    lookup_name="todo_colon"
)
```

For additional tags, use `tag_custom`:

```py
tag_custom(
    [
      (":attention:", "[attention]"),
      ("_noqa_", "(noqa)"),
      # ("_alter_", "<alter>"),
    ],
    bg_cls_dict,
)
```
This converts:
```
:attention: _noqa_
```

into a styled tag:

![Image](https://github.com/user-attachments/assets/e67f282c-e961-4e55-9169-2f20d7ccfbc6)

#### Limitations

1. Custom tags lack spacing optimization.
2. Tags may break with letter spacing > 0. See [#381](https://github.com/subframe7536/maple-font/issues/381#issuecomment-2808022878).
3. Tags inherit text color. See [#381](https://github.com/subframe7536/maple-font/issues/381#issuecomment-2809622541).

### Remove Infinite Ligatures

To disable infinite ligatures for `=`, `-`, `~`, and `#`, set `__USE_INFINITE = False` in `calt/_infinite_utils.py`.

## Variable Font Features

Two strategies exist for feature freezing:
1. Move ligature rules to `calt` (e.g., `ss08`)
2. Direct glyph substitution (e.g., `cv01`)

Currently, method 2 isn't supported in variable format. In V7.0, all variable format variants are identical except for family name. Use `--apply-fea-file` flag as needed.

Features now load dynamically via Python. The logic in `common.py` implements method 1. **Enable font ligatures** to use all features in variable fonts (not recommended).

## AST Utilities

Core utilities for defining OpenType features:

### `Clazz`

Represents a class of glyphs.

```py
from source.py.feature.ast import Clazz, subst

cls_digit = Clazz("Digit", ["zero", "one", "two", "three"])
cls_digit.state()
subst(cls_digit.use(), "a", "b", "c")
```

Generated fea string:

```fea
@Digit = [zero, one, two, three];
sub @Digit a' b by c;
```

### `Lookup`

Defines a lookup block for substitutions.

```py
from source.py.feature.ast import Lookup, subst

lookup_example = Lookup(
    name="example_lookup",
    desc="Example substitution",
    content=[
        subst("a", "b", None, "c"),
    ],
)
```

Generated fea string:

```fea
# Example substitution
lookup example_lookup {
  sub a b' by c;
} example_lookup;
```

### `Feature`

Represents an OpenType feature.

```py
from source.py.feature.ast import Feature

feature_example = Feature(
    tag="calt",
    content=[
        lookup_example,
    ],
)
```

Generated fea string:

```fea
feature calt {

  # Example substitution
  lookup example_lookup {
    sub a b' by c;
  } example_lookup;

}
```

### Create

Generates the final OpenType feature file content.

```py
from source.py.feature.ast import create

fea_content = create([feature_example])
print(fea_content)
```

## Generating Features

Features apply automatically during build. To update fea files manually:

```sh
uv run task.py fea
```

Example feature generation:

```py
from source.py.feature import generate_fea_string

fea_string = generate_fea_string(italic=False, cn=True)
print(fea_string)
```
