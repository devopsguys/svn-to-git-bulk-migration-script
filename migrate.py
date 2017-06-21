import subprocess
import os
import yaml

def get_repo_name_from_url(url):
    repo = filter(None, url.split("/"))
    return repo[-1]

def create_log_folder():
    if not os.path.exists("logs"):
        os.makedirs("logs")

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE) == 0

def verify_environment():
    if not cmd_exists("java"):
        raise "java is not installed"
    verify = subprocess.Popen(["java", "-jar", "svn-migration-scripts.jar", "verify"])
    if verify.returncode == 1:
        raise verify.communicate()[0]

def list_repositories():
    repositories_yml = open('repositories.yml')
    repositories = yaml.safe_load(repositories_yml)
    repositories_yml.close()
    return repositories

def clone(url, trunk, tags, branches):
    repo = get_repo_name_from_url(url)
    output_log = open("logs/{0}.log".format(repo), "ab")
    command = ["git", "svn", "clone", "--stdlayout", "--authors-file=authors.txt", url, repo,
               "--trunk='{0}'".format(trunk), "--tags='{0}'".format(tags),
               "--branches='{0}'".format(branches)]
    subprocess.check_call(command, stdout=output_log, stderr=output_log)

def clean(repo):
    output_log = open("logs/{0}.log".format(repo), "ab")
    command = ["java", "-Dfile.encoding=utf-8", "-jar", "../svn-migration-scripts.jar",
               "clean-git", "--force"]
    subprocess.check_call(command, stdout=output_log, stderr=output_log, cwd=repo)

def migrate_repo(repository):
    trunk = repository.get("trunk") or "trunk"
    tags = repository.get("tags") or "tags"
    branches = repository.get("branches") or "branches"
    clone(repository, trunk, tags, branches)

def main():
    create_log_folder()
    repositories = list_repositories()
    for repository in repositories:
        migrate_repo(repository)

main()
