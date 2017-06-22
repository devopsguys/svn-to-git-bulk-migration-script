import subprocess
import os
import sys
from multiprocessing import Pool
import yaml

LOGS_DIR = "logs"
MIGRATION_DIR = "migration"

def run_command(command, repo, cwd=sys.path[0]):
    output_log = open("logs/{0}.log".format(repo), "ab")
    print "[{0}] Running command {1}".format(repo, " ".join(command))
    subprocess.check_call(command, stdout=output_log, stderr=output_log, cwd=cwd)

def get_repo_name_from_url(url):
    repo = filter(None, url.split("/"))
    return repo[-1]

def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE) == 0

def verify_environment():
    if not cmd_exists("java"):
        raise "java is not installed"
    verify = subprocess.Popen(["java", "-jar", "svn-migration-scripts.jar", "verify"])
    if verify.returncode == 1:
        raise verify.communicate()[0]

def load_yaml_file(path):
    yaml_file = open(path)
    dataset = yaml.safe_load(yaml_file)
    yaml_file.close()
    return dataset

# --prefix= added so that the default branch mapping behaviour from git 1.x is restored
# Without this, the cleanup script at the end won't work!
def git_svn_init(url, repo, trunk, tags, branches):
    init_command = ["git", "svn", "init", url, repo, '--prefix=',
                    "--trunk={0}".format(trunk), "--tags={0}".format(tags),
                    "--branches={0}".format(branches)]
    run_command(init_command, repo, MIGRATION_DIR)

def git_svn_fetch(repo):
    fetch_command = ["git", "svn", "fetch", "--authors-file=../../authors.txt"]
    run_command(fetch_command, repo, os.path.join(MIGRATION_DIR, repo))

def git_svn_clean(repo):
    clean_command = ["java", "-Dfile.encoding=utf-8", "-jar", "../../svn-migration-scripts.jar",
                     "clean-git", "--force"]
    try:
        run_command(clean_command, repo, os.path.join(MIGRATION_DIR, repo))
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
    mkdir_p(LOGS_DIR)
    mkdir_p(MIGRATION_DIR)
    config = load_yaml_file('config.yml')[0]
    repositories = load_yaml_file('repositories.yml')
    pool = Pool(processes=config.get('max-processes'))
    pool.map(migrate_repo, repositories)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
