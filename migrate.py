import subprocess
import os
import sys

url = sys.argv[1]

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


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

for repo in list_repositories(url):
    print repo

