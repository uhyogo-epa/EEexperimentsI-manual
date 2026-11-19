#!/usr/bin/env python3
"""手引書・ワークシート・説明資料から，教員の情報共有用ウェブページを作る。

使い方（latexmk で PDF を作ったあと，リポジトリの最上位で実行）:
    python3 site/build_site.py --out _site

各回の資料は，SESSIONS の key と同じ名前のフォルダに置くと自動で載る。
  slides/<key>/    説明資料。同じ名前の .pptx と .pdf は1行にまとまる
  handouts/<key>/  配布物（Word の様式など）
  例: slides/01_tester/直流回路_説明.pptx，slides/01_tester/直流回路_説明.pdf
"""
import argparse
import datetime
import html
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

# スケジュール（配布資料 261005 より）。key があり，資料がある回にタブができる
SESSIONS = [
    ("10月5日", "ガイダンス", None),
    ("10月12日", "ロボットプログラミング 1", None),
    ("10月19日", "ロボットプログラミング 2", None),
    ("10月26日", "ロボットプログラミング 3", None),
    ("11月2日", "ロボットプログラミング 4", None),
    ("11月9日", "ロボットプログラミング 5", None),
    ("11月16日", "ロボットプログラミング 6（プレゼン・コンテスト）", None),
    ("11月23日", "実験レポート作成方法", "00_guidance"),
    ("11月30日", "直流回路", "01_tester"),
    ("12月7日", "交流回路", "02_oscilloscope"),
    ("12月14日", "実験レポート確認", "00_report_check"),
    ("12月21日", "ダイオードを用いた電子回路", "03_diode"),
    ("1月18日", "トランジスタを用いた電子回路", "04_transistor"),
    ("1月21日", "電圧波の観測", "05_voltagewave"),
    ("1月25日", "到達目標の確認・総括", "00_summary"),
]

# 手引書の共通部分を載せる回
EXTRA_MANUALS = {
    "00_guidance": [("00_report_guide", "手引書：レポートの書き方"), ("00_least_squares", "手引書：最小二乗法")],
}

CSS = """
:root{--bg:#fbfaf7;--card:#fff;--fg:#1f2328;--muted:#5d646e;--line:#e3e0d8;--accent:#1f4e79;--accent-bg:#e8eef5}
@media (prefers-color-scheme:dark){:root{--bg:#16181c;--card:#1e2126;--fg:#e6e6e6;--muted:#a0a7b0;--line:#30353c;--accent:#8db7e3;--accent-bg:#1f2a37}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic",sans-serif;line-height:1.7}
.wrap{max-width:1120px;margin:0 auto;padding:28px 16px 48px}
header h1{font-size:1.5rem;margin:0}
header p{margin:0;color:var(--muted);font-size:.9rem}
nav{display:flex;gap:2px;margin:20px 0 24px;border-bottom:2px solid var(--line);overflow-x:auto}
nav a{flex:none;padding:7px 14px 6px;color:var(--muted);text-decoration:none;font-size:.9rem;line-height:1.35;border-bottom:3px solid transparent;margin-bottom:-2px;text-align:center}
nav a small{display:block;font-size:.74rem}
nav a:hover{color:var(--fg)}
nav a[aria-selected=true]{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}
h2{font-size:1.25rem;margin:0 0 14px}
h2 small{color:var(--muted);font-size:.9rem;font-weight:400;margin-right:10px}
h3{font-size:1rem;margin:28px 0 8px}
a{color:var(--accent)}
.js .panel{display:none}.js .panel.on{display:block}
.panel{margin-bottom:32px}
table{width:100%;border-collapse:collapse;font-size:.93rem}
th,td{text-align:left;padding:7px 10px;border-top:1px solid var(--line);vertical-align:middle}
tr:first-child th,tr:first-child td{border-top:0}
th{color:var(--muted);font-weight:600;white-space:nowrap;width:7em}
.docs{background:var(--card);border:1px solid var(--line);border-radius:8px}
.docs tr.on{background:var(--accent-bg)}
.acts{text-align:right;white-space:nowrap;width:1%}
.btn{display:inline-block;font:inherit;font-size:.82rem;line-height:1.5;padding:2px 11px;margin-left:4px;border-radius:6px;border:1px solid var(--accent);color:var(--accent);background:transparent;text-decoration:none;cursor:pointer}
.btn:hover{background:var(--accent);color:var(--card)}
.none{color:var(--muted);font-size:.88rem}
.viewer{margin-top:14px}
.viewer iframe{display:block;width:100%;height:78vh;min-height:460px;border:1px solid var(--line);border-radius:8px;background:#525659}
.viewer iframe[hidden]{display:none}
footer{margin-top:40px;color:var(--muted);font-size:.8rem}
@media (max-width:640px){th,td{padding:7px 8px}th{width:5.5em}.list tr{display:block;padding:6px 8px;border-top:1px solid var(--line)}.list tr:first-child{border-top:0}.list td{display:block;border:0;padding:2px 0}.list .acts{width:auto;text-align:left;white-space:normal}.list .btn{margin:2px 4px 2px 0}.viewer iframe{height:62vh}}
"""

JS = """
(function(){
  var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
  function load(p){var f=p.querySelector('iframe');if(f&&!f.hidden&&!f.getAttribute('src'))f.src=f.dataset.src;}
  function show(id,focus){
    var t=tabs.filter(function(x){return x.getAttribute('href')==='#'+id;})[0]||tabs[0];
    tabs.forEach(function(x){
      var on=x===t,p=document.getElementById(x.getAttribute('aria-controls'));
      x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;p.classList.toggle('on',on);if(on)load(p);
    });
    t.scrollIntoView({block:'nearest',inline:'nearest'});if(focus)t.focus();
  }
  addEventListener('hashchange',function(){show(location.hash.slice(1));scrollTo(0,0);});
  document.querySelector('nav').addEventListener('keydown',function(e){
    var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!d)return;
    var i=tabs.indexOf(document.activeElement);if(i<0)return;e.preventDefault();
    location.hash=tabs[(i+d+tabs.length)%tabs.length].getAttribute('href');
    tabs[(i+d+tabs.length)%tabs.length].focus();
  });
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-view]');if(!b)return;
    var p=b.closest('.panel'),f=p.querySelector('iframe');
    f.hidden=false;f.src=b.dataset.view;f.title=b.dataset.name;
    p.querySelectorAll('tr.on').forEach(function(r){r.classList.remove('on');});
    b.closest('tr').classList.add('on');
    f.scrollIntoView({behavior:'smooth',block:'start'});
  });
  show(location.hash.slice(1));
})();
"""


def experiment_title(base: str) -> str:
    body = ROOT / "contents" / base / f"{base.split('_', 1)[1]}_body.tex"
    if body.exists():
        m = re.search(r"\\experimenttitle\{(.+?)\}\s*$", body.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    return base


def esc(s: str) -> str:
    return html.escape(s, quote=True)


class Site:
    def __init__(self, out: Path):
        self.out = out

    def copy(self, src: Path, rel: str) -> str:
        dst = self.out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return quote(rel)

    def built_pdf(self, base: str, label: str):
        src = ROOT / f"{base}.pdf"
        if not src.exists():
            return None
        return {"label": label, "pdf": self.copy(src, f"pdf/{base}.pdf"), "files": []}

    def folder(self, kind: str, key: str, prefix: str):
        """slides/ や handouts/ のファイルを，拡張子を除いた名前ごとにまとめる"""
        d = ROOT / kind / key
        groups = {}
        if d.is_dir():
            for f in sorted(p for p in d.iterdir() if p.is_file() and not p.name.startswith(".")):
                groups.setdefault(f.stem, []).append(f)
        docs = []
        for stem, files in groups.items():
            doc = {"label": f"{prefix}：{stem}", "pdf": None, "files": []}
            for f in files:
                href = self.copy(f, f"{kind}/{key}/{f.name}")
                ext = f.suffix.lower().lstrip(".")
                if ext == "pdf":
                    doc["pdf"] = href
                else:
                    doc["files"].append((ext.upper(), href, f.name))
            docs.append(doc)
        return docs


def doc_rows(docs, selected):
    rows = []
    for d in docs:
        acts = []
        if d["pdf"]:
            acts.append(f'<button class="btn" type="button" data-view="{esc(d["pdf"])}" data-name="{esc(d["label"])}">表示</button>')
            acts.append(f'<a class="btn" href="{esc(d["pdf"])}">PDF</a>')
        for ext, href, name in d["files"]:
            acts.append(f'<a class="btn" href="{esc(href)}" download="{esc(name)}">{esc(ext)}</a>')
        cls = ' class="on"' if d is selected else ""
        rows.append(f'<tr{cls}><td>{esc(d["label"])}</td><td class="acts">{"".join(acts)}</td></tr>')
    return "".join(rows)


def docs_block(docs, missing_slides=False):
    """資料の一覧と，PDF の埋め込み表示を作る。説明資料があれば最初に表示する"""
    selected = next((d for d in docs if d["pdf"]), None)
    rows = doc_rows(docs, selected)
    if missing_slides:
        rows = '<tr><td class="none">説明資料：未登録</td><td></td></tr>' + rows
    s = f'<table class="docs list">{rows}</table>'
    if selected:
        s += (f'<div class="viewer"><iframe data-src="{esc(selected["pdf"])}" '
              f'title="{esc(selected["label"])}" loading="lazy"></iframe></div>')
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site")
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    site = Site(out)

    repo = os.environ.get("GITHUB_REPOSITORY", "uhyogo-epa/EEexperimentsI-manual")
    sha = os.environ.get("GITHUB_SHA", "")
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    stamp = now.strftime("%Y-%m-%d %H:%M") + (f"（{sha[:7]}）" if sha else "")

    tabs, panels, rows = [], [], []
    for date, title, key in SESSIONS:
        docs, is_theme = [], False
        if key:
            is_theme = (ROOT / f"{key}.tex").exists()
            slides = site.folder("slides", key, "説明資料")
            docs += slides
            if is_theme:
                for base, label in [(key, "手引書"), (f"{key}_worksheet", "ワークシート"),
                                    (f"{key}_worksheet_answer", "ワークシート解答例")]:
                    d = site.built_pdf(base, label)
                    if d:
                        docs.append(d)
            for base, label in EXTRA_MANUALS.get(key, []):
                d = site.built_pdf(base, label)
                if d:
                    docs.append(d)
            docs += site.folder("handouts", key, "配布物")
        if docs:
            tid = key.replace("_", "-")
            short = title.replace("を用いた電子回路", "").replace("実験レポート作成方法", "レポート作成方法")
            tabs.append(f'<a role="tab" id="tab-{tid}" href="#{tid}" aria-controls="p-{tid}" aria-selected="false">'
                        f'<small>{esc(date)}</small>{esc(short)}</a>')
            heading = experiment_title(key) if is_theme else title
            panels.append(f'<section class="panel" id="p-{tid}" role="tabpanel" aria-labelledby="tab-{tid}">'
                          f'<h2><small>{esc(date)}</small>{esc(heading)}</h2>'
                          f'{docs_block(docs, is_theme and not slides)}</section>')
            cell = f'<a href="#{tid}">{esc(title)}</a>'
        else:
            cell = esc(title)
        rows.append(f"<tr><th>{esc(date)}</th><td>{cell}</td></tr>")

    overview = []
    d = site.built_pdf("main", "手引書（全テーマ・表紙と目次つき）")
    if d:
        overview.append(f'<table class="docs list">{doc_rows([d], None)}</table><div class="viewer"><iframe data-src="{esc(d["pdf"])}" title="{esc(d["label"])}" hidden></iframe></div>')
    overview.append(f'<h3>スケジュール</h3><table class="docs">{"".join(rows)}</table>')
    tabs.insert(0, '<a role="tab" id="tab-schedule" href="#schedule" aria-controls="p-schedule" aria-selected="false">'
                   '<small>全体</small>スケジュール</a>')
    panels.insert(0, '<section class="panel" id="p-schedule" role="tabpanel" aria-labelledby="tab-schedule">'
                     f'<h2>手引書とスケジュール</h2>{"".join(overview)}</section>')

    title = "電気電子工学実験 I 教員用資料"
    page = f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title}</title>
<script>document.documentElement.className='js'</script>
<link rel="stylesheet" href="style.css">
</head><body><div class="wrap">
<header><h1>{title}</h1><p>兵庫県立大学 工学部 電気電子工学コース</p></header>
<nav role="tablist" aria-label="実施回">{"".join(tabs)}</nav>
{"".join(panels)}
<footer>更新：{stamp}　|　<a href="https://github.com/{repo}">GitHub</a></footer>
</div><script src="site.js"></script></body></html>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    (out / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (out / "site.js").write_text(JS.strip() + "\n", encoding="utf-8")

    # 以前の教員用ページの URL からも開けるようにする
    (out / "teacher").mkdir()
    (out / "teacher" / "index.html").write_text(
        '<!doctype html><html lang="ja"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0; url=../">'
        f'<title>{title}</title></head><body><a href="../">{title}</a></body></html>\n', encoding="utf-8")
    (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"site written to {out}")


if __name__ == "__main__":
    main()
