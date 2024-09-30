import hashlib
import os
from urllib.error import HTTPError
from urllib.request import urlopen

from github import Github, UnknownObjectException  # needs PyGitHub

GITHUB_TOKEN = os.environ['GH_TOKEN']
TARGET_REPO = os.environ['TARGET_REPO']
TEMPLATE_PATH = os.environ['TEMPLATE_PATH']
FILES = os.environ['FILES']
USERNAME = os.environ['USERNAME']


def main():
    hash = create_hash()
    files = FILES.split(',')
    token = Github(GITHUB_TOKEN)

    target_repo = token.get_repo(TARGET_REPO)
    for file in files:
        try:
            target_repo.get_contents(f'{file}.py')
            print (f'{file}.py already exists')
            existing = True
        except UnknownObjectException as e:
            existing = False
        if not existing:
            contents = read_template(file, hash)
            target_repo.create_file(
                path=f'{file}.py',
                message='create class',
                content=contents
    )


def read_template(filename, hash):
    try:
        response = urlopen(f'{TEMPLATE_PATH}{filename}.csv')
        template = ''
        for line in response.readlines():
            template += line.decode('utf-8')
    except HTTPError as e:
        print (f'The file "{filename}" is unknown')
        template = f'""" Provides the class "{filename}" \t\t{hash}"""\n\nclass {filename}():\n    pass\n'
    return template.replace('{{HASH}}', hash)


def create_hash():
    hash = hashlib.sha256(USERNAME.encode()).hexdigest()
    print(hash)
    return hash[:8]


if __name__ == '__main__':
    main()
