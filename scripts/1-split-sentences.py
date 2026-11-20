"""Step 1. Keeps reviews with text, takes every review that would not recommend the item and the same number of random
reviews that would, and splits them into sentences of 3 words or more. Writes work/sents.json as [review id, sentence].
Download the data first: work/reviews.csv (Women's E-Commerce Clothing Reviews, public domain)."""
import pandas as pd, re, json
df = pd.read_csv('work/reviews.csv'); df = df[df['Review Text'].notna()].copy()
df['rid'] = df['Unnamed: 0']
un = df[df['Recommended IND'] == 0]; ha = df[df['Recommended IND'] == 1].sample(len(un), random_state=20261120)
sents = []
for r in pd.concat([un, ha]).itertuples():
    for t in re.split(r'(?<=[.!?])\s+', str(r._5).strip()):
        t = t.strip()
        if len(t.split()) >= 3: sents.append([int(r.rid), t])
print(len(un) + len(ha), 'reviews,', len(sents), 'sentences')
json.dump(sents, open('work/sents.json', 'w'))
