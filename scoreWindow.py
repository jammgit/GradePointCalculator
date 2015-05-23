# coding=utf-8
# Author : Jammgit
# built in : 2015/5/17

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit,QPushButton,QLabel,QVBoxLayout,QGridLayout
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QHBoxLayout,QComboBox
from PyQt5 import QtGui

class CScoreWindow(QtWidgets.QWidget): 
	def __init__(self):
		super(CScoreWindow , self).__init__()
		self.resize(1000,500)
		

	def setAll(self , XNandXQ ):
		( self.xn , self.xq ) = XNandXQ
		self.__initData()
		self.__initWidget()
		self.__initSignalSlot()
		self.__showScore(0,0)
		self.__initGradePoint()
		
	def __initData(self):
		self.classAttrList = []
		with open('classAttr.txt','r') as file:
			lines = file.readlines()
			for line in lines :
				line = line.strip('\n')
				self.classAttrList.append(line)			
				
		if not self.xn :
			return -1
			
		#  scoreList= [[year[grade1][grade2]] , [[],[]]]
		self.scoreList = []
		for sxn in self.xn:
			if not sxn == self.xn[0]:
				xq = 2
			else :
				xq = int(self.xq[0])
			sxq = 1
			middle = []
			while sxq <= xq :
				score = []
				with open('{0}grade{1}emScore.txt'.format(sxn , sxq),'r') as file:
					lines = file.readlines()
					for line in lines:
						line = line.strip('\n').split(' ')
						while '' in line :
							line.remove('')
						score.append(line)
				middle.insert(0 , score)
				sxq = sxq + 1
			self.scoreList.append(middle)
		#print(self.scoreList)
		
	def __initWidget(self):
		# class property 
		self.attrLabel = []
		for attr in self.classAttrList:
			edit = QLineEdit(attr)
			edit.setEnabled(False)
			# edit.setFormAlignment(Qt::AlignHCenter | Qt::AlignVCenter)
			self.attrLabel.append(edit)
		
		# get the max of class quantity , and create max * sum of property 's lineedit
		self.maxClassSum = len( self.scoreList[0][0] )
		for i in range(0 , len(self.scoreList)):
			for j in range(0 , len(self.scoreList[i])):
				if len(self.scoreList[i][j]) > self.maxClassSum:
					self.maxClassSum = len(self.scoreList[i][j])
			
		self.scoreLine = []
			
		index = 1 
		while index <= self.maxClassSum:
			tmp = 1
			middle = []
			while tmp <= len(self.classAttrList):
				line = QLineEdit()
				middle.append(line)
				tmp = tmp + 1
			self.scoreLine.append(middle)
			index = index + 1 
		# build xia la kuang
		self.comBox = []
		self.comBox.append(QComboBox())
		self.comBox.append(QComboBox())
		
		for i in range(0 , len(self.xn)):
			self.comBox[0].addItem(self.xn[i])
			
		xq = int(self.xq[0])
		while xq > 0:
			self.comBox[1].addItem(str(xq))
			xq = xq - 1
		
		# layout
		hLayout = QHBoxLayout()
		for label in self.attrLabel:
			hLayout.addWidget(label)
			
		hLayoutList = []
		for i in range(0 , self.maxClassSum):
			hLay = QHBoxLayout()
			for j in range(0 , len(self.attrLabel)):
				# line.setFormAlignment(Qt::AlignHCenter | Qt::AlignVCenter)
				hLay.addWidget(self.scoreLine[i][j])
			hLayoutList.append(hLay)
		
		gridLayout = QGridLayout()
		gridLayout.addWidget(self.comBox[0] , 0 , 0 , 1 , 1)
		gridLayout.addWidget(self.comBox[1] , 0 , 1 , 1 , 1)
		
		
		self.vLayout = QVBoxLayout()
		self.vLayout.addLayout(hLayout)
		for i in range(0 , len(hLayoutList)):
			self.vLayout.addLayout(hLayoutList[i])
			
		self.vLayout.addLayout(gridLayout)
		
		self.setLayout(self.vLayout)
		# self.scoreLabel = QLabel
		# display score initially
		self.currentXn = 0
		self.currentXq = 0
		
	def __initSignalSlot(self):
			self.comBox[0].currentIndexChanged.connect(self.__xnChangeScorePage)
			self.comBox[1].currentIndexChanged.connect(self.__xqChangeScorePage)
		
	def __xnChangeScorePage(self , index ):
		self.currentXn = index
		# self.comBox[1].removeItem(1)
		if len(self.scoreList[index]) == 1:
			self.comBox[1].removeItem(0)
		elif self.comBox[1].count() < len(self.scoreList[index]):
			self.comBox[1].insertItem(0 , str(2))
			
		self.__showScore(self.currentXn , self.currentXq)
		#print( self.currentXn )
	def __xqChangeScorePage(self , index ):
		self.currentXq = index	
		self.__showScore(self.currentXn , self.currentXq)
		#print( self.currentXq )
		
	def __showScore(self , xn , xq ):
		try:
			scoreList = self.scoreList[xn][xq]
			classSum = len(scoreList)

			for i in range(0 , classSum ):
				for j in range(0 , len(scoreList[i])):
					self.scoreLine[i][j].setEnabled(True)
					if scoreList[i][j] == '&nbsp;':
						self.scoreLine[i][j].setText('无')
					else :
						self.scoreLine[i][j].setText(scoreList[i][j])

				
			for i in range(classSum , self.maxClassSum):
				for j in range(0 , len(self.attrLabel)):
					self.scoreLine[i][j].setEnabled(False)
		except:
			print('__showScore')
		
	def __initGradePoint(self):
		try:
			# grade = len( self.xn )
			self.jdLabelList = []
			self.jdLineList = []	
			hLayout = QHBoxLayout()
			# build kongjian and add it into layout , 
			xn = len(self.scoreList)
			index = 0
			while xn > 0 :
				xq = len(self.scoreList[index])
				index = index + 1
				middleLine = []
				vLayoutLabel = QVBoxLayout()
				vLayoutLine = QVBoxLayout()
				
				while xq > 0 :
					# sub layout
					label = QLabel('大{0}第{1}学期绩点'.format(xn , xq))
					vLayoutLabel.addWidget(label)

					line = QLineEdit()
					line.setEnabled(False)
					vLayoutLine.addWidget(line)
					middleLine.append(line)
					xq = xq - 1
				# sub layout
				label = QLabel('大{0}学年绩点'.format(xn))
				vLayoutLabel.addWidget(label)

				line = QLineEdit()
				line.setEnabled(False)
				vLayoutLine.addWidget(line)
				middleLine.append(line)	
				# main layout
				hLayout.addLayout(vLayoutLabel)
				hLayout.addLayout(vLayoutLine)
				
				self.jdLineList.append(middleLine)
				xn = xn - 1
			
			self.vLayout.addLayout(hLayout)
		except:
			print('__initGradePoint')
		self.__calJd()
	
	# cal jidian
	def __calJd(self):
		# 3,7
		try:
			for i in range(0 , len(self.scoreList)):
				fz = 0.0
				fm = 0.0
				for k in range(0 , len(self.scoreList[i])):
					subfz = 0.0
					subfm = 0.0
					for j in range(0 , len(self.scoreList[i][k])):
						if self.scoreList[i][k][j][3] == '优秀' :
							tmp = 4.5
						elif self.scoreList[i][k][j][3] == '良好' :
							tmp = 3.5				
						elif self.scoreList[i][k][j][3] == '中等' or self.scoreList[i][k][j][3] == '中':
							tmp = 2.5			
						elif self.scoreList[i][k][j][3] == '及格' :
							tmp = 1.5				
						elif self.scoreList[i][k][j][3] == '不及格' or float(self.scoreList[i][k][j][3]) < 60.0 :
							tmp = 0.0			
						else :
							tmp = ( float(self.scoreList[i][k][j][3]) - 50 )/10
						subfz = subfz + tmp * float(self.scoreList[i][k][j][7]) 
						subfm = subfm + float(self.scoreList[i][k][j][7])
					if subfm != 0.0 :
						self.jdLineList[i][k].setText(str(subfz/subfm))
					else:
						self.jdLineList[i][k].setText(str(0))
					fz = fz + subfz
					fm = fm + subfm
				if fm != 0.0 :
					self.jdLineList[i][len(self.scoreList[i])].setText(str(fz/fm))
		except:
			print('__calJd')
				
				
				
				
				
				
				
				
		
				
	