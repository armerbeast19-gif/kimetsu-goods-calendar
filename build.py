import json, sys
url = sys.argv[1] if len(sys.argv) > 1 else ""
t = open("template.html", encoding="utf-8").read()
d = json.load(open("data.json", encoding="utf-8"))
emb = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
t = t.replace("/*__EMBED__*/null", emb).replace("__DATA_URL__", url)
open("kimetsu-calendar.html", "w", encoding="utf-8").write(t)
print("ok", len(t))
