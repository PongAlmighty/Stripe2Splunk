import json
import csv
import stripe 
import datetime
import time
from email import utils
nowdt = datetime.datetime.now()
nowtuple = nowdt.timetuple()
nowtimestamp = time.mktime(nowtuple)
DateTime = str(utils.formatdate(nowtimestamp))

stripe.api_key = "rk_live_9PafxWPlkkh79N3rcI8jWWI0005332wEdl"
stripe.api_version = '2019-11-05'

IsActive = ''
TotalCount = 0
OutputFile = open("JtoCOut.txt", "w+")
#print('StripeID, Email, DrupalID, DrupalDisName, DrupalName, DrupalLegName, IsActive')
#OutputFile.write('StripeID, Email, DrupalID, DrupalDisName, DrupalName, DrupalLegName, IsActive\n')

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

#	TODO: add in check for descr_dict exists
	TotalCount += 1
#	CustString = (',' + CustID + ',' + CustEmail + ',' + IsActive + '\n')
#	print(CustString, 'Line Number: ', TotalCount)

	#json.dumps(CustString)
	#print(json.dumps(CustString))
	#print(json.dumps(custDict))
	print('working on line: ', TotalCount)
	OutputFile.write(json.dumps(custDict))
	OutputFile.write('\\n')

#	for line in customer.readlines():
#		if 'id' in line:
#		print(line)	

OutputFile.close()

#read file
#with open('StripeCustTemp.txt', 'r') as jsonfile:
#  data=jsonfile.read()

# parse file
#jsonobj = json.loads(data)


#for key in keylist[0]:
#  if key in fieldsIWant :
#    keylist.append(key)

#f = csv.writer(open("test.csv", "w"))
#f.writerow(keylist)

#Iterate through each record in the JSON Array
#for record in jsonobj:
#Create placeholder to hold the data for the current record
#  currentrecord = []
#Iterate through each key in the keylist and add the data to our current record list
#for key in keylist:
#  currentrecord.append(record[key])
#Write the current record as a line in our CSV
#f.writerow(currentrecord)

