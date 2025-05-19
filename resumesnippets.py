import yaml
from string import Template

BEGIN_DOCUMENT = "\\begin{document}\n"
END_DOCUMENT = "\\end{document}\n"


def _print_education_bullets(degree, coursework):
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
    tagline,
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
    yield f"    {tagline}\n"

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
    yield Template("    \phonenumber{$phone}").substitute(phone=phone)
    yield "}\n"

    yield "\\end{tabular*}\n"
    yield "\\vspace{-3mm}\n"


def skills(*, languages):
    yield "\\section{Languages}\n"
    yield "\\vspace{2mm}\n"
    yield "\\color{resGray}\n"
    yield "\\hfill \\resDot \\hfill ".join(languages)


def experience(
    *, company, title, start, end, bullets, languages, bullet_printer=_print_bullets
):
    date = f"{start} -- {end}" if start != end else start

    if bullet_printer:
        yield "    \\begin{resElement}[\n"

    yield Template(
        "\t\t\\resItem\n\t\t{$big_text}\n\t\t{$small_text}\n\t\t{$date}\n\t\t{$languages}\n"
    ).substitute(
        big_text=company if company else title,
        small_text=title if company else company,
        languages=', '.join(languages),
        date=date
    )

    if bullet_printer:
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


def education(*, degree, school, start, end):
    yield from experience(
        company=school,
        title=degree,
        start=start,
        end=end,
        bullets=[],
        languages=[],
        bullet_printer=None
    )
