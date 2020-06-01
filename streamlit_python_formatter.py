from typing import List

import click
import streamlit



def _autoflake_params(parent=streamlit.sidebar):
    parent.subheader("[Autoflake](https://github.com/myint/autoflake) Parameters")
    widgets = {}
    widgets["expand_star_imports"] = parent.checkbox("Expand Star Imports", value=False)
    widgets["remove_all_unused_imports"] = parent.checkbox(
        "Remove Unused Imports", value=False
    )
    widgets["remove_duplicate_keys"] = parent.checkbox(
        "Remove Duplicate Keys", value=False
    )
    widgets["remove_unused_variables"] = parent.checkbox(
        "Remove Unused Variables", value=False
    )
    widgets["ignore_init_module_imports"] = parent.checkbox(
        "Ignore Init Module Imports", value=False
    )
    return widgets


def _autoflake(code: str, **params) -> str:
    import autoflake

    return autoflake.fix_code(code, **params)


def _autopep8_params(parent=streamlit.sidebar):
    parent.subheader("[Autopep8](https://github.com/hhatto/autopep8) Parameters")

    widgets = {}
    widgets["aggressive"] = parent.checkbox("Aggressive", value=False)
    widgets["max_line_length"] = line_length
    return widgets


def _autopep8(code: str, **params):
    import autopep8

    return autopep8.fix_code(code, options=params, encoding=None, apply_config=False)


def _docformatter_params(parent=streamlit.sidebar):
    parent.subheader("[Docformatter](https://github.com/myint/docformatter) Parameters")
    out_widgets = {}

    out_widgets["summary_wrap_length"] = parent.slider(
        "Summary Wrap Length", value=79, min_value=60, max_value=200
    )
    out_widgets["description_wrap_length"] = (
        parent.slider("Description Wrap Length", value=72, min_value=60, max_value=200),
    )
    out_widgets["pre_summary_newline"] = parent.checkbox(
        "Pre Summary Newline", value=False
    )
    out_widgets["make_summary_multi_line"] = parent.checkbox(
        "Make Summary Multi Line", value=False
    )
    out_widgets["post_description_blank"] = parent.checkbox(
        "Post Description Blank", value=False
    )
    out_widgets["force_wrap"] = parent.checkbox("Force Wrap", value=False)
    return out_widgets


def _docformatter(code: str, **params) -> str:
    import docformatter

    return docformatter.format_code(code, **params)


def _pyformat_params(parent=streamlit.sidebar):
    parent.subheader("[Pyformat](https://github.com/myint/pyformat) Parameters")
    out_widgets = {}

    out_widgets["aggressive"] = parent.checkbox("Aggressive", value=False)
    out_widgets["remove_all_unused_imports"] = parent.checkbox(
        "Remove unused imports", value=False
    )
    out_widgets["remove_unused_variables"] = parent.checkbox(
        "Remove unused variables", value=False
    )
    return out_widgets


def _pyformat(code: str, **params):
    import pyformat

    return pyformat.format_code(
        code,
        aggressive=True,
        apply_config=False,
        remove_all_unused_imports=False,
        remove_unused_variables=False,
    )




def _yapf_params(parent=streamlit.sidebar):
    parent.subheader("[YAPF](https://github.com/google/yapf) Parameters")
    out_widgets = {}

    out_widgets["style_config"] = parent.selectbox(
        "Style Config", ("pep8", "google", "facebook", "yapf")
    )

    return out_widgets


def _yapf(code: str, **params):
    from yapf.yapflib.yapf_api import FormatCode

    return FormatCode(code, **params)[0]


def _isort_params(parent=streamlit.sidebar):

    parent.subheader("[Isort](https://github.com/timothycrosley/isort) Parameters")
    out_widgets = {}

    return out_widgets


def _isort(code: str, **params):
    from isort import SortImports

    return SortImports(file_contents=code).output


def _black_params(parent=streamlit.sidebar):
    parent.subheader("[Black](https://github.com/psf/black) Parameters")
    out_widgets = {}

    out_widgets["line_length"] = line_length

    out_widgets["string_normalization"] = parent.checkbox(
        "string_normalization", value=True
    )

    return out_widgets


def _black(code: str, **params):
    import black

    file_mode = black.FileMode(**params)
    return black.format_str(code, mode=file_mode)


formatter_map = {
    "black": (_black, _black_params),
    "autoflake": (_autoflake, _autoflake_params),
    "autopep8": (_autopep8, _autopep8_params),
    "docformatter": (_docformatter, _docformatter_params),
    "pyformat": (_pyformat, _pyformat_params),
    "yapf": (_yapf, _yapf_params),
    "isort": (_isort, _isort_params),
}


def _reformat(code: str, formatters: List[str]):
    """The main reformat function."""

    for formatter in formatters:
        formatter, params = formatter_map[formatter]
        params = params()
        code = formatter(code, **params)

    return code


streamlit.title("Python Code Formatter")

formatters = streamlit.multiselect(
    "Choose your formatters (the order matters)",
    list(formatter_map.keys()),
    default=["black"],
    key="python-formatters",
)

line_length = streamlit.sidebar.slider(
    "Line Length", value=88, min_value=60, max_value=180
)

text = streamlit.text_area("Type your code here", height=300)

with streamlit.spinner("Formatting code ..."):
    streamlit.code(_reformat(text, formatters))