import json, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
S=json.load(open('work/sents.json')); X=np.fromfile('work/emb.f32',dtype='<f4').reshape(len(S),512); X/=np.linalg.norm(X,axis=1,keepdims=True)
df=pd.read_csv('work/reviews.csv'); rec=dict(zip(df['Unnamed: 0'],df['Recommended IND']))
rid=np.array([s[0] for s in S]); y=np.array([1-rec[r] for r in rid])  # 1 = sentence from a not-recommended review
oof=np.zeros(len(S))
for tr,te in GroupKFold(5).split(X,y,rid):
    m=LogisticRegression(C=1.0,max_iter=2000).fit(X[tr],y[tr]); oof[te]=m.predict_proba(X[te])[:,1]
print('sentence AUC', round(roc_auc_score(y,oof),3))
r=pd.DataFrame({'rid':rid,'p':oof,'y':y}).groupby('rid').agg(p=('p','max'),y=('y','first'))
print('review AUC (max sentence)', round(roc_auc_score(r.y,r.p),3))
np.save('work/oof.npy',oof)
for t in [0.6,0.7,0.8]: print(t, (oof>=t).sum(), 'sentences', 'share from unhappy', round(y[oof>=t].mean(),3))
