"""Reproducible synthetic longitudinal experiment. No clinical validity implied."""
from pathlib import Path
import json, csv, hashlib, platform
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, precision_score, recall_score, f1_score, average_precision_score, roc_auc_score, brier_score_loss, confusion_matrix

ROOT=Path(__file__).parent; DIST=ROOT/'dist'; OUT=ROOT/'research'; OUT.mkdir(exist_ok=True)
NAMES=['age','bmi','hba1c','diagnosis_years','genetic_risk_marker','glucose_now','glucose_15m','glucose_30m','glucose_60m','glucose_mean_60m','glucose_std_60m','slope_30m','sleep_hours','steps_last_hour','hrv_ms','heart_rate','hour_sin','hour_cos']
STATIC=5; HORIZON=24; SEED=20261018

def patient_timeline(pid,days=8):
    r=np.random.default_rng(SEED+pid*7919); n=days*288
    p=dict(id=f'SYN-{pid:03d}',age=int(r.integers(30,71)),sex=['Female','Male'][pid%2],bmi=round(r.uniform(22,35),1),hba1c=round(r.uniform(6,9.5),1),years=int(r.integers(1,15)),gene=int(r.integers(0,3)))
    sensitivity=.65+.11*(p['bmi']-22)+.13*(p['hba1c']-6)+.12*p['gene']
    times=np.arange(n)/12; sleep=np.repeat(r.uniform(4.8,8.7,days),288)
    activity=np.maximum(0,55+45*np.sin((times-8)*np.pi/12)+r.normal(0,32,n));activity[(times%24<6)]=0
    hrv=np.clip(51-1.2*(p['bmi']-22)+2.8*(sleep-7)+r.normal(0,4,n),15,80)
    hr=np.clip(74+.12*activity-.12*hrv+r.normal(0,3,n),48,140)
    meals=np.zeros(n)
    for day in range(days):
        for hour,scale in [(8,28),(13,40),(20,35)]:
            onset=day*24+hour+r.uniform(-.7,.7);u=times-onset
            response=np.where(u>0,(np.maximum(u,0)/1.1)**2*np.exp(-np.maximum(u,0)/.7),0)
            meals+=response*scale*4.5*r.uniform(.7,1.4)*sensitivity
    baseline=95+7*(p['hba1c']-6)+.45*(p['age']-40)+.6*(p['bmi']-25)
    noise=np.zeros(n)
    for i in range(1,n): noise[i]=.85*noise[i-1]+r.normal(0,2.6)
    g=baseline+meals+6*np.sin((times-5)*np.pi/12)-2*(sleep-7)-.055*activity+noise+r.normal(0,1.5,n)
    rows=np.column_stack([np.round(g,2),np.round(sleep,2),np.round(activity,1),np.round(hrv,1),np.round(hr,1)])
    return p,rows

def feature(p,rows,i):
    past=rows[max(0,i-12):i+1,0]; valid=past[np.isfinite(past)]
    current=valid[-1] if len(valid) else 130
    def lag(k):
        a=rows[max(0,i-k-12):i-k+1,0];a=a[np.isfinite(a)];return a[-1] if len(a) else current
    t=(i%288)/12
    return np.array([p['age'],p['bmi'],p['hba1c'],p['years'],p['gene'],current,lag(3),lag(6),lag(12),np.mean(valid) if len(valid) else current,np.std(valid) if len(valid) else 0,(current-lag(6))/30,rows[i,1],np.sum(rows[max(0,i-11):i+1,2]),rows[i,3],rows[i,4],np.sin(t*np.pi/12),np.cos(t*np.pi/12)])

profiles={};streams={};features=[];targets=[];groups=[];indices=[]
for pid in range(90):
    p,z=patient_timeline(pid);profiles[pid]=p;streams[pid]=z
    for i in range(72,len(z)-HORIZON,6):
        features.append(feature(p,z,i));targets.append(z[i+HORIZON,0]);groups.append(pid);indices.append(i)
X=np.array(features);y=np.array(targets);group=np.array(groups);idx=np.array(indices)
masks={k:np.isin(group,ids) for k,ids in {'train':range(54),'validation':range(54,66),'calibration':range(66,78),'test':range(78,90)}.items()}
tr,va,ca,te=[masks[k] for k in ['train','validation','calibration','test']]

def fit(kind,x,yy):
    if kind=='Ridge fusion': model=make_pipeline(SimpleImputer(),StandardScaler(),Ridge(alpha=30))
    elif kind=='Random forest fusion': model=RandomForestRegressor(n_estimators=60,max_depth=10,min_samples_leaf=12,max_features=.85,random_state=42,n_jobs=2)
    else: model=GradientBoostingRegressor(n_estimators=100,max_depth=3,min_samples_leaf=20,learning_rate=.07,loss='huber',random_state=42)
    return model.fit(x,yy)

models={};validation=[]
for name in ['Ridge fusion','Random forest fusion','Gradient boosting fusion']:
    print('Training',name,flush=True);model=fit(name,X[tr],y[tr]);models[name]=model
    validation.append({'model':name,'mae':float(mean_absolute_error(y[va],model.predict(X[va])))})
best=min(validation,key=lambda d:d['mae'])['model'];selected=models[best]
print('Selected on validation only:',best,flush=True)
# Separate patient cohort for residual interval and probability mapping.
cal_pred=selected.predict(X[ca]);residual=np.abs(y[ca]-cal_pred);q=float(np.quantile(residual,min(1,np.ceil((len(residual)+1)*.9)/len(residual)),method='higher'))
prob=LogisticRegression(C=1e3).fit(cal_pred.reshape(-1,1),(y[ca]>180).astype(int))
# Dedicated event detection: select model and alert cutoff on validation patients only.
eligible_train=tr & (X[:,5]<=180);eligible_val=va & (X[:,5]<=180);eligible_cal=ca & (X[:,5]<=180)
event_models={
 'Logistic spike classifier':make_pipeline(StandardScaler(),LogisticRegression(C=.1,max_iter=1000,class_weight='balanced')),
 'Random forest spike classifier':RandomForestClassifier(n_estimators=80,max_depth=9,min_samples_leaf=15,max_features=.85,class_weight='balanced',random_state=42,n_jobs=2)}
event_validation=[]
for name,m in event_models.items():
    print('Training',name,flush=True);m.fit(X[eligible_train],(y[eligible_train]>180).astype(int));scores_v=m.predict_proba(X[eligible_val])[:,1];truth_v=y[eligible_val]>180
    for cutoff in np.arange(.1,.91,.025):
        decision=scores_v>=cutoff;p0=precision_score(truth_v,decision,zero_division=0);r0=recall_score(truth_v,decision,zero_division=0);f2=5*p0*r0/(4*p0+r0) if 4*p0+r0 else 0
        event_validation.append(dict(model=name,cutoff=float(cutoff),f2=float(f2),precision=float(p0),recall=float(r0)))
event_choice=max(event_validation,key=lambda row:row['f2']);event_name=event_choice['model'];event_model=event_models[event_name]
event_cal_raw=event_model.predict_proba(X[eligible_cal])[:,1]
event_cal=LogisticRegression(C=100).fit(event_cal_raw.reshape(-1,1),(y[eligible_cal]>180).astype(int))
event_cut=float(event_cal.predict_proba([[event_choice['cutoff']]])[0,1])
def probability(pred):return prob.predict_proba(np.asarray(pred).reshape(-1,1))[:,1]
def metrics(target,pred,current,probabilities=None):
    eligible=current<=180;truth=target[eligible]>180;predicted=pred[eligible]>180
    tn,fp,fn,tp=confusion_matrix(truth,predicted,labels=[False,True]).ravel()
    result=dict(mae=float(mean_absolute_error(target,pred)),rmse=float(np.sqrt(mean_squared_error(target,pred))),precision=float(precision_score(truth,predicted,zero_division=0)),recall=float(recall_score(truth,predicted,zero_division=0)),f1=float(f1_score(truth,predicted,zero_division=0)),tp=int(tp),fp=int(fp),fn=int(fn),tn=int(tn),n=len(target),eligible=int(eligible.sum()),prevalence=float(truth.mean()))
    if probabilities is not None:
        pr=probabilities[eligible];result.update(auroc=float(roc_auc_score(truth,pr)),average_precision=float(average_precision_score(truth,pr)),brier=float(brier_score_loss(truth,pr)))
    return result

predictions={name:model.predict(X[te]) for name,model in models.items()}
predictions['Persistence (last glucose)']=X[te,5]
predictions['Linear trend (30-minute slope)']=np.clip(X[te,5]+120*X[te,11],40,400)
ablations={}
for name,cols in [('EHR only',np.arange(STATIC)),('Wearables only',np.arange(STATIC,len(NAMES)))]:
    model=fit(best,X[tr][:,cols],y[tr]);pr=model.predict(X[te][:,cols]);ablations[name]=metrics(y[te],pr,X[te,5])
scores={name:metrics(y[te],pr,X[te,5],probability(pr) if name==best else None) for name,pr in predictions.items()}
event_benchmarks={}
for name,m in event_models.items():
    choice=max((r for r in event_validation if r['model']==name),key=lambda r:r['f2']);raw=m.predict_proba(X[te])[:,1];eligible=X[te,5]<=180;t=y[te][eligible]>180;decision=raw[eligible]>=choice['cutoff'];tn,fp,fn,tp=confusion_matrix(t,decision,labels=[False,True]).ravel()
    event_benchmarks[name]=dict(precision=float(precision_score(t,decision,zero_division=0)),recall=float(recall_score(t,decision,zero_division=0)),f1=float(f1_score(t,decision,zero_division=0)),tp=int(tp),fp=int(fp),fn=int(fn),tn=int(tn),auroc=float(roc_auc_score(t,raw[eligible])),average_precision=float(average_precision_score(t,raw[eligible])),validation_f2=choice['f2'],raw_cutoff=choice['cutoff'])
event_probs=event_cal.predict_proba(event_model.predict_proba(X[te])[:,1].reshape(-1,1))[:,1]
event_benchmarks[event_name]['brier']=float(brier_score_loss(y[te & (X[:,5]<=180)]>180,event_probs[X[te,5]<=180]))
pr=predictions[best];coverage=float(np.mean(np.abs(y[te]-pr)<=q))
cv=[]
for fold,(a,b) in enumerate(GroupKFold(3).split(X[tr],y[tr],group[tr])):
    print('Grouped cross validation',fold+1,flush=True);m=fit(best,X[tr][a],y[tr][a]);cv.append(float(mean_absolute_error(y[tr][b],m.predict(X[tr][b]))))
# Temporal benchmark: fit early days, test later days on training patients only; labels end before cut.
early=tr & (idx+24<5*288);late=tr & (idx>=6*288)
temporal=fit(best,X[early],y[early]);temporal_score=metrics(y[late],temporal.predict(X[late]),X[late,5])
# Stress tests perturb only currently available observations; future labels remain unchanged.
stress={}
for kind in ['30-minute CGM gap','CGM noise (SD 10 mg/dL)']:
    rows=[];r=np.random.default_rng(701)
    for pid,i in zip(group[te],idx[te]):
        z=streams[int(pid)][:i+1].copy()
        if kind.startswith('30'):z[-6:,0]=np.nan
        else:z[-13:,0]+=r.normal(0,10,min(13,len(z)))
        rows.append(feature(profiles[int(pid)],z,int(i)))
    stress[kind]=metrics(y[te],selected.predict(np.array(rows)),X[te,5])
r=np.random.default_rng(52);test_ids=np.unique(group[te]);boot=[]
for _ in range(500):
    chosen=r.choice(test_ids,len(test_ids),replace=True);positions=np.concatenate([np.flatnonzero(group[te]==v) for v in chosen]);boot.append(mean_absolute_error(y[te][positions],pr[positions]))
subgroups={}
for label,condition in [('Female',group[te]%2==0),('Male',group[te]%2==1),('Age <50',X[te,0]<50),('Age ≥50',X[te,0]>=50)]:
    subgroups[label]=metrics(y[te][condition],pr[condition],X[te,5][condition])
report=dict(seed=SEED,synthetic=True,sklearn=sklearn.__version__,numpy=np.__version__,python=platform.python_version(),selected=best,selection_rule='Lowest validation MAE; no test-set selection',event_selected=event_name,event_selection=event_choice,event_benchmarks=event_benchmarks,event_probability_cutoff=event_cut,features=NAMES,horizon_minutes=120,event='Current glucose <=180 and observed glucose >180 mg/dL exactly 120 minutes later',split={k:{'patients':len(np.unique(group[v])),'windows':int(v.sum())} for k,v in masks.items()},validation=validation,benchmarks=scores,ablations=ablations,grouped_cv_mae=cv,temporal=temporal_score,stress=stress,subgroups=subgroups,interval={'nominal':.9,'half_width':q,'test_coverage':coverage,'calibration_patients':12,'method':'Absolute residual quantile on separate calibration patients; dependent windows, no formal iid coverage guarantee'},mae_patient_bootstrap_95=np.quantile(boot,[.025,.975]).tolist(),limitations=['Synthetic physiology is not clinically validated.','Unobserved future meals and activity limit predictability.','Overlapping windows are dependent; confidence interval resamples patients.','Hypothetical genetic marker, not a real genotype association.','Event is +120-minute endpoint elevation, not any crossing within two hours.'])

def export_tree(est):
    t=est.tree_;return dict(left=t.children_left.tolist(),right=t.children_right.tolist(),feature=t.feature.tolist(),threshold=t.threshold.tolist(),value=t.value[:,0,0].tolist())
if best=='Ridge fusion':
    sc=selected[1];rr=selected[2];artifact=dict(kind='ridge',mean=sc.mean_.tolist(),scale=sc.scale_.tolist(),weights=rr.coef_.tolist(),intercept=float(rr.intercept_))
elif best.startswith('Random'):
    artifact=dict(kind='forest',trees=[export_tree(t) for t in selected.estimators_])
else:artifact=dict(kind='boosting',trees=[export_tree(t[0]) for t in selected.estimators_],initial=float(selected.init_.constant_[0,0]),rate=float(selected.learning_rate))
artifact.update(features=NAMES,selected=best,interval=q,probability={'coef':float(prob.coef_[0,0]),'intercept':float(prob.intercept_[0])})
def export_classifier(m):
    if hasattr(m,'estimators_'):
        trees=[]
        for t in m.estimators_:
            d=export_tree(t);values=t.tree_.value[:,0,:];d['value']=(values[:,1]/values.sum(axis=1)).tolist();trees.append(d)
        return dict(kind='forest',trees=trees)
    scaler=m[0];reg=m[1];return dict(kind='logistic',mean=scaler.mean_.tolist(),scale=scaler.scale_.tolist(),weights=reg.coef_[0].tolist(),intercept=float(reg.intercept_[0]))
artifact['event_model']=export_classifier(event_model);artifact['event_model'].update(name=event_name,cal_coef=float(event_cal.coef_[0,0]),cal_intercept=float(event_cal.intercept_[0]),cutoff=event_cut)
(DIST/'trained-model.json').write_text(json.dumps(artifact,separators=(',',':')))
(DIST/'benchmark.json').write_text(json.dumps(report,indent=2))
# Replay patients are selected deterministically from the held-out cohort, with no model tuning.
demo=[]
for pid,name,city in [(78,'Ananya Sharma','Pune'),(79,'Rohan Mehta','Bengaluru'),(80,'Meera Iyer','Chennai')]:
    p=profiles[pid].copy();p.update(name=name,city=city,initials=''.join(s[0] for s in name.split()))
    z=streams[pid];demo.append(dict(profile=p,readings=z.tolist(),start=288+72))
(DIST/'patients.json').write_text(json.dumps(demo,separators=(',',':')))
with (OUT/'heldout-predictions.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['patient_id','origin_tick','current_glucose','actual_glucose_plus_120','predicted_glucose_plus_120','new_spike_actual','new_spike_alert','calibrated_event_probability'])
    for pid,i,c,a,b,ep in zip(group[te],idx[te],X[te,5],y[te],pr,event_probs):writer.writerow([profiles[int(pid)]['id'],i,c,a,b,int(c<=180 and a>180),int(c<=180 and ep>=event_cut),ep])
with (OUT/'ehr.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(profiles[0]));writer.writeheader();writer.writerows(profiles.values())
with (OUT/'wearables.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['patient_id','tick_5min','glucose','sleep','steps_5min','hrv','heart_rate'])
    for pid,z in streams.items():
        for i,row in enumerate(z):writer.writerow([profiles[pid]['id'],i,*row])
audit={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [DIST/'trained-model.json',DIST/'benchmark.json',OUT/'ehr.csv',OUT/'wearables.csv',OUT/'heldout-predictions.csv']}
(OUT/'sha256.json').write_text(json.dumps(audit,indent=2));print(json.dumps({'selected':best,'test':scores[best],'interval':report['interval'],'cv':cv},indent=2),flush=True)
