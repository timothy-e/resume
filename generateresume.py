import resumesnippets
import yaml
import yamlordereddictloader
import subprocess
import sys
from pathlib import Path
import os
import re


def prepare_string(d):
    if isinstance(d, str):
        s = d.replace("C++", "\\cpp")
        s = s.replace("c++", "\\cpp")
        s = s.replace("%", "\\%")

        s = re.sub(r'"(.*)"', r"``\1''", s) # replace quotes with LaTeX style quotes
        s = re.sub(r'LaTeX', r'\\LaTeX\ ', s, flags=re.IGNORECASE)

        return s
    elif isinstance(d, dict):
        for k, v in d.items():
            d[k] = prepare_string(v)
        return d
    elif isinstance(d, list):
        return [prepare_string(s) for s in d]
    elif isinstance(d, bool):
        return d
    elif isinstance(d, int):
        return d
    else:
        print("Unexpected item " + str(type(d)) + ", " + str(d))
        raise Exception


def generate_lines():
    with open("content.yaml") as f:
        content = yaml.load(f, Loader=yamlordereddictloader.Loader)
        content = prepare_string(content)

        with open ("packages.tex", "r") as packages:
            yield from packages.readlines()

        yield "\n"

        with open ("commands.tex", "r") as commands:
            yield from commands.readlines()

        yield resumesnippets.BEGIN_DOCUMENT
        yield from resumesnippets.heading(
            name=content["about"]["name"],
            tagline=content["about"]["tagline"],
            email=content["about"]["contact"]["email"],
            phone=content["about"]["contact"]["phone"],
            linkedin_url=content["about"]["contact"]["linkedin"]["url"],
            linkedin=content["about"]["contact"]["linkedin"]["display"],
            github_url=content["about"]["contact"]["github"]["url"],
            github=content["about"]["contact"]["github"]["display"],
        )

        yield from resumesnippets.skills(
            languages=content["qualifications"]["languages"]
        )

        yield from resumesnippets.start_section("Experience")
        for experience in content["experience"]:
            if not experience["hidden"]:
                yield from resumesnippets.experience(
                    company=experience["company"],
                    title=experience["title"],
                    start=experience["start"],
                    end=experience["end"],
                    bullets=experience["bullets"],
                    languages=experience["languages"],
                )

        yield from resumesnippets.start_section("Projects")
        for project in content["projects"]:
            if not project["hidden"]:
                yield from resumesnippets.project(
                    name=project["name"],
                    role=project["role"],
                    start=project["start"],
                    end=project["end"],
                    bullets=project["bullets"],
                    languages=project["languages"],
                )

        yield from resumesnippets.start_section("Education")
        edu = content["about"]["education"]
        yield from resumesnippets.education(
            degree=edu["degree"]["long"],
            school=edu["school"],
            start=edu["start"],
            end=edu["end"]
        )

        yield resumesnippets.END_DOCUMENT

def write_file(file):
    with open(file.with_suffix(".tex"), "w") as f:
        for output_line in generate_lines():
            f.write(output_line)


if __name__ == "__main__":
    file = Path(sys.argv[1])
    print(file)
    write_file(file)

    commandLine = subprocess.Popen(
        ["pdflatex", file.with_suffix(".tex"), file.with_suffix(".pdf")]
    )
    commandLine.communicate()

    os.unlink(file.with_suffix(".aux"))
    os.unlink(file.with_suffix(".log"))
    os.unlink(file.with_suffix(".out"))
    # os.unlink(file.with_suffix(".tex"))
