import source.py.feature.ast as ast


# https://github.com/subframe7536/maple-font/issues/348
def cv61_subst():
    return ast.subst_map(
        [",", ";", ";;", ";;;", "questiongreek"],
        target_suffix=".cv61",
    )


cv61_name = "Alternative `,` and `;` with straight tail"
cv61_feat = ast.CharacterVariant(
    id=61, desc=cv61_name, content=cv61_subst(), version="7.1", example=",;"
)
