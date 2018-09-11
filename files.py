import os,subprocess
import drive

class Files:
    def __init__(self):
        self.path = '/home/eduado/Documents/Projetos/'
        self.language = 'Python'

    def showProjectsLanguage(self):
        return os.listdir(self.path)

    def compactProject(self, _name):
        os.chdir(self.path + self.language)
        os.system('zip {} -r {}/'.format(_name,_name))

    def changeProjectLanguage(self, _language = None):
        self.language = _language
        if _language:
            os.chdir(self.path + self.language)
        else:
            return None

    def showProjects(self):
        return os.listdir(self.path + self.language)

    def getMimeType(self, _fileName):
        result = subprocess.check_output("file --mime-type " + _fileName, shell=True)
        return result.decode('utf-8')