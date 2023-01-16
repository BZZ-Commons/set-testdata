import csv
import json
import os
import urllib.request

from github import Github, UnknownObjectException  # needs PyGitHub

GITHUB_SECRET = os.environ['GHSECRET']
TARGET_REPO = os.getenv('TARGET_REPO')
DATA_PATH = os.environ['DATA_PATH']


def main():
    """
    main controller
    :return:
    """
    token = Github(GITHUB_SECRET)
    target_repo = token.get_repo(TARGET_REPO)
    owner = get_repo_owner()
    data = read_testdata(owner)
    json_data = json.dumps(data)
    write_testdata(json_data, target_repo)


def read_testdata(owner):
    """
    reads the csv-file with test data
    :param owner:
    :return:
    """
    response = urllib.request.urlopen(DATA_PATH)
    lines = [line.decode('utf-8') for line in response.readlines()]
    csv_reader_object = csv.DictReader(lines, delimiter=';')
    for row in csv_reader_object:
        if row['userid'] == owner:
            return row
    raise ValueError(f'The owner "{owner}" of this repository is unknown')


def get_repo_owner():
    """
    gets the owner from the repo name
    :return:
    """
    print(f'TARGET_REPO={TARGET_REPO}')
    repo_name = TARGET_REPO.split('/')[-1]
    print(f'repo_name={repo_name}')
    parts = repo_name.split('-', 1)
    print(f'parts={parts}')
    return parts[1]


def write_testdata(json_data, target_repo):
    """
    writes the json file with test data to the target repo
    :param json_data: the json-data to be written
    :param target_repo: Repository-object
    :return:
    """

    try:
        existing_data = target_repo.get_contents('testdata.json')
        target_repo.update_file(
            path='testdata.json',
            message='update tests',
            content=json_data,
            sha=existing_data.sha
        )
    except UnknownObjectException as e:  # File not found
        target_repo.create_file(
            path='testdata.json',
            message='create tests',
            content=json_data
        )
    pass


if __name__ == '__main__':
    main()
