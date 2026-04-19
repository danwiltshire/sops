from sops.utils.editor import _strip_comments


def test_strip_comments_removes_comment_lines():
    text = "# This is a comment\nActual content\n# Another comment\nMore content"
    assert _strip_comments(text) == "Actual content\nMore content"


def test_strip_comments_strips_surrounding_whitespace():
    text = "\n# comment\n\nActual content\n\n"
    assert _strip_comments(text) == "Actual content"


def test_strip_comments_all_comments_returns_empty():
    text = "# comment one\n# comment two"
    assert _strip_comments(text) == ""


def test_strip_comments_no_comments_unchanged():
    text = "Line one\nLine two"
    assert _strip_comments(text) == "Line one\nLine two"


def test_strip_comments_empty_string():
    assert _strip_comments("") == ""


def test_strip_comments_preserves_inline_hash():
    # A line that contains # but doesn't start with it should be kept
    text = "value: foo  # inline note"
    assert _strip_comments(text) == "value: foo  # inline note"
