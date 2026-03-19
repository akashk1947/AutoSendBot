
# createAccount2.py
# Send messages to multiple groups using round-robin across accounts and sessions.

# Define your accounts and their sessions
accounts = {
	'account_7741': [f'bot{i}' for i in range(1, 11)],  # bot1 to bot10
	'account_4139': [f'bot{i}' for i in range(1, 11)],
    # 'account_4254': [f'bot{i}' for i in range(1, 11)],
}

# List of group links to send messages to
groups = [
"https://t.me/ForceCertified",
"https://t.me/SalesforceUSA",
"https://t.me/usaproxysupport",
"https://t.me/usukjavajobsupport",
"https://t.me/testinginterviewsupport",
"https://t.me/usa_IT_Training_Job",
"https://t.me/Sfdctrainingjobsupport",
"https://t.me/QAsupport24x7",
"https://t.me/proxyinterviewjobsupport",
"https://t.me/interviewsupportworksupportgroup",
"https://t.me/java_jobs_inteview_support_proxy",
"https://t.me/salesforceB",
"https://t.me/pythonproexpert",
"https://t.me/salesforcee",
"https://t.me/microsoftal",
"https://t.me/jobSupportUSACanada",
"https://t.me/devopsfreelancers",
"https://t.me/usainterviewsupport",
"https://t.me/javafreelancers1",
"https://t.me/US_IT",
"https://t.me/MS_AZ_500",
"https://t.me/java_job_support_online",
"https://t.me/dataengineerjob",
"https://t.me/javasupportremote",
"https://t.me/jobsupport0",
"https://t.me/FreelanceJobSupport",
"https://t.me/Sfdc_kuldeep",
"https://t.me/SFb2bCom",
"https://t.me/springframeworks",
"https://t.me/salesforcesupportg",
"https://t.me/usa_laravel",
"https://t.me/usitjobsforprofessionalsgrp",
"https://t.me/SAP_USA_job",
"https://t.me/dump_servicenow_certified",
"https://t.me/python_india",
"https://t.me/java_py_script",
"https://t.me/mathurasalesforcedug",
"https://t.me/awsandazuresupport",
"https://t.me/Javaproxyjobsupport",
"https://t.me/Interviewproxy",
"https://t.me/NowLearners",
"https://t.me/SalesforceJobSupportUSA",
"https://t.me/pythonjobs",
"https://t.me/Data_Engineering_Support",
"https://t.me/awscloudsupportassociate",
"https://t.me/nowgeeks",
"https://t.me/AWS_Exam_Certifications",
"https://t.me/QAJobsAssistance",
"https://t.me/salesforcecertifications_1",
"https://t.me/uiuxindian",
"https://t.me/pythonjobsupdates",
"https://t.me/TechomExpert",
"https://t.me/salesforceusa1",
"https://t.me/bssoftwarejobs304",
"https://t.me/mernstackwebdevelopers",
"https://t.me/powerbi",
"https://t.me/reactjs_jobs",
"https://t.me/Interviews",
"https://t.me/Salesforcehelp1",
"https://t.me/gcpcertifications",
"https://t.me/usasoftwarejobs",
"https://t.me/India_IT_JOBS",
"https://t.me/pythonproxy",
"https://t.me/salesforcebatch3",
"https://t.me/reactjsproxysupport",
"https://t.me/proxyforreactjs",
"https://t.me/GCP_CLOUD_SUPPORT",
"https://t.me/reactproxyind",
"https://t.me/itjobsus",
"https://t.me/FullStackWebDeveloper2021",
"https://t.me/interviewproxyservice",
"https://t.me/Datascienceproxysupport",
"https://t.me/pythonsupportt",
"https://t.me/sfdc_coding",
"https://t.me/salesforceaccreditation",
"https://t.me/ITJobsOntarioCanada",
"https://t.me/SalesforceCertSupport",
"https://t.me/pythonselenium",
"https://t.me/salesforcencino",
"https://t.me/IT_Jobs_Europe",
"https://t.me/it_freshers_placements",
"https://t.me/TCSDigital_Deloitte_Infosys",
"https://t.me/canadaitjobs",
"https://t.me/SalesforceSupportHelp",
"https://t.me/ProxyJobSupports",
"https://t.me/sfdcinterviewquestions",
"https://t.me/Javasupport1",
"https://t.me/TechmonicsServiceNow",
"https://t.me/SalesforceDumz",
"https://t.me/PythonEx",
"https://t.me/infosys9",
"https://t.me/Az400AzureDevopsSupport",
"https://t.me/salesforceparttime",
"https://t.me/salesforceCertificationsA",
"https://t.me/snowinterviewquestions",
"https://t.me/Java_Certification",
"https://t.me/etldiscussion",
"https://t.me/Salesforce_Trailblazer",
"https://t.me/azure_data_engineerg",
"https://t.me/salesforce_administrator",
]

# Example message to send
message = "Hello! This is a test message sent using round-robin accounts and sessions."

def send_message(account, session, group, message):
	# TODO: Replace this with your actual message sending logic
	print(f"Sending from {account}/{session} to {group}: {message}")

# Prepare round-robin iterators
account_names = list(accounts.keys())
account_count = len(account_names)
session_indices = {acc: 0 for acc in account_names}

# Send to each group, rotating account and session
for i, group in enumerate(groups):
	account = account_names[i % account_count]
	sessions = accounts[account]
	session_idx = session_indices[account]
	session = sessions[session_idx]
	send_message(account, session, group, message)
	# Update session index for this account
	session_indices[account] = (session_idx + 1) % len(sessions)

# Replace the print statement with your actual Telegram/WhatsApp/etc. send logic.
