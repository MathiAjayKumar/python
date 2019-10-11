#!/usr/bin/env python
import re
import sys
import os
from datetime import datetime
import xml.etree.ElementTree as ET


curl_cmd = "/usr/bin/curl -s -k --data-binary "
TotalAppliances = 0
Cl_input = "false"
totalArgs = len(sys.argv)
MyProgName = sys.argv[0]
ApplianceList = [[]]


#------------------------------------------------------------------------------
## Functions
#------------------------------------------------------------------------------
## Perl trim function to remove whitespace from the start and end of the string
#------------------------------------------------------------------------------
def trim(str):
    str.lstrip()
    str.rstrip()
    return str


#------------------------------------------------------------------------------
## Logger function
#------------------------------------------------------------------------------
def logMessage(MyProgramName,MyMessage):
   time_v()
   print("$myTime: $MyProgramName : $MyMessage\n")

#-----------------------------------------------------------------------------
# Usage_cl provides format needs to command line operator
#-----------------------------------------------------------------------------
def usage_cl():
    print("\nUsage: xsg_backup.py [-h=<fully qualified Hostname,Environment,Realm>]\n\n")
    print(" -h= allows operator to execute backup for single appliance from command line")
    print("\n\nAdditional info: format for use of -h= should be:")
    print("\n\nxgXXXXXX.XXX.XXXX.statefarm.org,XXXX,XXXX")
    print("\n    where xgXXXXXX.XXX.XXXX.statefarm.org is the fully qualified appliance name")
    print("\n    where the second parameter ,XXXX is the Environment (test or prod)")
    print("\n    where the third parameter ,XXXX is the Realm (inf,dev,impl,perf,support)")
    print("\n    do not include spaces")
    print("\n\n\nPlease Contact WG5072 for more help with this utility")


#-----------------------------------------------------------------------------
# Function to read the Appliance input file or input argument and populate the
# list/Array
# Split TEST from PROD based on frequency of backup schedule (PROD is weekly 
# while TEST is daily)
# Parameters are optional
#-----------------------------------------------------------------------------
def ReadAppliances(helpParam):
    #Check if there are any input arguments are being passed
    #if there are no args passed ($#ARGV==-1), then read the appliances from XSGAppliances_test.txt and fill the array

    return 0
    ##Return 0 on Success

#-----------------------------------------------------------------------------
## Send request to appliance to generate backup
#-----------------------------------------------------------------------------
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
    curlCmd = curl +' '+xml_to_send+' '+ url + ' '+user
    result = os.system(curlCmd)

    #temp=substr(Dumper(result),1)

    print("$MyProgName", "CURL $curl \'$xml_to_send\' $url $user ----- TEMP: $temp ----- RESULT: $result")
    root = ET.fromstring(result)
    for fContent in root.iter('{http://www.datapower.com/schema/management}file'):
        if len(fContent.text):
            filename = re.split(r"\.",hostname)
            archiveFilename = filename[0] + ".zip"
            archiveFilePath = "/opt/automation/logs/share/datapower/var/nbk/datapower/"+archiveFilename
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

#------------------------------------------------------------------------------
# Main Code
# COMMAND LINE ACTIONS
# -h = allows operator to execute backup for single appliance from command line
# disregarding contents of XSGAppliances_test.txt (Must be fully qualified XSG
# appliance name)
#------------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Creates Date/Time stamp and appends to filename
#-----------------------------------------------------------------------------
def time_v():
    return datetime.now().strftime('%Y-%m-%d-%H%M%S')

myTime = time_v()
print(myTime)