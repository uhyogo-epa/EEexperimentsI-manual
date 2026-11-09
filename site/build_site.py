#!/usr/bin/env python3
"""手引書・ワークシートの PDF からウェブサイト（学生用トップ＋教員用ページ）を作る。

使い方（latexmk で PDF を作ったあと，リポジトリの最上位で実行）:
    python3 site/build_site.py --out _site

- 学生用トップ  : _site/index.html
- 教員用ページ  : _site/teacher/index.html
- PDF           : _site/pdf/
説明資料（スライドの PDF など）は slides/<テーマのファイル名>/ に置くと自動で載る。
  例: slides/05_voltagewave/電圧波_説明.pdf
"""
import argparse
import datetime
import html
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 共通（はじめに）の資料。テーマは NN_<名前>.tex から自動で拾う
INTRO = [
    ("00_report_guide", "レポートの書き方"),
    ("00_least_squares", "最小二乗法"),
]
INTRO_DIR = "contents/00_introduction"


def experiment_title(base: str) -> str:
    body = ROOT / "contents" / base / f"{base.split('_', 1)[1]}_body.tex"
    if body.exists():
        m = re.search(r"\\experimenttitle\{(.+?)\}\s*$", body.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    return base


def themes():
    out = []
    for tex in sorted(ROOT.glob("[0-9][0-9]_*.tex")):
        base = tex.stem
        if base.startswith("00_") or "_worksheet" in base:
            continue
        out.append(base)
    return out


def balanced(text: str, start: int) -> str:
    """text[start] が '{' のとき，対応する '}' までの中身を返す"""
    depth, i = 0, start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
        i += 1
    return text[start + 1:]


def todo_items(content_dir: Path):
    """\\chk{...} と TODO コメントを (ファイル, 行, 種類, 内容) で返す"""
    items = []
    for tex in sorted(content_dir.glob("*.tex")):
        lines = tex.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines, 1):
            m = re.search(r"%\s*TODO\s*(?:\(([^)]*)\))?\s*[:：]?\s*(.*)$", line)
            if m:
                kind = f"TODO（{m.group(1)}）" if m.group(1) else "TODO"
                items.append((tex, n, kind, m.group(2)))
            code = re.split(r"(?<!\\)%", line, maxsplit=1)[0]
            for m in re.finditer(r"\\chk\{", code):
                items.append((tex, n, "要確認", balanced(code, m.end() - 1)))
    return items


def tex_to_text(s: str) -> str:
    s = re.sub(r"\\SI\{([^}]*)\}\{([^}]*)\}", r"\1 \2", s)
    s = re.sub(r"\\SIrange\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", r"\1〜\2 \3", s)
    s = s.replace("\\ohm", "Ω").replace("\\,", " ")
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^]]*\])?", "", s)
    return s.replace("{", "").replace("}", "").strip()


CSS = """
:root{--bg:#fbfaf7;--card:#fff;--fg:#1f2328;--muted:#5d646e;--line:#e3e0d8;--accent:#1f4e79;--accent-bg:#e8eef5;--warn:#9a3412;--warn-bg:#fdf0e7}
@media (prefers-color-scheme:dark){:root{--bg:#16181c;--card:#1e2126;--fg:#e6e6e6;--muted:#a0a7b0;--line:#30353c;--accent:#8db7e3;--accent-bg:#1f2a37;--warn:#f0a070;--warn-bg:#33231a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic",sans-serif;line-height:1.7}
.wrap{max-width:880px;margin:0 auto;padding:32px 16px 64px}
header h1{font-size:1.6rem;margin:0 0 4px}
header p{margin:0;color:var(--muted);font-size:.92rem}
h2{font-size:1.1rem;margin:36px 0 12px;padding-bottom:6px;border-bottom:2px solid var(--line)}
.hero{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:20px;padding:16px;background:var(--accent-bg);border-radius:10px}
.hero .t{flex:1 1 240px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card h3{font-size:1rem;margin:0 0 10px}
.card .no{color:var(--muted);font-size:.8rem;display:block}
.links{display:flex;flex-wrap:wrap;gap:6px}
a{color:var(--accent)}
a.btn{display:inline-block;text-decoration:none;font-size:.88rem;padding:4px 12px;border-radius:999px;border:1px solid var(--accent);color:var(--accent);background:transparent}
a.btn:hover{background:var(--accent);color:var(--card)}
a.btn.primary{background:var(--accent);color:var(--card)}
.none{color:var(--muted);font-size:.85rem}
table{width:100%;border-collapse:collapse;font-size:.88rem;margin-top:8px}
th,td{text-align:left;padding:5px 8px;border-top:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;white-space:nowrap}
.tag{display:inline-block;font-size:.75rem;padding:0 6px;border-radius:4px;background:var(--warn-bg);color:var(--warn);white-space:nowrap}
details summary{cursor:pointer;color:var(--muted);font-size:.88rem;margin-top:8px}
footer{margin-top:48px;color:var(--muted);font-size:.8rem}
"""


def page(title: str, body: str, root_rel: str) -> str:
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{root_rel}style.css">
</head><body><div class="wrap">
{body}
</div></body></html>
"""


def btn(href: str, label: str, primary=False) -> str:
    cls = "btn primary" if primary else "btn"
    return f'<a class="{cls}" href="{html.escape(href)}">{html.escape(label)}</a>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site")
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "pdf").mkdir(parents=True)
    (out / "teacher").mkdir()

    repo = os.environ.get("GITHUB_REPOSITORY", "uhyogo-epa/EEexperimentsI-manual")
    sha = os.environ.get("GITHUB_SHA", "")
    ref = sha or "main"
    blob = f"https://github.com/{repo}/blob/{ref}"
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    stamp = now.strftime("%Y-%m-%d %H:%M") + (f"（{sha[:7]}）" if sha else "")

    def pdf(name: str):
        """PDF があれば _site/pdf/ にコピーして相対パスを返す"""
        src = ROOT / name
        if not src.exists():
            return None
        shutil.copy2(src, out / "pdf" / name)
        return f"pdf/{name}"

    def slides(base: str):
        d = ROOT / "slides" / base
        res = []
        if d.is_dir():
            (out / "slides" / base).mkdir(parents=True, exist_ok=True)
            for f in sorted(d.glob("*.pdf")):
                shutil.copy2(f, out / "slides" / base / f.name)
                res.append((f"slides/{base}/{f.name}", f.stem))
        return res

    # ---------------- 学生用トップ ----------------
    s = []
    s.append("<header><h1>電気電子工学実験 I</h1><p>兵庫県立大学 工学部 電気電子工学コース</p></header>")
    main_pdf = pdf("main.pdf")
    if main_pdf:
        s.append(f'<div class="hero"><span class="t">手引書（全テーマ・表紙と目次つき）</span>{btn(main_pdf, "PDF を開く", True)}</div>')

    s.append("<h2>はじめに読むもの</h2><div class=\"grid\">")
    for base, title in INTRO:
        p = pdf(f"{base}.pdf")
        links = btn(p, "手引書") if p else '<span class="none">準備中</span>'
        s.append(f'<div class="card"><h3>{html.escape(title)}</h3><div class="links">{links}</div></div>')
    s.append("</div>")

    s.append("<h2>実験テーマ</h2><div class=\"grid\">")
    theme_list = themes()
    for base in theme_list:
        title = experiment_title(base)
        links = []
        for name, label in [(f"{base}.pdf", "手引書"), (f"{base}_worksheet.pdf", "ワークシート")]:
            p = pdf(name)
            if p:
                links.append(btn(p, label))
        for href, stem in slides(base):
            links.append(btn(href, f"説明資料：{stem}"))
        no = base.split("_", 1)[0]
        s.append(f'<div class="card"><span class="no">テーマ {int(no)}</span><h3>{html.escape(title)}</h3>'
                 f'<div class="links">{"".join(links) or "<span class=none>準備中</span>"}</div></div>')
    s.append("</div>")
    s.append(f'<footer>更新：{stamp}　|　<a href="teacher/">教員用</a></footer>')
    (out / "index.html").write_text(page("電気電子工学実験 I", "\n".join(s), ""), encoding="utf-8")

    # ---------------- 教員用 ----------------
    t = []
    t.append("<header><h1>電気電子工学実験 I（教員用）</h1>"
             "<p>解答例・原本からの変更点・要確認箇所（本文中の青字 <code>\\chk{}</code> と TODO コメント）</p></header>")
    t.append(f'<p><a href="../">← 学生用ページ</a>　|　<a href="https://github.com/{repo}">ソース（GitHub）</a></p>')

    entries = [("00_introduction", "共通（はじめに・レポート・最小二乗法）", INTRO_DIR, [])]
    for base in theme_list:
        entries.append((base, f"テーマ {int(base[:2])}：{experiment_title(base)}", f"contents/{base}", [base]))

    for key, title, cdir, bases in entries:
        t.append(f"<h2>{html.escape(title)}</h2>")
        links = []
        for b in bases:
            p = pdf(f"{b}_worksheet_answer.pdf")
            if p:
                links.append(btn("../" + p, "ワークシート解答例"))
        changes = ROOT / cdir / "changes_from_original.md"
        if changes.exists():
            links.append(btn(f"{blob}/{cdir}/changes_from_original.md", "原本からの変更点"))
        links.append(btn(f"https://github.com/{repo}/tree/{ref}/{cdir}", "ソース"))
        t.append(f'<div class="links">{"".join(links)}</div>')

        items = todo_items(ROOT / cdir)
        if items:
            rows = []
            for tex, n, kind, text in items:
                rel = tex.relative_to(ROOT).as_posix()
                rows.append(f'<tr><td><span class="tag">{kind}</span></td>'
                            f'<td>{html.escape(tex_to_text(text)) or "（内容なし）"}</td>'
                            f'<td><a href="{blob}/{rel}#L{n}">{html.escape(tex.name)}:{n}</a></td></tr>')
            t.append(f'<details><summary>要確認箇所 {len(items)} 件</summary><table>'
                     f'<tr><th>種類</th><th>内容</th><th>場所</th></tr>{"".join(rows)}</table></details>')
        else:
            t.append('<p class="none">要確認箇所はありません。</p>')
    t.append(f"<footer>更新：{stamp}</footer>")
    (out / "teacher" / "index.html").write_text(page("電気電子工学実験 I（教員用）", "\n".join(t), "../"), encoding="utf-8")

    (out / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"site written to {out}")


if __name__ == "__main__":
    main()
