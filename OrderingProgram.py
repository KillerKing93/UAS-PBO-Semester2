
from PyQt6.QtWidgets import QScrollArea, QDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap, QGuiApplication, QIcon
from PyQt6.QtCore import Qt
from pathlib import Path
from datetime import datetime
import os, shutil

#Kelas yang berfungsi untuk mencetak hasil pembelian dari barang yang dibeli oleh pembeli
class printText(QDialog):
    #Method yang berfungsi sebagai penginisialisasi attribut kelas
    def __init__(self, item, order, count, dict = "nonSub"):
        super().__init__()
        self.item = item
        self.order = order
        self.setWindowTitle('Checkout')
        self.setGeometry(100,100,300,200)
        self.dict = dict
        self.itemsCounterPrinted = count
        self.itemsCounterParser = "Mi[{}XCVHELL{}]".format(self.itemsCounterPrinted, self.dict)
        self.PrintText()
        self.showD()
    
    #Method berfungsi sebagai pengformat teks dengan teks diprioritaskan untuk diletakkan di paling kiri
    def leftStringFormater(self, text, amnt):
        length = len(text)
        return text + " "*(amnt-length)

    #Method yang berfungsi sebagai pengformat teks dengan teks diprioritaskan untuk diletakkan di tengah
    def midStringFormater(self, text, amnt):
        length = len(text)
        length = abs((amnt-length)//2)
        return " "*length+text+" "*length

    #Method yang berfungsi sebagai pengformat teks dengan teks diprioritaskan untuk diletakkan di paling kanan
    def rightStringFormater(self, text, amnt):
        length = len(text)
        return " "*(amnt-length) + text

    #Method yang berfungsi untuk membuat teks yang nantinya akan ditampilkan ke pengguna
    def PrintText(self):
        length = 36
        self.text = ""
        self.text += "STARLA x STORE\n"
        self.text += "Ruko Starla Jati Asih\n"
        self.text += "(047)\n"
        self.text += ("-"*length) + "\n"
        Notes = "Kode Nota:     {} ".format(self.itemsCounterParser)
        Notes.center(14)
        self.text += (Notes)

        ###
        dataString = f"\n931242       {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n"
        dataString.center(length)
        dataString.replace(" ", "-")
        ###
        self.text += dataString
        self.text += ("-"*length) + "\n"
        self.text.center(length)

        total = 0
        self.text += "\n"
        self.text += "\n"
        for orderKey in self.order:
            text0 = "{}".format(self.item[orderKey].name)
            text0 = self.leftStringFormater(text0, 15)
            text1 = "{}".format("x"+str(self.order[orderKey]))
            text1 = self.rightStringFormater(text1, 8)
            text2 = "{}".format("Rp. "+str(self.item[orderKey].price))
            text2 = self.rightStringFormater(text2, 13)
            self.text += (text0+text1+text2+"\n")
            total += (self.order[orderKey] * self.item[orderKey].price)
        
        self.text += (("\n"+"-"*length) + "\n")
        self.text += ("TOTAL : Rp. {}\n".format(str(total)))
        self.text += ("-"*length) + "\n"

        thanks = '''
BERIKAN NOTA INI KEPADA KASIR
UNTUK MELAKUKAN PEMESANAN

THANK YOU
PLEASE BUY AGAIN
'''
        thanks.center(length)
        self.text += thanks

    #Method yang berfungsi untuk menetapkan teks yang dihasilkan di fungsi sebelumnya untuk ditampilkan ke pengguna ketika objek instansi kelas dipanggil
    def showD(self):
        self.itemsCounterPrinted +=1
        self.label = QLabel(self.text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""")
        
        self.button = QPushButton("Cetak")
        self.button.clicked.connect(self.callF)
        VBox = QVBoxLayout()
        VBox.addWidget(self.label)
        VBox.addWidget(self.button)
        self.setLayout(VBox)

    #Method yang berguna untuk menyimpan nota dari teks yang sudah dihasilkan sebelumnya
    def callF(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if filename:
            with open(filename, 'w') as f:
                f.write(self.text)
                ###print("Saved to {}".format(filename))

#Kelas yang berguna untuk menyimpan informasi dari Barang yang tersedia di program
class ItemNodes():
    def __init__(self, name, amnt = 0, price = 0, img = "", information = ""):
        self.name = name
        self.amnt = amnt
        self.price = price
        self.img = img
        self.information = information
    
    ### def check(self):
    ###print("ItemNode Check: {} {} {} {}".format(self.amnt, self.price, self.img, self.information))

#Kelas yang berguna untuk mengatur barang - barang di dalam program
class ItemsCore():
    #Method yang berfungsi untuk menginisialisasikan attribut objek instansi kelas pada saat objek di inisialisasi
    def __init__(self):
        self.itemNodesHolder = {}
        self.orderedItems = {}
        self.filpath = (str(__file__).replace(Path(__file__).name, "")+"src\\").replace("\\", "/")+"items.conf"
        ## self.itemNodesHolder["dav"] = ItemNodes(12, 12000, "C:/Users/KillerKing/Downloads/Screenshot-2022-09-13-183142.webp", "HI THERE!")
        ## self.itemNodesHolder["pena"] = ItemNodes(15, 600, )

    #Method yang berfungsi untuk mengecek apakah barang masih dapat dibeli
    def checkAval(self, key, amnt):
        return amnt < self.itemNodesHolder[key].amnt

    #Method yang berfungsi untuk mendapatkan informasi barang yang tersimpan di program
    def get(self):
        return dict(self.itemNodesHolder)
    
    #Method yang berfungsi untuk mendapatkan pesanan yang dibuat oleh pembeli
    def getOrder(self):
        return dict(self.orderedItems)

    #Method yang berfungsi untuk menambahkan 1 pesanan dari barang yang dipilih
    def incItem(self, key):
        key = key.lower()
        ###print(self.orderedItems)
        if key not in self.orderedItems:
            self.orderedItems[key] = 1
            ###print(self.orderedItems[key])
            return True
        elif self.orderedItems[key] < self.itemNodesHolder[key].amnt:
            self.orderedItems[key] += 1
            ###print(self.orderedItems[key])
            return True
        else:
            return False

    #Method yang berfungsi untuk mengurangi 1 pesanan dari barang yang dipilih
    def decItem(self, key):
        key = key.lower()
        if key not in self.orderedItems:
            return False
        self.orderedItems[key] -= 1
        ###print(self.orderedItems[key])
        if self.orderedItems[key] < 1:
            del self.orderedItems[key]
        return True

    #Method yang berfungsi untuk menyimpan seluruh informasi barang yang ada pada saat ini
    def saveCurrentItems(self):
        strs = ""
        for key in self.itemNodesHolder:
            strs += (key + " [!=-=Holder=-=!] " + self.itemNodesHolder[key].name +" [!=-=Holder=-=!] "+str(self.itemNodesHolder[key].amnt)+" [!=-=Holder=-=!] "+str(self.itemNodesHolder[key].price)+" [!=-=Holder=-=!] "+self.itemNodesHolder[key].img+" [!=-=Holder=-=!] "+self.itemNodesHolder[key].information+"\n")
        ###print(strs)
        try:
            with open(self.filpath, 'w') as f:
                f.write(strs)
                ###print('Saved to {}'.format(filpath))
                return True
        except(FileNotFoundError):
            ###print("ERROR!, {}".format(filpath))
            return 
    
    #Method yang berfungsi untuk memuat seluruh informasi barang yang dimodifikasi dan dibuat sebelumnya
    def loadItems(self):
        ##print(filpath)
        with open(self.filpath, 'r') as f:
            data = f.read()
            ##print(data)
            data = data.split("\n")
            for rdata in data:
                ##print(rdata)
                rdata = rdata.split(" [!=-=Holder=-=!] ")
                ##print(rdata)
                try:
                    self.itemNodesHolder[rdata[0]] = ItemNodes(rdata[1], int(rdata[2]), int(rdata[3]), rdata[4], rdata[5])
                except(IndexError):
                    pass
                ###print(rdata)
                ###print('Loaded from {}'.format(filpath))
    
    #Method yang berfungsi untuk menambahkan barang baru ke dalam objek instansi kelas dan berfungsi untuk menggandakan gambar
    #dari barang yang ditambahkan ke folder penyimpanan internal program yang bernamakan ./src/
    def addItem(self, key, name, amnt, price, img, information):
        
        ###print("addI, : | {} | {} | {} | {} | {} |".format(key, amnt, price, img, information))
        ###print(key, amnt, price, img, information)
        pureimg = img.strip().split("/")
        pureimg = pureimg[-1]
        if not os.path.isfile(self.filpath+pureimg):
            shutil.copy(img, self.filpath+pureimg)
            ##print("Image Moved Successfully")
        self.itemNodesHolder[key.lower()] = ItemNodes(name, amnt, price, pureimg, information)
        ##print (self.itemNodesHolder[key])
        self.saveCurrentItems()
        return True

    #Method yang berfungsi untuk menghapus barang dari dalam objek instansi kelas dan berfungsi untuk menghapus gambar yang
    #lokasinya didapat dari node barang yang akan dihapus
    def delItem(self, key):
        try:
            if os.path.isfile(self.filpath+self.itemNodesHolder[key].img):
                os.remove(self.filpath+self.itemNodesHolder[key].img)
            del self.itemNodesHolder[key]
            self.saveCurrentItems()
            return True
        except(KeyError):
             return False

    #Method yang berfungsi untuk mereset barang yang dibeli oleh pembeli
    def resetOrder(self):
        self.orderedItems = {}

#Kelas yang berfungsi untuk menampilkan peringatan ke pada pengguna
class ErrorPopUp(QDialog):
    #Method yang berfungsi untuk menginisialisasikan attribut objek dari instansi kelas
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Error!')
        self.setGeometry(100,100,300,200)
    
    #Method yang berfungsi untuk menetapkan teks peringatan yang akan ditampilkan
    def error(self, error):
        VBox = QVBoxLayout()
        label0 = QLabel(error)
        label0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VBox.addWidget(label0)
        self.setLayout(VBox)

# Kelas yang berfungsi untuk membuat box untuk menampilkan
# informasi penting barang seperti nama, jumlah barang, dan harga
class itemBoxDetail(QWidget):
    def __init__(self, name, itemAmnt, price):
        super().__init__()
        self.type = ""
        self.name = QLabel(str(name)+", ")
        self.amntBox = QLabel("   x"+str(itemAmnt)+",")
        self.priceBox = QLabel(str(price))
        HBox = QHBoxLayout()
        HBox.addWidget(self.name)
        HBox.addWidget(self.amntBox)
        HBox.addWidget(self.priceBox)
        self.setLayout(HBox)

#Kelas yang berfungsi untuk membuat box untuk menjelaskan barang
class itemDetail(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""")
    #Method yang sama dengan kelas sebelumnya. Method ini merupakan
    #sebuah artifak yang tidak lagi digunakan
    def updateItem(self, name, itemAmnt, price):
        self.type = ""
        self.nameIT = QLabel(str(name)+", ")
        self.amntBox = QLabel(str(itemAmnt+","))
        self.priceBox = QLabel(str(price))
        HBox = QHBoxLayout()
        HBox.addWidget(self.nameIT)
        HBox.addWidget(self.amntBox)
        HBox.addWidget(self.priceBox)
        HBox.layout()

    #Method yang berguna untuk memperbaharui informasi barang
    def updateItem(self, information):
        super().__init__()
        scrolls = Scrolly()
        self.label = QLabel(information)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""")
        scrolls.add_widget
        widget = QWidget()
        HBox = QHBoxLayout(self.label)
        widget.setLayout(HBox)
        scrolls.add_widget(widget)
        HBox = QHBoxLayout()
        HBox.addWidget(scrolls)
        self.layout(HBox)

#Kelas yang berfungsi sebagai widget yang dapat digulir oleh pengguna
#ke atas atau ke bawah untuk menampilkan lebih banyak informasi
class Scrolly(QScrollArea):
    #Method yang berfungsi untuk menginisialisasikan attribut 
    #objek instansi dari kelas
    def __init__(self):
        super().__init__()
        self.i = 0
        self.widget = QWidget()
        self.widget.setLayout(QVBoxLayout())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

    #Method yang berfungsi untuk menambahkan widget ke dalam objek gulir.
    def add_widget(self, widget):
        self.widget.layout().addWidget(widget)
        self.update()
        self.i += 1

#Kelas yang berfungsi sebagai widget utama yang akan menampilkan barang beserta
#informasi yang dimilikinya
class ImagedItemNode(QWidget):
    #Method yang berfungsi untuk menginisialisasikan atribut objek dari instansi
    #kelas
    def __init__(self, key, amnt, price, img, info, IC, types = "nonSub"):
        super().__init__()
        self.amnt = amnt
        self.img = (str(__file__).replace(Path(__file__).name, "")+"src/") + img
        self.subWidget = QWidget()
        self.key = key
        self.price = price
        self.info = info
        self.IC = IC
        self.types = types

        # Key #
        self.label = QLabel(key)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)   
        self.label.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""") 

        # Counter #
        self.counter = 0
        self.counterBox = QLabel("Dipesan: {}".format(str(self.counter)))
        self.counterBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counterBox.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""") 

        # Price #pixmap
        self.priceBox = QLabel("Rp. " + str(self.price))
        self.priceBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priceBox.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""") 

        # Icon #
        self.imgLabel = QLabel()
        self.pixmap = QPixmap('{}'.format(self.img))
        self.scaled_pixmap = self.pixmap.scaled(150, 150)
        self.imgLabel.setPixmap(self.scaled_pixmap)

    #Detail Box
        self.DetailBox = QPushButton("Detail")
        self.DetailBox.clicked.connect(self.updateDetailed)

    #Info Box
        self.infoBox = QWidget()
        self.scrolly = Scrolly()
        self.infos = None
        if self.types == "nonSub":
            self.infos = QLabel(str(info))      
        #Scroll Box
            self.infoV = QVBoxLayout()
            self.infoV.addWidget(self.infos)
            infoWidget = QWidget()
            infoWidget.setLayout(self.infoV)
            self.scrolly.add_widget(infoWidget)
            self.infoV2 = QVBoxLayout()
            self.infoV2.addWidget(self.scrolly)
            self.infoBox.setLayout(self.infoV2)
            self.infoBox.setHidden(True)

        #Vertical for adding utility
        self.counterBody = QVBoxLayout()
        self.amntBox = QLabel("Tersedia: {}".format(str(self.amnt)))
        self.amntBox.setStyleSheet("""
    QLabel {
        border: 1px solid black;
        border-radius: 0px;
    }
""") 
     
        self.buttonplus = QPushButton("+")
        self.buttonplus.clicked.connect(self.incBI)
        self.buttonnegav = QPushButton("-")
        self.buttonnegav.clicked.connect(self.decBI)
        self.buttonnegav.setEnabled(False)
        self.counterBody.addWidget(self.amntBox)
        self.counterBody.addWidget(self.counterBox)
        self.counterBody.addWidget(self.buttonplus)
        self.counterBody.addWidget(self.buttonnegav)

        #Horizontal for Img + adding utility
        self.bodyBox = QVBoxLayout()
        self.bodyBox.addWidget(self.imgLabel)

        #Body Column
        self.HbodyBox = QHBoxLayout()
        self.HbodyBox.addLayout(self.bodyBox)
        self.HbodyBox.addLayout(self.counterBody)

        # Name Column
        self.HBox1 = QHBoxLayout()
        self.HBox1.addWidget(self.DetailBox)

        self.VBox1 = QVBoxLayout()
        self.VBox1.addWidget(self.label)
        self.VBox1.addLayout(self.HbodyBox)
        self.VBox1.addWidget(self.priceBox)
        self.VBox1.addWidget(self.infoBox)
        self.VBox1.addLayout(self.HBox1)
        self.setLayout(self.VBox1)

    # Method yang berfungsi untuk memperbaharui visibilitas
    # dari widget infoBox
    def updateDetailed(self):
        ###print(self.info)
        if self.infoBox.isHidden():
            self.infoBox.setHidden(False)
            self.infoBox.update()   
        else:
            self.infoBox.setHidden(True)
            self.infoBox.update()
        self.update()

    # Method yang berfungsi untuk memperbaharui
    # kondisi tombol menambah dan mengurangi barang yang dibeli
    def incDecUpdate(self):
        self.buttonplus.setEnabled(self.checkAval())
        self.buttonnegav.setEnabled(self.counter > 0)
        self.update()

    # Method yang berfungsi untuk mengecek apakah barang dapat
    # dipesan oleh pembeli
    def checkAval(self):
        return self.counter < self.amnt

    # Method yang berfungsi untuk menambah jumlah dari barang yang dipesan
    def incBI(self):
        self.IC.incItem(self.key)
        self.counter += 1
        self.counterBox.setText("Dipesan: {}".format(str(self.counter)))  
        self.incDecUpdate()    
    
    # Method yang berfungsi untuk mengurangi jumlah dari barang yang dipesan
    def decBI(self):
        self.IC.decItem(self.key)
        self.counter -= 1
        self.counterBox.setText("Dipesan: {}".format(str(self.counter)))
        self.incDecUpdate()

#Kelas utama yang berfungsi sebagai media pemrosesan dan media pengeksekusian
#kode - kode tingkat atas sebelum data yang telah diolah diberikan ke objek
#instansi dari kelas lain di atas.
class LoginWindow(QMainWindow):
    # Method yang berfungsi untuk menginisialisasikan atribut objek instansi kelas
    def __init__(self):
        super().__init__()

        ### ESSENTIALS

        self.user = {"user":"user"}  #Default User Username & Password: user:user
        self.admin = {"admin":"admin"} #Default Admin Username & Password: admin:admin
        self.error = ""
        self.filePath = ""
        self.tempImgFile = ""
        self.loginType = "user"
        self.IC = ItemsCore()
        self.scrolls = Scrolly()
        self.curr_dir = (str(__file__).replace(Path(__file__).name, "")).replace("\\", "/")
        self.cfg_dir = self.curr_dir + "/Essentials/cfg.main"
        self.checkoutCount = 0

        ### ESSENTIALS

        self.iconLink = self.curr_dir.replace("/", "\\")+"src\Icon.png"
        self.setWindowIcon(QIcon(self.iconLink))
        self.setGeometry(500,250,500,200)
        self.MainMenu()

    # Method yang berfungsi sebagai media menyimpan noda barang - barang untuk nanti ditampilkan ke pengguna
    def scrollWidget(self):
        self.scrolls = Scrolly()
        data = self.IC.get()
        ###print(data)
        for key in data:
            amnt = int(data[key].amnt)
            price = int(data[key].price)
            img = data[key].img
            info = data[key].information
            ###print(amnt, price, img, info)
            self.scrolls.add_widget(ImagedItemNode(data[key].name, amnt, price, img, info, self.IC, "nonSub"))
        return self.scrolls

    #Method yang berfungsi untuk mereset self.scrolls
    def clearScrollWidget(self):
        self.scrollWidget().update()
        self.scrolls.update()
    
    #Method yang berfungsi untuk menambah jumlah barang yang dibeli,
    #merupakan sebuah artifak dari bagian kode yang tidak dipakai lagi
    def incItem(self,key):
        self.IC.incItem(key)
    
    #Method yang berfungsi untuk mengurangi jumlah barang yang dibeli,
    #merupakan sebuah artifak dari bagian kode yang tidak dipakai lagi
    def decItem(self,key):
        self.IC.decItem(key)
    
    #Method yang berfungsi untuk mendapatkan informasi user yang ada,
    #merupakan sebuah artifak dari bagian kode yang tidak dipakai lagi
    def getUser(self):
        return self.user

    #Method yang berfungsi untuk mendapatkan informasi admin yang ada,
    #merupakan sebuah artifak dari bagian kode yang tidak dipakai lagi
    def getAdmin(self):
        return self.admin

    #Method yang berfungsi untuk menambah user baru,
    #merupakan sebuah artifak dari bagian kode yang tidak dipakai lagi
    def addUser(self, type, user, pswd):
        if type == "user":
            self.user[user] = pswd
            return True
        elif type == "admin":
            self.admin[user] = pswd
            return True
        else:
            return False

    #Method yang berfungsi untuk menghapus user yang ada,
    #merupakan sebuah artifak dari bagian kode yang tidak dipakai lagi
    def delUser(self, user):
        try:     
            del self.user[user]
            return True
        except(KeyError):
             return False
    
    #Method yang berfungsi untuk memperbaharui password dari laman
    #login program
    def update_password(self):
        if self.cfg_dir:
            try:
                with open(self.cfg_dir, 'r') as f:
                    self.admin["admin"] = f.read().strip()
                    ###print("Password Admin: " + self.admin["admin"])
            except(FileNotFoundError):
                self.default()
    
    #Method yang berfungsi untuk mengganti password dari laman login program
    def change_password(self, pswd):
        with open(self.cfg_dir, 'w') as f:
                  f.write(pswd)
    
    #Method yang berfungsi untuk membuat file config baru jika file config tidak ada.
    def default(self):
        with open(self.cfg_dir, 'w') as f:
            f.write("admin")

    #Method yang berfungsi untuk menyamakan password yang dimasukkan pengguna maupun
    #program dan menentukan ke menu mana pengguna akan dikirim
    def matchPswd(self, type, user, pswd):
        ###print(type, user, pswd)
        if type == "user" and pswd == self.user[user]:
            return "user"
        elif type == "admin" and pswd == self.admin[user]:
            return "admin"
        else:
            return False

    #Method yang berfungsi untuk mencari apakah pengguna merupakan
    #pengguna tipe user atau tipe admin
    def findUser(self, user, pswd):
        ###print(user,pswd)
        if user in self.user:
            return self.matchPswd("user", user, pswd)
        elif user in self.admin:
            return self.matchPswd("admin", user, pswd)
        else:
            return False

    #Method yang berfungsi untuk menampilkan peringatan ke pengguna
    def errorPop(self):
        error = ErrorPopUp()
        error.error(self.error)
        error.exec()

    #Method yang berfungsi untuk mencetak barang yang dibeli oleh pengguna
    def checkout(self):
        item = self.IC.get()
        order = self.IC.getOrder()
        order = printText(item, order, self.checkoutCount)
        order.exec()
        self.checkoutCount += 1
    
    #Method yang berfungsi untuk menampilkan menu utama ke pada pengguna,
    #disini juga pengguna ditampilkan dua opsi, apakah pengguna ingin ke membeli,
    #atau pengguna merupakan sebuah admin yang ingin memanajemen program.
    def MainMenu(self):
        self.setWindowTitle('Main Menu')
        self.IC.resetOrder()
        VBox = QVBoxLayout()
        self.setStyleSheet("QMainWindow {background-color: Lavender;}")
        self.applabel = QLabel("\nSTARLA x STORE\n")
        self.applabel.setStyleSheet("""
        QLabel {
            color: lightcoral;
            font-size: 34px;
            font: bold italic large "Times New Roman";
        }
        """)

        self.applabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VBox.addWidget(self.applabel)

        self.labelIcon = QLabel()
        ###print(self.iconLink)
        self.labelpixmap = QPixmap('{}'.format(self.iconLink))
        self.scaled_labelpixmap = self.labelpixmap.scaled(250, 200)
        self.labelIcon.setPixmap(self.scaled_labelpixmap)
        self.labelIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VBox.addWidget(self.labelIcon)
        fill = QLabel()
        masuk = QPushButton("Mulai")
        masuk.clicked.connect(lambda: self.login("user", "user"))
        admin = QPushButton("Admin")
        admin.clicked.connect(self.AdminLogin)
        VBox.addWidget(fill)
        VBox.addWidget(masuk)
        VBox.addWidget(admin)
        widg = QWidget()
        widg.setLayout(VBox)
        self.setCentralWidget(widg)

    #Method yang berfungsi sebagai media agar pengguna biasa
    #tidak dapat mengakses menu yang hanya dapat di akses
    #pengguna administrasi
    def AdminLogin(self):
        self.setWindowTitle('Login Window')
        self.update_password()
        VBox = QVBoxLayout()
        username_label = QLabel ('username:', self)
        username_label.setStyleSheet("""
        QLabel {
            color: bold black;
            }""")
        username_input = QLineEdit(self)
        HBox0 = QHBoxLayout()
        HBox0.addWidget(username_label)
        HBox0.addWidget(username_input)
        VBox.addLayout(HBox0)

        #Create Password and its input boxes
        password_label = QLabel('password:', self)
        password_label.setStyleSheet("""
        QLabel {
            color: bold black;
            }""")
        password_input = QLineEdit(self)
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        HBox1 = QHBoxLayout()
        HBox1.addWidget(password_label)
        HBox1.addWidget(password_input)
        VBox.addLayout(HBox1)

        kembali = QPushButton("Kembali")
        kembali.clicked.connect(self.MainMenu)
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(lambda: self.login(username_input.text(), password_input.text()))
        HBox3 = QHBoxLayout()
        HBox3.addWidget(kembali)
        HBox3.addWidget(login_button)
        VBox.addLayout(HBox3)
        tempWidget = QWidget(self)
        tempWidget.setLayout(VBox)
        self.setCentralWidget(tempWidget)

    # Method yang berfungsi untuk menyamakan 
    def login(self, user, pswd):
        ###print(user, pswd)
        stats = self.findUser(user, pswd)
        ###print(stats)
        if stats and stats == "user":
            self.UserMenu()
        elif stats and stats == "admin":
            self.adminMenu()
        else:
            error = ErrorPopUp()
            error.error("User atau Password Salah!")
            error.exec()

    # Method yang berfungsi untuk memperbaharui widget program utama
    def UpdateDisplay(self, Update):
            self.centralWidget(Update)

    # Method yang berfungsi untuk menampilkan menu ke pada pengguna biasa
    def UserMenu(self):
        self.setWindowTitle('User Menu')
        self.loadLogic()
        self.scrollWidget().update()
        self.VBox1 = QVBoxLayout()
        self.HBox1 = QHBoxLayout()

        out = QPushButton("Log Out")
        out.clicked.connect(self.MainMenu)
        self.VBox1.addWidget(self.scrollWidget())
        refreshB = QPushButton("Refresh")
        refreshB.clicked.connect(self.updateScroll)
        self.label = QPushButton("Finalkan Pembelian")
        self.HBox1.addWidget(out)
        self.HBox1.addWidget(self.label)
        self.HBox1.addWidget(refreshB)
        self.label.clicked.connect(self.checkout)  
        self.VBox1.addLayout(self.HBox1)
        widget = QWidget()
        widget.setLayout(self.VBox1)
        self.setCentralWidget(widget)

    # Method untuk menyimpan konfigurasi program saat ini
    def saveLogic(self):
        ##self.filepath, _ = QFileDialog.getSaveFileName(self, 'Save File')
        ###print(self.filepath)
        ##filtxt = str(self.filepath)  
        self.IC.saveCurrentItems()
        QGuiApplication.processEvents()

    # Method untuk mmemuat konfigurasi program yang disimpan sebelumnya
    def loadLogic(self):
        ##self.filepath, _ = QFileDialog.getOpenFileName(self, 'Load File')
        ###print(self.filepath)
        ##filtxt = str(self.filepath) 
        self.IC.loadItems()
        ##data = self.IC.get()
        ###print("This is Load Logic: {}".format(data))
        self.updateScroll()
        self.update()
        QGuiApplication.processEvents()

    # Method untuk memperbaharui widget guling pada menu pengguna user dan
    # menu pengguna admin
    def updateScroll(self):
        self.clearScrollWidget()
        self.update()

    # Method yang berfungsi untuk menampilkan menu administrasi ke pengguna
    def adminMenu(self):
        self.setWindowTitle('Admin Menu')
        self.loadLogic()
        self.updateScroll()
        VBox0 = QVBoxLayout()
        self.loc = QLineEdit()
        self.loc.setText(self.tempImgFile)
        refreshB = QPushButton("Refresh")
        refreshB.clicked.connect(self.updateScroll)
        showUserB = QPushButton("Ganti Password Admin")
        showUserB.clicked.connect(self.changePasswordMenu)
        tambahBarang = QPushButton("Tambah Barang")
        tambahBarang.clicked.connect(self.tambahBarang)
        ubahBarang = QPushButton("Ubah Barang")
        ubahBarang.clicked.connect(self.tambahBarang)
        hapusBarang = QPushButton("Hapus Barang")
        hapusBarang.clicked.connect(self.hapusBarang)
        buttonK = QPushButton("LogOut")
        buttonK.clicked.connect(self.MainMenu)
        VBox0.addWidget(showUserB)
        VBox0.addWidget(tambahBarang)
        VBox0.addWidget(ubahBarang)
        VBox0.addWidget(hapusBarang)
        VBox0.addWidget(buttonK)
        self.VBox1 = QVBoxLayout()
        widg = self.scrollWidget()
        self.VBox1.addWidget(widg)
        self.label = QPushButton("Finalkan Pembelian")
        self.label.clicked.connect(self.checkout)
        HBox1 = QHBoxLayout()
        HBox1.addWidget(self.label)
        HBox1.addWidget(refreshB)
        self.VBox1.addLayout(HBox1)
        HBox0 = QHBoxLayout()
        HBox0.addLayout(VBox0)
        HBox0.addLayout(self.VBox1)
        widget = QWidget()
        widget.setLayout(HBox0)
        self.setCentralWidget(widget)
    
    # Method yang berguna sebagai menu agar pengguna dapat berinteraksi dan mengganti
    # Sandi admin
    def changePasswordMenu(self):
        self.update_password()
        lab1 = QLabel("Masukkan Password Sebelumnya: ")
        lab2 = QLabel("Masukkan Password Baru:       ")
        lab3 = QLabel("Masukkan Ulang Password Baru: ")

        lineIn1 = QLineEdit()
        lineIn2 = QLineEdit()
        lineIn3 = QLineEdit()

        submit = QPushButton("Selesai")
        submit.clicked.connect(lambda: self.changeProcess(lineIn1.text(), lineIn2.text(), lineIn3.text()))
        back = QPushButton("Kembali")
        back.clicked.connect(self.adminMenu)

        H1 = QHBoxLayout()
        H1.addWidget(lab1)
        H1.addWidget(lineIn1)

        H2 = QHBoxLayout()
        H2.addWidget(lab2)
        H2.addWidget(lineIn2)

        H3 = QHBoxLayout()
        H3.addWidget(lab3)
        H3.addWidget(lineIn3)

        H4 = QHBoxLayout()
        H4.addWidget(back)
        H4.addWidget(submit)

        Vbox = QVBoxLayout()
        Vbox.addLayout(H1)
        Vbox.addLayout(H2)
        Vbox.addLayout(H3)
        Vbox.addLayout(H4)

        widg = QWidget()
        widg.setLayout(Vbox)
        self.setCentralWidget(widg)
    
    # Method yang berfungsi untuk memproses perubahan sandi baru
    def changeProcess(self, curr, new, rnew):
        if curr == self.admin["admin"]:
            if new == rnew:
                self.change_password(new)
                self.error = "Sukses!"
                self.errorPop()
                self.adminMenu()
                return
            self.error = "Sandi Baru Tidak Sama!"
            self.errorPop()
            self.adminMenu()
            return
        self.error = "Sandi Salah!"
        self.errorPop()
        self.adminMenu()

    # Method yang berfungsi untuk menampilkan menu untuk menambahkan barang ke dalam program
    def tambahBarang(self):
        kembali = QPushButton("Kembali")
        kembali.clicked.connect(self.adminMenu)
        input_N = QLabel("Nama Barang: ")
        input_NB = QLineEdit()
        name_box = QHBoxLayout()
        name_box.addWidget(input_N)
        name_box.addWidget(input_NB)
        amnt_N = QLabel("Jumlah Barang: ")
        amnt_NB = QLineEdit()
        amnt_box = QHBoxLayout()
        amnt_box.addWidget(amnt_N)
        amnt_box.addWidget(amnt_NB)
        prc_N = QLabel("Harga Satuan: ")
        prc_NB = QLineEdit()
        price_box = QHBoxLayout()
        price_box.addWidget(prc_N)
        price_box.addWidget(prc_NB)
        img_N = QLabel("Pilih Lokasi Gambar: ")
        img_NB = QPushButton("Pilih")
        img_NB.clicked.connect(self.openImgFile)
        img_box = QHBoxLayout()
        img_box.addWidget(img_N)
        img_box.addWidget(img_NB)
        info_N = QLabel("Informasi Barang: ")
        info_NB = QLineEdit()
        info_box = QHBoxLayout()
        info_box.addWidget(info_N)
        info_box.addWidget(info_NB)
        VBox0 = QVBoxLayout()
        VBox0.addLayout(name_box)
        VBox0.addLayout(amnt_box)
        VBox0.addLayout(price_box)
        VBox0.addLayout(img_box)
        VBox0.addWidget(self.loc)
        VBox0.addLayout(info_box)
        konfirmasi = QPushButton("Konfirmasi")
        konfirmasi.clicked.connect(lambda: self.inputted(input_NB.text(), amnt_NB.text(), prc_NB.text(), self.loc.text(), info_NB.text()))
        HBox = QHBoxLayout()
        HBox.addWidget(kembali)
        HBox.addWidget(konfirmasi)
        VBox0.addLayout(HBox)
        widg = QWidget()
        widg.setLayout(VBox0)
        self.setCentralWidget(widg)
    
    # Method yang berfungsi untuk menambahkan barang ke dalam program
    def inputted(self, nama, amnt, prc, img, info):     
        if "\\" in img:
            img = img.replace("\\", "/")
        self.IC.addItem(nama.lower(), nama, int(amnt), int(prc), img, info)
        self.tempImgFile = ""
        self.loc.setText(self.tempImgFile)
        self.adminMenu()

    # Method yang berfungsi untuk mengecek apakah nama barang ada di dalam program
    def avalNamaBarang(self):
        data = self.IC.get()
        VBox0 = QVBoxLayout()
        scrollable = Scrolly()
        for key in data:
            scrollable.add_widget(itemBoxDetail(key, data[key].amnt, data[key].price))
        VBox0.addWidget(scrollable)
        return VBox0

    # Method yang berfungsi untuk menampilkan menu untuk menghapus barang ke pada
    # pengguna
    def hapusBarang(self):
        kembali = QPushButton("Kembali")
        kembali.clicked.connect(self.adminMenu)
        HBox = QHBoxLayout()
        VBox = QVBoxLayout()
        x = self.avalNamaBarang()
        VBox.addLayout(x)
        HBox0 = QHBoxLayout()
        name = QLabel("Nama Barang: ")
        inputN = QLineEdit()
        HBox0.addWidget(name)
        HBox0.addWidget(inputN)
        VBox.addLayout(HBox0)
        konfirmasi = QPushButton("Konfirmasi")
        konfirmasi.clicked.connect(lambda: self.delBarang(inputN.text()))
        HBox.addWidget(kembali)
        HBox.addWidget(konfirmasi)
        VBox.addLayout(HBox)
        widget = QWidget()
        widget.setLayout(VBox)
        self.setCentralWidget(widget)

    #Method yang berfungsi untuk menghapus barang
    def delBarang(self, name):
        self.IC.delItem(name)
        self.hapusBarang()
        self.updateScroll()

    # Method yang berfungsi untuk menyimpan lokasi gambar barang yang ingin
    # ditambahkan oleh pengguna
    def openImgFile(self):
        filname, _ = QFileDialog.getOpenFileName(self, 'Load File')
        self.tempImgFile = filname
        self.loc.setText(self.tempImgFile)

# Percabangan if yang berfungsi sebagai pengaman, sehingga program
# tidak akan berjalan jika di impor oleh kode python lain
if __name__ == '__main__':
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec()