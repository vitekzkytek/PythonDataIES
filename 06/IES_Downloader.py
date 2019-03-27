import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from IES_Pages import *


class IES_Downloader:
    '''
    Download manager class for IES web
    
    It contains methods for collection of links, downloading itself and storing results
    '''
    def __init__(self,allowLog=True):
        '''
        creates IES_Downloader object with self.links, that store links to be downloaded
        and self.people, self.courses and self.theses to store individual IES_Web-like objects
        '''
        self.allowLog = allowLog
        self.links = {
            'people':{},
            'courses':[],
            'theses':{}
        }
        self.people = []
        self.courses = []
        self.theses = []
        
        if self.allowLog:
            print('Succesfully initialized IES Downloader')
    
    def getPeopleLinksForCategory(self,link,category):
        '''
        Downloads all person links in the specified webpage and saves it to self.links
        '''
        if self.allowLog:
            print('Searching for Person-links of {} on {} ...'.format(category,link))
        r = requests.get(link)
        r.encoding = 'UTF-8'
        soup = BeautifulSoup(r.text,'lxml')

        self.links['people'][category] = self.getLinksByCondition(soup,'td[class=peopleTableCellName] > a')

        if self.allowLog:
            print('Found {} Person-links for {}'.format(len(self.links['people'][category]),category))
            
    def getThesesLinksForCategory(self,link,category):
        '''
        Downloads all theses-links in the specified webpage between 1994 and 2020 and saves it to self.links
        link -- a webpage to parse from
        category -- indicates a type of thesis
        
        does not return anything, but fills in self.links['theses'][category] instead
        '''
        if self.allowLog:
            print('Searching for theses-links of {} on {} ...'.format(category,link))

        l = []
        for year in range(1994,2020):
            tblLink = link + 'year/' + str(year)
            
            r = requests.get(tblLink)
            soup = BeautifulSoup(r.text,'lxml')
            l = l + self.getLinksByCondition(soup,'a[href*=/work/]')
            
        self.links['theses'][category] = l
        if self.allowLog:
            print('Found {} Theses-links for {}'.format(len(self.links['theses'][category]),category))

    def downloadPeople(self,pause=0.1):
        '''
        Download all links stored in self.link['people'] and store it in self.people
        pause -- how long to pause between requests? (in seconds)
        tqdm -- the progress bar showing a progress of iterator
        '''
        if self.allowLog:
            count = sum([len(self.links['people'][key])for key in self.links['people']])
            print('Downloading all {} persons ...'.format(count))

        for key in self.links['people']:
            for link in tqdm(self.links['people'][key],desc=key):
                person = IES_Person(link,key)
                self.people.append(person)
                time.sleep(pause)
        if self.allowLog:
            print('Succesfully downloaded {} persons'.format(len(self.people)))

    def downloadTheses(self,pause=0.1):
        '''
        Download all links stored in self.link['theses'] and store it in self.theses
        pause -- how long to pause between requests? (in seconds)
        tqdm -- the progress bar showing a progress of iterator

        '''
        if self.allowLog:
            count = sum([len(self.links['theses'][key])for key in self.links['theses']])
            print('Downloading all {} theses ...'.format(count))

        for key in self.links['theses']:
            for link in tqdm(self.links['theses'][key],desc=key):
                thesis = IES_Thesis(link,key)
                self.theses.append(thesis)
                time.sleep(pause)
        if self.allowLog:
            print('Succesfully downloaded {} theses'.format(len(self.theses)))

    def downloadCourses(self,pause=0.1):
        '''
        Download all links stored in self.link['courses'] and store it in self.courses
        pause -- how long to pause between requests? (in seconds)
        tqdm -- the progress bar showing a progress of iterator
        '''
        if self.allowLog:
            count = len(self.links['courses'])
            print('Downloading all {} courses ...'.format(count))

        for link in tqdm(self.links['courses'],desc='Courses'):
            course = IES_Course(link)
            self.courses.append(course)
            time.sleep(pause)
                    
        if self.allowLog:
            print('Succesfully downloaded {} courses'.format(len(self.courses)))

    
    def getCoursesLinksFromPersons(self):
        '''
        In all persons stored in self.people, find all links containing substring 'syllab'
        Exclude duplicates and store in self.links['courses']
        '''
        if self.allowLog:
            print('Looking for course links in already downloaded persons  ...')
        total_links = [person.soup.select('a[href*=syllab]') for person in self.people]
        for person_links in total_links:
            for link in person_links:
                ident = 'http://ies.fsv.cuni.cz/en/syllab/' + link['href'].split('/')[-1]
                if ident not in self.links['courses']:
                    self.links['courses'].append(ident)
        if self.allowLog:
            print('Among {} persons found {} unique courses'.format(len(self.people),len(self.links['courses'])))
        
    def getLinksByCondition(self,soup,cond):
        '''
        find all links satisfying condition cond in soup object
        '''
        links = soup.select(cond)
        return ['http://ies.fsv.cuni.cz'  + l['href'] for l in links]