import hashlib
import os
import re
from urllib.error import HTTPError
from urllib.request import urlopen

from github import Github, UnknownObjectException  # needs PyGitHub

GITHUB_TOKEN = os.environ['GH_TOKEN']
TARGET_REPO = os.environ['TARGET_REPO']
USERNAME = os.environ['USERNAME']
ASSETS_PATH = 'https://it.bzz.ch/assets/'


def main():
    assignment_name = extract_repo_name()
    print(f'assignment_name={assignment_name}')
    hash = create_hash()
    files = read_filenames(assignment_name)
    token = Github(GITHUB_TOKEN)

    target_repo = token.get_repo(TARGET_REPO)
    for file in files:
        try:
            target_repo.get_contents(f'{file}')
            print(f'{file} already exists')
            existing = True
        except UnknownObjectException as e:
            existing = False
        if not existing:
            contents = read_template(file, assignment_name, hash)
            target_repo.create_file(
                path=f'{file}',
                message='create class',
                content=contents
            )


def extract_repo_name():
    repo_only = TARGET_REPO.split('/')[1]
    no_user = repo_only.replace(f'-{USERNAME}', '')
    return no_user


def read_template(filename, repo_template, hash):
    try:
        response = urlopen(f'{ASSETS_PATH}{repo_template}/{filename}')
        template = ''
        for line in response.readlines():
            template += line.decode('utf-8')
    except HTTPError as e:
        print(f'The file "{filename}" is unknown')
        template = f'""" Provides the class "{filename}" \t\t{hash}"""\n\nclass TODO:\n    pass\n'
    return template.replace('{{HASH}}', hash)


def read_filenames(repo_template):
    path = f'{ASSETS_PATH}{repo_template}'
    filelist = []
    try:
        urlpath = urlopen(path)
        output = urlpath.read().decode('utf-8')
        pattern = re.compile('\w*.py"')
        onlyfiles = pattern.findall(output)
        for filename in onlyfiles:
            filename = filename.replace('"', '')
            filelist.append(filename)
    except HTTPError as e:
        print(f'The path "{path}" is unknown')
    return filelist


def create_hash():
    hash = hashlib.sha256(USERNAME.encode()).hexdigest()
    print(hash)
    return hash[:8]


if __name__ == '__main__':
    main()
