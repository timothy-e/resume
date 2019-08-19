import yaml
from string import Template

PACKAGES = r"""
\documentclass[letterpaper, 11pt]{article}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
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
\usepackage[sfdefault]{roboto}
\renewcommand\familydefault{\sfdefault}
\usepackage[T1]{fontenc}
\usepackage{makecell}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}


\addtolength{\oddsidemargin}{-0.375in}
\addtolength{\evensidemargin}{-0.375in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
    \vspace{-3pt}\titlerule\raggedright\LARGE\bfseries
}{}{0em}{}[\color{black}\vspace{-2pt}\titlerule \vspace{-8pt}]

\definecolor{resBlue}{HTML}{418AB3}
\definecolor{resGray}{HTML}{595959}
"""

COMMANDS = r"""
%%%%%%%%%%%%%%%%%
%% My Commands %%
%%%%%%%%%%%%%%%%%

\newcommand{\styleDate}[1]{
    {{\color{resGray}\MakeTextUppercase{#1}}}
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

\newcommand{\resBulletPoint}[2][]{
    \item\styleDescription{
        \ifthenelse
            {\isempty{#1}}
            {}
            {\textbf{#1}: }
        #2
    }
}

\newcommand{\resItem}[3]{
    \vspace{6pt}
    \styleDate{#3} \\
    \stylePosition{#1}\styleEmployer{-- #2}
}

\newenvironment{resElement}[1][]{
    #1
    \begin{itemize}[leftmargin=2ex, nosep, noitemsep]
}{
    \end{itemize}
}
%%%%%%%%%%%%%%%%
"""

BEGIN_DOCUMENT = '\\begin{document}\n'
END_DOCUMENT = '\\end{document}\n'


def _print_education_bullets(term, degree, coursework):
    yield Template("    \\resBulletPoint{Currently enrolled in $term of a $degree}\n").substitute(term=term, degree=degree)
    yield Template("    \\resBulletPoint[Relevant coursework]{$coursework}\n").substitute(coursework=', '.join(coursework))

def _print_bullets(bullets):
    for bullet in bullets:
        yield Template("    \\resBulletPoint{$bullet}\n").substitute(bullet=bullet)


def start_section(section_name):
    yield Template("\\section{$section_name}\n").substitute(section_name=section_name)


def heading(
    *,
    name,
    term,
    program,
    school,
    email,
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
    yield Template(
        "    \\href{$linkedin_url}{$linkedin} \\\\\n"
    ).substitute(linkedin_url=linkedin_url, linkedin=linkedin)
    yield Template("    \\href{$github_url}{$github}\n").substitute(
        github_url=github_url, github=github
    )
    yield "}\n"

    yield "\\end{tabular*}\n"
    yield "\\vspace{-3mm}\n"

    print('done heading')


def summary_of_qualifications(*, languages, bullets, bullet_printer=_print_bullets):
    yield "\\section{Summary of Qualifications}\n"
    yield "    \\begin{resElement}\n"

    yield Template("    \\resBulletPoint[Languages]{$languages}\n").substitute(
        languages=",".join(languages)
    )

    yield from bullet_printer(bullets)

    yield "    \\end{resElement}\n"


def experience(*, company, title, start, end, bullets, bullet_printer=_print_bullets):
    date = f"{start} -- {end}" if start != end else start

    yield "    \\begin{resElement}[\n"
    yield Template("\t\t\\resItem\n\t\t{$title}\n\t\t{$company}\n\t\t{$date}\n").substitute(
        title=title, company=company, date=date
    )
    yield '    ]\n'

    yield from bullet_printer(bullets)

    yield "    \\end{resElement}\n"

def project(*, name, role, start, end, bullets, bullet_printer=_print_bullets):
    yield from experience(company=name, title=role, start=start, end=end, bullets=bullets, bullet_printer=bullet_printer)

def education(*, degree, school, start, end, term, coursework):
    yield from experience(
        company=degree,
        title=school,
        start=start,
        end=end,
        bullets=[],
        bullet_printer=lambda x: _print_education_bullets(term, degree, coursework)
    )
