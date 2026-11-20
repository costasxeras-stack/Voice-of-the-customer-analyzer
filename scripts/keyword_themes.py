"""Keyword baseline: the theme list a PM would write before reading the reviews.
Written before the AI grouping was run, and not changed afterwards.
A review counts for a theme if any of its words or phrases appears in the review text."""
import re

THEMES = {
    "Fit and sizing": ["runs small", "runs large", "runs big", "too small", "too big", "too tight", "too loose", "size up", "size down",
                       "sizing", "fit", "fits", "snug", "baggy", "boxy", "tight", "loose"],
    "Length": ["too long", "too short", "length", "hem", "cropped"],
    "Fabric and quality": ["fabric", "material", "quality", "cheap", "thin", "flimsy", "pilling", "pills", "itchy", "scratchy", "wrinkle"],
    "See-through": ["see-through", "see through", "sheer", "transparent", "lining", "lined"],
    "Color": ["color", "colour", "faded", "shade"],
    "Looks different from the photo": ["picture", "photo", "model", "online", "pictured"],
    "Price": ["price", "expensive", "overpriced", "worth", "money"],
    "Washing and care": ["wash", "washed", "washing", "shrunk", "shrink", "dry clean"],
    "Construction and defects": ["seam", "stitching", "hole", "tear", "ripped", "zipper", "button", "unraveling"],
}
PATTERNS = {t: re.compile(r"(?<![a-z])(" + "|".join(re.escape(w) for w in ws) + r")(?![a-z])") for t, ws in THEMES.items()}


def themes_of(text):
    t = str(text).lower()
    return [name for name, p in PATTERNS.items() if p.search(t)]
