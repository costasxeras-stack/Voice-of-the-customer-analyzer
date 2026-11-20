import json, numpy as np, pandas as pd, re, collections
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
S=json.load(open('work/sents.json')); X=np.fromfile('work/emb.f32',dtype='<f4').reshape(len(S),512)
X/=np.linalg.norm(X,axis=1,keepdims=True)
df=pd.read_csv('work/reviews.csv'); rec=dict(zip(df['Unnamed: 0'],df['Recommended IND']))
K=int(__import__('sys').argv[1])
km=KMeans(K,n_init=5,random_state=7).fit(X); lab=km.labels_
rid=np.array([s[0] for s in S]); txt=[s[1] for s in S]
un_ids={r for r in set(rid) if rec[r]==0}; ha_ids={r for r in set(rid) if rec[r]==1}
cv=CountVectorizer(stop_words='english',ngram_range=(1,2),min_df=5); M=cv.fit_transform(txt); voc=np.array(cv.get_feature_names_out())
tot=np.asarray(M.sum(0)).ravel()+1
out=[]
for c in range(K):
    idx=np.where(lab==c)[0]; rs=set(rid[idx])
    u=len(rs&un_ids)/len(un_ids); h=len(rs&ha_ids)/len(ha_ids)
    tf=np.asarray(M[idx].sum(0)).ravel(); score=tf/tot*np.log(1+tf)
    terms=list(voc[np.argsort(-score)[:10]])
    d=X[idx]@km.cluster_centers_[c]/np.linalg.norm(km.cluster_centers_[c]); rep=[txt[i] for i in idx[np.argsort(-d)[:6]]]
    out.append(dict(c=c,n=len(idx),u=u,h=h,lift=u/max(h,1e-9),terms=terms,rep=rep))
np.save(f'work/labels_k{K}.npy',lab)
for o in sorted(out,key=lambda o:-(o['u']-o['h'])):
    print(f"#{o['c']} n={o['n']} unhappy {o['u']*100:.1f}% happy {o['h']*100:.1f}% lift {o['lift']:.2f} | {', '.join(o['terms'][:8])}")
    for r in o['rep'][:3]: print('     -',r[:110])
