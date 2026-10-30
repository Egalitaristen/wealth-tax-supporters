"""Refresh Portugal's seat chart from Parliament's complete sitting-member list.

python skill/scripts/seats_pt.py data/pt [--local downloaded-list.html]
Only exact normalized name matches are marked current. HTML changes or incomplete
lists stop the refresh before any file is changed.
"""
import argparse
import csv
import datetime
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.request import Request, urlopen

URL = 'https://www.parlamento.pt/DeputadoGP/Paginas/Deputadoslista.aspx'
PARTIES = [('L','#008b4a'),('BE','#cf252b'),('PCP','#bd1725'),('PS','#ef5a89'),('PAN','#2c9e86'),('PSD','#f28c28'),('CDS-PP','#1768b3'),('IL','#13b9ce'),('JPP','#805bb0'),('CH','#173e83')]

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c)).strip()

class Members(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.rows={}; self.active=None; self.parts=[]; self.text=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs); m=re.search(r'rptResultsByDate_ctl(\d+)_(hplNome|lblCE|lblGP)$',d.get('id',''))
        if m: self.active=(m.group(1),m.group(2),tag); self.parts=[]
    def handle_data(self,data):
        self.text.append(data)
        if self.active: self.parts.append(data)
    def handle_endtag(self,tag):
        if self.active and self.active[2]==tag:
            i,field,_=self.active; self.rows.setdefault(i,{})[field]=' '.join(''.join(self.parts).split()); self.active=None

def read_csv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); return r.fieldnames,list(r)
def write_csv(p,fields,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fields); w.writeheader(); w.writerows(rows)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('folder',type=Path); ap.add_argument('--local',type=Path); args=ap.parse_args(); p=args.folder
    raw=args.local.read_bytes() if args.local else urlopen(Request(URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
    doc=Members(); doc.feed(raw.decode('utf-8')); rows=list(doc.rows.values())
    match=re.search(r'Deputados em fun(?:ç|c)ões à data de\s*(\d{4}-\d{2}-\d{2})', ' '.join(doc.text))
    if not match or len(rows)!=230 or any(set(r)!= {'hplNome','lblCE','lblGP'} for r in rows): raise SystemExit('Incomplete official member list or missing date; nothing changed.')
    date=match.group(1); datetime.date.fromisoformat(date)
    counts={k:0 for k,_ in PARTIES}
    for r in rows:
        if r['lblGP'] not in counts: raise SystemExit('Unknown parliamentary group: '+r['lblGP'])
        counts[r['lblGP']]+=1
    af,actors=read_csv(p/'actors.csv'); pf,positions=read_csv(p/'positions.csv'); bf,bodies=read_csv(p/'bodies.csv'); sf,_=read_csv(p/'seats.csv'); gf,geo=read_csv(p/'geo_units.csv')
    byname={}
    for r in rows: byname.setdefault(norm(r['hplNome']),[]).append(r)
    regions={norm(g['name']):g for g in geo if g['level']=='region'}
    existing={(o['actor_id'],o['body_id'],o['role']):o for o in positions}
    ids=[int(o['position_id'][1:]) for o in positions if re.fullmatch(r'O\d+',o['position_id'])]; nxt=max(ids,default=0)+1
    hits=[]
    for a in actors:
        if a['kind']!='person' or a['actor_type']!='politician': continue
        found=byname.get(norm(a['name']),[])
        if len(found)!=1: continue
        r=found[0]; district=regions.get(norm(r['lblCE']))
        if not district: raise SystemExit('No region for constituency '+r['lblCE'])
        key=(a['actor_id'],'B0001','Deputy (XVII legislature)'); o=existing.get(key)
        if o is None:
            o={k:'' for k in pf}; o['position_id']=f'O{nxt:05d}'; nxt+=1; positions.append(o)
        o.update(actor_id=a['actor_id'],body_id='B0001',role=key[2],party=r['lblGP'],geo_unit_id=district['geo_unit_id'],current='y',checked=date,source_url=URL)
        a['location']='Portugal > '+district['name']; a['geo_unit_id']=district['geo_unit_id']; a['role']='Deputy, Assembleia da República'; hits.append(a['name'])
    sitting_ids={a['actor_id'] for a in actors if a['name'] in hits}
    for o in positions:
        if o['body_id']=='B0001' and o['role']=='Deputy (XVII legislature)' and o['actor_id'] not in sitting_ids: o['current']=''; o['checked']=''
    body=next(b for b in bodies if b['body_id']=='B0001'); body.update(seats='230',as_of=date,source_url=URL,seat_view='y',notes='Sitting deputies by parliamentary group on the official list; unlit seats do not imply opposition.')
    seats=[dict(seat_id=f'S{i:05d}',body_id='B0001',party=party,seats=str(counts[party]),colour=colour,order=str(i)) for i,(party,colour) in enumerate(PARTIES,1) if counts[party]]
    write_csv(p/'actors.csv',af,actors); write_csv(p/'positions.csv',pf,positions); write_csv(p/'bodies.csv',bf,bodies); write_csv(p/'seats.csv',sf,seats)
    print('Official list date:',date,'; parties:',counts,'; matched supporters:',len(hits)); print('\n'.join(hits))
if __name__=='__main__': main()
