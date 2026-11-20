import json, numpy as np, pandas as pd, sys
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
S=json.load(open('work/sents.json')); X=np.fromfile('work/emb.f32',dtype='<f4').reshape(len(S),512); X/=np.linalg.norm(X,axis=1,keepdims=True)
oof=np.load('work/oof.npy'); df=pd.read_csv('work/reviews.csv'); rec=dict(zip(df['Unnamed: 0'],df['Recommended IND']))
K=int(sys.argv[1]); T=0.7
idx=np.where(oof>=T)[0]; rid=np.array([s[0] for s in S]); txt=[s[1] for s in S]
km=KMeans(K,n_init=10,random_state=7).fit(X[idx]); lab=km.labels_
un={r for r in set(rid) if rec[r]==0}; ha={r for r in set(rid) if rec[r]==1}
cv=CountVectorizer(stop_words='english',ngram_range=(1,2),min_df=4); M=cv.fit_transform([txt[i] for i in idx]); voc=np.array(cv.get_feature_names_out()); tot=np.asarray(M.sum(0)).ravel()+1
res=[]
for c in range(K):
    j=np.where(lab==c)[0]; rs=set(rid[idx[j]]); u=len(rs&un)/len(un); h=len(rs&ha)/len(ha)
    tf=np.asarray(M[j].sum(0)).ravel(); terms=list(voc[np.argsort(-(tf/tot*np.log(1+tf)))[:9]])
    cen=km.cluster_centers_[c]/np.linalg.norm(km.cluster_centers_[c]); d=X[idx[j]]@cen
    res.append(dict(c=c,n=len(j),u=u,h=h,terms=terms,rep=[txt[idx[j[k]]] for k in np.argsort(-d)[:8]]))
json.dump(dict(idx=idx.tolist(),lab=lab.tolist()),open(f'work/themes_k{K}.json','w'))
for o in sorted(res,key=lambda o:-o['u']):
    print(f"#{o['c']} n={o['n']} unhappy {o['u']*100:.1f}% happy {o['h']*100:.1f}% | {', '.join(o['terms'])}")
    for r in o['rep'][:5]: print('     -',r[:120])
