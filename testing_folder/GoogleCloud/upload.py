# pip install Office365-REST-Python-Client
# https://medium.com/@giniya86/upload-file-to-sharepoint-site-using-python-5e9d06860538

# Contains a class which is constructed with a session name.
# When constructed, format files on Sharepoint using the session name. 
# Look for the top level folder Wild-Futures-DMMS in the user's directory. If not there, make it.
# Make a folder inside with the session name (can be based on the time?)
# Periodically upload outputs to this lower level folder (csv, mp4, jpg, txt)
# The user can navigate on their drive to this location.

import os
import datetime
import time
import threading

# Google Drive
# https://pypi.org/project/PyDrive/ vs https://docs.iterative.ai/PyDrive2/
# https://pythonhosted.org/PyDrive/quickstart.html - follow the quickstart guide for handover. 
# https://stackoverflow.com/questions/56434084/google-pydrive-uploading-a-file-to-specific-folder - about saving to specific folders.
# https://stackoverflow.com/questions/66107562/create-new-folder-on-gdrive-using-pydrive-module - about creating a folder
# https://workspace.google.com/marketplace/app/drivewatcher_bot/535963999861 - can use this for automatic notifications?

# Get gauth.ServiceAuth() to get automatic authentication to work.

# Test with the following dummy files:
# - jpg, png
# - mp4
# - csv
# - folders

# To update a file, upload with its id identical to the file to be updated.
# https://stackoverflow.com/questions/56082335/how-to-replace-update-a-file-on-google-drive-with-pydrive

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from googleapiclient.discovery import build
import httplib2

# https://docs.python.org/3/library/email.examples.html
import smtplib
# from email.message import EmailMessage
# from email.mime.text import MIMEText

class GoogleServices:
    def __init__(self, sessionName, authPath ,newFolder=True): # When initialising session, call the class and give the session a name.
        # Save the name of the session for folder creation and navigation.
        self.sessionName = sessionName + str(datetime.datetime.now())

        # Set up Google Drive settings:
        self.settings = {
            "client_config_backend" : "service",
            "service_config" : {
                "client_json_file_path" : f"{authPath}"
            }
        }

        # Connect to Google Drive
        self.gauth = GoogleAuth(settings=self.settings)

        # Legacy:
        # gauth.LocalWebserverAuth() # Need to do something else besides opening browser to complete auth as this can't be done on the pi.
        # gauth.ServiceAuth() # this will do it automatically, but it requires certain auths.

        # Authenticate and authorize using P12 private key, client id
        # and client email for a Service account.
        # :raises: AuthError, InvalidConfigError
        self.gauth.ServiceAuth()
        self.drive = GoogleDrive(self.gauth)

        # Get the Wild-Futures-DMMS Folder id. This needs to be shared with the service account beforehand.
        # A better way of doing this is needed, find the correct query to retrieve it.
        self.topFolder = '0ACG41D1Cz9gpUk9PVA' #self.getRootFolderID('Wild-Futures-DMMS') # root directory id is 'root'

        if newFolder:
            # Create a folder for this session and save its id.
            self.createFolder(self.topFolder, self.sessionName)
            # A delay is necessary for the folder to be created and uploaded before trying to get its id.
            self.sessionFolder = None
            print('Getting session folder id')
            while self.sessionFolder == None:
                time.sleep(0.1)
                self.sessionFolder = self.getFolderID(self.sessionName, self.topFolder)
                print(' . ')
            print('Top Folder:', self.topFolder)
            print('Session Folder:', self.sessionFolder)

        # Grab the mailList from the drive's top folder.
        # self.mailListId = self.getIdOfTitle('mailList.txt', self.topFolder)
        # # print(mailListId)

        # # Get the mail recipients list.
        # self.mailList = self.downloadConfig(self.mailListId)

        # Create a log file.
        self.logFile = self.drive.CreateFile({'title' : f'{self.sessionName}_log.txt', 'parents' : [{'id' : self.sessionFolder}]})
        self.logContent = f'[{datetime.datetime.now()}] Session started.'
        self.logFile.SetContentString(self.logContent)

        # Upload the log file and then get its id for reference.
        self.logFile.Upload()
        self.logId = None
        while self.logId == None:
            time.sleep(0.1)
            self.logId = self.getIdOfTitle(f'{self.sessionName}_log.txt', self.sessionFolder)
            print(' . ')
        print('Log File ID: ' + str(self.logId))
        self.logFile = self.drive.CreateFile({'title' : f'{self.sessionName}_log.txt',
                                               'parents' : [{'id' : self.sessionFolder}],
                                               'id' : self.logId})
        # print(self.logFile)

        print('Session started')

        # Test a dummy upload
        # file1 = self.drive.CreateFile({'title': 'test.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        # file1.SetContentString('testing!') # Set content of the file from given string.
        # # file1.SetContentFile() # As above, but with a file that was already created. Good for MIME types: can do mp4, jpg, png, csv
        # file1.Upload()

        


    def updateLog(self, content):
        # Add a new line to the log. This should probably be threaded?
        self.logContent += f'\n [{datetime.datetime.now()}] {content}'
        self.logFile.SetContentString(self.logContent)
        # self.logFile.Upload()

    def uploadLog(self):
        self.logThread = threading.Thread(target=self.logFile.Upload)
        # if self.logThread.is_alive() == False:
        # print("Uploading log")
        self.logThread.start()
        # else:
            # print("Log upload already in progress, try again.")


    def getIdOfTitle(self, title, parent_directory_id):
        foldered_list=self.drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
        for file in foldered_list:
            if(file['title']==title):
                return file['id']
            return None

    # Create a folder in specified place with specified name.
    def createFolder(self, parentFolderID, subFolderName):
        newFolder = self.drive.CreateFile({'title': subFolderName, "parents": [{"kind": "drive#fileLink", "id": \
            parentFolderID}],"mimeType": "application/vnd.google-apps.folder"})
        newFolder.Upload()

    # Get the ID of the top-level shared folder. This only looks for shared files.
    def getRootFolderID(self, title):
        foldered_list = self.drive.ListFile({'q': "sharedWithMe=true and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
        for file in foldered_list:
            if(file['title']==title):
                return file['id']
            return None

    def getFolderID(self, title, parent_directory_id):
        foldered_list = self.drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
        # print(foldered_list)
        for file in foldered_list:
            if(file['title']==title):
                return file['id']
            return None

    def listFiles(self):
        # print('\nLocal Drive')
        print('\nShared Drive')
        file_list = self.drive.ListFile({'q': "'"+self.topFolder+"' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
        # print('\nShared Folder')
        # file_list = []
        # file_list = self.drive.ListFile({'q': "sharedWithMe=true and trashed=false"}).GetList()
        # for file1 in file_list:
        #     print('title: %s, id: %s' % (file1['title'], file1['id']))
        # print('\nShared Drive')
        # file_list = []
        # file_list = self.drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and trashed=false",
        #                     'teamDriveId': '0ACG41D1Cz9gpUk9PVA',
        #                     'supportsAllDrives': True,
        #                     'corpora': 'drive',
        #                     'includeItemsFromAllDrives': True
        #                     }).GetList()
        # for file1 in file_list:
        #     print('title: %s, id: %s' % (file1['title'], file1['id']))


    def deleteByID(self, id):
        delete = self.drive.CreateFile({'id' : id})
        delete.Delete()

    # Upload a MIME type file to the session folder.
    def upload(self, path): 
        file = self.drive.CreateFile({'parents' : [{'id' : self.sessionFolder}]})
        file.SetContentFile(path)
        file.Upload()

    # To only be used to download config .txt files.
    def downloadConfig(self, id):
        configFile = self.drive.CreateFile({'id' : id})
        content = configFile.GetContentString().splitlines()
        # print(recipients)
        return content

# Test script for uploading log file.
# gdSession = GoogleServices('testSession') # note, datetime will automatically be appended to the folder name.
# i = 0
# while True:
#     print(i)
#     gdSession.updateLog(f'{i}')
#     i += 1
#     time.sleep(1)
#     if (i % 30) == 0:
#         gdSession.uploadLog()
# gdSession.logThread.join()

# Testing for uploading different file types.
# print(gdSession.drive.GetAbout()) # Use to see the current drive usage for the service account. Ensure that the quota is not changing.
# # gdSession.upload("testFiles/test_img.png") # files with the same name do not overwrite each other or update the original file.
# gdSession.upload("testFiles/test_img.png")
# gdSession.upload("testFiles/Honey bee foraging on Ceanothus.mp4")
# gdSession.upload("testFiles/test_csv.csv")

# gdSession.listFiles()

# credentials = gdSession.gauth.credentials
# http_timeout = 10
# http = httplib2.Http(timeout=http_timeout)
# http = credentials.authorize(http)
# service = build("drive", "v2", http=http, cache_discovery=False)
# metadata = (
#     service.drives()
#     .list()
#     .execute(http=http)
# )
# print(f'metadata={metadata}')
# #  metadata={'nextPageToken': '<very-long-token>', 'kind': 'drive#driveList', 'items': [{'id': '1234ASDFG...', 'name': '1st Drive', 'kind': 'drive#drive'}, ...]}
# for i,item in enumerate(metadata["items"]):
#   print(f'  {i}: id={item["id"]} name="{item["name"]}"')