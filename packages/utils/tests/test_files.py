from pylibs_utils import make_filename


def test_make_filename() -> None:
    assert make_filename("Quarterly Report: Q3", "pdf") == "quarterly-report-q3.pdf"


def test_make_filename_strips_leading_dot() -> None:
    assert make_filename("notes", ".txt") == "notes.txt"


def test_make_filename_empty_title() -> None:
    assert make_filename("!!!", "md") == "untitled.md"
