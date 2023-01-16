# Script to automate the process of inviting and reviewing GitHub invitations
# The script will provide the option of:
# 1. Sending invitations to all users in a CSV file
import csv
import os
import time
import requests
import json
import argparse
import tqdm

# Extract the API token from the environment
GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')

# Set the default organization
GITHUB_ORG = 'LSSTISSC'

# Global variables
GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_VERSION = 'application/vnd.github.v3+json'
GITHUB_API_HEADERS = {'Accept': GITHUB_API_VERSION}
GITHUB_API_INVITATIONS = '/orgs/{org}/invitations'

def invite_user(email):
    """ Send an invitation to a user through the REST API.
    """
    url = GITHUB_API_URL + GITHUB_API_INVITATIONS.format(org=GITHUB_ORG)
    headers = GITHUB_API_HEADERS
    headers['Authorization'] = 'Bearer {}'.format(GITHUB_API_TOKEN)
    data = {"email": email, 'role': 'direct_member'}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print('Invitation sent to {}'.format(email))
    else:
        print('Error sending invitation to {}: {}'.format(email, response.text))


def invite_users(filename):
    """ Reads the CSV file and invites all users in the file.
    """
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in tqdm.tqdm(reader):
            # Extract the email from the row, and send the invite using the REST API
            email = row['Email']
            if '@' not in email:
                print('Invalid email: {}'.format(email))
                continue
            invite_user(email)
            time.sleep(1) # To avoid rate limiting

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GitHub Butler')

    parser.add_argument('--invite', help='CSV file with users to invite')
    args = parser.parse_args()

    if args.invite:
        invite_users(filename=args.invite)
    else:
        parser.print_help()
