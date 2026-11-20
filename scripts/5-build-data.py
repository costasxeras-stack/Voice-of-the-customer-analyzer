import json, numpy as np, pandas as pd, random, sys
sys.path.insert(0,'scripts')
from keyword_themes import themes_of, THEMES
S=json.load(open('work/sents.json')); oof=np.load('work/oof.npy'); th=json.load(open('work/themes_k12.json'))
df=pd.read_csv('work/reviews.csv'); df=df[df['Review Text'].notna()]
meta={int(r['Unnamed: 0']):r for _,r in df.iterrows()}
# Group names were written by Claude during the build, from each group's top words and example sentences.
NAMES={1:('fit','Fit','cause','Too tight or too loose in one area (waist, chest, shoulders, hips), or too big, small, short or long overall. Two groups merged.'),
 9:('fit','Fit','cause',''),
 10:('fabric','Fabric and quality','cause','Fabric feels cheap, stiff, thin, fuzzy or sheer, or is poorly made.'),
 2:('shape','No shape, or not like the photo','cause','Shapeless or unflattering, or looks different from the model photo.'),
 8:('color','Color','cause','The color looks different, dull or does not suit.'),
 0:('care','Washing and wear','cause','Shrinks, gets holes or tears after washing or a few wears.'),
 7:('value','Value and ordering','cause','Not worth the price, or the wrong size was ordered.'),
 6:('dress','Dresses that did not work','mixed','Mixed complaints about dresses: fit, fabric and look.'),
 3:('top','Tops and sweaters that did not work','mixed','Mixed complaints about shirts, sweaters and jackets.'),
 11:('disappointed','General disappointment','outcome','"I was disappointed" with no specific reason in that sentence.'),
 4:('returned','Sent back','outcome','"I had to return it" or "it is going back".'),
 5:('returned','Sent back','outcome','')}
rid_all=np.array([s[0] for s in S]); idx=np.array(th['idx']); lab=np.array(th['lab'])
sample_ids=set(rid_all.tolist())
un=[r for r in sample_ids if meta[r]['Recommended IND']==0]; ha=[r for r in sample_ids if meta[r]['Recommended IND']==1]
members={}  # theme key -> {review ids}
sents={}
for i,c in zip(idx,lab):
    k=NAMES[c][0]; members.setdefault(k,set()).add(int(rid_all[i])); sents.setdefault(k,[]).append(int(i))
deps=['Tops','Dresses','Bottoms','Intimate','Jackets']
themes=[]; rnd=random.Random(20261120); seen={}
for c,(k,name,kind,desc) in NAMES.items():
    if k in seen: continue
    seen[k]=1; m=members[k]
    u=sum(1 for r in un if r in m); h=sum(1 for r in ha if r in m)
    by={d:dict(n=sum(1 for r in un if meta[r]['Department Name']==d), k=sum(1 for r in un if r in m and meta[r]['Department Name']==d)) for d in deps}
    ex=rnd.sample(sents[k],min(12,len(sents[k])))
    themes.append(dict(key=k,name=name,kind=kind,desc=desc,unhappy=u,happy=h,sentences=len(sents[k]),by_dept=by,
      examples=[dict(t=S[i][1],id=S[i][0],rating=int(meta[S[i][0]]['Rating']),dept=str(meta[S[i][0]]['Department Name']),rec=int(meta[S[i][0]]['Recommended IND'])) for i in ex]))
fit=members['fit']
combined=dict(fit=dict(unhappy=sum(1 for r in un if r in fit),happy=sum(1 for r in ha if r in fit)))
# keyword baseline on the same sample and on all reviews
kw=[]
for t in THEMES:
    u=sum(1 for r in un if t in themes_of(meta[r]['Review Text'])); h=sum(1 for r in ha if t in themes_of(meta[r]['Review Text']))
    kw.append(dict(name=t,unhappy=u,happy=h))
allrev=dict(reviews=int(len(df)),unhappy=int((df['Recommended IND']==0).sum()))
out=dict(n_unhappy=len(un),n_happy=len(ha),sentences=len(S),complaint_sentences=int(len(idx)),threshold=0.7,
  model=dict(sentence_auc=0.786,review_auc=0.864),themes=sorted(themes,key=lambda t:-t['unhappy']),combined=combined,keywords=kw,all=allrev)
json.dump(out,open('data/themes.json','w'),ensure_ascii=False)
for t in out['themes']: print(f"{t['name']:38} {t['kind']:8} unhappy {t['unhappy']/len(un)*100:5.1f}% happy {t['happy']/len(ha)*100:5.1f}%  x{(t['unhappy']/len(un))/(t['happy']/len(ha)):.1f}")
print('fit combined', combined, len(un), len(ha))
for k in kw: print(f"KW {k['name']:32} {k['unhappy']/len(un)*100:5.1f}% {k['happy']/len(ha)*100:5.1f}%")
