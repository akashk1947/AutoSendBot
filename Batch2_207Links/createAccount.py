# pip install telethon
# python createAccount.py

"""
createAccount.py
================
Run this script to scaffold a complete new bot account folder.

Usage:
    python createAccount.py

You will be prompted for:
  - Mobile number (e.g. +919876541234)
  - API ID
  - API Hash

The script creates:
    account_XXXX/           <- last 4 digits of the mobile number
        __init__.py
        api.py
        groups.txt
        should_send_message.py
        run_all_bots.py
        main.py
        common/
            __init__.py
            common_functions.py
        bot1/ .. bot10/
            start.py
"""

import os
import re
import shutil

# ─────────────────────────────────────────────
# Prompt user
# ─────────────────────────────────────────────
mobile = input("Enter mobile number (e.g. +919876541234): ").strip()
api_id  = input("Enter API ID: ").strip()
api_hash = input("Enter API Hash: ").strip()

digits_only = re.sub(r'\D', '', mobile)
last4 = digits_only[-4:]
account_name = f"account_{last4}"
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), account_name)

if os.path.exists(base_dir):
    overwrite = input(f"[WARNING] Folder '{account_name}' already exists. Overwrite? (y/n): ").strip().lower()
    if overwrite != 'y':
        print("Aborted.")
        exit(0)
    shutil.rmtree(base_dir)

os.makedirs(base_dir)
common_dir = os.path.join(base_dir, "common")
os.makedirs(common_dir)

# ─────────────────────────────────────────────
# __init__.py  (account root + common)
# ─────────────────────────────────────────────
open(os.path.join(base_dir, "__init__.py"), "w").close()
open(os.path.join(common_dir, "__init__.py"), "w").close()

# ─────────────────────────────────────────────
# api.py  — use placeholder tokens to avoid f-string conflicts
# ─────────────────────────────────────────────
api_py_template = (
'Mobile = "%%MOBILE%%"\n'
'\n'
'_api_id = %%API_ID%%\n'
'_api_hash = "%%API_HASH%%"\n'
'_session_name = "auto_send_session"\n'
'\n'
'def apiId():\n'
'    return _api_id\n'
'def apiHash():\n'
'    return _api_hash\n'
'def sessionName():\n'
'    return _session_name\n'
'\n'
'def setApiId(value):\n'
'    global _api_id\n'
'    _api_id = value\n'
'\n'
'def setApiHash(value):\n'
'    global _api_hash\n'
'    _api_hash = value\n'
'\n'
'def setSessionName(value):\n'
'    global _session_name\n'
'    _session_name = value\n'
'\n'
'KEYWORDS = [\n'
'    "proxy support",\n'
'    "interview support",\n'
'    "interview",\n'
'    "interview help",\n'
'    "support available",\n'
'    "proxy",\n'
'    "assessment",\n'
'    "exam",\n'
'    "test",\n'
'    "8106368645",\n'
']\n'
'\n'
'\n'
'FORMAT_1 = """+91 91338_17162 whatsapp only\n'
'\n'
'\U0001f4e2 Interview support\n'
'         Apttitude round support\n'
'             Online Test/Exam support \n'
'\n'
'We Cover All technologies example:\n'
'    Java | Python | Node.js | React.js | Angular .NET | Salesforce | DevOps | AWS | Azure GCP | Data Science | ML | AI | BA | Manual Testing Automation (Selenium, Cypress) ,SAP | ServiceNow SQL | Oracle | Power BI | Tableau n all\n'
'\n'
'\U0001f3a4 Proxy with advance software\n'
'Which gonna be invisible \n'
'\U0001f539 100\u2103 invisible on screen share\n'
'\U0001f539 100\u2103 invisible in task Manager\n'
'\U0001f539 100% on spot answers\n'
'\U0001f539 100\u2103 safe and secured \n'
'\n'
'\U0001f30d supported \U0001f1fa\U0001f1f8 \U0001f1ec\U0001f1e7 \U0001f1ee\U0001f1f3 \U0001f1e8\U0001f1e6 \U0001f1e6\U0001f1fa & All\n'
'\n'
'+91 91338_17162 whatsapp only"""\n'
'\n'
'FORMAT_2 = """\U0001f6a9interview support-\u203c\ufe0f\n'
'\n'
'We are providing  interview support  for below technologies\n'
'\n'
'* Python (Full Stack, Front end, Backend)\n'
'* Java ( Fullstack, Front end, Backend,)\n'
'\U0001f4cdAWS , AZURE\n'
'\U0001f4cdReact ,js\n'
'\U0001f4cdData Engineer\n'
'\U0001f4cdData Analyst \n'
'\U0001f4cdSQL/Power BI/ selenium \n'
'\U0001f4cdData science\n'
'\U0001f4cdTableau\n'
'\U0001f4cdService Now, Salesforce\n'
'\U0001f4cdETL Testing, QA manual, QA Automation\n'
'\U0001f4cdAnd All Tech Stach we cover\n'
'\n'
'and all IT certification and online Test Support.\n'
'\n'
'For INDIA,USA,UK,Canada,Australia\n'
'*(IST/CST/PST/EST time zones)*\n'
'WhatsApp Only : +91 98850_74380"""\n'
'\n'
'FORMAT_3 = """Hi everyone \U0001f44b We providing \n'
'\n'
'Interview support available for all technologies \n'
'\n'
'For:\n'
'\U0001f449 Salesforce \n'
'\U0001f449Java\n'
'\U0001f449Java full stack  \n'
'\U0001f449 C , C ++\n'
'\U0001f449Spring Boot Microservices \n'
'\U0001f449spring Hibernate \n'
'\U0001f449Dot Net\n'
'\U0001f449SAP\n'
'\U0001f449Data science \n'
'\U0001f449Aws admin\n'
'\U0001f449Aws Devops\n'
'\U0001f449Azure admin\n'
'\U0001f449Azure Data Engineer \n'
'\U0001f449Data Engineering \n'
'\U0001f449Azure devops\n'
'\U0001f449Selenium\n'
'\U0001f449Manuel Testing\n'
'\U0001f449Automation testing \n'
'\U0001f449Python\n'
'\U0001f449Python full stack \n'
'\U0001f449SQL\n'
'\U0001f449Power Bi\n'
'\U0001f449Restapi\n'
'\U0001f449Django\n'
'\U0001f449Bigdata\n'
'\U0001f449React js & node js\n'
'\U0001f449Mango DB\n'
'\U0001f449Oracle \n'
'\n'
'Online test support & Exam support also available \n'
'\n'
'WhatsApp me for more details....\n'
'+91 91338_17162"""\n'
'\n'
'FORMAT_4 = """_._._._._._._._._._._._\n'
'Interview Support \n'
'\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\u00b0\n'
'\n'
'\U0001f4cdData Science\U0001f4cdData Analyst\U0001f4cdBA\U0001f4cdETL\U0001f4cdDevops \U0001f4cdSalesforce \U0001f4cdJava\U0001f4cdPython \U0001f4cdPower bi\U0001f4cd React Angular\U0001f4cdQA\U0001f4cdAzure \U0001f4cdDot Net\U0001f4cdPL/SQL\U0001f4cdNetworking \U0001f4cdSAP\U0001f4cdService Now\U0001f4cdAI/ML and many more\n'
'\n'
'By using advance tool which is\n'
'\U0001f539 100\u2103 invisible in task Manager\n'
'\U0001f539 100\u2103 invisible on screen share\n'
'\U0001f539 100\u2103 guaranteed support\n'
'\U0001f539 100\u2103 on spot answers\n'
'\U0001f539 100\u2103 safe and secured \n'
'\n'
'For INDIA,USA,UK,Canada,Australia\n'
'*(IST/CST/PST/EST time zones)\n'
'\n'
'Whatsapp: +91 91338_17162"""\n'
'\n'
'FORMAT_5 = """Hello  All !!\n'
'\n'
'I am providing interview support\n'
'\n'
'Salesforce/ Aws/ Devops/ Azure/Python/java/service now/snowflake/oracle and All technologies \n'
'\n'
'I am handling all  India/USA/UK / Australia/Singapore/ Canada\n'
'\n'
'(All time zones)\n'
'\n'
'Ping me if you need interview help at less price..\n'
'\n'
'Assesments for interviews also available\n'
'\n'
'WhatsApp me on \n'
'+91 98850_74380"""\n'
'\n'
'FORMAT_6 = """Hii Everyone \U0001f64b\u200d\u2640\ufe0f\n'
'\n'
'We are providing interview support for:\n'
'All technologies.\n'
'\U0001f449We are handling all time zones\n'
'\u2728US\n'
'\u2728UK\n'
'\u2728INDIA\n'
'\u2728CANADA\n'
'\u2728AUSTRALIA\n'
'\u2728SINGAPORE\n'
'\u2728Malaysia\n'
'\u2728Egypt\n'
'\u2728Britain\n'
'\u2728Bangladesh\n'
'\u2728China\n'
'\u2728Indonesia\n'
'\u2728Argentina\n'
'\u2728Pakistan\n'
'\u2728Dubai\n'
'\u2728France\n'
'\u2728Germany\n'
'\u2728Italy\n'
'\u2728Spain\n'
'\u2728Turkey\n'
'\u2728Netherlands\n'
'\u2728Russia\n'
'\u2728Japan\n'
'\u2728And All\n'
'\n'
'For more details ping me or\n'
'DM on WhatsApp\n'
'+91 91338_17162"""\n'
'\n'
'Format_7 = """\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n'
'\U0001f680 READY TO MASTER YOUR IT INTERVIEW? \U0001f680\n'
'\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n'
'\n'
'\U0001f4bc INTERVIEW PROXIES & SUPPORT\n'
'\U0001f539 All Domains Covered \u2013 IT, Software, Data, Cloud, Testing, and more!\n'
'\U0001f539 Nominal Fees \u2013 Affordable, transparent pricing for every candidate.\n'
'\U0001f539 \U0001f3af 100% SUCCESS RATE \u2013 Proven track record with real testimonials.\n'
'\U0001f539 \U0001f30d Supported: \U0001f1fa\U0001f1f8 USA | \U0001f1ec\U0001f1e7 UK | \U0001f1ee\U0001f1f3 India | \U0001f1e8\U0001f1e6 Canada | \U0001f1e6\U0001f1fa Australia & All Countries\n'
'\U0001f539 Demos available before the call \u2013 Experience our process firsthand.\n'
'\U0001f539 Personalized guidance for every interview scenario.\n'
'\n'
'\u2705 Real-time rounds \u2013 Live support during your interview sessions.\n'
'\u2705 Confidential & Proven \u2013 Your privacy and success are our top priorities.\n'
'\u2705 Expert mentors with years of industry experience.\n'
'\u2705 Step-by-step preparation for technical, HR, and managerial rounds.\n'
'\n'
'\u26a1 Limited Slots \u2014 Act NOW!\n'
'\n'
'\U0001f4e2 Don\'t miss out! Get ready for your dream job with our exclusive proxy and interview support.\n'
'\n'
'\n'
'DM "BOOK" to secure your slot: +91-98850_74380\n'
'\n'
'\n'
'#ITPrep #TechTalk #CareerBoos #JobSuccess #InterviewSupport"""\n'
'\n'
'Format_8 = """\n'
'\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n'
'\U0001f31f ACE YOUR IT INTERVIEW WITH EXPERT SUPPORT! \U0001f31f\n'
'\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n'
'\n'
'\U0001f6e1\ufe0f INTERVIEW ASSISTANCE & PROXY SERVICES\n'
'\u2022 All IT Domains & Technologies Supported\n'
'\u2022 Affordable, transparent pricing for every candidate\n'
'\u2022 \U0001f3c6 99% Success Rate \u2013 Trusted by professionals worldwide\n'
'\u2022 \U0001f30f Global Coverage: \U0001f1fa\U0001f1f8 \U0001f1ec\U0001f1e7 \U0001f1ee\U0001f1f3 \U0001f1e8\U0001f1e6 \U0001f1e6\U0001f1fa \U0001f1f8\U0001f1ec \U0001f1e9\U0001f1ea \U0001f1eb\U0001f1f7 & more\n'
'\u2022 Free demo sessions before your interview\n'
'\u2022 Customized strategies for technical, HR, and managerial rounds\n'
'\n'
'\u2705 Real-time guidance during interviews\n'
'\u2705 Confidential, secure, and proven methods\n'
'\u2705 Experienced mentors with industry expertise\n'
'\u2705 Mock interviews, live feedback, and exam support\n'
'\n'
'\U0001f6a8 Limited slots available \u2013 Reserve yours now!\n'
'\n'
'\U0001f4ac Message "PREPARE" to book your session: +91-91338_17162\n'
'\n'
'#ITSuccess #InterviewPrep #GlobalSupport #CareerGrowth #TechMentors\n'
'"""\n'
'\n'
'Format_9 = """\n'
'\U0001f4a1 Unlock Your IT Career \u2014 Interview Success Awaits!\n'
'\n'
'\U0001f9e9 What We Offer:\n'
'\u2022 Personalized Interview Coaching for Every Tech Role\n'
'\u2022 Real-time Proxy Assistance \u2014 Seamless, Secure, and Discreet\n'
'\u2022 Interactive Practice Sessions & Live Q&A\n'
'\u2022 Global Reach: USA, UK, India, Canada, Australia, Singapore, Europe & More\n'
'\u2022 Transparent Pricing \u2014 No Hidden Fees\n'
'\u2022 Demo Before You Commit \u2014 Try Us Risk-Free!\n'
'\n'
'\U0001f393 Supported Technologies:\n'
'- Cloud, DevOps, Data Science, AI/ML, Web & Mobile, QA, ERP, Cybersecurity, and all trending stacks\n'
'\n'
'\U0001f512 Why Choose Us?\n'
'\u2022 1-on-1 Guidance from Industry Experts\n'
'\u2022 Confidentiality Guaranteed\n'
'\u2022 Success Stories from Hundreds of Candidates\n'
'\u2022 Flexible Scheduling \u2014 We Adapt to Your Time Zone\n'
'\n'
'\U0001f680 Ready to Get Started?\n'
'Whatsapp for your exclusive slot!\n'
'+91-98850_74380"""\n'
'\n'
'Format_10 = """\n'
'\U0001f9be Revolutionize Your Interview Journey \u2014 Stand Out & Succeed!\n'
'\n'
'\U0001f514 New-Age Interview Proxy & Support Service\n'
'\n'
'What Sets Us Apart?\n'
'\u2022 AI-powered coaching for every IT domain\n'
'\u2022 Real-time proxy support \u2014 online & offline\n'
'\u2022 Gamified mock interviews for skill mastery\n'
'\u2022 Global coverage: All time zones, all countries\n'
'\u2022 Free trial session \u2014 see the difference\n'
'\u2022 Hyderabad in-person support available\n'
'\u2022 Monthly, unlimited, and custom packages\n'
'\u2022 Work support, exam prep, certifications, and BGV docs\n'
'\n'
'\U0001f310 Supported Technologies:\n'
'Cloud, DevOps, Data Science, AI/ML, Web, Mobile, ERP, Cybersecurity, and more\n'
'\n'
'\U0001f6e1\ufe0f Why Us?\n'
'\u2022 Confidential, secure, and ethical\n'
'\u2022 Transparent pricing \u2014 no surprises\n'
'\u2022 End-to-end guidance: resume to offer letter\n'
'\u2022 Only for genuine, committed candidates\n'
'\u2022 No time-wasters \u2014 serious inquiries only\n'
'\n'
'Ready to transform your career?\n'
'DM "WINNER" to +91 91338_17162 and claim your slot!\n'
'\n'
'#AIInterview #ProxySupport #CareerUpgrade #GlobalMentors #Hyderabad #SkillMastery #OfferLetter #BGV #NoTimeWasting\n'
'"""\n'
'\n'
'Format_11 = """\U0001f31f Ace Your Next Interview Without Breaking the Bank! \U0001f31f\n'
'\n'
'\U0001f4b8 Stop Overpaying for Interview Help \u2013 Get Expert Support at a Fraction of the Cost!\n'
'\n'
'\U0001f517 Connect Directly \u2013 No Agents, No Extra Fees, No Hassle.\n'
'\n'
'\U0001f6e1\ufe0f Transparent Pricing | Flexible Plans | Real-Time Guidance\n'
'\n'
'\U0001f680 Ready for Multiple Interviews? Try Our Monthly Mentorship \u2013 Unlimited Support, One Simple Fee!\n'
'\n'
'\U0001f4bc Technologies We Cover:\n'
'\n'
'Frontend: React, Angular, JS, TS\n'
'Backend: Java, Python, .NET, Node, Spring Boot\n'
'Full Stack: MERN, MEAN, Java/.NET\n'
'Cloud & DevOps: AWS, Azure, GCP, Docker, K8s, Jenkins\n'
'Data: SQL, Power BI, Tableau, AI, Data Science\n'
'Testing: Selenium, Cypress, Manual\n'
'Enterprise: Salesforce, ServiceNow, SAP, Oracle, Power Apps, React Native\n'
'\u2728 Why Us?\n'
'\n'
'Direct, Confidential Support\n'
'Flexible Scheduling Worldwide\n'
'No Recruiter Can Catch You\n'
'\U0001f4f2 WhatsApp: +91 98850_74380"""\n'
'\n'
'FORMAT_12 = """\U0001f6a9 \U0001f6a9*Interview support and work support* \U0001f6a9\U0001f6a9\n'
'\n'
'We provide \U0001f447\n'
'\n'
'\U0001f4d8 Online Training\n'
'\U0001f4d7 Job Support\n'
'\U0001f4d9 Interview Support\n'
'\U0001f4d5 Assessment Support\n'
'\n'
'\u2699\ufe0f Technologies:\n'
'\n'
'\U0001f539 Data Engineering | Data Analytics | Data Science\n'
'\U0001f539 Business Analysis | QA | Testing\n'
'\U0001f539 Java | Python | DotNet | Fullstack\n'
'\U0001f539 AWS | Azure | DevOps\n'
'\U0001f539 Salesforce | ServiceNow | Workday\n'
'\U0001f539 Power BI | Tableau\n'
'\U0001f539 Cyber Security | Networking\n'
'\U0001f539 Oracle | PL/SQL | Snowflake\n'
'\U0001f539 Tosca | SAP | Big Data\n'
'\U0001f539 And All Technologies\n'
'\n'
'\U0001f30f Locations Covered: India | USA | UK | Canada | Australia\n'
'\U0001f552 All Time Zones Available (IST / CST / EST / PST)\n'
'\n'
'\U0001f4de WhatsApp :- *+91 91338_17162*\n'
'\n'
'\U0001f449 Low prices \u2013 Best support\n'
'\n'
'Thank you \U0001f64f"""\n'
'\n'
'def formats():\n'
'    return [FORMAT_1, FORMAT_2, FORMAT_3, FORMAT_4, FORMAT_5, FORMAT_6, Format_7, Format_8, Format_9, Format_10, Format_11, FORMAT_12]\n'
)
api_py = api_py_template.replace("%%MOBILE%%", mobile).replace("%%API_ID%%", api_id).replace("%%API_HASH%%", api_hash)
with open(os.path.join(base_dir, "api.py"), "w", encoding="utf-8") as f:
    f.write(api_py)

# ─────────────────────────────────────────────
# groups.txt  (empty, user fills this in)
# ─────────────────────────────────────────────
with open(os.path.join(base_dir, "groups.txt"), "w", encoding="utf-8") as f:
    f.write("# Add your Telegram group links here, one per line\n")
    f.write("# Example:\n")
    f.write("# https://t.me/yourgroupname\n")

# ─────────────────────────────────────────────
# should_send_message.py
# ─────────────────────────────────────────────
should_send = '''def should_send_message(text, length, has_keyword):
    special_numbers = ["91338_17162", "98850_74380"]
    is_special = any(num in text.lower() for num in special_numbers)
    if is_special:
        return False
    if has_keyword or length > 250:
        return True
    return False
'''
with open(os.path.join(base_dir, "should_send_message.py"), "w", encoding="utf-8") as f:
    f.write(should_send)

# ─────────────────────────────────────────────
# common/common_functions.py
# ─────────────────────────────────────────────
common_functions = '''import os
import asyncio
import random
import threading
import time
from telethon.errors import FloodWaitError


def file_exists(path):
    return os.path.isfile(path)

def load_formats(formats_path):
    FORMATS = []
    if os.path.isfile(formats_path):
        with open(formats_path, "r", encoding="utf-8") as f:
            content = f.read()
        namespace = {}
        exec(content, namespace)
        FORMATS = [namespace.get(f\'FORMAT_{i}\') for i in range(1, 5) if f\'FORMAT_{i}\' in namespace]
        return FORMATS
    else:
        print(f"\\u26a0\\ufe0f formats file not found at {formats_path}")
        return []

def load_target_groups(groups_path, bot_id=None, total_bots=10, fromItem=0, toItem=3):
    if not os.path.isfile(groups_path):
        print(f"[WARNING] groups.txt not found at {groups_path}")
        return []

    with open(groups_path, "r", encoding="utf-8") as gf:
        all_lines = [line.strip() for line in gf if line.strip() and not line.strip().startswith("#")]

    if bot_id is not None:
        try:
            if isinstance(bot_id, str):
                digits = "".join(ch for ch in bot_id if ch.isdigit())
                if not digits:
                    print(f"[WARNING] Invalid bot_id: {bot_id}")
                    return []
                bot_number = int(digits)
            else:
                bot_number = int(bot_id)
        except Exception:
            print(f"[WARNING] Invalid bot_id: {bot_id}")
            return []

        if bot_number < 1 or bot_number > total_bots:
            print(f"[WARNING] bot_id out of range 1..{total_bots}: {bot_id}")
            return []

        total_links = len(all_lines)
        base_size = total_links // total_bots
        remainder = total_links % total_bots
        start_index = (bot_number - 1) * base_size + min(bot_number - 1, remainder)
        end_index = start_index + base_size + (1 if bot_number <= remainder else 0)
        return all_lines[start_index:end_index]

    return all_lines[fromItem:toItem]

def next_format(chat_id, last_format_index, FORMATS):
    i = last_format_index.get(chat_id, -1)
    i = (i + 1) % len(FORMATS)
    last_format_index[chat_id] = i
    return FORMATS[i]

def contains_keyword(text, KEYWORDS):
    t = text.lower()
    return any(k.lower() in t for k in KEYWORDS)

async def send_message_safe(client, chat_id, chat_title, group_link, FORMATS, last_format_index, active_groups):
    try:
        await asyncio.sleep(random.randint(5, 15))
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            print(f"\\u23ed Skipped (already last): {group_link}")
            return
        msg = next_format(chat_id, last_format_index, FORMATS)
        await client.send_message(chat_id, msg)
        print(f"\\u2705 Sent in: {group_link}")
    except FloodWaitError as e:
        print(f" Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")
    except Exception as e:
        print(f" Error in {group_link}: {e}")
    finally:
        active_groups.discard(chat_id)

def handler_factory(client, TARGET_GROUPS, KEYWORDS, should_send_message, FORMATS, last_format_index, active_groups):
    from telethon import events
    async def handler(event):
        if event.out:
            return
        if not event.is_group:
            return
        if not event.raw_text:
            return
        chat = await event.get_chat()
        if not getattr(chat, "username", None):
            return
        group_link = f"https://t.me/{chat.username}"
        if group_link not in TARGET_GROUPS:
            return
        text = event.raw_text.strip()
        length = len(text)
        has_keyword = contains_keyword(text, KEYWORDS)
        if not should_send_message(text, length, has_keyword):
            return
        gid = event.chat_id
        if gid in active_groups:
            print(f"\\u23f3 Already queued: {group_link}")
            return
        last_msg = await client.get_messages(gid, limit=1)
        if last_msg and last_msg[0].out:
            print(f"\\u23ed Skipped (our last msg): {chat.title}")
            return
        active_groups.add(gid)
        asyncio.create_task(
            send_message_safe(client, gid, chat.title, group_link, FORMATS, last_format_index, active_groups)
        )
    return handler
'''
with open(os.path.join(common_dir, "common_functions.py"), "w", encoding="utf-8") as f:
    f.write(common_functions)

# ─────────────────────────────────────────────
# run_all_bots.py
# ─────────────────────────────────────────────
run_all = '''import subprocess
import os

workspace_root = os.path.dirname(os.path.abspath(__file__))
bot_dirs = [f\'bot{i}\' for i in range(1, 11)]
processes = []

for bot_dir in bot_dirs:
    start_py = os.path.join(workspace_root, bot_dir, \'start.py\')
    env = os.environ.copy()
    env[\'PYTHONPATH\'] = workspace_root
    proc = subprocess.Popen(
        [\'python\', start_py],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.join(workspace_root, bot_dir),
        env=env
    )
    processes.append((bot_dir, proc))
    print(f"[START] {bot_dir} launched (PID {proc.pid})")

print("\\nAll 10 bots launched. Waiting for completion...\\n")

for bot_dir, proc in processes:
    stdout, stderr = proc.communicate()
    print(f\'\\n--- Output for {bot_dir} ---\')
    print(stdout)
    if stderr:
        print(f\'--- Errors for {bot_dir} ---\')
        print(stderr)
'''
with open(os.path.join(base_dir, "run_all_bots.py"), "w", encoding="utf-8") as f:
    f.write(run_all)

# ─────────────────────────────────────────────
# main.py  (re-generates bot1..bot10/start.py)
# ─────────────────────────────────────────────
bot_start_template = r'''
import asyncio
import random
import sys
import os
import sqlite3
import shutil
account_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(account_dir))
from telethon import TelegramClient, events
from should_send_message import should_send_message
from telethon.errors import FloodWaitError
from common.common_functions import load_target_groups, next_format, contains_keyword, send_message_safe, file_exists
parent = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
groups_path = os.path.join(os.path.dirname(parent), "groups.txt")
try:
    from api import apiId, apiHash, sessionName, KEYWORDS, formats
    api_id = apiId()
    api_hash = apiHash()
    session_name = sessionName()
    FORMATS = formats()
except Exception as e:
    print(f"[WARNING] Failed to import from api.py: {e}")
    api_id = None
    api_hash = None
    session_name = None
    KEYWORDS = None
    FORMATS = []
TARGET_GROUPS = load_target_groups(groups_path, bot_id="{BOT_ID}")
last_format_index = {}
active_groups = set()
session_base = session_name[:-8] if isinstance(session_name, str) and session_name.endswith(".session") else session_name
session_path = os.path.join(account_dir, session_base)
client = TelegramClient(session_path, api_id, api_hash)

async def start_client_with_lock_recovery():
    global client
    for _ in range(5):
        try:
            await client.start()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" not in str(e).lower():
                raise
            await asyncio.sleep(2)
    fallback_session_path = f"{session_path}_fallback_{os.getpid()}"
    src = f"{session_path}.session"
    dst = f"{fallback_session_path}.session"
    if os.path.isfile(src):
        try:
            shutil.copy2(src, dst)
        except Exception:
            pass
    print("[WARNING] Session database is locked. Using fallback session file.")
    client = TelegramClient(fallback_session_path, api_id, api_hash)
    await client.start()

async def send_message_safe(chat_id, chat_title, group_link):
    try:
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            print(f"⏭ Skipped (already last): {group_link}")
            return
        msg = next_format(chat_id, last_format_index, FORMATS)
        await client.send_message(chat_id, msg)
        print(f"[OK] Sent in: {group_link}")
        await asyncio.sleep(random.randint(30, 45))
    except FloodWaitError as e:
        print(f"[WARNING] Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")
    except Exception as e:
        print(f"[ERROR] Error in {group_link}: {e}")
    finally:
        active_groups.discard(chat_id)

@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return
    if not event.is_group:
        return
    if not event.raw_text:
        return
    chat = await event.get_chat()
    if not getattr(chat, "username", None):
        return
    group_link = f"https://t.me/{chat.username}"
    if group_link not in TARGET_GROUPS:
        return
    text = event.raw_text.strip()
    length = len(text)
    has_keyword = contains_keyword(text, KEYWORDS)
    if not should_send_message(text, length, has_keyword):
        return
    gid = event.chat_id
    if gid in active_groups:
        print(f"[INFO] Already queued: {group_link}")
        return
    last_msg = await client.get_messages(gid, limit=1)
    if last_msg and last_msg[0].out:
        print(f"[INFO] Skipped (our last msg): {chat.title}")
        return
    active_groups.add(gid)
    asyncio.create_task(
        send_message_safe(gid, chat.title, group_link)
    )

async def main():
    print("=== Starting Bot Setup ===")
    if not TARGET_GROUPS or len(FORMATS) == 0:
        print("[ERROR] Failed to load target groups or formats. Exiting.")
        return
    print(f"[OK] Setup complete. Starting bot...")
    await start_client_with_lock_recovery()
    me = await client.get_me()
    print(f"[INFO] Bot Account: {me.first_name}, Running (Selected Groups Only)")
    print("Loaded links:")
    for idx, link in enumerate(TARGET_GROUPS, 1):
        print(f"{idx}. {link}")
    print("Started Sending_ _ _ ________________________________")
    await client.run_until_disconnected()

asyncio.run(main())
'''

main_py = f'''import os

# Path setup
GROUPS_PATH = os.path.join(os.path.dirname(__file__), \'groups.txt\')
API_PATH = os.path.join(os.path.dirname(__file__), \'api.py\')

if not os.path.isfile(API_PATH):
    print(f"[ERROR] api.py not found at {{API_PATH}}")
    exit(1)
if not os.path.isfile(GROUPS_PATH):
    print(f"[ERROR] groups.txt not found at {{GROUPS_PATH}}")
    exit(1)

num_bots = 10

bot_code = {repr(bot_start_template)}

for i in range(1, num_bots + 1):
    bot_dir = os.path.join(os.path.dirname(__file__), f\'bot{{i}}\')
    os.makedirs(bot_dir, exist_ok=True)
    start_path = os.path.join(bot_dir, \'start.py\')
    code = bot_code.replace("{{BOT_ID}}", f\'bot{{i}}\')
    with open(start_path, \'w\', encoding=\'utf-8\') as sf:
        sf.write(code)
    print(f"[OK] Generated {{bot_dir}}/start.py")

print(f"\\n[DONE] All {{num_bots}} bot files generated for this account.")
'''
with open(os.path.join(base_dir, "main.py"), "w", encoding="utf-8") as f:
    f.write(main_py)

# ─────────────────────────────────────────────
# Generate bot1..bot10/start.py immediately
# ─────────────────────────────────────────────
for i in range(1, 11):
    bot_dir = os.path.join(base_dir, f"bot{i}")
    os.makedirs(bot_dir, exist_ok=True)
    code = bot_start_template.replace("{BOT_ID}", f"bot{i}")
    with open(os.path.join(bot_dir, "start.py"), "w", encoding="utf-8") as f:
        f.write(code)

# ─────────────────────────────────────────────
print(f"""
================================================
✅  Account folder created successfully!

  Folder : {base_dir}

Next steps:
  1. Add your Telegram group links to:
       {os.path.join(base_dir, 'groups.txt')}
     (one link per line, e.g. https://t.me/groupname)

  2. To run all 10 bots at once:
       cd {base_dir}
       python run_all_bots.py

  3. To run a single bot:
       cd {os.path.join(base_dir, 'bot1')}
       python start.py

  4. If you update groups.txt later, re-run:
       python main.py   (inside the account folder)
     to redistribute links across bots.
================================================
""")
