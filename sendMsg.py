# -*- coding: utf8 -*-

'''
Created on 2014-11-26

@author: zhanghl
'''
import re
import urllib2

if __name__ == '__main__':
    pass

str = 'Created: ${voicemail_time}'
str += ';From: ${voicemail_caller_id_number}'
str += ';Duration: ${voicemail_message_len}'
str += ';Account: ${voicemail_account}@${voicemail_domain}'



print str

print '=-==================================='


#取匹配信息
def getInfo(messageStr):
    pattern = re.compile(r'Created: (.*);From: (.*);Duration: (.*);Account: (.*)')
    match = pattern.match(messageStr)
    result = {};
    if match:
        print '--------------------------'
        result['created']=match.group(1)
        result['from']=match.group(2)
        result['duration']=match.group(3)
        result['account']=match.group(4)
        
        print result
        
    return result
# 发送通知
def openUrl(info,url):
    if any(info):
        url += '?created=' + info['created']
        url += '&from' + info['from']
        url += '&duration' + info['duration']
        url += '&account' + info['account']
    
    print "url:" + url
    data = urllib2.urlopen(url).read()
    print data
          
    

#d = getInfo(str)
#openUrl(d, "http://1111")

messageStr = 'adfa'
messageStr += ''
messageStr += ''
messageStr += '--000XXX000'
messageStr += '\r\nContent-Type: text/plain; charset=ISO-8859-1; Format=Flowed'
messageStr += '\r\nContent-Disposition: inline'
messageStr += '\r\nContent-Transfer-Encoding: 7bit'
messageStr += '\r\n'
messageStr += '\r\nCreated: Wednesday, November 26 2014, 04 45 PM'
messageStr += '\r\nFrom: "Extension 1002" <1002>'
messageStr += '\r\nDuration: 00:00:03'
messageStr += '\r\nAccount: 1015@172.30.91.190'

messageStr = messageStr.replace('\r\n',';')

pp = re.compile(r'.*Created: (.*);From: (.*);Duration: (.*);Account: (.*).*')
matcher = pp.match(messageStr)
if matcher:
    print matcher.group(1)
    print matcher.group(2)
    print matcher.group(3)
    print matcher.group(4)
