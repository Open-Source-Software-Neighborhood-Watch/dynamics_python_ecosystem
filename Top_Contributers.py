# Importing Libraries
import pandas as pd
import os
from collections import Counter
import mysql.connector

def get_top_contributers(repo_name):
    #Set Working Directory
    wd = os.getcwd() + '\\' + repo_name + '\\'

    #Import lists
    commits = pd.read_csv(wd + repo_name + '_commits.csv', encoding='ISO-8859-1', engine='python', sep=',', quotechar='"', error_bad_lines=False)
    pull_requests = pd.read_csv(wd + repo_name + '_pull_requests.csv', encoding='ISO-8859-1', engine='python', sep=',', quotechar='"', error_bad_lines=False)
    dups_commits = commits.pivot_table(index=['author_login'], aggfunc='size')
    dups_pull_requests = pull_requests.pivot_table(index=['pull_request_author'], aggfunc='size')
    dups_commits_dict = dups_commits.to_dict()
    dups_pull_requests_dict = dups_pull_requests.to_dict()
    dups_commits_dict = Counter(dups_commits_dict)
    dups_pull_requests_dict = Counter(dups_pull_requests_dict)
    combined = dups_pull_requests_dict + dups_commits_dict

    combined = pd.DataFrame(combined.items(), columns=['username', 'commits+pulls'])
    combined = combined.sort_values('commits+pulls', ascending=False)
    top_ten = combined.head(10)
    file_path = os.getcwd() + '\\Top_Contributers\\' + repo_name + '.csv'
    top_ten.to_csv(file_path, index=False, header=True)

get_top_contributers('click')
get_top_contributers('cpython')
get_top_contributers('django')
get_top_contributers('matplotlib')
get_top_contributers('numpy')
get_top_contributers('odoo')
get_top_contributers('pandas')
get_top_contributers('pytest')
get_top_contributers('pytest-cov')
get_top_contributers('python-dateutil')
get_top_contributers('pyyaml')
get_top_contributers('requests')
get_top_contributers('scipy')
get_top_contributers('setuptools')
get_top_contributers('six')
get_top_contributers('sphinx')