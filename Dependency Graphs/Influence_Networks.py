# Importing Libraries
import pandas as pd
import os
import mysql.connector

#Set Working Directory
wd = os.getcwd() + '\\Top_Contributers\\'

# Importing top contributer lists
click_cont = pd.read_csv(wd + 'click.csv', encoding = 'ISO-8859-1', engine = 'python')
cpython_cont = pd.read_csv(wd + 'cpython.csv', encoding = 'ISO-8859-1', engine = 'python')
django_cont = pd.read_csv(wd + 'django.csv', encoding = 'ISO-8859-1', engine = 'python')
matplotlib_cont = pd.read_csv(wd + 'matplotlib.csv', encoding = 'ISO-8859-1', engine = 'python')
numpy_cont = pd.read_csv(wd + 'numpy.csv', encoding = 'ISO-8859-1', engine = 'python')
odoo_cont = pd.read_csv(wd + 'odoo.csv', encoding = 'ISO-8859-1', engine = 'python')
pandas_cont = pd.read_csv(wd + 'pandas.csv', encoding = 'ISO-8859-1', engine = 'python')
pytest_cont = pd.read_csv(wd + 'pytest.csv', encoding = 'ISO-8859-1', engine = 'python')
pytest_cov_cont = pd.read_csv(wd + 'pytest-cov.csv', encoding = 'ISO-8859-1', engine = 'python')
pdate_cont = pd.read_csv(wd + 'python-dateutil.csv', encoding = 'ISO-8859-1', engine = 'python')
pyyaml_cont = pd.read_csv(wd + 'pyyaml.csv', encoding = 'ISO-8859-1', engine = 'python')
requests_cont = pd.read_csv(wd + 'requests.csv', encoding = 'ISO-8859-1', engine = 'python')
scipy_cont = pd.read_csv(wd + 'scipy.csv', encoding = 'ISO-8859-1', engine = 'python')
setuptools_cont = pd.read_csv(wd + 'setuptools.csv', encoding = 'ISO-8859-1', engine = 'python')
six_cont = pd.read_csv(wd + 'six.csv', encoding = 'ISO-8859-1', engine = 'python')
sphinx_cont = pd.read_csv(wd + 'sphinx.csv', encoding = 'ISO-8859-1', engine = 'python')

# Setting up database access
connection = mysql.connector.connect(host='localhost', database='ghtorrent_restore',
                                         user='', password='')
# Function for pulling contributer usernames to a list
def user_list(dataframe):
    list = dataframe['username'].tolist()
    return list

# Function to pull contributer networks
def network_pull(cont_df, repo_name):
    # Pulling User IDs for database
    ul = user_list(cont_df)
    if not os.path.exists(os.getcwd() + '\\Top_Contributer_Networks\\' + repo_name):
        os.mkdir(os.getcwd() + '\\Top_Contributer_Networks\\' + repo_name)
    for user in ul:
        cursor = connection.cursor(buffered=True)
        id_query = '''SELECT * FROM users WHERE users.login = %s'''
        cursor.execute(id_query, (user,))
        users = cursor.fetchall()
        user_dir = os.getcwd() + '\\Top_Contributer_Networks\\' + repo_name + '\\' + user
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)

        # Pulling User followers from database
        for row in users:
            ID = (row[0])
            followers_query = '''SELECT a.follower_id, b.login, a.created_at FROM followers a, users b WHERE a.user_id =
            %s AND a.follower_id = b.id'''
            cursor.execute(followers_query, (ID,))
            followers = cursor.fetchall()
            followers_df = pd.DataFrame(followers, columns=['user_id', 'username', 'date_followed'])
            file_path = user_dir + '\\followers.csv'
            followers_df.to_csv(file_path, index=False, header=True)

        # Pulling User follows from database
        for row in users:
            ID = (row[0])
            follows_query = '''SELECT a.user_id, b.login, a.created_at FROM followers a, users b WHERE a.follower_id = 
            %s AND a.user_id = b.id'''
            cursor.execute(follows_query, (ID,))
            follows = cursor.fetchall()
            follows_df = pd.DataFrame(follows, columns=['user_id', 'username', 'date_followed'])
            file_path = user_dir + '\\follows.csv'
            follows_df.to_csv(file_path, index=False, header=True)

        # Pulling User watches (stars) from database
        for row in users:
            ID = (row[0])
            watching_query = '''SELECT a.repo_id, b.name, a.created_at FROM watchers a, projects b WHERE a.user_id = 
            %s AND a.repo_id = b.id'''
            cursor.execute(watching_query, (ID,))
            watching = cursor.fetchall()
            watching_df = pd.DataFrame(watching, columns=['repo_id', 'repo_name', 'date_watched'])
            file_path = user_dir + '\\watching.csv'
            watching_df.to_csv(file_path, index=False, header=True)

        # Pulling User forks from the database
        for row in users:
            ID = (row[0])
            forks_query = '''SELECT a.id, a.name, a.created_at FROM projects a WHERE a.owner_id = %s AND 
            a.forked_from IS NOT NULL'''
            cursor.execute(forks_query, (ID,))
            forks = cursor.fetchall()
            forks_df = pd.DataFrame(forks, columns=['repo_id', 'repo_name', 'date_watched'])
            file_path = user_dir + '\\forks.csv'
            forks_df.to_csv(file_path, index=False, header=True)

# Running the code
network_pull(click_cont, 'click')
network_pull(cpython_cont, 'cpython')
network_pull(django_cont, 'django')
network_pull(matplotlib_cont, 'matplotlib')
network_pull(numpy_cont, 'numpy')
network_pull(odoo_cont, 'odoo')
network_pull(pandas_cont, 'pandas')
network_pull(pytest_cont, 'pytest')
network_pull(pytest_cov_cont, 'pytest-cov')
network_pull(pdate_cont, 'python-dateutil')
network_pull(pyyaml_cont, 'pyyaml')
network_pull(requests_cont, 'requests')
network_pull(scipy_cont, 'scipy')
network_pull(setuptools_cont, 'setuptools')
network_pull(six_cont, 'six')
network_pull(sphinx_cont, 'sphinx')
