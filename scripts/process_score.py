#!/usr/bin/env python3
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

BODY=os.environ.get('ISSUE_BODY','')
ISSUE_NUMBER=int(sys.argv[1])
ISSUE_AUTHOR=sys.argv[2]
RANKING=Path('ranking.json')

if '<!-- SUPER_DDS_SCORE_V1 -->' not in BODY:
    raise SystemExit('Marcador de pontuação ausente.')

def field(label):
    m=re.search(rf'^## {re.escape(label)}\s*\n([^\n]+)',BODY,re.M)
    if not m: raise ValueError(f'Campo ausente: {label}')
    return m.group(1).strip()

def integer(label,minimum,maximum):
    raw=field(label)
    if not re.fullmatch(r'\d+',raw): raise ValueError(f'{label} inválido')
    value=int(raw)
    if not minimum<=value<=maximum: raise ValueError(f'{label} fora do limite')
    return value

player=re.sub(r'\s+',' ',field('Jogador')).upper()
if not re.fullmatch(r"[A-ZÀ-ÖØ-Ý0-9 ._'\-]{3,24}",player): raise ValueError('Nome inválido')
score=integer('Pontuação',1,99999)
time=integer('Tempo em segundos',1,86399)
coins=integer('Moedas',0,10000)
medals=integer('Medalhas',0,100)
version=field('Versão')
if not re.fullmatch(r'1\.\d+(?:\.\d+)?',version): raise ValueError('Versão inválida')

payload=json.loads(RANKING.read_text(encoding='utf-8')) if RANKING.exists() else {'schemaVersion':1,'updatedAt':None,'entries':[]}
entries=payload.get('entries',[])
now=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
new={'player':player,'score':score,'time':time,'coins':coins,'medals':medals,'version':version,'date':now,'githubUser':ISSUE_AUTHOR,'issue':ISSUE_NUMBER}
idx=next((i for i,x in enumerate(entries) if x.get('player','').upper()==player),None)
if idx is None:
    entries.append(new); action='incluído'
else:
    old=entries[idx]
    better=(score>int(old.get('score',0))) or (score==int(old.get('score',0)) and time<int(old.get('time',10**9)))
    if better: entries[idx]=new; action='atualizado'
    else: action='ignorado'; print(f'RESULT={action}',file=sys.stderr); Path(os.environ['GITHUB_OUTPUT']).write_text(f'result={action}\n',encoding='utf-8'); raise SystemExit(0)
entries.sort(key=lambda x:(-int(x['score']),int(x['time']),-int(x['coins']),x['player']))
payload={'schemaVersion':1,'updatedAt':now,'entries':entries[:100]}
RANKING.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path(os.environ['GITHUB_OUTPUT']).write_text(f'result={action}\n',encoding='utf-8')
