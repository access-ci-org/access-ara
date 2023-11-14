# ACCESS Recommender
## Running the application
1. Pull down the repo in your home directory: ```git clone <URL>```
2. Run ```source setup.sh``` (you must have virtualenv installed)
    - Use the `test` argument to reset the database using local data (this data may be incomplete) `source setup.sh test`
    - Use the `conf` argument to reset the database using data from confluence `source setup.sh conf` (refer to the Confluence API section below if you are having trouble with this)
    - If you are having trouble with `source setup.sh` (on VS Code or elsewhere) 
    change your terminal to use bash (git bash works well) or manually install the requirements in `app/requirements.txt`
    and reset the database using `reset_database.py`
3. Run the app with  `cd app`, ```flask run``` or ```python3 -m flask run```
    - To run in production, use `uwsgi --ini wsgi.ini` (make edits in the wsgi.ini file as necessary)

## Developing
1. Follow the above steps to set up your application
2. Pick an issue from the Issues tab on GitHub 
3. Assign yourself to that issue (on the right where it says Assignees)
4. Make sure you are on the flask-app branch (```git branch``` use ```git checkout <branch-name>``` to switch branches)
5. Pull from GitHub to make sure your local files are up to date (```git pull```)
6. From the flask-app branch, Create a new branch ( ```git checkout -b issue-<#>-<descriptor>```)
    This is the branch where you will make the changes to resolve the Issue
7. Once the issue is resolved and everything is pushed, create a pull request from your branch to the flask-app branch on the GitHub website.
8. **Never** Push to the main (flask-app) branch. Others will be pulling from that branch and unfinished
    code will lead to errors for them as well
9. We will review Pull Requests (PRs) together and merge them to the flask-app branch or suggest changes

## Database
- If you make any changes to the database or the models file, make sure you make the appropriate changes in the
    ```reset_database.py``` file as well. (If you add a new column to the RPS table, 
    make sure to add some data for that column in the ```reset_database.py``` file as well)
- If you want to reset the database at any point, run ```python3 reset_database.py test```.
    Doing this will drop and recreate all tables and populate them with some sample data.
    - Use the `conf` parameter instead if you want to use the data in Confluence. (Refer to the Confluence API
    section below if you are having trouble with this.)

## Confluence API
- First, create your API token here: https://id.atlassian.com/manage-profile/security/api-tokens
- Once you have your API token, create a `.env` file in the project folder
- Inside the `.env` file, add the following:  
    `atlassian_username = ""`  
    `confluence_token = ""`  
    Replace the empty strings with the appropriate information (**they must be on two separate lines**).
- That's it you're done! (The relevant code is in the `confluenceAPI.py` file. Run that file to see the results)

## Getting Modules
- To get a list of the available modules on an HPC run `module avail`
- To capture that output into a file, (first make sure you are in your scratch or work space)
    run  `module avail &> <file-name>.txt` (replace `file-name` with a descriptive name)
- To parse through that data and get only the software and version, pass the file to the `get_modules_and_versions` function
    in the `parse_modules` file in this repo.

**TODO:**
See the issues on GitHub for TODO items
