# 0004: Compare with an equal-size random sample of happy reviews

**Status:** accepted, 0.1.0

## Context

There are 4,101 "would not recommend" reviews and 18,540 "would recommend" reviews with text. Turning all of them into sentence numbers would take nearly three times longer, and the complaint model would learn mostly from happy sentences.

## Decision

Use all unhappy reviews and a random sample of the same number of happy reviews (fixed random seed). Report each theme as a share within each group.

## Trade-off

- Shares within each group are valid. The mix across the two groups is not the real one, so the page never reports an overall share of all reviews.
- A different random sample could move the happy shares slightly. With 4,100 happy reviews, a share of 9.2% has a 95% margin of about ±0.9 points.
