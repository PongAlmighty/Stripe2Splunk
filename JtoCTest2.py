import json
import csv
import stripe 
import datetime
import time
import config

from email import utils
nowdt = datetime.datetime.now()
nowtuple = nowdt.timetuple()
nowtimestamp = time.mktime(nowtuple)
DateTime = str(utils.formatdate(nowtimestamp))

stripe.api_key = config.apikey
stripe.api_version = '2019-11-05'

IsActive = ''
TotalCount = 0
OutputFile = open("/opt/splunk/bin/scripts/JtoCOut.txt", "w+")

TmpCustList = stripe.Customer.list(limit=100)
for customer in TmpCustList.auto_paging_iter():
	CustPlanInfo = str(customer.subscriptions.data)
	NumOfActives = 0
	for line in CustPlanInfo.split(','):
		if  '\"status\": \"active\"' in line:
			NumOfActives += 1 

	if NumOfActives == 0:
		IsActive = 'False'
	else:
		IsActive = 'True'

	descr_dict = json.loads(customer.description)
	custDict = dict()
	custDict['Date'] = DateTime
	custDict['StripeID'] = str(customer.id)
	custDict['Email'] = str(customer.email)


	for Thing1 in customer.subscriptions.data:
		custDict['PlanType'] = str(Thing1.plan.id)
		custDict['PlanCreated'] = str(Thing1.plan.created)
	if descr_dict['drupal_id']:
		custDict['DrupalID'] = descr_dict['drupal_id']
	else:
		custDict['DrupalID'] = 'None'

	if descr_dict['drupal_name']:
                custDict['DrupalName'] = descr_dict['drupal_name']
	else:
                custDict['DrupalName'] = 'None'

	if descr_dict.get('drupal_display_name','None') == 'None':
		custDict['DrupalDisplayName'] = 'None'
	else:
		custDict['DrupalDisplayName'] = descr_dict['drupal_display_name']

	if descr_dict.get('drupal_legal_name','None') == 'None':
		custDict['DrupalLegalName'] = 'None'
	else:
		custDict['DrupalLegalName'] = descr_dict.get('drupal_legal_name','None')


	custDict['IsMember'] = IsActive

	TotalCount += 1
	#print('working on line: ', TotalCount)
	OutputFile.write(json.dumps(custDict))
	OutputFile.write("\n")

print('Completed! Total lines: ', TotalCount)
OutputFile.close()


