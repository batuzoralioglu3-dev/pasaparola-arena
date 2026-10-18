from pathlib import Path
import json,re,unicodedata,collections
root=Path(__file__).resolve().parent.parent
base=root/'content/base.json'
if not base.exists():
 s=(root/'dist/index.html').read_text();base.write_text(re.search(r'const QUESTION_BANK=(.*?);\n',s).group(1))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower().replace('ı','i')) if c.isalnum())
learn={}
for l in (root/'content/english-learning.tsv').read_text().splitlines():
 w,t,e,et=l.split('|');assert w.lower() not in learn,w;learn[w.lower()]=(t,e,et)
rows=[]
for q in json.loads(base.read_text()):
 level,kind,letter,word,clue=q
 if level=='tr':
  if word in ['Lügat','Jurnal']:level='tr-medium'
  else:level='tr-easy'
  rows.append(dict(level=level,kind=kind,letter=letter,word=word,clue=clue))
 else:
  t,e,et=learn[word.lower()];rows.append(dict(level=level,kind='word' if word=='scupper' else kind,letter=letter,word=word,clue=clue,tr=t,example=e,exampleTr=et))
for line in (root/'content/english-new.tsv').read_text().splitlines():
 level,kind,word,clue,t,e,et=line.split('|');rows.append(dict(level=level,kind=kind,letter=word[0].upper(),word=word,clue=clue,tr=t,example=e,exampleTr=et))
for line in (root/'content/turkish-new.tsv').read_text().splitlines():
 level,word,clue=line.split('|');word=word.replace('Zerafet','Zarafet').replace('Iztırap','Istırap');letter=word[0].replace('i','İ').replace('ı','I').upper();rows.append(dict(level='tr-'+level,kind='word',letter=letter,word=word,clue=clue))
# Preserve one question per answer within each level; use the newly curated clue on collisions.
unique={}
for q in rows:unique[(q['level'],norm(q['word']))]=q
rows=list(unique.values())
example_fixes={
 'sycophant':('He is a sycophant who flatters every manager.','O, her yöneticiyi öven bir dalkavuktur.'),
 'vicissitude':('Losing his job was one more vicissitude in his life.','İşini kaybetmesi hayatındaki bir başka talih değişikliğiydi.'),
 'contain':('This box can contain all your old letters.','Bu kutu bütün eski mektuplarını alabilir.'),
 'search':('We need to search the room for the missing key.','Kayıp anahtarı bulmak için odayı aramamız gerekiyor.')
}
for q in rows:
 if not q['level'].startswith('tr-') and q['word'] in example_fixes:q['example'],q['exampleTr']=example_fixes[q['word']]
 if q['word']=='Pazar':q['clue']='Haftanın cumartesiden sonra gelen günü.'
 if q['word']=='shoes':q['clue']='A pair of these covers your feet outdoors. Give the plural form.';q['tr']='Dışarıda iki ayağa giyilen eşya. Çoğul biçimini yaz.'
 if q['word']=='grocery':q['clue']='A word used before store to describe a shop selling food and household goods.'
 if q['level'].startswith('tr-'):
  assert q['letter'] in 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ',q
 else:assert all(q.get(k) for k in ['tr','example','exampleTr']),q

print('Total:',len(rows),'Levels:',dict(collections.Counter(q['level'] for q in rows)))



# Arena 5: preserve every existing answer and all its level memberships, then
# enrich it and append individually authored vocabulary assets.
asset_paths=[root/f'content/enrichment/{lang}-{i}-output.json' for lang in ['tr','en'] for i in range(3)]
assert all(p.exists() for p in asset_paths), "All six vocabulary assets are required"
if all(p.exists() for p in asset_paths):
 def wordkey(q):
  tr=q['level'].startswith('tr-')
  return ('tr' if tr else 'en',q['word'].translate(str.maketrans({'I':'ı','İ':'i'})).lower() if tr else q['word'].lower())
 grouped={}
 for q in rows:
  k=wordkey(q)
  if k in grouped:
   if q['level'] not in grouped[k]['levels']:grouped[k]['levels'].append(q['level'])
  else:grouped[k]={**q,'levels':[q['level']]}
 for path in asset_paths:
  asset=json.loads(path.read_text());lang=path.name.split('-')[0]
  for item in asset['existing']:
   key=wordkey({'level':'tr-easy' if lang=='tr' else 'a1','word':item['word']})
   assert key in grouped,(path,key)
   grouped[key].update({k:v for k,v in item.items() if k!='word'})
  for item in asset['new']:
   key=wordkey(item)
   assert key not in grouped,('Duplicate new word',path,key)
   grouped[key]={**item,'levels':[item['level']]}
 rows=list(grouped.values())
 counts=collections.Counter('tr' if q['level'].startswith('tr-') else 'en' for q in rows)
 assert counts=={'tr':1500,'en':2500},counts
 for q in rows:
  assert q.get('clue') and q.get('example') and isinstance(q.get('synonyms'),list),q
  assert all(isinstance(x,str) and x.strip() for x in q['synonyms']),q
  if q['level'].startswith('tr-'):assert q.get('en'),q
  else:assert q.get('tr') and q.get('exampleTr'),q
  assert q['word'].lower() not in [s.lower() for s in q['synonyms']],q
 (root/'public/questions.js').write_text('const QUESTION_BANK='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n')
 (root/'content/questions.json').write_text(json.dumps(rows,ensure_ascii=False))
 print('Arena 5 unique vocabulary:',dict(counts),'Total:',len(rows))
