#!/usr/bin/env python3
"""Tests for email_list_cleaner.py"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from email_list_cleaner import (
    normalize_email, validate_email, split_name,
    normalize_organization, deduplicate,
)
import pandas as pd

passed = 0
failed = 0

def test(name, actual, expected):
    global passed, failed
    if actual == expected:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        print(f"  ✗ {name}")
        print(f"    Expected: {expected}")
        print(f"    Got:      {actual}")


print("\n--- normalize_email ---")
test("basic cleanup", normalize_email("  John@GMAIL.COM  "), "john@gmail.com")
test("strips mailto", normalize_email("mailto:test@test.com"), "test@test.com")
test("returns None for missing @", normalize_email("not-an-email"), None)
test("returns None for NaN", normalize_email(float('nan')), None)
test("returns None for empty after @", normalize_email("user@"), None)

print("\n--- validate_email ---")
test("valid email", validate_email("user@example.com"), "valid")
test("missing email", validate_email(None), "missing")
test("typo .cmo", validate_email("user@gmail.cmo"), "possible_typo:.cmo->.com")
test("disposable", validate_email("user@mailinator.com"), "disposable")
test("invalid format", validate_email("user@"), "invalid_format")

print("\n--- split_name ---")
test("simple name", split_name("Maria Santos"), ("Maria", "Santos"))
test("with Dr.", split_name("Dr. Maria Santos"), ("Maria", "Santos"))
test("with Prof.", split_name("Prof. James Wilson"), ("James", "Wilson"))
test("with Jr.", split_name("Robert Kim Jr."), ("Robert", "Kim"))
test("with III", split_name("Ben Taylor III"), ("Ben", "Taylor"))
test("with PhD", split_name("Amanda Foster PhD"), ("Amanda", "Foster"))
test("with Mrs.", split_name("Mrs. Rachel Adams"), ("Rachel", "Adams"))
test("None input", split_name(None), (None, None))
test("empty string", split_name(""), (None, None))

print("\n--- normalize_organization ---")
test("TAMU", normalize_organization("TAMU"), "Texas A&M University")
test("Texas A & M", normalize_organization("Texas A & M"), "Texas A&M University")
test("CU Boulder", normalize_organization("CU Boulder"), "University of Colorado Boulder")
test("CSU", normalize_organization("CSU"), "Colorado State University")
test("Notre Dame", normalize_organization("Notre Dame"), "University of Notre Dame")
test("already correct", normalize_organization("Harvard University"), "Harvard University")
test("None input", normalize_organization(None), None)
test("custom map", normalize_organization("MIT", {"mit": "Massachusetts Institute of Technology"}),
     "Massachusetts Institute of Technology")

print("\n--- deduplicate ---")
df = pd.DataFrame({
    'email_clean': ['a@b.com', 'a@b.com', 'c@d.com'],
    'name': ['Alice', None, 'Charlie'],
    'org': ['Acme', 'Acme Inc', 'Beta'],
})
unique, dupes = deduplicate(df)
test("keeps most complete", unique.iloc[0]['name'], 'Alice')
test("unique count", len(unique), 2)
test("dupe count", len(dupes), 1)

print(f"\n{'─' * 40}")
print(f"  {passed} passed, {failed} failed\n")
sys.exit(1 if failed else 0)
