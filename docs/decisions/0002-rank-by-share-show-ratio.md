# 0002: Rank themes by how many unhappy reviews mention them, show the ratio next to it

**Status:** accepted, 0.1.0

## Context

Two numbers can rank a theme: how many unhappy reviews mention it, and how many times more common it is in unhappy reviews than in happy ones. They disagree. Fit is the most common (31.5%, 3.4×). Fabric and quality has the higher ratio (21.5%, 5.2×). "Sent back" has the highest ratio of all (9.4×) but says nothing about the cause.

## Decision

Rank by the share of unhappy reviews, and show the happy share and the ratio on every line. Hide outcome and mixed themes by default, with a switch to show them.

## Trade-off

- The share is closer to how many unhappy shoppers a fix could reach. The ratio is better at showing what is specific to unhappy shoppers.
- Showing both on each line costs some space, but lets a reader rank the other way if they prefer.
