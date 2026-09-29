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

\newcommand{\experimenttitle}[1]{%
  \clearpage
  \stepcounter{eg@experiment}%
  \setcounter{section}{0}%
  \setcounter{figure}{0}%
  \setcounter{table}{0}%
  \setcounter{equation}{0}%
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
