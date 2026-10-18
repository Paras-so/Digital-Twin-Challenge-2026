"""Standard-library checks: actual timeline labels, cohort separation, hashes, links."""
from pathlib import Path
import csv,json,hashlib,math
ROOT=Path(__file__).parent
def main():
    r=json.loads((ROOT/'dist/benchmark.json').read_text()); model=json.loads((ROOT/'dist/trained-model.json').read_text())
    with (ROOT/'research/ehr.csv').open() as f: ehr={p['id']:p for p in csv.DictReader(f)}
    assert len(ehr)==90
    stream={p:[] for p in ehr}
    with (ROOT/'research/wearables.csv').open() as f:
        for row in csv.DictReader(f):
            pid=row['patient_id'];i=int(row['tick_5min']);assert i==len(stream[pid]);values=[float(row[k]) for k in ['glucose','sleep','steps_5min','hrv','heart_rate']];assert all(math.isfinite(v) for v in values);stream[pid].append(values)
    assert all(len(z)==2304 for z in stream.values())
    counts={p:0 for p in ehr if 78<=int(p[-3:])<90};tp=fp=fn=tn=0;error=0;n=0
    with (ROOT/'research/heldout-predictions.csv').open() as f:
        for row in csv.DictReader(f):
            pid=row['patient_id'];i=int(row['origin_tick']);assert pid in counts;counts[pid]+=1;n+=1
            current=float(row['current_glucose']);actual=float(row['actual_glucose_plus_120']);prediction=float(row['predicted_glucose_plus_120']);risk=float(row['calibrated_event_probability'])
            assert stream[pid][i][0]==current and stream[pid][i+24][0]==actual
            truth=current<=180 and actual>180;flag=current<=180 and risk>=model['event_model']['cutoff'];assert int(row['new_spike_actual'])==truth;assert int(row['new_spike_alert'])==flag
            error+=abs(actual-prediction)
            if current<=180:
                if flag:
                    if truth: tp+=1
                    else: fp+=1
                elif truth: fn+=1
                else: tn+=1
    assert n==4416 and set(counts.values())=={368}
    s=r['event_benchmarks'][r['event_selected']];assert [tp,fp,fn,tn]==[s[k] for k in ['tp','fp','fn','tn']]
    assert abs(error/n-r['benchmarks'][r['selected']]['mae'])<1e-9
    hashes=json.loads((ROOT/'research/sha256.json').read_text())
    for filename,expected in hashes.items():
        path=(ROOT/'dist'/filename) if filename in ['trained-model.json','benchmark.json'] else (ROOT/'research'/filename)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,filename
    assert sum(v['patients'] for v in r['split'].values())==90
    assert len(r['features'])==18 and r['horizon_minutes']==120
    print(f'PASS: 90 EHR records, 207360 ordered wearable events, {n} actual future labels, all event counts and hashes.')
if __name__=='__main__':main()
