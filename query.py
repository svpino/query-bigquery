import os
import sys
import httplib2

from apiclient.discovery import build

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

APPLICATION_ID = "henlein-staging"

def main():
	if len(sys.argv) != 2:
		print "Usage: $ python query.py query-file"
		print "Where query-file contains the SQL query to execute."
		print ""

		return

	query = open(sys.argv[1], "rU").read()
	if query is None:
		print "Couldn't read the query file provided."
		return		

	flow = flow_from_clientsecrets('query_authentication.json', scope='https://www.googleapis.com/auth/bigquery')

	storage = Storage('bigquery_credentials.dat')
	credentials = storage.get()

	if credentials is None or credentials.invalid:
		credentials = tools.run_flow(flow, storage, tools.argparser.parse_args([]))

	http = httplib2.Http()
	http = credentials.authorize(http)

	bigquery_service = build('bigquery', 'v2', http=http)

	query_response = bigquery_service.jobs().query(projectId = APPLICATION_ID, body={'query': query}).execute()

	result_row = []
	for field in query_response['schema']['fields']:
		result_row.append(field['name'])

	print (',').join(result_row)

	for row in query_response['rows']:
		result_row = []
		for field in row['f']:
			value = field['v'] if field['v'] is not None else ''
			if ',' in value:
				value = '"' + value + '"'

			result_row.append(value)

		print (',').join(result_row)

if __name__ == '__main__':
	main()