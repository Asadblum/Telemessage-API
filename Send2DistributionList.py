import requests
import xml.etree.ElementTree as ET
import getpass

url = 'https://xml.telemessage.com/partners/xmlMessage.jsp'

# build xml content for a simple message
# https://www.telemessage.com/developer/send-a-message-7/#Simple%20text%20Message 
def buildXML(username, password, subject, messageContent, DLIndex):
    doc = '''<?xml version="1.0" encoding="UTF-8" ?>
    <TELEMESSAGE>
        <TELEMESSAGE_CONTENT>
            <MESSAGE>
                <MESSAGE_INFORMATION>
                    <SUBJECT>{sub}</SUBJECT>
                </MESSAGE_INFORMATION>
                <USER_FROM>
                    <CIML>
                        <NAML>
                            <LOGIN_DETAILS>
                                <USER_NAME>{user}</USER_NAME>
                                <PASSWORD>{pwd}</PASSWORD>
                            </LOGIN_DETAILS>
                        </NAML>
                    </CIML>
                </USER_FROM>
                <MESSAGE_CONTENT>
                    <TEXT_MESSAGE>
                        <MESSAGE_INDEX>0</MESSAGE_INDEX>
                        <TEXT>{content}</TEXT>
                    </TEXT_MESSAGE>
                </MESSAGE_CONTENT>
                <USER_TO>
                    <CIML_INDEX>
                        <DEVICE_TYPE DEVICE_TYPE="SMS"/>
                        <VISIBILITY>SHARED</VISIBILITY>
    		<CONTACT_INDEX CONTACT_TYPE="DISTRIBUTION">{index}</CONTACT_INDEX>
    		</CIML_INDEX>
                </USER_TO>
            </MESSAGE>
        </TELEMESSAGE_CONTENT>
        <VERSION>1.6</VERSION>
    </TELEMESSAGE>
    '''.format(sub=subject, user=username, pwd=password, content=messageContent, index=DLIndex)
    
    return doc

# input variables
user = input("Username:")
pwd = getpass.getpass("Password:")
subject = input("SMS Subject:")
content = input("SMS Content:")
index =input("Distribution List Index:")

# function call to create xml strinh
doc = buildXML(user,pwd,subject,content,index)
headers = {'Content-Type': 'text/xml'}
# posting xml request 
response =  requests.post(url, data=doc, headers=headers)
# converting the response to XML format
xmlResponse = ET.fromstring(response.text)
# extracting the values from xml and assiging them to local variabels 
for child in xmlResponse.iter():
    if child.tag == 'MESSAGE_ID':
        MsgId = child.text
    if child.tag == 'MESSAGE_KEY':
        MsgKey = child.text
    if child.tag == 'RESPONSE_STATUS_DESC':
        MsgDescription = child.text
# if we got 200 request => printing the value of the message id and key
if response.ok:
    print(MsgDescription)
    print('Message ID:',MsgId)
    print('Message Key:',MsgKey)