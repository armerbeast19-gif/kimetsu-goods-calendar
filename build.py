import json, sys, html
url = sys.argv[1] if len(sys.argv) > 1 else ""
t = open("template.html", encoding="utf-8").read()
d = json.load(open("data.json", encoding="utf-8"))
try:
    c = json.load(open("config.json", encoding="utf-8"))
except FileNotFoundError:
    c = {}
e = lambda s: html.escape(str(s), quote=True)
emb = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
client = c.get("adsenseClient", "").strip()
slot = c.get("adsenseSlot", "").strip()
head = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={e(client)}" crossorigin="anonymous"></script>' if client else "")
adslot = (f'<div class="adwrap"><ins class="adsbygoogle" style="display:block" data-ad-client="{e(client)}" data-ad-slot="{e(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>' if client and slot else "")
links = [l for l in c.get("links", []) if l.get("url")]
x = c.get("xUrl", "").strip()
top = "".join(f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["label"])}</a>' for l in links)
if x: top = f'<a href="{e(x)}" target="_blank" rel="noopener">𝕏 フォロー</a>' + top
follow = ""
if x:
    follow = f'<div class="follow"><p>発売日・抽選・締切の情報を毎日Xでもお知らせしています。</p><a class="bt y" href="{e(x)}" target="_blank" rel="noopener">𝕏 {e(c.get("xLabel") or "フォローする")}</a></div>'
foot = ""
if links or x:
    items = ([f'<a href="{e(x)}" target="_blank" rel="noopener">X</a>'] if x else []) + [f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["label"])}</a>' for l in links]
    foot = "<p>" + "　｜　".join(items) + "</p>"
t = (t.replace("/*__EMBED__*/null", emb).replace("__DATA_URL__", url)
      .replace("<!--__ADSENSE_HEAD__-->", head).replace("<!--__AD_SLOT__-->", adslot)
      .replace("<!--__TOPLINKS__-->", top).replace("<!--__FOLLOW__-->", follow)
      .replace("<!--__FOOTLINKS__-->", foot))
open("kimetsu-calendar.html", "w", encoding="utf-8").write(t)
print("ok", len(t))
