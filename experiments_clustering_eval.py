"""Clustering experiment: embed concepts (embeddinggemma), evaluate KMeans vs
Agglomerative vs HDBSCAN over a k-range with 3 internal metrics. For the docs."""
import json, httpx, numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, HDBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
OLL="http://localhost:11434/api/embed"; M="embeddinggemma:latest"
ont=json.load(open("out/ontology.json")); nodes=ont["nodes"]
texts=[f"{n['name']['en']}. {n['definition']['en']}" for n in nodes]
vecs=[]
with httpx.Client(timeout=180) as c:
    for i in range(0,len(texts),32):
        vecs.extend(c.post(OLL,json={"model":M,"input":texts[i:i+32]}).json()["embeddings"])
X=np.asarray(vecs,dtype=np.float32); Xn=X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-9)
np.save("build/embeddings_embgemma.npy", X)
print(f"EMB dims={X.shape[1]} n={X.shape[0]}", flush=True)
rows=[]
for k in range(6,17):
    for name,mdl in (("KMeans",KMeans(k,n_init=10,random_state=0)),
                     ("Agglomerative(ward)",AgglomerativeClustering(k))):
        lab=mdl.fit_predict(Xn)
        rows.append((name,k,silhouette_score(Xn,lab,metric="cosine"),
                     davies_bouldin_score(Xn,lab),calinski_harabasz_score(Xn,lab)))
for mcs in (8,12,16,20):
    lab=HDBSCAN(min_cluster_size=mcs).fit_predict(Xn)
    nclu=len(set(lab))-(1 if -1 in lab else 0); noise=int((lab==-1).sum())
    try: sil=silhouette_score(Xn[lab!=-1],lab[lab!=-1],metric="cosine") if nclu>1 else float('nan')
    except: sil=float('nan')
    rows.append((f"HDBSCAN(mcs={mcs})",nclu,sil,float('nan'),float('nan'),noise))
print("METHOD | k | silhouette↑ | davies_bouldin↓ | calinski_harabasz↑ | noise", flush=True)
for r in rows:
    extra=f" | noise={r[5]}" if len(r)>5 else ""
    print(f"{r[0]:22s} | {r[1]:2d} | {r[2]:.4f} | {r[3]:.3f} | {r[4]:.1f}{extra}", flush=True)
print("EVAL_DONE", flush=True)
