#!/usr/bin/env python
#coding=utf-8

'''
    python爬虫 : requests
'''
import requests
import traceback
import sys

reload(sys) 
sys.setdefaultencoding('utf8')

class RequestsCrawler(object):

    def __init__(self, headers = {},debug = True, p = ''):
        self._allow_redirects=True
        self._verify=True
        self.debug=debug
        self.timeout=5
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
        }
        #header
        self.headers.update(headers)
        self.proxies={}
        if p!='':             
            self.proxies={
                'http':p,
                'https':p
            }

        self.s=requests.Session()

    def set_debug(self,debug):
        self.debug=debug

    def add_referer(self, referer):
        if referer!=None and referer!='':
            self.headers.update({'Referer':referer})

    def add_header(self, headers = {}):
        self.headers.update(headers)

    def set_proxy(self, p=''):
        if p!='':             
            self.proxies={
                'http':p,
                'https':p
            }
    #get
    def get(self, url, paras = {}, html_flag = False):
        ret = ''
        try:
            print 'get : '+url,
            req = requests.Request('GET', url,params=paras,headers=self.headers)
            prepped=self.s.prepare_request(req)
            r=self.s.send(prepped, proxies=self.proxies,allow_redirects=self._allow_redirects,verify=self._verify,timeout=self.timeout)
            if self.debug:
                print ''
                if len(r.history)!=0:
                    #whether redirect or not
                    for _r in r.history:
                        for header in _r.request.headers:
                            print 'request : '+header+' : '+_r.request.headers[header]
                        print ''
                        print 'replay :'+str(_r.status_code)
                        for header in _r.headers:
                            print 'response : '+header+' : '+_r.headers[header]
                print ''
                for header in r.request.headers:
                    print 'request : '+header+' : '+r.request.headers[header]
                print ''
                print 'replay :'+str(r.status_code)
                for header in r.headers:
                    print 'response : '+header+' : '+r.headers[header]
            print ''
            if html_flag:
                ret = r.content

        except Exception, e:
            if self.debug:
                print e
                #traceback.print_exc()

        return ret


    #post
    def post(self, url, paras = {}, html_flag = False):
        ret = ''
        try:
            print 'post : '+url
            post_data=''
            for i in  paras:
                post_data+=i+'='+paras[i]+'&'
            print post_data[0:-1]

            req = requests.Request('POST', url,data=paras,headers=self.headers)
            prepped=self.s.prepare_request(req)
            r=self.s.send(prepped, proxies=self.proxies,allow_redirects=self._allow_redirects,verify=self._verify,timeout=self.timeout)
            if self.debug:
                print ''
                if len(r.history)!=0:
                    #whether redirect or not
                    for _r in r.history:
                        for header in _r.request.headers:
                            print 'request : '+header+' : '+_r.request.headers[header]
                        print ''
                        print 'replay :'+str(_r.status_code)
                        for header in _r.headers:
                            print 'response : '+header+' : '+_r.headers[header]
                print ''
                for header in r.request.headers:
                    print 'request : '+header+' : '+r.request.headers[header]
                print ''
                print 'replay :'+str(r.status_code)
                for header in r.headers:
                    print 'response : '+header+' : '+r.headers[header]
            print ''
            if html_flag:
                ret = r.content

        except Exception, e:
            if self.debug:
                print e
                #traceback.print_exc()

        return ret



if __name__ == '__main__':

    try:
        headers={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
        }
        mc = RequestsCrawler(debug=False)
        mc.add_header(headers)
        #mc.set_proxy('127.0.0.1:8080')
        mc.set_debug(True)
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
   
    
   