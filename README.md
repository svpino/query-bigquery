# Running queries in BigQuery from the command line

I know you can do this with the [bq command line tool](https://cloud.google.com/bigquery/bq-command-line-tool), but if you need to run queries from a Windows shell (which sucks), and you have complicated enough queries (several pages long), you might want to consider this script.

_(I tried, and had to write this instead. The Windows shell complained all the time with the quote symbols used by the queries, and having to format the content to fit in the command line wasn't a fun task.)_

I'm sure that if you are smarter than me, you'll be able to figure out the bq tool, but if you don't have the time, feel free to use this Python script.

## Files and folders

We are connecting to BigQuery, so we need a few libraries in our path to run the script:

* `httplib2`
* `apiclient`
* `oauth2client`
* `uritemplate`

Outside those folders, `query.py` is where everything happens. I did include a `_queries\sample` file with a sample query so you can test the script right away.

## Authenticating with BigQuery

This `query.py` script will request access to the Big Query API using OAuth2, so before executing it, we need to generate a client ID and client secret:

1. Visit the Google Developers Console and select your project.

2. Click on __APIS & AUTH__ on the menu on the left, then select __Credentials__. Click on __Create new Client ID__.

3. Select __Installed application__.

4. Click __Create Client ID__, then click __Download JSON__ to download the client file.

5. Copy the downloaded file to the root folder of the application, and give it the name `query_authentication.json` (This is the way I'm referencing the file in the `query.py` script. If you want a different name for this file, you can go and change the code.) 

6. The first time you execute the `query.py` script, the OAuth2 authentication process will take place and a `bigquery_credentials.dat` file will be created in your local folder.

## Running queries from the command line

The `query.py` script requires only one argument: the name of the file containing the SQL query to be executed in Big Query. You can find one example query inside the `/_queries` folder. To execute it, run the following command:

    $ python query.py _queries/sample

The result is a comma-separated list of all the fields returned by the query.