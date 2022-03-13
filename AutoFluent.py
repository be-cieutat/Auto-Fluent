# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:00:52 2022
@author: boyan

This code runs for Edge exclusively.
Maybe I'll introduce a slider for browser selection in V.2
I plan on a tutorial mode with pop-ups explaining the app behaviour.
The stored data are encoded for more protection.
"""
#%% Debug

stored_id = "boyan-edouard.cieutat@edu.devinci.fr"
stored_password = "Sonnet45"
tutorial = 0

#%% Def

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import PySimpleGUI as sg
from cryptography.fernet import Fernet

"""
VARIABLES:
    ID:Identifiant Utilisateur, str
    PASS: Mot de Passe Utilisateur, str
    TUTORIAL: Valeur d'activation du mode tutoriel => actif si TUTORIAL==True
              Au premier lancement TUTORIAL=True, bool 
"""


#%% Launch, Password and UI

def ReadDATA():
    try:
        #Read key and data
        with open('key.key','rb') as file:
            key = file.read()
        with open('DATA.txt','rb') as f:
            encrypted=f.read()
        #Decrypt data
        decrypted_data = Fernet(key).decrypt(encrypted)
        #Decode data byte values
        data = decrypted_data.decode('utf-8').split(';')
        return data
    except FileNotFoundError:
        return [None,None,True]

def WriteDATA(ID,PASS,TUTORIAL):
    #Generate associated key
    key = Fernet.generate_key()
    #Format data
    str_data=str(ID)+';'+str(PASS)+';'+str(TUTORIAL)
    data=bytes(str_data, 'utf-8')
    #Encrypt data
    encrypted=Fernet(key).encrypt(data)
    #Save key and data
    with open('key.key','wb') as file:
        file.write(key)
    with open('DATA.txt','wb') as f:
        f.write(encrypted)

def UI(ID,PASS,TUTORIAL):
    icon = b'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'
    sg.theme('SystemDefault1')
    
    layout_l = [
        [sg.Image(icon)
          ],
        [sg.Text('Auto-Fluent 1.0; licensé CC BY 4.0',font='Courier 8')
          ]
        ]

    layout_r = [
        [sg.Text('Identifiant: ',font='Courier 12 bold'), sg.InputText(size=35,default_text=ID,enable_events=True,key='-ID-')
          ],
        [sg.Text('Mot de Passe:',font='Courier 12 bold'), sg.InputText(size=35,default_text=PASS,password_char='*',enable_events=True,key='-PASS-')
          ],
        [sg.Checkbox('Afficher le Mot de Passe',font='Courier 10',enable_events=True,key='-DISP_PASS-'),sg.Checkbox('Se souvenir de moi.',font='Courier 10',enable_events=True,key='-REMEMBER_PASS-')
          ],
        [sg.Button(button_text='Se connecter',font='Courier 9'), sg.Button(button_text='Quitter',font='Courier 9')]
        ]

    layout= [[sg.T('AutoFluent', font='_ 20 bold', justification='c', expand_x=True)],[sg.Col(layout_l), sg.Col(layout_r)]]

    window = sg.Window('AutoFluent - Your Personnal Homework Assistant',layout,finalize=True)
    # window.SetIcon('AutoFluent.ico')
    return window

def LaunchAPP(ID,PASS,TUTORIAL):
    DISP_PASS=False
    REMEMBER_PASS=False
    window=UI(ID,PASS,TUTORIAL)
    while True:
        event, values = window.read()
        ID=values['-ID-']
        PASS=values['-PASS-']
        if event in (sg.WIN_CLOSED, 'Quitter'):
            CONTINUE=False
            break
        if event == 'Se connecter':
            CONTINUE=True
            break
        if event == '-REMEMBER_PASS-':
            REMEMBER_PASS = not REMEMBER_PASS
            WriteDATA(ID,PASS,False) if REMEMBER_PASS else WriteDATA('','',False)             
        if event == '-DISP_PASS-':
            DISP_PASS = not DISP_PASS
            print(DISP_PASS,'|',values['-PASS-'])
            # PASS=values['-PASS-']
            # window['-PASS-'].update(password_char='*' if DISP_PASS else None)
    window.close()
    return CONTINUE


#%% Auto-Log
""" Must be in __main__"""
def LaunchDRIVER():
    driver = webdriver.Edge()
    driver.get('https://portal.gofluent.com/app/dashboard')
    login = driver.find_element(By.NAME,"login")
    password = driver.find_element(By.NAME,"password")
    login.clear()
    login.send_keys(ID)
    password.clear()
    password.send_keys(PASS)
    password.send_keys(Keys.ENTER)
    while True:
         None   
        

#%% Network_Read

""" for reference https://selenium-python.readthedocs.io/navigating.html"""

#     Script = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
#     NetData = str(driver.execute_script(Script))

# while True:
#      # if [condition de quiz]:
#      NetData = str(driver.execute_script(Script))
#      debut = NetData.find('quiz')
#      if debut !=-1:
#          fin = NetData.find('}',debut)
#          quiz=Netdata[debut:fin]
#          Loop=False
#          print(quiz)
 


#%% Main
if __name__=='__main__':
    #Lecture DATA 
    data=ReadDATA()
    ID=data[0]
    PASS=data[1]
    TUTORIAL=data[2]
    
    if LaunchAPP(ID,PASS,TUTORIAL):
        LaunchDRIVER()
   