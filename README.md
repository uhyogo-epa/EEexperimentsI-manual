# 電気電子工学実験 I 手引書（Experiments on Electrical and Electronic Engineering I）

## フォルダ構成

```
main.tex                        全テーマをまとめた1冊（配布用。表紙・目次・注意事項付き）
00_report_guide.tex             レポートの書き方（単体で確認するとき用）
00_least_squares.tex            最小二乗法（単体で確認するとき用）
01_tester.tex ～ 05_voltagewave.tex
                                テーマ単体の確認用（中身は1行 \input するだけ）
01_tester_worksheet.tex         直流回路 ワークシート（学生配布用）
01_tester_worksheet_answer.tex  同 実施例版（TA の予備測定データ入り）
02_oscilloscope_worksheet.tex   オシロスコープ 記録用紙（学生配布用）
03_diode_worksheet.tex          ダイオード課題（学生配布用）
03_diode_worksheet_answer.tex   同 解答例版
04_transistor_worksheet.tex     トランジスタ ワークシート（学生配布用）
05_voltagewave_worksheet.tex    電圧波の観測 ワークシート（学生配布用）
experimentguide.cls             共通スタイル（取りまとめ担当のみ編集）
latexmkrc                       LuaLaTeX でコンパイルする設定
contents/
  00_introduction/
    purpose_body.tex            ← 実験の目的（手引書のはじめに入る）
    introduction_body.tex       ← 注意事項（実験の目的の次に入る）
    report_guide_body.tex       ← レポートの書き方（注意事項の次に入る）
    least_squares_body.tex      ← 最小二乗法（レポートの書き方の次に入る）
  01_tester/
    tester_body.tex             ← 本文（担当の先生が編集）
    figures/                    ← 図
    changes_from_original.md    ← Word 原本からの変更点と要確認事項
  02_oscilloscope/
    oscilloscope_body.tex
    oscilloscope_worksheet_body.tex ← 記録用紙本文
    figures/
  03_diode/
    diode_body.tex
    diode_worksheet_body.tex    ← 課題シート本文
    figures/
  04_transistor/                （同様：transistor_body.tex，transistor_worksheet_body.tex，figures/）
  05_voltagewave/               （同様：voltagewave_body.tex，voltagewave_worksheet_body.tex，figures/）
```
各フォルダに changes_from_original.md（原本からの変更点）があります。

テーマの順番（ファイル名の番号）：
01 テスター → 02 オシロスコープ → 03 ダイオード → 04 トランジスタ → 05 電圧波

## 編集するのはどこか

- 各テーマの担当の先生は **`contents/<番号>_<テーマ>/` の中だけ** を編集してください。
- 見た目（色・余白・見出しの形など）を変えたいときは，本文で直接指定せず取りまとめ担当に相談してください（`experimentguide.cls` で全テーマ一括で変更します）。

## Overleaf での使い方

1. 左上メニュー → **Compiler** を `LuaLaTeX` にする（`latexmkrc` でも指定済み）
2. 同じメニュー → **Main document** で，確認したいファイルを選ぶ
   - 自分のテーマだけ確認：`03_diode.tex` など
   - 全体を確認：`main.tex`
3. `contents/<番号>_<テーマ>/<テーマ>_body.tex` を編集して Recompile

※ Overleaf ではメインファイルをプロジェクト最上位に置く必要があるため，テーマ単体用のファイルも最上位にあります。

## ローカルでの一括コンパイル（取りまとめ担当向け）

`EEexperimentsI-manual` で引数なしの `latexmk` を実行すると，`latexmkrc` の `@default_files` に並べたファイルがまとめてコンパイルされます。テーマやワークシートを追加したら，`main.tex` の `\input` と `latexmkrc` の `@default_files` の両方に1行足してください。中間ファイルの削除は `latexmk -c` です。

Overleaf では Main document に指定した1ファイルだけがコンパイルされます。

## 表紙・目次・注意事項（main.tex のみ）

- 表紙の文字は `main.tex` の冒頭で指定します。
  - `\coursename{...}`（科目名），`\courseenglish{...}`（英語名），`\academicyear{...}`（年度），`\organization{...}`（大学名など）
- 目次は自動で作られます（テーマ名のみ。PDF のしおりには節まで出ます）。
- 注意事項は `contents/00_introduction/introduction_body.tex` を編集してください。
- ページ番号は，目次と注意事項がローマ数字（i, ii），各テーマが 1 からです。

## 表記ルール

| 項目 | ルール | 例 |
|---|---|---|
| 句読点 | 全角コンマ「，」と全角まる「。」 | 電圧を測定し，記録します。 |
| 文体 | です・ます調 | ～を測定します。～してください。 |
| 単位付きの数値 | `\SI{数値}{単位}` | `\SI{100}{\ohm}`，`\SI{10}{\micro F}`，`\SI{2.00}{V}/DIV` |
| 変数・記号 | 数式モードで | `$V$`，`$R_0$` |
| 英語の併記 | 全角かっこ・全角コロンで，各単語の先頭を大文字 | `交流（AC：Alternating Current）`，`瞬時値（Instantaneous Value）` |
| 見出し | `\section`，`\subsection`，`\subsubsection`（番号は自動） | 「２.１.」などの手書き番号は付けない |
| 実験手順 | `procedure` 環境（番号付き） | |
| 強調 | 太字は `\important{}`。特に重要な部分・安全上の注意は波線 `\wave{}` | `\wave{必ず電源を外した状態で行います。}`（長い文でも行末で折り返されます） |
| 編集用のメモ | 気になる点などは `\chk{}` で青字のメモとして残す（配布前に削除） | `\chk{ここは担当の先生に確認}` |

## 図の入れ方

- 図ファイルは `contents/<番号>_<テーマ>/figures/` に置き，ファイル名はテーマ名で始める（例：`diode_rectifier.pdf`）
- ラベルは `fig:<テーマ>-○○` の形にする（1冊にまとめたときの重複防止）

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\linewidth]{diode_rectifier.pdf}
  \caption{整流回路}
  \label{fig:diode-rectifier}
\end{figure}
\cref{fig:diode-rectifier}に示すように……   % →「図 3 に示すように」
```

- 図番号は自動で振られます。本文中で「図3」と直接書かず，`\cref{ラベル}` を使ってください。「図」「表」「式」と番号の間の細い空きも自動で入ります（`図\ref{...}` と書く必要はありません）。
- 簡単な回路図は，画像の代わりに `circuitikz` で本文中に直接描けます（例：`contents/02_oscilloscope/oscilloscope_body.tex` の RC ローパスフィルタの図）。

## 課題シート（ワークシート）

- 学生が記入するものは手引書本文とは別ファイルにします（例：`diode_worksheet_body.tex`）。
- 解答は `\answer{...}` で書くと，解答例版（`*_worksheet_answer.tex`）にだけ赤字で表示されます。
- ワークシートの最後に `\freenotepage` と書くと，自由記入欄（5 mm 方眼の枠）のページが入ります。

## 原本からの変更点

各テーマのフォルダにある `changes_from_original.md` に，Word 原本から変えた点（構成・表記・図・内容の修正）と，担当の先生に確認してほしい点（チェックボックス付き）をまとめています。校正のときはまずこのファイルを確認してください。確認が済んだ項目は `- [x]` にしてください。

## 原本

Word の原本は Overleaf には置かず，取りまとめ担当のローカル（`原本wordファイル/`）で保管しています。
- 長いコラムは `\begin{column}[コラム：○○] ... \end{column}` で書くと，補足の枠と同じ見た目で，ページをまたいで分割されます。

## ウェブサイト（GitHub Pages）

- 学生用：https://uhyogo-epa.github.io/EEexperimentsI-manual/
- 教員用：https://uhyogo-epa.github.io/EEexperimentsI-manual/teacher/
  （解答例，原本からの変更点，要確認箇所＝本文中の `\chk{}` と `% TODO` コメントの一覧）

GitHub（https://github.com/uhyogo-epa/EEexperimentsI-manual）の `main` に push されると，
GitHub Actions（`.github/workflows/site.yml`）が全テーマをコンパイルし，`site/build_site.py` でページを作って公開します。
検索エンジンには載らない設定（noindex）にしてあります。

- 説明資料（スライドの PDF など）は `slides/<テーマのファイル名>/` に PDF を置くと，学生用ページのテーマ欄に自動で載ります
  （例：`slides/05_voltagewave/説明資料.pdf`）。
- Overleaf と GitHub の両方に同じ履歴を push して同期します（`git push origin main` と `git push github main`）。
