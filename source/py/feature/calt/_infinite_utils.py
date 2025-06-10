import source.py.feature.ast as ast


__USE_INFINITE = True


def use_infinite():
    return __USE_INFINITE


def ignore_when_using_infinite(*items: str | ast.Lookup) -> list:
    if __USE_INFINITE:
        return []
    return items  # type: ignore


def ignore_when_not_using_infinite(*items: str | ast.Lookup) -> list:
    if not __USE_INFINITE:
        return []
    return items  # type: ignore


def infinite_rules(
    glyph: str,
    cls_start: ast.Clazz,
    symbols: list[str],
    extra_rules: list[ast.Line] = [],
):
    prefix = []

    for s in symbols:
        prefix.append(ast.gly_seq(s + glyph, "sta"))
        prefix.append(ast.gly_seq(s + glyph, "mid"))

    prefix_cls = ast.cls(prefix, cls_start)

    return [
        ast.subst(
            prefix_cls, glyph, ast.cls(symbols, glyph), ast.gly_seq(glyph, "mid")
        ),
        ast.subst(prefix_cls, glyph, None, ast.gly_seq(glyph, "end")),
        *[
            [
                ast.subst(cls_start, s, glyph, ast.gly_seq(s + glyph, "mid")),
                ast.subst(cls_start, s, None, ast.gly_seq(s + glyph, "end")),
                ast.subst(None, s, glyph, ast.gly_seq(s + glyph, "sta")),
            ]
            for s in symbols
        ],
        *extra_rules,
        # Must be end of rules
        ast.subst(None, glyph, ast.cls(symbols, glyph), ast.gly_seq(glyph, "sta")),
    ]
