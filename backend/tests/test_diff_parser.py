from app.services.diff_parser import DiffParser

SAMPLE_DIFF = """diff --git a/src/main.py b/src/main.py
index 1234567..89abcdef 100644
--- a/src/main.py
+++ b/src/main.py
@@ -10,4 +10,6 @@ def calculate_total(items):
     total = 0
     for item in items:
         total += item.price
+    if total < 0:
+        raise ValueError("Total cannot be negative")
     return total
"""


def test_diff_parser_valid_patch():
    parsed = DiffParser.parse_patch(SAMPLE_DIFF)
    assert parsed.total_files == 1
    assert parsed.files[0].file_path == "src/main.py"
    assert parsed.files[0].additions_count == 2
    assert parsed.files[0].deletions_count == 0
    assert len(parsed.files[0].chunks) == 1
    assert parsed.files[0].chunks[0].new_start == 10


def test_diff_parser_empty_patch():
    parsed = DiffParser.parse_patch("")
    assert parsed.total_files == 0
    assert parsed.total_additions == 0
    assert parsed.total_deletions == 0
