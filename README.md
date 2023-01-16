# collab_mngt_tools
A Set of Utility Scripts and Tools to Help Manage the Collaboration


## Scripts


### GitHub Butler: to Manage GitHub invitations in Bulk

1. Create a personal GitHub API token (see here: https://github.com/settings/tokens), save it in your environment under 'GITHUB_API_TOKEN'

2. Export the ISSC members list as CSV from the LSST contacts database https://project.lsst.org/LSSTContacts/level3.php

3. Run the following to send an invite to all the emails in that CSV file

```python
python scripts/github_butler.py --invite contactdbexport.csv
```

And then be patient, to avoid going over the rate limit, the invitations will be sent at a rate of about 1 per second.

