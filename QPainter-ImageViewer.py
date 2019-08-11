from PyQt5 import QtSql,QtGui,QtCore,QtWidgets,Qt,QtPrintSupport
import os, sys

class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle("ImageViewer")
        self.resize(500,500)
        #self.resize(self.image.width(),self.image.height())

        self.menu = self.menuBar().addMenu("&菜单")
        self.toolbar = self.addToolBar('Print')
        
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel1 = QtWidgets.QLabel()
    
        #self.layout.addWidget(self.imageLabel1)
        
        self.image = QtGui.QImage()
        #self.image.load(r"C:\Users\ASUS\Desktop\project\Qt_GridLayout\Images\logo.png")

        # 设置 scrollarea,对于scrollarea，widget需设置最小size
        self.scrollarea = QtWidgets.QScrollArea()
        self.scrollarea.setVisible(True)
        self.imageLabel.setMinimumSize(1030,1000)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)

        # enable to scale the image to whatever size they want when Fit to Window option is turned on
        # self.imageLabel.setSizePolicy(Qt.QSizePolicy.Ignored)
        # enable the image to scale properly when zooming
        self.imageLabel.setScaledContents(True)
        self.scrollarea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollarea.setWidget(self.imageLabel)
        self.scrollarea.setVisible(True)
        
        self.setCentralWidget(self.scrollarea)
        
        self.loadAct = QtWidgets.QAction('Load',self)
        self.saveAsAct = QtWidgets.QAction('Save',self)
        self.printAct = QtWidgets.QAction('Print',self)
        self.copyAct = QtWidgets.QAction('Copy',self)
        self.zoomInAct = QtWidgets.QAction('ZoomIn',self)
        self.zoomOutAct = QtWidgets.QAction('ZoomOut',self)
        self.fitToWindowAct = QtWidgets.QAction('FitToWindow',self)

        self.loadAct.setShortcut('ctrl+l')
        self.loadAct.setStatusTip('load image')
        self.loadAct.triggered.connect(self.imageFileDialog)
        self.menu.addAction(self.loadAct)

        self.saveAsAct.setShortcut('ctrl+s')
        self.saveAsAct.setStatusTip('save image')
        self.saveAsAct.triggered.connect(self.save)
        self.menu.addAction(self.saveAsAct)

        self.printAct.setShortcut('ctrl+p')
        self.printAct.setStatusTip('print image')
        self.printAct.setEnabled(True)
        self.printAct.triggered.connect(self.print)
        self.menu.addAction(self.printAct)

        self.copyAct.setShortcut('ctrl+c')
        self.copyAct.setStatusTip('copy image')
        self.copyAct.triggered.connect(self.save)
        self.menu.addAction(self.copyAct)

        self.zoomInAct.setShortcut('ctrl+c')
        self.zoomInAct.setStatusTip('zoom in')
        self.zoomInAct.triggered.connect(self.zoomIn)
        self.menu.addAction(self.zoomInAct)
        
        self.zoomOutAct.setStatusTip('zoom out')
        self.zoomOutAct.triggered.connect(self.zoomOut)
        self.menu.addAction(self.zoomOutAct)
        
        self.fitToWindowAct.setStatusTip('fit to window')
        self.fitToWindowAct.setEnabled(True)
        self.fitToWindowAct.triggered.connect(self.fitToWindow)
        self.menu.addAction(self.fitToWindowAct)

        self.scaleFactor = 1

        self.toolbar.addAction(self.printAct)

        if (not(self.fitToWindowAct.isChecked())):
        # the same as imageLabel.resize(imageLabel.pixmap().size())
            self.imageLabel.adjustSize()
            
    def adjustSize(self):
        pass
    
    def save(self):
        pass
   
    def adjustScrollBar(self,scrollbar,factor):
        pass

    def imageFileDialog(self):
        # 如设置多个文件扩展名过滤，用双引号隔开
        # getOpenFileName返回tuple
        self.fname,_ = QtWidgets.QFileDialog.getOpenFileName(self,'OpenFile',"./Images/","Image files (*.jpg *.gif *.png)")

        self.imageLabel.setPixmap(QtGui.QPixmap(self.fname))
        self.image.load(self.fname)
        self.size = self.image.size()

        #self.imageLabel1.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def updateActions(self):
        #self.saveAsAct.setEnabled(not(self.image.isNULL()))
        #self.copyAct.setEnabled(not(self.image.isNULL()))
        pass
    
    def imageInformation(self):
        # QImage的信息
        data = self.image.bits()
        w = self.image.width()
        h = self.image.height()
        return w,h

    def print(self):
        # 调试使用Q_Assert(self.imageLabel.pixmap())

        self.print = QtPrintSupport.QPrinter()
        self.printDialog = QtPrintSupport.QPrintDialog(self.print,self)
        if self.printDialog.exec_():

            # 实例化视图窗口,此处注意:实例化的painter应为局部变量，不要加self
            # print imageLabel 而不是image
            painter = Qt.QPainter(self.print)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(),QtCore.Qt.KeepAspectRatio)

            # specifie the device coordinate system
            painter.setViewport(rect.x(),rect.y(),size.width(),size.height())

            # specifie the logicl coordinate system
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0,0,self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)
    
    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1

    def fitToWindow(self):
        # action check
        self.fitCheck = self.fitToWindowAct.isChecked()
        self.scrollarea.setWidgetResizable(self.fitCheck)
        if (not self.fitCheck):
            self.normalSize()
        self.updateActions()

    def scaleImage(self,factor):
        self.scaleFactor *= factor
        #调整label size
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.zoomInAct.setEnabled(self.scaleFactor<3.0)
        self.zoomInAct.setEnabled(self.scaleFactor>0.333)
        
app=QtWidgets.QApplication(sys.argv)
imageviewer=ImageViewer()
imageviewer.show()
sys.exit(app.exec_())       
    
    
