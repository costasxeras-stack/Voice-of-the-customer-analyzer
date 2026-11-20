# 0003: A local text model, no paid AI calls

**Status:** accepted, 0.1.0

## Context

A large language model could read every review and tag its complaints. For 8,201 reviews that means thousands of paid calls, and my n8n AI credits appeared to run low during the Catalog Attribute Extractor run on the same day.

## Decision

Use a small sentence model that runs locally (Universal Sentence Encoder through EnergeticAI) to turn sentences into numbers, then a simple trained model and grouping. A language model (Claude) was used once, during the build, to name the 12 groups from their top words and example sentences. The names are labelled as Claude's on the page and in the docs.

## Trade-off

- A language model would probably tag complaints more cleanly, and could split mixed groups by cause.
- The local approach costs nothing per run, takes about 15 minutes on a laptop, keeps review text on the machine, and gives the same output every time.
