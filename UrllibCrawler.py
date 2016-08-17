#!/usr/bin/env python
#coding=utf-8

'''
    python爬虫 : urllib2
'''
import urllib
import urllib2
import cookielib
import traceback
import sys

reload(sys) 
sys.setdefaultencoding('utf8')

class UrllibCrawler(object):

    def __init__(self, headers = {},debug = True, p = ''):
        #timeout 
        self.timeout=5
        #cookie handler
        self.cookie_processor = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
      
        #debug handler
        self.debug = debug
        if self.debug:
            self.httpHandler = urllib2.HTTPHandler(debuglevel=1)
            self.httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        else:
            self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
            self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
         
        #proxy handler (http)
        if p != '' and p != 'None' and p != None and p != 'NULL':
            self.proxy_handler = urllib2.ProxyHandler({'http': p})
        else:
            self.proxy_handler = urllib2.ProxyHandler({})
 
        #opener
        self.opener = urllib2.build_opener( self.cookie_processor,self.proxy_handler, self.httpHandler, self.httpsHandler)
        
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'),]
       
        #header
        for key in headers.keys():
            cur=self._replace(key)
            if cur!=-1:
                self.opener.addheaders.pop(cur)

            self.opener.addheaders += [(key, headers[key]), ]
    

    def add_referer(self, referer):
        cur=self._replace('Referer')
        if cur!=-1:
            self.opener.addheaders.pop(cur)
        self.opener.addheaders+=[('Referer',referer),]
      
    def add_header(self, headers = {}):
        for key in headers.keys():
            cur=self._replace(key)
            if cur!=-1:
                self.opener.addheaders.pop(cur)
            self.opener.addheaders += [(key, headers[key]), ]

    def _replace(self,key):
        cur=0
        for header in self.opener.addheaders:
            if header[0]==key:
                return cur
            cur+=1
        return -1

    #get
    def get(self, url, paras = {}, html_flag = False):
        html = ''
        for key in paras.keys():
            url += key + '=' + paras[key] + '&'
        if len(url) > 0 and len(paras) > 0:
            url = url[0:-1]
        try:
            print url
            resp = self.opener.open(url,timeout=self.timeout)
            if html_flag:
                html = resp.read()
        except Exception, e:
            if self.debug:
                print e

        return html

    #post
    def post(self, url, paras = {}, html_flag = False):
        html = ''
        req = urllib2.Request(url)  
        datas = urllib.urlencode(paras)  
        try:
            print url
            resp = self.opener.open(req, datas,timeout=self.timeout)
            if html_flag:
                html = resp.read()
        except Exception, e:
            if self.debug:
                print e

        return html


if __name__ == '__main__':

    try:
        headers={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
        }
        mc = UrllibCrawler(debug=True)
        mc.add_header(headers)
        
        page1=mc.get('http://sep.ucas.ac.cn/',html_flag=True)
        #print page1
        mc.add_referer('http://sep.ucas.ac.cn/')
        data={
            'userName':'xxxxxx',
            'pwd':'xxxxxx',
            'sb':'sb'
        }
        page2=mc.post('http://sep.ucas.ac.cn/slogin',paras=data,html_flag=True)
        #print page2
    except Exception, e:
        #raise e
        traceback.print_exc()  
   
    
   
    
   