import yaml
from string import Template

PACKAGES = r"""
\documentclass[letterpaper, 11pt]{article}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{mwe}
\usepackage{latexsym}
\usepackage{marvosym}
\usepackage[usenames, dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage{ragged2e}
\usepackage{xifthen}
\usepackage{xcolor}
\usepackage[pdftex]{hyperref}
\usepackage{fancyhdr}
\usepackage[overload]{textcase}
\usepackage[scaled]{helvet}
% \usepackage[sfdefault]{roboto}
% \renewcommand\familydefault{\sfdefault}
\usepackage[T1]{fontenc}
\usepackage{makecell}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\makeatletter
\renewcommand\section{\@startsection {section}{1}{\z@}%
    {5pt}%
    {0.5pt}%
    {\normalfont\Large\bfseries\headingbox}}
\def\@seccntformat#1{} % no section numbers
\makeatother

\newcommand*{\headingbox}[1]{%
    \noindent\colorbox{resBlue}{%
        \parbox[c][5mm]{\dimexpr\columnwidth-2\fboxsep\relax}{%
        \textcolor{white}{#1}}}}


\addtolength{\oddsidemargin}{-0.37in}
\addtolength{\evensidemargin}{-0.37in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
    \vspace{-3pt}\titlerule\raggedright\LARGE\bfseries
}{}{0em}{}[\color{black}]

\definecolor{resBlue}{HTML}{418AB3}
\definecolor{resGray}{HTML}{595959}
"""

COMMANDS = r"""
%%%%%%%%%%%%%%%%%
%% My Commands %%
%%%%%%%%%%%%%%%%%

\renewcommand\labelitemi{{\Large\boldmath$\cdot$}}

\newcommand{\cpp}{C\texttt{++}}
\newcommand{\styleDate}[1]{
    {{\color{resGray}#1}}
}
\newcommand{\styleDescription}[1]{
    {\color{resGray}#1}
}
\newcommand{\styleEmployer}[1]{
    {\Large{\color{resGray}#1}}
}
\newcommand{\stylePosition}[1]{
    {\Large{\textbf{\color{resBlue}#1}}}
}

\newcommand{\styleLanguages}[1]{
    {\color{resBlue}#1}
}

\newcommand{\resBulletPoint}[2][]{
    \item\styleDescription{
        \ifthenelse
            {\isempty{#1}}
            {}
            {\textbf{#1}: }
        #2
    }
}

\newcommand{\resDot}{
    \hspace{2mm}\color{resBlue}$\bullet$\color{resGray}\hspace{2mm}
}

\newcommand{\resItem}[4]{
    \vspace{5pt}
    \styleDate{#3} \\
    \begin{tabularx}{\textwidth}[t]{lXr}
    \stylePosition{#1}\ifthenelse{\isempty{#2}}{}{\styleEmployer{|\hspace{0.2em} #2}} & & \styleLanguages{#4}
    \end{tabularx}
    \vspace{-14pt}
}

\newenvironment{resElement}[1][]{
    #1
    \begin{itemize}[leftmargin=2ex, nosep, noitemsep]
}{
    \end{itemize}
}
%%%%%%%%%%%%%%%%
"""

BEGIN_DOCUMENT = "\\begin{document}\n"
END_DOCUMENT = "\\end{document}\n"


def _print_education_bullets(term, degree, coursework):
    yield Template(
        # "    \\resBulletPoint{Currently enrolled in $term of a $degree}\n"
        "    \\resBulletPoint{Entering $term of a $degree}\n"
    ).substitute(term=term, degree=degree)
    yield Template(
        "    \\resBulletPoint[Relevant coursework]{$coursework}\n"
    ).substitute(coursework=", ".join(coursework))


def _print_bullets(bullets):
    for bullet in bullets:
        yield Template("    \\resBulletPoint{$bullet}\n").substitute(
            bullet=bullet
        )


def start_section(section_name):
    yield Template("\\section{$section_name}\n").substitute(
        section_name=section_name
    )


def heading(
    *,
    name,
    term,
    program,
    school,
    email,
    phone,
    linkedin_url,
    linkedin,
    github_url,
    github,
):
    yield "\\begin{tabular*}{\\textwidth}{l@{\\extracolsep{\\fill}}r}\n"
    yield "\\makecell[l]{\n"
    yield Template(
        "\\textbf{\\href{$linkedin_url}{\\Huge $name}}\\\\\n"
    ).substitute(linkedin_url=linkedin_url, name=name)
    yield "    {term}, {school}, {program}\n".format(
        term=term, school=school, program=program
    )

    yield "} & \\makecell[r]{\n"

    yield Template("    \\href{mailto:$email}{$email}\\\\\n").substitute(
        email=email
    )
    yield Template("    \\href{$linkedin_url}{$linkedin}\\\\\n").substitute(
        linkedin_url=linkedin_url, linkedin=linkedin
    )
    yield Template("    \\href{$github_url}{$github}\\\\\n").substitute(
        github_url=github_url, github=github
    )
    yield Template("    $phone").substitute(phone=phone)
    yield "}\n"

    yield "\\end{tabular*}\n"
    yield "\\vspace{-3mm}\n"


def skills(*, languages):
    yield "\\section{Skills}\n"
    yield "\\vspace{2mm}\n"
    yield "\\color{resGray}\n"
    yield "\\resDot ".join(languages)


def experience(
    *, company, title, start, end, bullets, languages, bullet_printer=_print_bullets
):
    date = f"{start} -- {end}" if start != end else start

    yield "    \\begin{resElement}[\n"
    yield Template(
        "\t\t\\resItem\n\t\t{$big_text}\n\t\t{$small_text}\n\t\t{$date}\n\t\t{$languages}\n"
    ).substitute(
        big_text=company if company else title,
        small_text=title if company else company,
        languages=', '.join(languages),
        date=date
    )
    yield "    ]\n"

    yield from bullet_printer(bullets)

    yield "    \\end{resElement}\n"


def project(*, name, role, start, end, bullets, languages, bullet_printer=_print_bullets):
    yield from experience(
        company="",
        title=name,
        start=start,
        end=end,
        bullets=bullets,
        languages=languages,
        bullet_printer=bullet_printer,
    )


def education(*, degree, school, start, end, term, coursework):
    yield from experience(
        company=school,
        title=degree,
        start=start,
        end=end,
        bullets=[],
        languages=[],
        bullet_printer=lambda x: _print_education_bullets(
            term, degree, coursework
        ),
    )
