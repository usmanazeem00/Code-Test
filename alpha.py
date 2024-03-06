import sqlite3
import requests
import CheckOwnershipTransfer as co

# GET ALL REPOS
def retrieve_all_rows():
    # Connect to SQLite database
    conn = sqlite3.connect('RepositoryName.db')
    cursor = conn.cursor()
    
    # Retrieve all rows from the table
    cursor.execute('''SELECT * FROM RepoName''')
    rows = cursor.fetchall()
    
    # Close connection
    conn.close()
    
    return rows

def owner_profile_date(name,reponame):
    conn = sqlite3.connect('RepositoryName.db')
    cursor = conn.cursor()
    
    # Retrieve all rows from the table
    cursor.execute('''SELECT profile_creation_date FROM RepoName where username=? and reponame=?''',(name,reponame))
    rows = cursor.fetchone()
    
    # Close connection
    conn.close()
    
    return rows


def fetch_user_repos(username, token):
    repo_names=[]
    # GitHub API endpoint to fetch user repositories
    url = f"https://api.github.com/search/repositories?q=user:{username}"
    
    # Set the request headers to include the personal access token for authentication
    #headers = {"Authorization": f"Bearer {token}"}
    
    # Make a GET request to the GitHub API
    response = requests.get(url) #,headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            repositories=response.json()['items']
            for  repo in repositories:
                repo_names.append(repo['name'])
                # Return the JSON response containing user repositories
            return repo_names
        except:
            return []
    else:
        # If the request failed, print an error message
        print(f"Failed to fetch repositories for user '{username}'. Status code: {response.status_code}")
        return None
    

#UPDATE
def delete_username(old_username, reponame):
    conn = sqlite3.connect('RepositoryName.db')
    cursor = conn.cursor()  
    # Update the username
    cursor.execute('''Delete from RepoName where username=? and reponame=?''', (old_username,reponame))  
    conn.commit()


# Insert  Repo Names
def insert_repo(username, reponame,date):
    # Connect to SQLite database
    conn = sqlite3.connect('RepositoryName.db')
    cursor = conn.cursor()    
    # Insert data into the table
    cursor.execute('''INSERT OR REPLACE INTO RepoName (username, reponame,profile_creation_date)
                      VALUES (?, ?,?)''', (username, reponame,date))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
# Example usage:
if __name__ == "__main__":
    i=0
    while i<2:
        
     username=input('Enter the User Name')
     i+=1
    #private_token=input('Enter the Private token')

    # GET REPOS
    
    #username='hamzaMSC'
     private_token='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'
     date=co.get_profile_creation_date(username)
     if(date):
         repolist=fetch_user_repos(username,private_token)
         if len(repolist)>0:
             for name in repolist:
                 print(name)
                 insert_repo(username,name,date)
         else :
             print('No Repos For Current User')
     else:
         print('USER DOESNOT EXIST')




    #insert_repo("muhammadusman000", "Cyber", "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")


