"""Cache only public RSS headlines; LOGBOOK personal entries never leave the device."""
import datetime as dt, email.utils, html, json, re, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
 ('hyperallergic','Hyperallergic','https://hyperallergic.com/','https://hyperallergic.com/feed/'),
 ('filmmaker','Filmmaker','https://filmmakermagazine.com/','https://filmmakermagazine.com/feed/'),
 ('nieman','Nieman Lab','https://www.niemanlab.org/','https://www.niemanlab.org/feed/'),
 ('artnews','ARTnews','https://www.artnews.com/','https://www.artnews.com/feed/'),
 ('verge','The Verge','https://www.theverge.com/','https://www.theverge.com/rss/index.xml'),
]
NS={'a':'http://www.w3.org/2005/Atom'}
def text_of(el,fields):
 for name in fields:
  node=el.find(name,NS)
  if node is not None:
   result=''.join(node.itertext()).strip()
   if result:return result
 return ''
def strip(s):
 return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s or ''))).strip()
def dateval(raw):
 try:return email.utils.parsedate_to_datetime(raw).astimezone(dt.timezone.utc).isoformat()
 except (ValueError,TypeError):
  try:return dt.datetime.fromisoformat(raw.replace('Z','+00:00')).isoformat()
  except (ValueError,AttributeError):return ''
def parse(data,sid):
 root=ET.fromstring(data)
 nodes=root.findall('.//item') or root.findall('.//a:entry',NS)
 out=[]
 for el in nodes[:12]:
  title=strip(text_of(el,['title','a:title']))
  link=text_of(el,['link'])
  if not link:
   ln=el.find('a:link',NS)
   link=ln.attrib.get('href','') if ln is not None else ''
  if not title or not link.startswith(('http://','https://')):continue
  out.append(dict(sourceId=sid,title=title[:180],url=link,summary=strip(text_of(el,['description','summary','a:summary','a:content']))[:220],published=dateval(text_of(el,['pubDate','a:published','a:updated']))))
 return out
def main():
 dest=ROOT/'feeds.json'
 previous=json.loads(dest.read_text()) if dest.exists() else {'items':[]}
 old={}
 for item in previous.get('items',[]):old.setdefault(item.get('sourceId'),[]).append(item)
 items=[]
 for sid,name,site,url in SOURCES:
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'LOGBOOK RSS reader/0.1','Accept':'application/xml,application/rss+xml,*/*'})
   with urllib.request.urlopen(req,timeout=18) as response:raw=response.read(2_000_000)
   fresh=parse(raw,sid)
   print(name,len(fresh))
   items.extend(fresh or old.get(sid,[]))
  except Exception as exc:
   print(name,'unavailable',exc)
   items.extend(old.get(sid,[]))
 items.sort(key=lambda x:x.get('published') or '',reverse=True)
 dest.write_text(json.dumps({'updatedAt':dt.datetime.now(dt.timezone.utc).isoformat(),'sources':[{'id':i,'name':n,'site':s} for i,n,s,_ in SOURCES],'items':items[:65]},ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
