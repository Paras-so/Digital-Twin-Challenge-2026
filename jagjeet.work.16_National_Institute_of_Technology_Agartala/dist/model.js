/* Inference only: parameters are trained offline by train.py. */
(function(root){
function tree(t,x){let n=0;while(t.left[n]!==-1)n=Math.fround(x[t.feature[n]])<=t.threshold[n]?t.left[n]:t.right[n];return t.value[n];}
function predict(model,x){if(model.kind==='ridge')return model.intercept+x.reduce((v,z,i)=>v+(z-model.mean[i])/model.scale[i]*model.weights[i],0);const sum=model.trees.reduce((v,t)=>v+tree(t,x),0);return model.kind==='forest'?sum/model.trees.length:model.initial+model.rate*sum;}
function features(p,rows,i){const past=rows.slice(Math.max(0,i-12),i+1).map(r=>r[0]).filter(Number.isFinite),g=past.at(-1)??130;
function lag(k){return rows.slice(Math.max(0,i-k-12),i-k+1).map(r=>r[0]).filter(Number.isFinite).at(-1)??g;}
const mean=past.length?past.reduce((a,b)=>a+b,0)/past.length:g,std=past.length?Math.sqrt(past.reduce((s,z)=>s+(z-mean)**2,0)/past.length):0,h=(i%288)/12;
return [p.age,p.bmi,p.hba1c,p.years,p.gene,g,lag(3),lag(6),lag(12),mean,std,(g-lag(6))/30,rows[i][1],rows.slice(Math.max(0,i-11),i+1).reduce((a,r)=>a+r[2],0),rows[i][3],rows[i][4],Math.sin(h*Math.PI/12),Math.cos(h*Math.PI/12)];}
function snapshot(patient,i,quality='complete'){const rows=patient.readings.slice(0,i+1).map(r=>r.slice());if(quality==='gap')for(let j=Math.max(0,i-5);j<=i;j++)rows[j][0]=null;if(quality==='noise')for(let j=Math.max(0,i-12);j<=i;j++)rows[j][0]+=10*Math.sin(j*13.31);return {x:features(patient.profile,rows,i),rows};}
function probability(model,x){const e=model.event_model;let raw;if(e.kind==='logistic'){const z=e.intercept+x.reduce((v,z,i)=>v+(z-e.mean[i])/e.scale[i]*e.weights[i],0);raw=1/(1+Math.exp(-z));}else raw=predict(e,x);const z=e.cal_coef*raw+e.cal_intercept;return 1/(1+Math.exp(-z));}
root.TwinModel={predict,features,snapshot,probability};
})(typeof window!=='undefined'?window:globalThis);
