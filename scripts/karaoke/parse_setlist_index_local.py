import argparse, hashlib, json, re
from datetime import date
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

def clean(s):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", s))).strip()

def seconds(s):
    out=0
    for part in s.split(":"):
        out=out*60+int(part)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path, default=Path("data/karaoke/normalized"))
    ap.add_argument("--metadata", type=Path, default=Path("data/karaoke/source-metadata/setlist-index.json"))
    args=ap.parse_args()
    raw=args.input.read_bytes()
    html=raw.decode("utf-8", "replace")
    source="https://setlist.kibunya.org/channel/@OtonoseKanade/"
    broadcasts=[]; performances=[]
    for chunk in html.split('<div class="video-card')[1:]:
        head=re.search(r'<h3[^>]*>\s*<a href="([^"]+)"[^>]*>(.*?)</a>',chunk,re.S)
        dm=re.search(r"配信日:\s*(\d{4})/(\d{1,2})/(\d{1,2})",chunk)
        if not head or not dm: continue
        y,m,d=dm.groups(); url=head.group(1); bid=parse_qs(urlparse(url).query).get("v",[""])[0]
        if not bid: continue
        card={"id":bid,"title":clean(head.group(2)),"date":f"{int(y):04d}-{int(m):02d}-{int(d):02d}","youtubeUrl":url,"broadcastUrl":url,"sources":[source],"status":"source-confirmed"}
        broadcasts.append(card)
        for order,part in enumerate(chunk.split('<div class="song-row')[1:],1):
            tm=re.search(r"font-mono[^>]*>\s*([^<]+?)\s*</div>",part,re.S)
            sm=re.search(r"font-bold text-gray-800[^>]*>\s*([^<]+?)\s*</div>",part,re.S)
            am=re.search(r"text-xs text-gray-500[^>]*>\s*([^<]*?)\s*</div>",part,re.S)
            um=re.search(r'<a href="(https://youtube\.com/watch\?v=[^"]+&t=\d+s)"',part)
            if not tm or not sm: continue
            ts=clean(tm.group(1)); start=seconds(ts); title=clean(sm.group(1)); artist=clean(am.group(1)) if am else None
            performances.append({"id":f"{bid}-{order:02d}","broadcastId":bid,"date":card["date"],"order":order,"title":title,"normalizedTitle":title,"artist":artist,"timestamp":ts,"timestampSeconds":start,"sourceUrl":um.group(1) if um else f"{url}&t={start}s","sources":[source],"evidence":[{"type":"setlist-index","url":source}],"status":"source-confirmed"})
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/"broadcasts.json").write_text(json.dumps({"schemaVersion":1,"broadcasts":broadcasts},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (args.output/"performances.json").write_text(json.dumps({"schemaVersion":1,"source":str(args.input),"performances":performances},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    meta={"schemaVersion":1,"sourceUrl":source,"observedAt":date.today().isoformat(),"extractionMode":"local-html","rawFileUploaded":False,"sourceSnapshotName":args.input.name,"sourceSnapshotSha256":hashlib.sha256(raw).hexdigest(),"broadcastCount":len(broadcasts),"performanceCount":len(performances),"dateRange":{"earliestObserved":min(x["date"] for x in broadcasts),"latestObserved":max(x["date"] for x in broadcasts)},"parserVersion":"local-block-v2"}
    args.metadata.parent.mkdir(parents=True,exist_ok=True)
    args.metadata.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(meta,ensure_ascii=False))

if __name__=="__main__": main()


