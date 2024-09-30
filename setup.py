import hashlib
import os

from github import Github, UnknownObjectException  # needs PyGitHub

GITHUB_SECRET = os.environ['GHSECRET']
TARGET_REPO = os.environ['TARGET_REPO']
TEMPLATE_REPO = os.environ['TEMPLATE_REPO']
FILES = os.environ['FILES']
OWNER = os.environ['OWNER']

def main():
    hash = create_hash()
    files = FILES.split(',')
    token = Github(GITHUB_SECRET)
    target_repo = token.get_repo(TARGET_REPO)
    for file in files:
        contents = f'""" Provides the class "{file}"\t{hash} """\nclass {file}:\n\tpass'
        target_repo.create_file(
            path=f'{file}.py',
            message='create class',
            content=contents
        )

def create_hash():
    hash = hashlib.sha256(OWNER.encode()).hexdigest()
    print(hash)
    return hash[:8]

if __name__ == '__main__':
    main()