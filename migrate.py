import subprocess
import os
import sys
import yaml


def run_command(command, repo, cwd=sys.path[0]):
    output_log = open("logs/{0}.log".format(repo), "ab")
    print "Running command {0}".format(" ".join(command))
    subprocess.check_call(command, stdout=output_log, stderr=output_log, cwd=cwd)

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

def git_svn_init(url, repo, trunk, tags, branches):
    init_command = ["git", "svn", "init", url, repo,
                    "--trunk={0}".format(trunk), "--tags={0}".format(tags),
                    "--branches={0}".format(branches)]
    run_command(init_command, repo)

def git_svn_fetch(repo):
    fetch_command = ["git", "svn", "fetch", "--authors-file=../authors.txt"]
    run_command(fetch_command, repo, repo)

def git_svn_clean(repo):
    clean_command = ["java", "-Dfile.encoding=utf-8", "-jar", "../svn-migration-scripts.jar",
                     "clean-git", "--force"]
    try:
        run_command(clean_command, repo, repo)
    except subprocess.CalledProcessError:
        print "Error generated while cleaning repository {0}".format(repo)

def migrate_repo(repository):
    trunk = repository.get("trunk") or "trunk"
    tags = repository.get("tags") or "tags"
    branches = repository.get("branches") or "branches"
    url = repository.get("repo")
    repo = get_repo_name_from_url(url)
    if not os.path.isdir(repo):
        git_svn_init(url, repo, trunk, tags, branches)
    git_svn_fetch(repo)
    git_svn_clean(repo)

def main():
    create_log_folder()
    repositories = list_repositories()
    for repository in repositories:
        migrate_repo(repository)

main()
