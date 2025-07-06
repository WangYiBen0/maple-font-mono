import source.py.feature.ast as ast


def cv63_subst():
    return [
        ast.subst_map(
            "<=",
            target_suffix=".cv63",
        ),
    ]


cv63_name = "Alternative `<=` in arrow style"
cv63_feat = ast.CharacterVariant(
    id=63, desc=cv63_name, content=cv63_subst(), version="7.1", example="<="
)
