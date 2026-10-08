# LuaLaTeX でコンパイル（ローカル・Overleaf 共通）
$pdf_mode = 4;
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

# ローカルで引数なしの `latexmk` を実行したときに一括コンパイルする対象
# （Overleaf は Main document を指定して呼ぶので，この設定は影響しない）
# テーマを追加したらここにも1行足してください。
@default_files = (
  'main.tex',
  '00_report_guide.tex',
  '01_tester.tex',
  '01_tester_worksheet.tex',
  '01_tester_worksheet_answer.tex',
  '02_oscilloscope.tex',
  '02_oscilloscope_worksheet.tex',
  '03_diode.tex',
  '03_diode_worksheet.tex',
  '03_diode_worksheet_answer.tex',
  '04_transistor.tex',
  '04_transistor_worksheet.tex',
  '05_voltagewave.tex',
  '05_voltagewave_worksheet.tex',
);
