# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:53:40 2023

@author: a5278
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 10:50:24 2023

@author: a5278
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:06:04 2023

@author: a5278
"""


from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import QAbstractTableModel, Qt

import numpy as np
# from matplotlib import pyplot as plt
import pandas as pd
import datetime as dt
# import time
# import os
# import glob


# import requests
# from io import BytesIO
# import pandas as pd

from threading import Timer
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

import serial
# import os
# import pandas as pd
# import datetime as dt
import pynmea2
#%%

#%%
class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class CustomDialog(QDialog):
    def __init__(self,df):
        super().__init__()
        
        self.setWindowTitle("Edit table")

        QBtn = QDialogButtonBox.Ok 

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Edit table")
        # self.layout.addWidget(message)
        
        self.table = QtWidgets.QTableView()

        self.model = PandasModel( df)
        self.table.setModel(self.model)
        # self.table.setFixedWidth(200)

        self.layout.addWidget(self.table)       
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
        # self.setMinimumSize(200, 500)
        self.setMinimumSize(200, 500)

        self.df=df
        
        # return df
    # def submit_table(self):
    #     print(self.df)
        
    #     self.accept
    #     return self.df
        
        
class MainWindow(QtWidgets.QMainWindow):

    # def get_nmea(self,comport='COM13',baudrate=4800):
    
    #     with serial.Serial(comport, baudrate=baudrate, timeout=1) as ser:
    #         # read 10 lines from the serial output
    #         for i in range(15):
    #             nmea_sentence = ser.readline().decode('ascii', errors='replace')
    #             # print(nmea_sentence.strip())
                
    #             # if nmea_sentence[0:6] == '$GPGGA':
    #             #     GPGGA = pynmea2.parse(nmea_sentence)
    #             if nmea_sentence[0:6] == '$GPRMC':
    #                 GPRMC = pynmea2.parse(nmea_sentence)               
    #                 # print(GPRMC)    

         
    
    #         tx = GPRMC.datestamp.strftime('%Y-%m-%d ') + GPRMC.timestamp.strftime("%H:%M:%S")           
    #         t = pd.to_datetime( tx )
            
    
    #         lat= GPRMC.latitude 
    #         lon= GPRMC.longitude
            
    #     return t, lat , lon

    def serial_ports(self):
        """ Lists serial port names
    
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
                
            
 
    def log_nmea(self,comport='COM13',baudrate=4800):
     try:
        with serial.Serial(comport, baudrate=baudrate, timeout=1) as ser:
            # read 10 lines from the serial output
            for i in range(15):
                nmea_sentence = ser.readline().decode('ascii', errors='replace')
                # print(nmea_sentence.strip())
                
                # if nmea_sentence[0:6] == '$GPGGA':
                #     GPGGA = pynmea2.parse(nmea_sentence)
                if nmea_sentence[0:6] == '$GPRMC':
                    GPRMC = pynmea2.parse(nmea_sentence)               
                    # print(GPRMC)    
                # nmea_sentence = ser.readline()
                # nmea_data += nmea_sentence                 
            # print(GPRMC.latitude)
            # print(GPRMC.longitude)
            # print(GPRMC.timestamp)
            # print(GPRMC.datestamp)
            
            # print(GPGGA.latitude)
            # print(GPGGA.longitude)
            # print(GPGGA.timestamp)
    
            tx = GPRMC.datestamp.strftime('%Y-%m-%d ') + GPRMC.timestamp.strftime("%H:%M:%S")
            
            t = pd.to_datetime( tx )
            
            self.current_gpstime=t
            self.current_lat=GPRMC.latitude 
            self.current_lon= GPRMC.longitude
            
            self.df_gps.loc [len(self.df_gps)] = [ t, GPRMC.latitude , GPRMC.longitude] 
            # df=pd.read_csv('gps.csv',index_col=0)
            # df.loc[len(df)] = [ t, GPRMC.latitude , GPRMC.longitude]
            # df.to_csv('gps.csv')
     except Exception as e:
            print(e)         
                
        
    def start_obs_period(self): 
        self.obs_running=True
        self.df=pd.DataFrame(columns=['timestamp','species','groupsize','distance','bearing','visibility','comment','lat','lon'])
        self.model = PandasModel( self.df)
        self.table.setModel(self.model)
            
        self.obs_starttime= pd.to_datetime( dt.datetime.now() )
        
        # items = ("Sebastian","Bjørn", "Astrid", "Linn","Andy")	
        items = self. df_observer.iloc[:,0].values.tolist() 
        self.observer, ok = QtWidgets.QInputDialog.getItem(self, "Select observer", 
                                                 "Observers", items, 0, False)
        
        items = ("Starbord","Portside")	
        self.side, ok = QtWidgets.QInputDialog.getItem(self, "Select observed quarter", 
                                                 "Side", items, 0, False)

        items = ("clear","clouds","fog","glare")	
        self.vis_status, ok = QtWidgets.QInputDialog.getItem(self, "Input Dialog", 
                                                 "Select visibilty conditions", items, 0, False)
                    
        # self.waveheight, ok = QtWidgets.QInputDialog.getInt(self, 'Input Dialog',
        #                                         'Wave height:')            
        items = np.arange(21).astype(str)	
        wstr, ok = QtWidgets.QInputDialog.getItem(self, 'Input Dialog',
                                              'Wave height in m:', items, 0, False)  
        self.waveheight = int(wstr)
         
        # self.observer, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
        #                                         'Enter Observer ID:')
        # self.seastate, ok = QtWidgets.QInputDialog.getInt(self, 'Input Dialog',
        #                                         'Seastate:')
        # self.statusstring = 'Logging! Observer: '+ self.observer + ' / Side: ' + self.side  + ' / Sea state: ' +  str( self.seastate)  \
        #     + ' / Start@'+str(self.obs_starttime)
        self.statusstring = 'Logging! Observer: '+ self.observer + ' / Side: ' + self.side   + ' / Start@'+str(self.obs_starttime)
            
        print( self.statusstring)
        self.label1.setText(self.statusstring)
        self.button_start.setEnabled(False)    
        self.button_stop.setEnabled(True)  
        self.button_submit.setEnabled(True)  
        self.button_quit.setEnabled(False)  

        self.df_gps= pd.DataFrame(columns=['time','lat','lon'])
        # df.to_csv('gps.csv')
        self.timer_gps = RepeatTimer(5, self.log_nmea , args=(self.gpsport,self.gpsbaudrate) )
        self.timer_gps.start()
        
        
        
        
        # clear_dat = 'http://' + self.phoneip + '/control?cmd=clear'  #Clearing a data collection
        # r = requests.get(clear_dat)
        # start_dat = 'http://' + self.phoneip + '/control?cmd=start'  #Starting a data collection
        # r = requests.get(start_dat)


        
    def stop_obs_period(self): 
        self.obs_running=False
        self.obs_stoptime= pd.to_datetime( dt.datetime.now() )
  
        self.statusstring = 'Not logging'
        print( self.statusstring)
        self.label1.setText(self.statusstring)
        self.button_stop.setEnabled(False)  
        self.button_start.setEnabled(True)     
        self.button_submit.setEnabled(False)  
        self.button_quit.setEnabled(True)  

        # save df
        if len(self.df)==0:
            self.df.loc[0,'timestamp'] = np.nan

        self.df['observer'] = self.observer
            
        self.df['observation_period_starttime'] =  self.obs_starttime
        self.df['observation_period_stoptime'] =  self.obs_stoptime
        self.df['forward_quarter_side'] =  self.side
        self.df['vis_status'] =  self.vis_status
        self.df['waveheight'] =  self.waveheight
        # self.df['seastate'] =  self.seastate

        savename=self. obs_starttime.strftime('mmobs_%Y_%m_%d_%H_%M_%S')
        print('location is:' + savename)

        # savename = QtWidgets.QFileDialog.getSaveFileName(self,"", "", "csv files (*.csv)")
        # print('location is:' + savename[0])
        
        ######
        self.timer_gps.cancel()

        # gpsactive=False
        # try:
        #     gpstrack=pd.read_csv('gps.csv',index_col=0)
        #     if len(gpstrack)>2:
        #         gpsactive=True

        # except:
        #     print('no GPS')
        ###### gps
        
        if len(savename[0])>0:
                self.df.to_csv(savename+'_obs.csv')    
                # if gpsactive==True:
                self.df_gps.to_csv(savename+'_track.csv')    
                    
                    
                        
        self.button_stop.clicked.connect(self.stop_obs_period)     
        self.button_stop.setStyleSheet("background-color: red ; font-size: 18pt")
        self.button_stop.setEnabled(False)  
      

    def removeline(self):
        # self.df.drop(self.df.tail(1).index,inplace=True)
        if len(self.df)>0:
            self.df.drop(0,inplace=True)
            self.df.reset_index(drop=True,inplace=True)
            print(self.df)
            self.model = PandasModel( self.df)
            self.table.setModel(self.model)
        
    def func_quit(self):
        # self.statusBar().removeWidget(self.label_1)   
        # self.startautoMenu.setEnabled(True)
        # self.exitautoMenu.setEnabled(False)     
        QtWidgets.QApplication.instance().quit()     
        # QCoreApplication.quit()
        self.close()   

      
    def submitobs(self): 
        
            ######
            # try:
            #     # gpstime,lat,lon = self.get_nmea(comport='COM13',baudrate=4800)
                
            #     # gpstrack=pd.read_csv('gps.csv',index_col=0)
            #     # lat = gpstrack.loc[ len(gpstrack)-1,'lat']
            #     # lon = gpstrack.loc[ len(gpstrack)-1,'lon']
            #     # gpstime = gpstrack.loc[ len(gpstrack)-1,'time']
                
            #     gpstime = self.current_gpstime
            #     lat= self.current_lat
            #     lon= self.current_lon
                
                
            # except:
            #     print('no GPS')
            #     lat=np.nan
            #     lon=np.nan
            #     gpstime=np.nan
            
            gpstime = self.current_gpstime
            lat= self.current_lat
            lon= self.current_lon
                
            ###### gps
            
            t= pd.to_datetime( dt.datetime.now() )
            s=self.species_widget.currentItem().text()
            g=self.group_widget.currentItem().text()
            d=self.distance_widget.currentItem().text()
            b= self.bearing_widget.currentItem().text()
            v=self.visibility_widget.currentItem().text()
            
            c=   self.comment.text()
            
            # print(str(t)+s+g+d+b)
            
            self.df_new= pd.DataFrame(columns=['timestamp','species','groupsize','distance','bearing','visibility','comment'])
            self.df_new.loc[0,'timestamp'] = t
            self.df_new.loc[0,'species'] = s
            self.df_new.loc[0,'groupsize'] = g
            self.df_new.loc[0,'distance'] = d
            self.df_new.loc[0,'bearing'] = b
            self.df_new.loc[0,'visibility'] = v             
            self.df_new.loc[0,'comment'] = c
            self.df_new.loc[0,'lat'] = lat
            self.df_new.loc[0,'lon'] = lon
            self.df_new.loc[0,'gpstime'] = gpstime

                            
            self.df=pd.concat([self.df_new , self.df],ignore_index=True)
            
            
            print(self.df)
            
            self.model = PandasModel( self.df)
            self.table.setModel(self.model)

                

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

       ##############
        self.obs_running= False
        self.statusstring = 'Not logging'
        
        self.current_gpstime=np.nan
        self.current_lat=np.nan
        self.current_lon= np.nan
        self.gpsport='COM13'
        self.gpsbaudrate=4800
        

        
        
        # self.phoneip='192.168.78.10:8080'
           
        self.df= pd.DataFrame(columns=['timestamp','species','groupsize','distance','bearing','visibility','comment','lat','lon'])

        outer_layout = QtWidgets.QVBoxLayout()

        
        top_layout = QtWidgets.QHBoxLayout()       
        
        self.button_start=QtWidgets.QPushButton('Start')
        
        
        self.button_start.clicked.connect(self.start_obs_period)     
        self.button_start.setStyleSheet("background-color: green; font-size: 18pt")
        # self.button_start.setStyleSheet("font-size: 18pt")

        top_layout.addWidget(self.button_start)
        
        self.button_stop=QtWidgets.QPushButton('Stop')
        self.button_stop.clicked.connect(self.stop_obs_period)     
        self.button_stop.setStyleSheet("background-color: red ; font-size: 18pt")
        self.button_stop.setEnabled(False)  
        
        top_layout.addWidget(self.button_stop)
        

        self.label1=QtWidgets.QLabel(self.statusstring)
        top_layout.addWidget( self.label1 )        

    
   
 
        button_removeline=QtWidgets.QPushButton('Remove last entry')
        
        button_removeline.clicked.connect(self.removeline)
        button_removeline.setStyleSheet( "font-size: 18pt")
        top_layout.addWidget(button_removeline)     
        
        
        self.button_quit=QtWidgets.QPushButton('Quit')
        self.button_quit.clicked.connect(self.func_quit)
        self.button_quit.setStyleSheet( "font-size: 18pt")
        self.button_quit.setEnabled(True)  

        top_layout.addWidget(self.button_quit)     
        
        
        
        
        # top_layout.addWidget(button_no)
        # top_layout.addWidget(button_previous)
        
        # button_quit=QtWidgets.QPushButton('Quit')
        # def funquit():
        #        msg = QtWidgets.QMessageBox()
        #        msg.setIcon(QtWidgets.QMessageBox.Information)   
        #        msg.setText("Are you sure you want to quit and loose all data?")
        #        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        #        returnValue = msg.exec()
        #        if returnValue == QtWidgets.QMessageBox.Yes:
        #            print('closing')
        #            QtWidgets.QApplication.instance().quit()
        #            # QApplication.quit()
        # button_quit.clicked.connect(funquit)
        # button_quit.setStyleSheet( "font-size: 18pt")
        # top_layout.addWidget(button_quit)


        
        inputbuttons_layout = QtWidgets.QHBoxLayout()
        
        self.df_species = pd.DataFrame(["Unknown whale","Unknown seal", "Fin whale",\
                                        "Humpback whale","Blue whale",'Minke whale','Sei whale',\
                                            'Southern Right whale','Antarctic fur seal','Elephant seal',\
                                                'Orca','See Comment','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],\
                                       columns=['Species'])	
                
            # ask for observerlists

            
        dlg2 = CustomDialog(self.df_species)
        dlg2.exec()
        self.df_species = dlg2.df        
        
        # ask for observerlists
        self.df_observer = pd.DataFrame(["Sebastian","Bjørn", "Astrid", "Linn","Andy",'','','','','','','','','','','','','','','','','','','','','','','','','','',''],columns=['Observers'])	
        dlg = CustomDialog(self.df_observer)
        dlg.exec()
        self.df_observer = dlg.df
        
        species_layout= QtWidgets.QVBoxLayout()
        species_layout.addWidget( QtWidgets.QLabel('Species') )                
  		# creating a QListWidget
        self.species_widget = QtWidgets.QListWidget()
  		# setting geometry to it
        # species_widget.setGeometry(50, 70, 150, 60)
  		# adding items to the list widget
          
        for name in self.df_species.iloc[:,0]:
            self.species_widget.addItem(QListWidgetItem(name))

        # self.species_widget.addItem(QListWidgetItem("Unknown whale"))
        # self.species_widget.addItem(QListWidgetItem("Unknown seal"))
        # self.species_widget.addItem(QListWidgetItem("Fin whale"))
        # self.species_widget.addItem(QListWidgetItem("Blue whale"))
        # self.species_widget.addItem(QListWidgetItem("Humpback whale"))
        # self.species_widget.addItem(QListWidgetItem("Minke whale"))
        # self.species_widget.addItem(QListWidgetItem("Sei whale"))
        # self.species_widget.addItem(QListWidgetItem("Southern Right whale"))
        
        # self.species_widget.addItem(QListWidgetItem("Antarctic fur seal"))
        # self.species_widget.addItem(QListWidgetItem("Elephant seal"))
        # self.species_widget.addItem(QListWidgetItem("See Comment"))
        
        
        self.species_widget.setStyleSheet( "font-size: 18pt")

  		# setting current row
        self.species_widget.setCurrentRow(0)
        species_layout.addWidget(self.species_widget)        
        inputbuttons_layout.addLayout(species_layout)
  
        group_layout= QtWidgets.QVBoxLayout()
        group_layout.addWidget(QtWidgets.QLabel( 'Groupsize') ) 
  		# creating a QListWidget
        self.group_widget = QtWidgets.QListWidget()
  		# setting geometry to it
        # species_widget.setGeometry(50, 70, 150, 60)
  		# adding items to the list widget
        gsize=np.arange(1,11)  
        gsize=np.append(gsize, np.arange(20,110,10) )
        for i in gsize:
            item = QListWidgetItem(str(i))
            self.group_widget.addItem(item)
  
  		# setting current row
        self.group_widget.setCurrentRow(0)
        self.group_widget.setStyleSheet( "font-size: 18pt")

        group_layout.addWidget(self.group_widget)  
        inputbuttons_layout.addLayout(group_layout)
        
        
        distance_layout= QtWidgets.QVBoxLayout()
        distance_layout.addWidget(QtWidgets.QLabel( 'Distance in m') ) 
        self.distance_widget = QtWidgets.QListWidget()
        gsize=np.arange(0,1100,100)  
        gsize=np.append(gsize, np.arange(1500,15000,500) )
        for i in gsize:
            item = QListWidgetItem(str(i))
            self.distance_widget.addItem(item)
  		# setting current row
        self.distance_widget.setCurrentRow(0)
        self.distance_widget.setStyleSheet( "font-size: 18pt")
        distance_layout.addWidget(self.distance_widget)  
        inputbuttons_layout.addLayout(distance_layout)


######

        visibility_layout= QtWidgets.QVBoxLayout()
        visibility_layout.addWidget(QtWidgets.QLabel( 'Visibility in m') ) 
        self.visibility_widget = QtWidgets.QListWidget()
        gsize= np.arange(1000,21000,1000) 
        for i in gsize:
            item = QListWidgetItem(str(i))
            self.visibility_widget.addItem(item)
  		# setting current row
        self.visibility_widget.setCurrentRow(0)
        self.visibility_widget.setStyleSheet( "font-size: 18pt")
        visibility_layout.addWidget(self.visibility_widget)  
        inputbuttons_layout.addLayout(visibility_layout)
        
        #######
        
        # bearing_layout= QtWidgets.QVBoxLayout()
        # bearing_layout.addWidget(QtWidgets.QLabel( 'Bearing') ) 
        # self.valudiallabel=QtWidgets.QLabel( '0') 
        # bearing_layout.addWidget( self.valudiallabel ) 
        # def dial_changed():
        #     self.valudiallabel.setText(str(self.dial.value()))
        # self.dial = QtWidgets.QDial()
        # self.dial.setMinimum(-180)
        # self.dial.setMaximum(180)
        # self.dial.setValue(0)
        # self.dial.setNotchesVisible(True)
        # self.dial.valueChanged.connect(dial_changed)



        
        # bearing_layout.addWidget(self.dial)  
        # inputbuttons_layout.addLayout(bearing_layout)
        
        bearing_layout= QtWidgets.QVBoxLayout()
        bearing_layout.addWidget(QtWidgets.QLabel( 'Bearing in degree') ) 
        self.bearing_widget = QtWidgets.QListWidget()
        gsize= np.arange(0,100,5) 
        for i in gsize:
            item = QListWidgetItem(str(i))
            self.bearing_widget.addItem(item)
  		# setting current row
        self.bearing_widget.setCurrentRow(0)
        self.bearing_widget.setStyleSheet( "font-size: 18pt")
        bearing_layout.addWidget(self.bearing_widget)  
        inputbuttons_layout.addLayout(bearing_layout)
        
        ######

        
        
        
        # combine layouts together
        
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(inputbuttons_layout)

        # comment        
        self.comment=QtWidgets.QLineEdit()
        self.comment.setText('Comment') 
        self.comment.setStyleSheet( "font-size: 18pt")
        outer_layout.addWidget(self.comment)      
        
        
        # submit button
        self.button_submit=QtWidgets.QPushButton('Submit observation')
        self.button_submit.setEnabled(False)  
        self.button_submit.setStyleSheet("background-color: yellow; font-size: 18pt")
        
                        

        self.button_submit.clicked.connect(self.submitobs)
        outer_layout.addWidget(self.button_submit)       

 
######## table
        
        self.table = QtWidgets.QTableView()

        self.model = PandasModel( self.df)
        self.table.setModel(self.model)
        self.table.setFixedHeight(200)

        outer_layout.addWidget(self.table)       
        
    
                
        ######        
        widget = QtWidgets.QWidget()
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
  
        self.show()
        
        #### scan serial ports fro gps 
        self.portlist = self.serial_ports()
        items = self.portlist	
        self.gpsport, ok = QtWidgets.QInputDialog.getItem(self, "Select GPS COM port", 
                                                 "Ports:", items, 0, False)
        print(self.gpsport)    
        

        

        

app = QtWidgets.QApplication(sys.argv)
app.setApplicationName("MMOBS")
app.setStyleSheet("QLabel{font-size: 18pt;}")


w = MainWindow()
sys.exit(app.exec_())


