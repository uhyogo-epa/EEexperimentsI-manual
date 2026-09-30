% experimentguide.cls
% Laboratory manual class
% Recommended engine: LuaLaTeX
% Version: 0.2 (2026-09-29)

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{experimentguide}[2026/09/29 v0.2 Laboratory manual class]

% ------------------------------------------------------------
% Options
% ------------------------------------------------------------
\newif\ifeg@instructor
\eg@instructorfalse

\DeclareOption{student}{\eg@instructorfalse}
\DeclareOption{instructor}{\eg@instructortrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{jlreq}}
\ProcessOptions\relax

% ------------------------------------------------------------
% Base class
% ------------------------------------------------------------
\LoadClass[
  paper=a4,
  fontsize=11pt,
  line_length=42zw,
  number_of_lines=38,
  hanging_punctuation
]{jlreq}

% ------------------------------------------------------------
% Packages
% ------------------------------------------------------------
\RequirePackage{iftex}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{siunitx}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{enumitem}
\RequirePackage{tcolorbox}
\RequirePackage[normalem]{ulem}
\RequirePackage{fancyhdr}
\RequirePackage{comment}
\RequirePackage{hyperref}
\RequirePackage{caption}
\RequirePackage{tikz}

\tcbuselibrary{breakable,skins}

% ------------------------------------------------------------
% Japanese font setup
% ------------------------------------------------------------
\ifLuaTeX
  \RequirePackage{luatexja-fontspec}
  \setmainjfont{HaranoAjiMincho}
  \setsansjfont{HaranoAjiGothic}
\fi

% ------------------------------------------------------------
% Basic layout
% ------------------------------------------------------------
\setlength{\parindent}{1\zw}
\setlength{\parskip}{0.20\baselineskip}
\setlength{\headheight}{16pt}

% ------------------------------------------------------------
% Colors
% ------------------------------------------------------------
\definecolor{EGMain}{RGB}{30,70,115}
\definecolor{EGSub}{RGB}{235,241,247}
\definecolor{EGWarn}{RGB}{150,55,45}
\definecolor{EGWarnBG}{RGB}{250,242,240}
\definecolor{EGGray}{gray}{0.35}

% ------------------------------------------------------------
% Metadata
% ------------------------------------------------------------
\newcommand{\eg@coursename}{電気電子工学実験 I}
\newcommand{\eg@experimentname}{}
\newcommand{\eg@experimentnumber}{}

\newcommand{\coursename}[1]{\renewcommand{\eg@coursename}{#1}}
\newcommand{\experimentnumber}[1]{\renewcommand{\eg@experimentnumber}{#1}}

% 表紙用（main.tex で指定）
\newcommand{\eg@courseenglish}{}
\newcommand{\eg@academicyear}{}
\newcommand{\eg@organization}{}
\newcommand{\eg@documenttitle}{実験手引書}
\newcommand{\courseenglish}[1]{\renewcommand{\eg@courseenglish}{#1}}
\newcommand{\academicyear}[1]{\renewcommand{\eg@academicyear}{#1}}
\newcommand{\organization}[1]{\renewcommand{\eg@organization}{#1}}
\newcommand{\documenttitle}[1]{\renewcommand{\eg@documenttitle}{#1}}

% ------------------------------------------------------------
% Experiment title
% ------------------------------------------------------------
% テーマごとに節・図・表・式の番号を 1 から振り直す
% （main.tex で全テーマを1冊にまとめても番号やリンクが重複しないようにする）
\newcounter{eg@experiment}
\AtBeginDocument{%
  \renewcommand{\theHsection}{\arabic{eg@experiment}.\arabic{section}}%
  \renewcommand{\theHfigure}{\arabic{eg@experiment}.\arabic{figure}}%
  \renewcommand{\theHtable}{\arabic{eg@experiment}.\arabic{table}}%
  \renewcommand{\theHequation}{\arabic{eg@experiment}.\arabic{equation}}%
}

% タイトルと下線（テーマの見出し・前付けの見出しで共通）
\newcommand{\eg@titleblock}[1]{%
  \renewcommand{\eg@experimentname}{#1}%
  \markboth{#1}{#1}%
  \thispagestyle{fancy}%
  \vspace*{0.2\baselineskip}%
  % 字下げなしで左端をそろえ，タイトルを線に近づけ，線と本文の間は少しあける
  \begingroup
    \setlength{\parskip}{0pt}%
    \noindent{\sffamily\gtfamily
      \ifx\eg@experimentnumber\empty\else
        {\large\bfseries\color{EGMain}\eg@experimentnumber\quad}%
      \fi
      {\LARGE\bfseries #1}}\par
    % 行送りによる空きを無効にし，タイトルの下端から線までを直接指定
    \nointerlineskip\vskip 5pt
    \noindent{\color{EGMain}\rule{\linewidth}{1.2pt}}\par
  \endgroup
  \vspace{0.4\baselineskip}%
}

% 各テーマの見出し（番号をリセットし，目次にテーマ名を載せる）
\newcommand{\experimenttitle}[1]{%
  \clearpage
  \stepcounter{eg@experiment}%
  \setcounter{section}{0}%
  \setcounter{figure}{0}%
  \setcounter{table}{0}%
  \setcounter{equation}{0}%
  \phantomsection
  \addcontentsline{toc}{egexperiment}{#1}%
  \eg@titleblock{#1}%
}

% 前付け（注意事項など）の見出し（番号は付けない）
\newcommand{\introtitle}[1]{%
  \clearpage
  \phantomsection
  \addcontentsline{toc}{egexperiment}{#1}%
  \eg@titleblock{#1}%
}

% ------------------------------------------------------------
% Table of contents
% ------------------------------------------------------------
% 目次はテーマ名（egexperiment）のみ。PDF のしおりには節まで出す
\setcounter{tocdepth}{0}
\hypersetup{bookmarksdepth=1}
\newcommand*{\toclevel@egexperiment}{0}% PDF のしおりでテーマの下に節を並べる
\newcommand*{\l@egexperiment}[2]{%
  \addpenalty{-\@highpenalty}%
  \vskip 1.1\baselineskip plus 2pt
  \begingroup
    \setlength{\parskip}{0pt}%
    \noindent{\sffamily\gtfamily\bfseries\large\color{EGMain}#1}%
    \nobreak\hskip 1em
    {\color{black!40}\leaders\hbox to 0.9em{\hss.\hss}\hfill}%
    \nobreak\hskip 1em{\sffamily\bfseries\large #2}\par
  \endgroup
}

\newcommand{\experimenttoc}{%
  \clearpage
  \eg@titleblock{目次}%
  \begingroup
    \setlength{\parskip}{0pt}% 目次の中は段落間の空きをなくして1ページに収める
    \@starttoc{toc}%
  \endgroup
}

% ------------------------------------------------------------
% Cover
% ------------------------------------------------------------
\newcommand{\makecover}{%
  \begin{titlepage}
    \thispagestyle{empty}%
    \begin{tikzpicture}[remember picture, overlay]
      % 上部の帯
      \fill[EGMain] (current page.north west) rectangle ([yshift=-118mm]current page.north east);
      \fill[EGMain!55] ([yshift=-118mm]current page.north west) rectangle ([yshift=-121mm]current page.north east);
      % 年度
      \node[anchor=north west, text=white, font=\sffamily\gtfamily\large]
        at ([xshift=24mm, yshift=-26mm]current page.north west) {\eg@academicyear};
      % タイトル
      \node[anchor=south west, text=white, align=left, inner sep=0pt]
        at ([xshift=24mm, yshift=-100mm]current page.north west)
        {{\sffamily\gtfamily\bfseries\fontsize{30}{40}\selectfont \eg@coursename}\\[6mm]
         {\sffamily\gtfamily\bfseries\fontsize{22}{30}\selectfont \eg@documenttitle}};
      % 英語名
      \node[anchor=north west, text=EGMain, font=\sffamily\large, inner sep=0pt]
        at ([xshift=24mm, yshift=-132mm]current page.north west) {\eg@courseenglish};
      % 所属
      \node[anchor=south west, text=black, font=\sffamily\gtfamily\large, inner sep=0pt]
        at ([xshift=24mm, yshift=30mm]current page.south west) {\eg@organization};
      \draw[EGMain, line width=1.2pt]
        ([xshift=24mm, yshift=24mm]current page.south west) -- ([xshift=-24mm, yshift=24mm]current page.south east);
    \end{tikzpicture}
  \end{titlepage}
}

% ------------------------------------------------------------
% Header / footer
% ------------------------------------------------------------
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\sffamily\gtfamily \eg@coursename}
\fancyhead[R]{\small\sffamily\gtfamily \eg@experimentname}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% ------------------------------------------------------------
% Heading styles
% ------------------------------------------------------------
\ModifyHeading{section}{
  font={\Large\sffamily\gtfamily\bfseries\color{EGMain}},
  before_space=1.3\baselineskip,
  after_space=0.55\baselineskip
}
\ModifyHeading{subsection}{
  font={\large\sffamily\gtfamily\bfseries},
  before_space=1.0\baselineskip,
  after_space=0.4\baselineskip
}
\ModifyHeading{subsubsection}{
  font={\normalsize\sffamily\gtfamily\bfseries},
  before_space=0.8\baselineskip,
  after_space=0.3\baselineskip
}

% ------------------------------------------------------------
% Figures and tables
% ------------------------------------------------------------
\captionsetup{
  font=small,
  labelfont=bf,
  labelsep=quad,
  justification=centering
}
\renewcommand{\figurename}{図}
\renewcommand{\tablename}{表}

% ------------------------------------------------------------
% Lists
% ------------------------------------------------------------
\setlist[itemize]{
  leftmargin=2.1em,
  itemsep=0.25\baselineskip,
  topsep=0.35\baselineskip
}
\setlist[enumerate]{
  leftmargin=2.4em,
  itemsep=0.35\baselineskip,
  topsep=0.35\baselineskip
}

% Experimental procedure list
\newlist{procedure}{enumerate}{2}
\setlist[procedure,1]{
  label=\textbf{\arabic*.},
  leftmargin=2.6em,
  itemsep=0.55\baselineskip,
  topsep=0.45\baselineskip
}
\setlist[procedure,2]{
  label=(\arabic*),
  leftmargin=2.4em,
  itemsep=0.35\baselineskip
}

% ------------------------------------------------------------
% Semantic environments
% ------------------------------------------------------------
\newtcolorbox{experiment}[1][]{
  enhanced,
  breakable,
  colback=white,
  colframe=EGMain,
  boxrule=0.9pt,
  arc=1.2mm,
  left=2.5mm,
  right=2.5mm,
  top=2mm,
  bottom=2mm,
  fonttitle=\sffamily\gtfamily\bfseries,
  toptitle=1mm,
  bottomtitle=1mm,
  coltitle=white,
  colbacktitle=EGMain,
  title={#1},
  before skip=0.8\baselineskip,
  after skip=0.8\baselineskip
}

\newtcolorbox{equipment}[1][使用器具]{
  enhanced,
  breakable,
  colback=EGSub,
  colframe=EGMain,
  boxrule=0.6pt,
  arc=1mm,
  left=2.5mm,
  right=2.5mm,
  top=1.5mm,
  bottom=1.5mm,
  fonttitle=\sffamily\gtfamily\bfseries,
  toptitle=1mm,
  bottomtitle=1mm,
  coltitle=white,
  colbacktitle=EGMain,
  title={#1},
  before skip=0.7\baselineskip,
  after skip=0.7\baselineskip
}

\newtcolorbox{caution}[1][注意]{
  enhanced,
  breakable,
  colback=EGWarnBG,
  colframe=EGWarn,
  boxrule=0.8pt,
  arc=1mm,
  left=2.5mm,
  right=2.5mm,
  top=1.5mm,
  bottom=1.5mm,
  fonttitle=\sffamily\gtfamily\bfseries,
  toptitle=1mm,
  bottomtitle=1mm,
  coltitle=white,
  colbacktitle=EGWarn,
  title={\(\blacktriangle\)\ #1},
  before skip=0.7\baselineskip,
  after skip=0.7\baselineskip
}

\newtcolorbox{kakunin}[1][確認]{
  enhanced,
  breakable,
  colback=white,
  colframe=EGGray,
  boxrule=0.6pt,
  arc=1mm,
  left=2.5mm,
  right=2.5mm,
  top=1.5mm,
  bottom=1.5mm,
  fonttitle=\sffamily\gtfamily\bfseries,
  toptitle=1mm,
  bottomtitle=1mm,
  title={#1},
  before skip=0.7\baselineskip,
  after skip=0.7\baselineskip
}

\newtcolorbox{hosoku}[1][補足]{
  enhanced,
  breakable,
  colback=white,
  colframe=black!35,
  boxrule=0.5pt,
  arc=1mm,
  left=2.5mm,
  right=2.5mm,
  top=1.5mm,
  bottom=1.5mm,
  fonttitle=\sffamily\gtfamily\bfseries,
  toptitle=1mm,
  bottomtitle=1mm,
  coltitle=black,
  colbacktitle=black!12,
  title={#1},
  before skip=0.7\baselineskip,
  after skip=0.7\baselineskip
}

% ------------------------------------------------------------
% Local emphasis
% These intentionally remain available so each experiment can
% keep its own local emphasis style when appropriate.
% ------------------------------------------------------------
\newcommand{\important}[1]{\textbf{#1}}
\newcommand{\keyword}[1]{{\sffamily\gtfamily\bfseries #1}}
\newcommand{\wave}[1]{\uwave{#1}}

% ------------------------------------------------------------
% Instructor-only notes
% Useful for notes that belong to the manual itself.
% Worksheets and student answer sheets should be separate files.
% ------------------------------------------------------------
\ifeg@instructor
  \newenvironment{instructoronly}
    {\par\begingroup\color{EGWarn}\small
     \noindent\textbf{【教員用】}\ }
    {\par\endgroup}
\else
  \excludecomment{instructoronly}
\fi

% ------------------------------------------------------------
% SI / hyperlinks
% ------------------------------------------------------------
\sisetup{
  detect-all,
  per-mode=symbol
}

\hypersetup{
  colorlinks=true,
  linkcolor=EGMain,
  urlcolor=EGMain,
  citecolor=EGMain,
  pdfborder={0 0 0}
}

\endinput
