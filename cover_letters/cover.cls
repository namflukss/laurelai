% cover.cls — Laurel festival cover-letter class
% A clean, one-page cover letter for film-festival submissions.
% Targets pdflatex (standard TeX Live). Lato is used if installed, else falls back gracefully.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cover}[2026/06/08 Laurel festival cover letter]

\LoadClass[11pt]{article}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[a4paper,margin=1in]{geometry}
\RequirePackage{parskip}
\RequirePackage{xcolor}
\RequirePackage[hidelinks]{hyperref}

% Lato if available (TeX Live package), otherwise the default roman face.
\IfFileExists{lato.sty}{\RequirePackage[default]{lato}}{}

\definecolor{accent}{HTML}{F4530E}   % Laurel orange
\definecolor{ink}{HTML}{1C2029}
\color{ink}
\setlength{\parskip}{0.7em}
\pagestyle{empty}

% ── Sender identity (set in the preamble) ───────────────────────────
\newcommand{\sendername}{}
\newcommand{\senderrole}{Director}
\newcommand{\sendercontact}{}
\newcommand{\setsender}[3]{%
  \renewcommand{\sendername}{#1}%
  \renewcommand{\senderrole}{#2}%
  \renewcommand{\sendercontact}{#3}%
}

% ── Letterhead: \letterhead{Festival, City}{Date} ────────────────────
\newcommand{\letterhead}[2]{%
  {\fontsize{20}{22}\selectfont\bfseries\sendername}\\[-0.2em]
  {\color{accent}\rule{2.2cm}{2pt}}\\[0.4em]
  {\small\senderrole\ \textbar\ \sendercontact}\par
  \vspace{1.4em}
  {\small #2}\par
  \vspace{0.3em}
  {\bfseries #1}\par
  \vspace{1.4em}
}

% ── Sign-off: \signoff ───────────────────────────────────────────────
\newcommand{\signoff}{%
  \vspace{1.2em}
  Warm regards,\\[1.4em]
  \sendername\\
  {\small\senderrole}\par
}
