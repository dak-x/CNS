import json
from random import randint
import toml
# Generates 
class CreateDB:
    def __init__(self, personal_domain, institute_domain, Sections, names):
        self.personal_domain = personal_domain
        self.institute_domain = institute_domain
        self.names = names
        self.Sections = Sections
        self.DB = dict()

    def genPhno(self):
        phNo = ''
        for i in range(10):
            phNo += str(randint(1, 9))
        return phNo

    def genEmails(self, name):
        emailP = ''
        for j in name:
            if (j != ' '):
                emailP += j.lower()
        emailIn = emailP + self.institute_domain
        emailP += self.personal_domain
        return emailP, emailIn

    def genSection(self):
        idx = randint(0, len(self.Sections) - 1)
        section = self.Sections[idx]
        return section

    def CreateRecord(self, name):
        d = dict()
        d['Phone No.'] = self.genPhno()
        d['Email Personal'], d['Email Institute'] = self.genEmails(name)
        d['Section'] = self.genSection()
        return d

    def Generate(self):
        for name in self.names:
            self.DB[name.lower()] = self.CreateRecord(name)

    def SaveDB(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.DB, fp)

conf = toml.load("setup.toml")
database_config = conf.get("database")
personal_domain = '@gmail.com'
institue_domain = '@itu.edu.in'
Sections = ['Academic', 'Administration', 'Director Office', 'Hostel']
names = ['Rob Marlo', 'Chenzi Dobi', 'Bran Lopez',
         'Courntey Cooper', 'Martha Stewart', 'Anglo Mathews',
         'Mathew Hayden','Levy Bonstad','Ashton Agar','Michael Meyers']

C_X = CreateDB(personal_domain, institue_domain, Sections, names)
C_X.Generate()
C_X.SaveDB(database_config.get("path"))
