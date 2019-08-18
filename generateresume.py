import resumesnippets
import yaml
import yamlordereddictloader
import subprocess
import os


def generate_lines():
    with open("content.yaml") as f:
        content = yaml.load(f, Loader=yamlordereddictloader.Loader)
        print(content['about']['contact'].keys())

        yield resumesnippets.PACKAGES
        yield resumesnippets.COMMANDS
        yield resumesnippets.BEGIN_DOCUMENT
        yield from resumesnippets.heading(
            name=content['about']['name'],
            term=content['about']['education']['term'],
            program=content['about']['education']['degree']['short'],
            school=content['about']['education']['school'],
            email=content['about']['contact']['email'],
            linkedin_url=content['about']['contact']['linkedin']['url'],
            linkedin=content['about']['contact']['linkedin']['display'],
            github_url=content['about']['contact']['github']['url'],
            github=content['about']['contact']['github']['display'],
        )

        yield from resumesnippets.summary_of_qualifications(
            languages=content['qualifications']['languages'],
            bullets=content['qualifications']['bullets'],
        )

        yield '\\section{Experience}\n'

        for experience in content['experience']:
            if not experience['hidden']:
                yield from resumesnippets.experience(
                    company=experience['company'],
                    title=experience['title'],
                    start=experience['start'],
                    end=experience['end'],
                    bullets=experience['bullets'],
                )

        yield resumesnippets.END_DOCUMENT

with open('resume.tex', 'w') as f:
    for output_line in generate_lines():
        f.write(output_line)

commandLine = subprocess.Popen(['pdflatex', 'test.tex', 'test.pdf'])
commandLine.communicate()

os.unlink('resume.aux')
os.unlink('resume.log')
os.unlink('resume.tex')
