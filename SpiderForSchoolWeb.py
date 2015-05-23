# coding=utf-8
# Author : Jammgit
# built in : 2015/5/17


import http.cookiejar as cookiejar
import urllib.request
import urllib.parse
import re
import sys
import os
import threading


# the login web'd format is ?xh=xxx&xm=xxx&gnmkdm=Nxxx

authUrl = 'http://jwgl.gdut.edu.cn/CheckCode.aspx?'
loginUrl = 'http://jwgl.gdut.edu.cn/default2.aspx?'

# there need to add some form data for student
# gnmkdm=N121605
scoreUrl = 'http://jwgl.gdut.edu.cn/xscj.aspx?'

# it is not legal to add Chinese in url , we can use urllib.request.urkencode to add it in url
# cjUrl = 'http://jwgl.gdut.edu.cn/xscj.aspx?xh=3113006314&xm=%BD%AD%CE%B0%C1%D8&gnmkdm=N121605'
evaluateUrl = 'http://jwgl.gdut.edu.cn/xsjxpj.aspx?'

# gnmkdm=N121603
scheduleUrl = 'http://jwgl.gdut.edu.cn/xskbcx.aspx?'


class CSpiderSchoolWeb:
	def __init__(self):
		

		# init the cookie , add the support of cookie
		cookie = cookiejar.CookieJar()
		self.cookieOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
		urllib.request.install_opener(self.cookieOpener)
		
		# add headers for cookie
		self.cookieOpener.addheaders.append(('Referer','http://jwgl.gdut.edu.cn/'))
		self.cookieOpener.addheaders.append(('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'))
		self.cookieOpener.addheaders.append(('Host','jwgl.gdut.edu.cn'))
		self.cookieOpener.addheaders.append(('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'))
		self.cookieOpener.addheaders.append(('Connection','keep-alive'))
		self.cookieOpener.addheaders.append(('Cache-Control','private'))
		self.cookieOpener.addheaders.append(('Content-Type','text/html; charset=gb2312'))
		self.cookieOpener.addheaders.append(('Date','Thu, 14 May 2015 01:28:09 GMT'))
		#self.cookieOpener.addheaders.append(('Location','/xs_main.aspx?xh=xxxxx'))
		self.cookieOpener.addheaders.append(('Server','Microsoft-IIS/6.0'))
		self.cookieOpener.addheaders.append(('X-AspNet-Version','1.1.4322'))
		self.cookieOpener.addheaders.append(('X-Powered-By','ASP.NET'))
		self.cookieOpener.addheaders.append(('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
		self.cookieOpener.addheaders.append(('Accept-Encoding','gzip, deflate'))
		# self.headers = {
			# 'Referer','http://jwgl.gdut.edu.cn/',
			# 'User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
			# 'Host','jwgl.gdut.edu.cn',
			# 'Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			# 'Connection','keep-alive',
			# 'Cache-Control','private',
			# 'Content-Type','text/html; charset=gb2312',
			# 'Date','Thu, 14 May 2015 01:28:09 GMT',
			# 'Location','/xs_main.aspx?xh='+ self.userName,
			# 'Server','Microsoft-IIS/6.0',
			# 'X-AspNet-Version','1.1.4322',
			# 'X-Powered-By','ASP.NET',
			# 'Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			# 'Accept-Encoding','gzip, deflate'
		# }
		# in the form , __VIEWSTATE is variable
		self.reViewState = re.compile(r'name=\"__VIEWSTATE\" value=\"(.*?)\" />')
		
	def getAuthCode( self ):
		self.__storeImage( self.cookieOpener , authUrl )
		# open the authcode with DOS
		# self.__storeImage()
		# openImageThread = threading.Thread( target = self.__openImage , name = 'OpenImageThread' )
		# openImageThread.start()
		# openImageThread.join()
		
	def loginSchoolWeb(self , userName , passwd , authCode ):
		self.userName = userName
		self.passwd = passwd
		
		# get the value of __VIEWSTATE
		loginPage = self.cookieOpener.open(urllib.request.Request( loginUrl )).read()

		viewState = self.reViewState.findall(loginPage.decode('gb2312'))

		# authCode = input("Please input Verification Code:")
		
		#print('Logining the school web ... ')
		
		data = {
			'__VIEWSTATE':viewState[0],
			'txtUserName':self.userName,
			'TextBox2':self.passwd,
			'txtSecretCode':authCode,
			'RadioButtonList1':'学生',
			'Button1':'',
			'lbLanguage':'',
			'hidPdrs':'',
			'hidsc':''
		}
		# 
		# build form data
		encodeData = urllib.parse.urlencode( data , encoding = 'gb2312' )
		# use the reserved cookie open url
		loginPage = self.cookieOpener.open( urllib.request.Request( loginUrl , encodeData.encode('utf-8') ) )
		

		pageSource = loginPage.read().decode('gb2312')
		# scrawl the student name			
		scoreUrlAdd = re.compile(r'([^\"<]*)\" target=\'zhuti\'.*?\'成绩查询').findall(pageSource)
		self.xm = re.compile('xm=(.*?)&gnmkdm').findall(scoreUrlAdd[0])
		
		#print('Login success!')
		# according to the xn and xq ，setting the sum of threading
		self.threadList = self.__setThread()
		self.__startThread( self.threadList )
		#self.__getStudentScore()
		
	def getStudentGradeAndSem(self):
		if not self.xn:
			return -1 
		else :
			return ( self.xn , self.xq )
		
	def __setThread(self):
		#print('Be scrawling scores ...')
		urlAdd = {
			'xh' : self.userName,
			'xm' : self.xm,
			'gnmkdm' : 'N121605'
		}
		# get viewState's value
		scorePage = self.cookieOpener.open( urllib.request.Request\
					(scoreUrl + urllib.parse.urlencode(urlAdd , encoding = 'gb2312') ) ).read()
					
		viewState = self.reViewState.findall( scorePage.decode('gb2312') )
		
		(xn , xq) = self.__getStudentGradeAndSemester()
		
		# create threading
		threadList = []
		for sxn in xn:
			if sxn == xn[0]:
				xq = int(xq[0])
			else:
				xq = 2
			sxq = 1
			while sxq <= xq :
				if sxn == xn[0]:
					thread = threading.Thread( target = self.__threadingForScrawlScore ,
												args = [ sxn , sxq , viewState[0] , 1] ,
												name = '{0}grade{1}semThread'.format(
												sxn , sxq))
				else:
					thread = threading.Thread( target = self.__threadingForScrawlScore ,
												args = [ sxn , sxq , viewState[0] ] ,
												name = '{0}grade{1}semThread'.format(
												sxn , sxq))					
				threadList.append(thread)
				sxq = sxq + 1
		return threadList
		
	def __startThread(self , threadList ):
		if not threadList:
			return -1
		# start thread
		for thread in threadList :
			thread.start()
		# make main func in waiting the child thread	
		for thread in threadList :
			thread.join()
			
	def __threadingForScrawlScore( self , xn , xq ,viewState , GETCLASSATTR = 0):			
		self.__getStudentScore( xn , xq , viewState , GETCLASSATTR )
		
	def __storeImage(self , cookieOpener , authUrl):
		authImg = self.cookieOpener.open(urllib.request.Request( authUrl )).read()
		with open('image.gif','wb') as file:
			file.write(authImg)		
		
	def __storeWebPage(self , webOpened , txtName ):
		with open(txtName , 'w') as file:
			file.write(webOpened.read().decode('gb2312'))
			file.flush()
			
	def __openImage(self):
		os.system(r'image.gif')

	def __getStudentGradeAndSemester(self ):
	
		urlAdd = {
			'xh' : self.userName ,
			'xm' : self.xm ,
			'gnmkdm' : 'N121603'
		}
		# when have no the form data , server return the current grade , but I just use two information
		schedule = self.cookieOpener.open( urllib.request.Request\
					( scheduleUrl + urllib.parse.urlencode(urlAdd) ) )
		scheduleData = schedule.read().decode('gb2312')
		# get the suitable grade
		xn = re.compile('<select name=\"xnd\"[^>]*>(.*?)</select>' , re.S).findall(scheduleData)
		xn = re.compile('<option[^>]*>(.*?)</option>' , re.S).findall(xn[0])
	
		xq = re.compile('<select name=\"xqd\"[^>]*>(.*?)</select>' , re.S).findall(scheduleData)
		# 事实上 ， 一定会找到xq （2015/5/20：发现有些账号在显示成绩时出错。原因：从课表抓回来的学期是当前学期，可是可能当前学期还没有出成绩，故绩点为零，在计算
		#							时出现除以零，所以出错（scoreWindow.py 中的class.__calJd()）！）
		if xq :
			xq = re.compile('<option selected=[^>]*>(.*?)</option>' , re.S).findall(xq[0])
		else :
			xq = 0
		
		( self.xn , self.xq ) = ( xn , xq )	
		return (xn , xq)
	
	
	def __getClassAttrOrScore(self , scoreWebOpened , xn , xq , GETATTR = 0):
	
		scorePage = scoreWebOpened.read().decode('gb2312')
		# when GETATTR is 1 then scrawl the class attribute
		if GETATTR == 1:
			classAttr = re.compile( '<tr class=\"datelisthead\">(.*?)</tr>' , re.S).findall(scorePage)
			classAttr = re.compile( '<td>(.*?)</td>' , re.S).findall( classAttr[0] )
			with open('classAttr.txt' , 'w') as file:
				for attr in classAttr:
					file.write(attr + '\n')
		
		# tag is exist in there
		middledata = re.compile('<table class=\"datelist\"[^>]*>(.*?)</table>' , re.S)\
					.findall(scorePage)[0]
		middleScore = re.compile('<tr>(.*?)</tr>' , re.S).findall(middledata)
		if not middleScore:
			middleScore = []
		middleScore.extend(
					re.compile('<tr class=\"alt\">(.*?)</tr>' , re.S).findall(middledata)
					)
		# delete tag
		score = []
		for middle in middleScore:
			score.append(re.compile('<td>(.*?)</td>',re.S).findall(middle))
		
		# Save score and some attr to txt
		with open('{0}grade{1}emScore.txt'.format(xn , xq) , 'w') as file:
			for sscore in score:
				for attr in sscore:
					file.write(attr + ' ')
				file.write('\n')
		
	def __getStudentScore(self , xn , xq , viewState , GETCLASSATTR ):
		# print('Be scrawling scores ...')
		urlAdd = {
			'xh' : self.userName,
			'xm' : self.xm,
			'gnmkdm' : 'N121605'
		}

		formToCjUrl = {
			'xh' : self.userName,
			'xm' : self.xm,
			'gnmkdm':'N121605',
			'__VIEWSTATE':viewState, 
			'ddlXN':xn,          
			'ddlXQ':xq,			
			'txtQSCJ':'0',
			'txtZZCJ':'100',
			'Button1':'按学期查询'
		}
		encodeForm = urllib.parse.urlencode( formToCjUrl )
		
		scorePage = self.cookieOpener.open(urllib.request.Request\
					( scoreUrl + urllib.parse.urlencode(urlAdd , encoding = 'gb2312')
					, encodeForm.encode('utf-8') ))
		# whether should get classAttr

		self.__getClassAttrOrScore( scorePage , xn , xq , GETCLASSATTR )		
		
		# print('Finish scrawling scores!')

	




