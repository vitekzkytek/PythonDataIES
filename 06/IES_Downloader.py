import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from IES_Pages import *
from sqlalchemy import *


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
    
    def saveDFs(self):
        dfs = {}
        dfs['theses'] = pd.DataFrame([x.characteristics for x in self.theses])
        dfs['courses'] = pd.DataFrame([x.characteristics for x in self.courses])
        dfs['people'] =  pd.DataFrame([x.characteristics for x in self.people])    
        self.dfs = dfs
        
    def initDB(self,connstring):        
        engine = create_engine(connstring)
        conn = engine.connect()
        metadata = MetaData(engine)
        return engine,conn,metadata

    def saveToDB(self,connstring='postgresql://student_ies:PythonData@localhost:5432/student_ies'):
        def simplifyColnames(df):
            df.columns = [simplifyColname(col) for col in df.columns]
            return df

        def simplifyColname(s):
            return s.replace(':','').replace(' ','_').lower()
        
        def generateSchema(df,metadata,tblName,conn):
            # for all column names that are not id and name
            cols = [col for col in df.columns if col not in ('id', 'name')]

            # create a Column object (string value)
            def giveType(colname):
                l = ['bachelor_all','bachelor_awarded','master_all','master_awarded','Credit']
                if colname in l:
                    return Float()
                else:
                    return String()
            colobjs = [Column(col,giveType(col)) for col in cols]

            # then create a Table
            tbl = Table(tblName,metadata,
                       Column('id',String(),primary_key=True),
                       Column('name',String()),
                       *colobjs
                       )
            metadata.create_all()
            d = df.to_dict(orient='records')

            conn.execute(tbl.insert(),d)
            return tbl

        def generateConnections(df,N_col,col1,col2,):
            l = []
            for i,row in df.iterrows():
                for sup in row[N_col]:
                    l.append({col1:sup,col2:row['id']})
            return l

        def generateConnectionTable(tbl1,tbl2,data,conn,metadata):
            tbl = Table('{}_{}'.format(tbl1,tbl2),metadata,
                Column(tbl1 + '-id',String(),ForeignKey(tbl1 +'.id')),
                Column(tbl2 + '-id',String(),ForeignKey(tbl2 +'.id'))
               )
            metadata.create_all()
            conn.execute(tbl.insert(),data)

        def insertNonExistingIDs(nonids,tbl,metadata,conn):
            df = pd.DataFrame(columns=[c.name for c in tbl.columns])
            df['id'] = nonids
            d = df.to_dict(orient='records')
            conn.execute(tbl.insert(),d)

        def processNonExistingIDs(ids,newids,tbl,metadata,conn,meanwhileadded = []):
            Tracer()()
            def DoIDsExist(cell,ids,nonids):
                for xid in cell:
                    if xid not in ids:
                        if xid not in nonids:
                            if xid not in meanwhileadded:
                                nonids += [xid]
            nonids = []

            newids.apply(lambda cell:DoIDsExist(cell,ids,nonids) ) # fills  previous list of nonids

            insertNonExistingIDs(nonids,tbl,metadata,conn)
            return meanwhileadded + nonids # return newly added items

        #deepCopies
        dfCourses = simplifyColnames(self.dfs['courses']).drop('supervisors',axis=1)
        dfTheses = simplifyColnames(self.dfs['theses']).drop('supervisor-id',axis=1).rename({'thesis-id':'id'},axis=1)
        dfPeople = simplifyColnames(self.dfs['people']).drop_duplicates('id')

        # Initialize a DB
        engine,conn,metadata = self.initDB(connstring)
        
        # drop previous versions
        metadata.reflect(engine)
        metadata.clear()
        for tbl in reversed(metadata.sorted_tables):
            engine.execute(tbl.delete())

        #conn.commit()
        # add raw tables
        ppl = generateSchema(dfPeople,metadata,'people',conn)
        crs = generateSchema(dfCourses,metadata,'courses',conn)
        ths = generateSchema(dfTheses,metadata,'theses',conn)

        #check if all related people exist and add those that do not
        tblppl = Table('people', metadata, autoload=True, autoload_with=engine)
        newids = processNonExistingIDs(self.dfs['people'].id.unique(),self.dfs['courses'].supervisors.dropna(),tblppl,metadata,conn)
        processNonExistingIDs(self.dfs['people'].id.unique(),self.dfs['theses']['supervisor-id'],tblppl,metadata,conn,meanwhileadded=newids)

        #add connecting tables  # will not work because there are people not listed

        pplcrs = generateConnections(self.dfs['courses'][['id','supervisors']].dropna(),'supervisors','people-id','courses-id')
        generateConnectionTable('people','courses',pplcrs,conn,metadata)

        pplths = generateConnections(self.dfs['theses'][['supervisor-id','id']],'supervisor-id','people-id','theses-id')
        generateConnectionTable('people','theses',pplths,conn,metadata)

        conn.close()
