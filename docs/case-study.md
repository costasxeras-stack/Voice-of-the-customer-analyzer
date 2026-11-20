# Case study: Voice of the Customer Analyzer

## The question

Shoppers who would not recommend a clothing item: what are they complaining about, and what should the team fix first? And would the usual first approach, counting keywords, give the same answer?

## Data

Women's E-Commerce Clothing Reviews: 23,486 reviews from one online clothing shop, public domain. 22,641 have text. Every reviewer gave a star rating and said whether they would recommend the item. 4,101 said they would not.

The "would recommend" answer is the outcome. It is cleaner than the star rating: 1,653 three-star reviews would not recommend and 1,170 would.

## Approach

1. **Keyword list first.** Before running any AI, I wrote the nine themes a PM would expect (fit and sizing, length, fabric and quality, see-through, color, looks different from the photo, price, washing and care, construction and defects) with their keywords. It was not changed afterwards.
2. **Sample.** All 4,101 "would not recommend" reviews and 4,101 random "would recommend" reviews, split into 38,066 sentences. One happy review had no sentence of three words or more, so 4,100 happy reviews remain.
3. **Sentence meaning.** Each sentence was turned into numbers with a small text model that runs locally (Universal Sentence Encoder through EnergeticAI). No paid AI calls.
4. **First attempt.** Grouping all sentences found topics, not complaints. "Fabric" mixed "beautiful fabric" with "the fabric is a total miss". The output is kept in `docs/data/first-try-all-sentences-k20.txt` (decision 0001).
5. **Find complaint sentences.** A simple model learned which sentences come from "would not recommend" reviews. Each sentence was scored by a model trained on other reviews only (5 rounds, split by review).
6. **Group the complaints.** The 9,274 sentences scoring 0.7 or more were grouped into 12 groups. Claude named each group from its top words and example sentences during the build. Two fit groups were merged, and two "sent back" groups were merged, giving 10 themes.
7. **Rank.** For each theme: the share of unhappy reviews with at least one of its sentences, next to the same share for happy reviews.

## Findings

### 1. Fit is the biggest cause of "would not recommend" (confirmed)

| Theme | Type | Would not recommend | Would recommend | Ratio |
|---|---|---|---|---|
| Fit | Cause | 31.5% | 9.2% | 3.4× |
| Fabric and quality | Cause | 21.5% | 4.2% | 5.2× |
| Sent back | Outcome | 16.8% | 1.8% | 9.4× |
| General disappointment | Outcome | 16.5% | 3.4% | 4.9× |
| No shape, or not like the photo | Cause | 14.9% | 3.9% | 3.8× |
| Dresses that did not work | Mixed | 14.6% | 4.0% | 3.6× |
| Tops and sweaters that did not work | Mixed | 14.0% | 3.2% | 4.3× |
| Value and ordering | Cause | 12.6% | 4.3% | 2.9× |
| Color | Cause | 10.2% | 2.1% | 4.8× |
| Washing and wear | Cause | 9.5% | 2.6% | 3.7× |

"Outcome" themes say what happened (returned, disappointed) but not why. "Mixed" themes are complaints about one product type with several causes. Neither tells a team what to change, so the results page hides them by default.

Fit leads in every department, from 28% of unhappy reviews for jackets to 33% for dresses. Fabric and quality is highest for jackets (27%).

### 2. Keyword counting hides the biggest problem (confirmed)

| Keyword theme | Would not recommend | Would recommend | Ratio |
|---|---|---|---|
| Washing and care | 6.2% | 3.5% | 1.77× |
| Construction and defects | 8.5% | 5.0% | 1.70× |
| Looks different from the photo | 25.0% | 16.4% | 1.52× |
| Price | 10.3% | 6.9% | 1.51× |
| Fabric and quality | 51.0% | 36.2% | 1.41× |
| See-through | 8.8% | 7.7% | 1.15× |
| Fit and sizing | 47.2% | 51.1% | 0.92× |
| Color | 16.3% | 18.5% | 0.88× |
| Length | 12.5% | 16.5% | 0.76× |

Fit words appear in more happy reviews than unhappy ones, because happy shoppers write "fits perfectly" and "true to size". Ranked by ratio, keywords put fit seventh of nine. Ranked by raw count, it is second, but at the same level as in happy reviews, so it looks like noise. Finding the complaint sentences first is what separates the two.

### 3. Frequency and ratio answer different questions (confirmed)

Fit is the most common complaint. Fabric and quality is the most specific one: 5.2 times more common in unhappy reviews. I rank by frequency, because it is closer to how many unhappy shoppers a fix could reach, and show the ratio next to it (decision 0002).

### 4. Fit and "not like the photo" may share a fix (hypothesis)

Fit (31.5%), no shape or not like the photo (14.9%) and value and ordering, which includes ordering the wrong size (12.6%), all point at the gap between what the shopper expected and what arrived. Better size guidance and photos on more body types might reduce all three. This needs a test, for example on the products with the most fit complaints.

## How good is the complaint model?

- Sentence level: 0.786 on a 0-to-1 ranking score, where 0.5 is chance.
- Review level, using each review's most complaint-like sentence: 0.864.
- 81.5% of the sentences scoring 0.7 or more come from "would not recommend" reviews.

Happy reviews also contain complaints ("runs big but I love it"), and some sentences in each group are not complaints at all. The results page shows random sentences, not the best ones, so readers can judge.

## What I learned as a PM

- Pick an outcome first. "Would not recommend" turns a pile of text into a question with an answer.
- Count complaints, not words. The same word is praise in one review and a complaint in the next.
- Separate causes from outcomes. "I returned it" is the most specific sentence and the least useful.
- A small local model was enough. No paid AI calls were needed, so the analysis can be rerun on new reviews for free.

## Limits

- One shop, one product category, English only, no dates.
- The sample has equal numbers of happy and unhappy reviews. The shares within each group are valid, but not the overall mix of reviews.
- Reviews are cut at about 500 characters in the original data (4,714 of 22,641 reviews reach the cap), so complaints near the end of long reviews are missed.
- The 0.7 score threshold and 12 groups are my choices. The theme names are labels, and no person has checked how clean each group is.

## What I would do next

1. Have a person label 50 sentences per theme to measure how clean the groups are.
2. Rank products by fit complaints, and test better size guidance on the top ones.
3. Run the same steps on a second review source to see if the ranking holds.

## My role

I framed the question, wrote the keyword list before the analysis, chose the method and wrote the findings. Claude (Anthropic) wrote the code with me, named the groups and ran the checks.
