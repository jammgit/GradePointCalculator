# coding=utf-8
# Author : Jammgit
# built in : 2015/5/17

from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLineEdit,QPushButton,QLabel,QVBoxLayout,QGridLayout
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView,QHBoxLayout,QCheckBox
from PyQt5.QtGui import QImage, QPixmap
from SpiderForSchoolWeb import CSpiderSchoolWeb
from scoreWindow import CScoreWindow
import sys


class mainWindow(QtWidgets.QWidget):
	def __init__(self):
		super(mainWindow , self).__init__()
		self.__initWidget()
		self.__initSignalSlot()
		self.__initUser()
		
	def __initWidget(self):
		self.resize(300,200)
		self.xhLabel = QLabel('学号')
		self.mmLabel = QLabel('密码')
		self.authLabel = QLabel('验证码')
		self.imageLabel = QLabel()
		
		self.xhLine = QLineEdit()
		self.mmLine = QLineEdit()
		self.mmLine.setEchoMode(QLineEdit.Password)
		self.authLine = QLineEdit()
		#self.authImageScene = QGraphicsScene
		self.authButton = QPushButton('获取验证码')
		self.okButton = QPushButton('登陆')
		self.chBox = QCheckBox('记住密码')
		self.chBox.setCheckState(Qt.Checked)

		self.displayScoreButton = QPushButton('显示成绩')
		self.okButton.setEnabled(False)
		self.displayScoreButton.setEnabled(False)
		self.tips = QLabel('正在登录 ...')
		self.tipsOk = QLabel('登陆成功！')
		
		self.gridLayout = QGridLayout()
		self.gridLayout.addWidget(self.xhLabel , 0 , 0 , 1 , 1)
		self.gridLayout.addWidget(self.mmLabel , 1 , 0 , 1 , 1)
		self.gridLayout.addWidget(self.authLabel , 2 , 0 , 1 , 1)
		self.gridLayout.addWidget(self.xhLine , 0 , 1 , 1 , 1)
		self.gridLayout.addWidget(self.mmLine , 1 , 1 , 1 , 1)
		self.gridLayout.addWidget(self.authLine , 2 , 1 , 1 , 1)
		self.gridLayout.addWidget(self.imageLabel , 3 , 1 , 1 , 1)
		self.gridLayout.addWidget(self.tipsOk , 4 , 1 , 2 , 1)
		self.gridLayout.addWidget(self.tips , 4 , 1 , 2 , 1)
		
		self.tips.hide()
		self.tipsOk.hide()
		
		self.hLayout = QHBoxLayout()
		self.hLayout.addWidget(self.authButton)
		self.hLayout.addWidget(self.okButton)
		self.hLayout.addStretch(3)
		self.hLayout.addWidget(self.chBox)
		
		self.vLayout = QVBoxLayout()
		self.vLayout.addStretch(10)
		self.vLayout.addLayout(self.hLayout)
		self.vLayout.addStretch(10)
		self.vLayout.addWidget(self.displayScoreButton)
		
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.gridLayout)
		self.mainLayout.addLayout(self.vLayout)
		self.setLayout(self.mainLayout)
	
	def __initSignalSlot(self):
		self.okButton.clicked.connect(self.__logClicked)
		self.authButton.clicked.connect(self.__getAuthCode)
		self.displayScoreButton.clicked.connect(self.__showScore)
		#self.chBox.stateChanged.connect(self.__chBoxChange)
	
	def __initUser(self):
		self.user = []
		try:
			with open('user.txt' , 'r') as file:
				lines = file.readlines()
				for line in lines:
					self.user.append(line.strip('\n'))
		except :
			self.user.extend(['',''])
		self.xhLine.setText(self.user[0])
		if len(self.user) > 1:
			self.mmLine.setText(self.user[1])
			
	def __getAuthCode(self):
		self.tips.hide()
		
		# get authcode
		self.login = CSpiderSchoolWeb()
		self.login.getAuthCode()
		
		image = QImage()
		image.load('image.gif')
		self.imageLabel.setPixmap(QPixmap.fromImage(image))
		
		self.tipsOk.hide()
		self.okButton.setEnabled(True)
		self.displayScoreButton.setEnabled(False)
		
	def __logClicked(self):

		self.tips.show()
		xh = self.xhLine.text()
		mm = self.mmLine.text()
		auth = self.authLine.text()
		
		with open('user.txt','w') as file:
			file.write(xh + '\n')
			if self.chBox.checkState() == Qt.Checked:
				file.write(mm + '\n')
		# login
		self.login.loginSchoolWeb(xh , mm , auth)
		
		self.displayScoreButton.setEnabled(True)
		self.okButton.setEnabled(False)
		
		self.tips.hide()
		self.tipsOk.show()	

	def __showScore(self):
		# remember use self.XXX , otherwise the windows exit imidatelt
		self.scoreWin = CScoreWindow()
		self.scoreWin.setAll( self.login.getStudentGradeAndSem() )
		#self.scoreWin.setAll( (['2014-2015','2013-2014'] , ['2']) )
		self.scoreWin.show()

		
def main():

	app = QtWidgets.QApplication(sys.argv)

	mainWin = mainWindow()
	mainWin.show()

	sys.exit(app.exec_())	
	
if __name__ == '__main__' :
	main()