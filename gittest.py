import os
import git
import github

from git import Repo
from github import Github
from github import InputGitTreeElement

import os.path as osp    
    
repo_dir =  os.getcwd() + '\Repo'
file_name = repo_dir + '\gittest.py'
token = 'fae88b79568930dd8cc3a0422e108c2a09fdff99'
r = Repo.init(repo_dir)
# This function just creates an empty file ...
r.index.add([file_name])
r.index.commit("initial commit")
g = Github("avatR630", token)
repo = g.get_user().get_repo('MI465-Youtube-Comments-NLP')
files = [os.getcwd() + '/testing.py', os.getcwd() + 'gittest.py']
commit_message = 'First commit'

master_ref = repo.get_git_ref('heads/master')
master_sha = master_ref.object.sha
base_tree = repo.get_git_tree(master_sha)
element_list = list()
for entry in file_list:
    with open(entry, 'rb') as input_file:
        data = input_file.read()
    if entry.endswith('.png'):
        data = base64.b64encode(data)
    element = InputGitTreeElement(entry, '100644', 'blob', data)
    element_list.append(element)
tree = repo.create_git_tree(element_list, base_tree)
parent = repo.get_git_commit(master_sha)
commit = repo.create_git_commit(commit_message, tree, [parent])
master_ref.edit(commit.sha)