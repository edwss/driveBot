from googleapiclient.discovery import build,MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import os

class Drive:
    def __init__(self):
        try:
            SCOPES = 'https://www.googleapis.com/auth/drive.file'
            os.chdir("/home/eduado/Documents/Projetos/Python/DriveBot/tmp/")
            store = file.Storage('../token/token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('../credentials/credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            self.service = build('drive', 'v3', http=creds.authorize(Http()))
        except:
            self.__init__()

    def uploadFile(self, _filename, _mimeType):
        try:
            file_metadata = {'name': _filename, 'parents': ["17NNaQFAd3YvUDGD0eWfSxWUyAw0dmi0c"]}
            media =  MediaFileUpload(_filename,mimetype=_mimeType)
            fileUpload = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(fileUpload)
            if fileUpload:
                print('File ID: %s' % fileUpload.get('id'))
                os.remove(_filename)
                return 1
            else:
                self.__init__()
                self.uploadFile(_filename, _mimeType)
        except:
            self.__init__()
            self.uploadFile(_filename,_mimeType)

    def searchForFolders(self):
        try:
            parents = self.service.files().list(corpus='user',includeTeamDriveItems=False,q="mimeType='application/vnd.google-apps.folder'").execute()
            print(parents)
        except Exception as e:
            print('An error occurred: %s' % e)

    def createafolder(self):
        folder_metadata = {'name': 'Invoices', 'mimeType': 'application/vnd.google-apps.folder'}
        file = self.service.files().create(body=folder_metadata,fields='id').execute()