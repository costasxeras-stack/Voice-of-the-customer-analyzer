# 0001: Find the complaint sentences first, then group them

**Status:** accepted, 0.1.0

## Context

The first attempt grouped all 38,066 sentences into 20 groups. The groups were topics: fabric, color, sizes, dresses, how to wear it. Most groups mixed praise and complaints, so their share in unhappy and happy reviews was similar. Only one group clearly leaned unhappy (specific fit problems, 31% against 10%). The output is in `docs/data/first-try-all-sentences-k20.txt`.

## Decision

Add a step before grouping. A simple model (logistic regression on the sentence numbers) learns which sentences come from "would not recommend" reviews. Each sentence is scored by a model that was trained on other reviews. Only sentences scoring 0.7 or more are grouped.

## Trade-off

- The step uses the outcome to pick sentences, so it can only find complaints that go with "would not recommend". A complaint that happy shoppers make just as often is left out. For deciding what to fix, that is the point.
- The 0.7 threshold is a choice. At 0.7, 81.5% of the selected sentences come from unhappy reviews and 9,274 sentences are kept. A higher threshold gives cleaner but fewer sentences.
