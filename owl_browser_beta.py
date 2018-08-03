from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

import sys

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 设置窗口标题
		self.setWindowTitle('Owl Browser')
		# 设置窗口图标
		self.setWindowIcon(QIcon('icons/owl.png'))
		self.resize(1440,900)
		self.show()
		# 添加 URL 地址栏
		self.urlbar = QLineEdit()
		# 让地址栏能响应回车按键信号
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# 添加标签栏
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)

		self.add_new_tab(QUrl('http://www.zhihu.com'))

		self.setCentralWidget(self.tabs)

		new_tab_action = QAction(QIcon('icons/add_page.png'), 'New Page', self)
		new_tab_action.triggered.connect(self.add_new_tab)
		
		# 添加导航栏
		navigation_bar = QToolBar('Navigation')
		# 设定图标的大小
		navigation_bar.setIconSize(QSize(16, 16))
		self.addToolBar(navigation_bar)

		# 导航栏左侧控制按钮
		back_button = QAction(QIcon('icons/back.png'), 'Back', self)
		next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
		stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
		reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)

		# 导航栏左侧控制按钮点击事件
		back_button.triggered.connect(self.tabs.currentWidget().back)
		next_button.triggered.connect(self.tabs.currentWidget().forward)
		stop_button.triggered.connect(self.tabs.currentWidget().stop)
		reload_button.triggered.connect(self.tabs.currentWidget().reload)

		# 导航栏右侧书签
		baidu_button = QAction(QIcon('icons/baidu.png'), 'baidu', self)
		zhihu_button = QAction(QIcon('icons/zhihu.png'), 'zhihu', self)
		github_button = QAction(QIcon('icons/github.png'), 'github', self)
		about_button = QAction(QIcon('icons/owl.png'), 'about', self)

		# 导航栏右侧书签点击事件
		baidu_button.triggered.connect(self.go_to_baidu)
		zhihu_button.triggered.connect(self.go_to_zhihu)
		github_button.triggered.connect(self.go_to_github)
		about_button.triggered.connect(self.about)

		# 将按钮添加到导航栏上

		# 左侧
		navigation_bar.addAction(back_button)
		navigation_bar.addAction(next_button)
		navigation_bar.addAction(stop_button)
		navigation_bar.addAction(reload_button)
		# 分割线
		navigation_bar.addSeparator()
		# 导航栏
		navigation_bar.addWidget(self.urlbar)
		navigation_bar.addSeparator()
		# 右侧
		navigation_bar.addAction(baidu_button)
		navigation_bar.addAction(zhihu_button)
		navigation_bar.addAction(github_button)
		navigation_bar.addAction(about_button)

	
	# 响应回车按钮，将浏览器当前访问的 URL 设置为用户输入的 URL
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == '':
			q.setScheme('http')
		self.tabs.currentWidget().setUrl(q)

	def renew_urlbar(self, q, browser=None):
		# 如果不是当前窗口所展示的网页则不更新 URL
		if browser != self.tabs.currentWidget():
			return
		# 将当前网页的链接更新到地址栏
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

	# 添加新的标签页
	def add_new_tab(self, qurl=QUrl(''), label='新标签页'):
		# 为标签创建新网页
		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)

		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser=browser: self.renew_urlbar(qurl, browser))

		browser.loadFinished.connect(lambda _, i=i, browser=browser: 
			self.tabs.setTabText(i, browser.page().title()))

	# 双击标签栏打开新页面
	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()

	# 书签1 - 百度
	def go_to_baidu(self):
		q = QUrl('http://www.baidu.com')
		self.tabs.currentWidget().setUrl(q)
	# 书签2 - Github
	def go_to_github(self):
		q = QUrl('http://www.github.com')
		self.tabs.currentWidget().setUrl(q)
	# 书签3 - 知乎
	def go_to_zhihu(self):
		q = QUrl('http://www.zhihu.com')
		self.tabs.currentWidget().setUrl(q)
	
	# 标签页切换
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		# self.tabs.setTabText(i, browser.page().mainFrame().title())
		self.renew_urlbar(qurl, self.tabs.currentWidget())

	def close_current_tab(self, i):
		# 如果当前标签页只剩下一个则不关闭
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)

	def about(self):  
            QMessageBox.about(self, '关于','Owl Browser v1.02 beta by Jack Li')

# 创建应用
app = QApplication(sys.argv)
# 创建主窗口
window = MainWindow()
# 显示窗口
window.show()
# 运行应用，并监听事件
app.exec_()