#!/usr/bin/env python
import re
import sys
import os
from datetime import datetime
import xml.etree.ElementTree as ET


Testxml = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelop xmlns:env="http://schemes.xmlsoap.org/soap/envelop/">
<env:Body><dp:response xmlns:dp="http://www.datapower.com/schema/management">
<dp:timestamp>2019-09-25T 10:26:27-05:00</dp:timestamp>
<dp:file>sample file content</dp:file>
</dp:response>
</env:Body>
</env:Envelop>"""
    #tree = ET.parse(Testxml)
#root = ET.fromstring(Testxml)
#print(root.attrib)
#for dp in root.iter('dp:file'):
#    print(dp.tag, dp.attrib)


country_data_as_string = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelop xmlns:env="http://schemes.xmlsoap.org/soap/envelop/">
<env:Body>
<dp:response xmlns:dp="http://www.datapower.com/schema/management">
<dp:timestamp>2019-09-25T 10:26:27-05:00</dp:timestamp>
<dp:file>sample file content</dp:file>
</dp:response>
</env:Body>
</env:Envelop>"""

root = ET.fromstring(country_data_as_string)
#for yup in root.iter('{http://www.datapower.com/schema/management}file'):
#    if len(yup.text):
#        f = open("/opt/automation/logs/share/datapower/var/nbk/datapower/archiveFilename.txt","w+")
#        f.write(yup.text)
#        f.close()
#        print(yup.attrib, yup.text)


def createbkup(hostname, userName,hostType):
    userName = re.sub(r"\s+", "", userName)
    ## Build fully qualified URL https://xg95ss01.opr.test.statefarm.org:5150
    url = "https://"+hostname+":5150"

    ## Match admin account with encrypted password for use in curl command

    user = ''#getCredentials(userName,hostType)

    xml_to_send="""
        <?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management">
        <dp:do-backup format="ZIP">
        <dp:domain name="all-domains"/>
        </dp:do-backup>
        </dp:request>
        </soapenv:Body>
        </soapenv:Envelope>
    """

    # Send XML command to appliance and capture response
    # $curl is a global variable
    #logMessage( "$MyProgName","CURL Command: $curl \'$xml_to_send\' $url $user\n");
    curl="/usr/bin/curl -s -k --data-binary "
    #curlCmd = curl +' '+xml_to_send+' '+ url + ' '+user
    #result = os.system(curlCmd)

    #temp=substr(Dumper(result),1)

    print("$MyProgName", "CURL $curl \'$xml_to_send\' $url $user ----- TEMP: $temp ----- RESULT: $result")
    result = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelop xmlns:env="http://schemes.xmlsoap.org/soap/envelop/">
<env:Body>
<dp:response xmlns:dp="http://www.datapower.com/schema/management">
<dp:timestamp>2019-09-25T 10:26:27-05:00</dp:timestamp>
<dp:file>sample file content</dp:file>
</dp:response>
</env:Body>
</env:Envelop>"""
    root = ET.fromstring(result)
    for fContent in root.iter('{http://www.datapower.com/schema/management}file'):
        if len(fContent.text):
            filename = re.split(r"\.",hostname)
            #archiveFilename = filename[0] + ".zip"
            archiveFilename = filename[0] + ".txt"
            archiveFilePath = archiveFilename
            print(archiveFilename)
            #archiveFilePath = "/opt/automation/logs/share/datapower/var/nbk/datapower/"+archiveFilename
            f = open("%s" % archiveFilePath,"w+")
            f.write(fContent.text)
            f.close()
            print(fContent.attrib, fContent.text)
            if(os.path.isfile(archiveFilePath)):
                print("sucess")
                #logMessage( "$MyProgName", "$ApplianceList[$i][0],$ApplianceList[$i][1],$ApplianceList[$i][2] Backup - Passed File Check")
            else:
                print("fail 1")
                #logMessage( "$MyProgName", "$ApplianceList[$i][0],$ApplianceList[$i][1],$ApplianceList[$i][2] Backup $filename - FAILED (Backup file does not exist)")
                return 0
        else:
            print("fail 2")
            #logMessage( "$MyProgName", "$ApplianceList[$i][0],$ApplianceList[$i][1],$ApplianceList[$i][2] Backup - FAILED (Could not process result. DP Result is blank)")
            return 1

hostname = "xi71dx01.opr.test.statefarm.org"
userName = "autobackup"
hostType = 'xsg'
createbkup(hostname,userName,hostType)