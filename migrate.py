import subprocess
import sys
import os

URL = sys.argv[1]

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

def list_repositories(url):
    repositories = subprocess.check_output(['svn', 'list', url])
    repository_list = repositories.split('/\n')
    return filter(None, repository_list)

def migrate_repo(url, repo):
    clone(repo, url)

def clone(url, repo):
    output_log = open("logs/{0}.log".format(repo), "ab")
    repo_url = "{0}/{1}".format(url, repo)
    command = ["git", "svn", "clone", "--stdlayout", "--authors-file=authors.txt", repo_url, repo]
    print " ".join(command)
    subprocess.check_call(command, stdout=output_log, stderr=output_log)

def main():
    create_log_folder()
    repositories = list_repositories(URL)
    for repository in repositories:
        clone(URL, repository)

main()
