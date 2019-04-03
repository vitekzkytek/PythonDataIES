import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from IPython.core.debugger import Tracer

class IES_Web:
    '''
    Class containing methods for parsing IES websites from self.soup attribute.
    It is designed as a parent class for specific pages
    '''
    
    def __init__(self,link):
        self.link = link
        r = requests.get(link)
        r.encoding='UTF-8'
        self.soup = BeautifulSoup(r.text,'lxml')
    
    def parseH2(self):
        '''
        Returns a text of first <h2></h2> element in self.soup. 
        '''
        return self.soup.find('h2').text.strip()
    
    def parseH3(self):
        '''
        Returns a text of first <h3></h3> element in self.soup. 
        '''
        return self.soup.find('h3').text.strip()
    
    def pdSiblingsOfStrong(self,strongTexts):
        '''
        For a list of strings expected inside <strong> element 
        returns pandas Series with corresponding sibling elements.
        
        <strong>strongText</strong> valueText
        
        See _siblingOfStrong() for detailed implementation
        
        Input: list of expected strongTexts
        Output: pd.Series with strongTexts as index and valueTexts as series values.
        '''
        return pd.Series({key:self._siblingOfStrong(key) for key in strongTexts})
    
    def _siblingOfStrong(self,strongText):
        '''
        for the following structure:
        <strong>strongText</strong> valueText 
        
        takes strongText as an input and returns ValueText (stripped) or None, if StrongText does not exist
        '''
        el = self.soup.find('strong',text=strongText)
        if el:
            valueText = el.next_sibling
            if valueText:
                return valueText.strip()

        
    def pdSiblingsOfStrongParents(self,strongs):
        '''
        For a list of strings expected inside <strong> element 
        returns pandas Series with corresponding sibling elements.
        Structure:
        
        <element>
            <strong>strongText</strong>
        </element>
        <element>
            valueText
        </element>
        
        Input: list of strongTexts expected
        Output: pd.Series with strongTexts as index and valueTexts as series values.
        '''

        return pd.Series({key:self._siblingOfStrongParents(key) for key in strongs})

    
    def _siblingOfStrongParents(self,strongText):
        '''
        for the following structure:
        <element>
            <strong>strongText</strong>
        </element>
        <element>
            valueText
        </element>
        
        takes strongText as an input and returns ValueText (stripped) or None, if StrongText does not exist
        '''
        el = self.soup.find('strong',text=strongText)
        if el:
            valueText = el.parent.next_sibling.text
            if valueText:
                return valueText.strip()
        
    def numbersNextToStrongBelowH3(self,headerText):
        '''
        for the following structure:
        <h3>headerText</h3>
        <element>
            <strong>strongText</strong>
            number1/number2
        </element>
        takes headerText as argument and returns (number1/number2) as a tuple if it exists.
        
        headerText -- string expected inside <h3> element
        
        returns (number1/number2) or (None,None)
        '''
        el = self.soup.find('h3',text=headerText)
        if el:
            counts = el.next_sibling.next_sibling.find('strong').next_sibling.strip()
            number1 = int(counts.split('/')[0])
            number2 = int(counts.split('/')[1])
            return (number1,number2)
        else:
            return (None,None)
        
    def parseThsAndTdsFromEl(self,selector):
        '''
        Finds all <th> and <tds> in the element defined by selector and return it as Series
        with <th> as an index and <td> as values.
        
        <element>
            <th>Key1</th><td>Value1</td>
            <th>Key2</th><td>Value2</td>
            ...
        </element>
        
        selector -- unique identifer of element
        
        returns pd.Series, where index is Key1,Key2 ... and values are Value1,Value2 ....
        '''
        el = self.soup.select_one(selector)
        
        ths = [th.text for th in el.findAll('th')]
        tds = [td.text for td in el.findAll('td')]
        
        return pd.Series(tds,index=ths)
    def getLinksWithStringFromEl(self,selector,linkText):
        '''
        Inside the element specified by a selector finds all links containing linkText
        
        selector -- string that can be used in BeautifulSoup select_one function. 
        Beware that only first element is taken into account
        
        linkText -- string that specified links should containt
        '''
        el = self.soup.select_one(selector)
        links = el.select('a[href*={}]'.format(linkText))
        
        return [l['href'] for l in links]
    
    def getTdForCorrespondingTh(self,selector,thText):
        """
        From the table inside selector-defined element returns 
        content of <td> by the value of corresponding <th>.
        
        See the element structure:
        
        <element>
            <th>Key1</th><td>Value1</td>
            <th>Key2</th><td>Value2</td>
            ...
        </element>
        
        selector - unique selector of <element>
        thText -- string in the <th> - Key1 or Key2 from the example.
        
        returns a correpsonding content -  Value1 or Value2 from the example.
        """
        el = self.soup.select_one(selector)

        ths = [th.text for th in el.findAll('th')]
        tds = [td for td in el.findAll('td')]
        if thText in ths:
            return tds[ths.index(thText)]

class IES_Person(IES_Web):
    '''
    Class representing a personal website of IES researchers, Ph.D students etc.
    
    Inherits from the IES_Web class, so that it access its XML parsing methods
    '''
    def __init__(self,link,category):
        '''
        Constructor for IES_Person calls parents IES_Web constructor first,
        where self.link, self.request and self.soup are created
        
        Then unique id, name and characteristics are generated as IES_Person attributes
        '''
        
        # calling a parents IES_Web constructor
        super().__init__(link)
        
        # read Persons ID from link
        self.id = self.linkToID()
        
        # Is he internal, external, administrative or Ph.D. candidate?
        self.category = category
        
        # read persons name from <h2>
        self.name = self.parseH2()
        
        # get the rest of informations
        self.characteristics = self.parseCharacteristics()
    
    def linkToID(self):
        '''
        Person IDs are derived from the last part of the his personal website
        '''
        llink = self.link.split('/')
        return llink[len(llink)-1]
    
    def parseCharacteristics(self):
        '''
        returns pandas series with IES_Person characteristics
        
        See documentation of individual methods methods for details
        and example page: http://ies.fsv.cuni.cz/cs/staff/barunik
        '''
        
        # Generate first pandas series - see ?self.pdSiblingsOfStrong
        nextSiblings = ['Position:','Field of interest:','Membership:','Office:','Email:','Phone:','Available:']       
        ser_nextSiblings = self.pdSiblingsOfStrong(nextSiblings)
        
        # Generate second pandas series - see ?self.pdSiblingsOfStrongParents
        parentsNextSiblings = ['Organisation Memberships','Education','Job history','Extra activities','Bachelor theses','Master theses']
        ser_parentsNextSiblings = self.pdSiblingsOfStrongParents(parentsNextSiblings)
        
        # merge first and second together
        chars = pd.concat([ser_nextSiblings,ser_parentsNextSiblings])
        
        # add object details
        chars.loc['researcher'] = self.name
        chars.loc['id'] = self.id
        chars.loc['category'] = self.category
        
        # parse bachelor and master thesis counts (both all and marked)
        d = {'bachelor':'Supervised Bachelor theses','master':'Supervised Master Theses'}
        for key in d:
            total, awarded = self.numbersNextToStrongBelowH3(d[key])
            chars.loc[key + '_all'] = total
            chars.loc[key + '_awarded'] = awarded
        return chars
    
class IES_Thesis(IES_Web):
    def __init__(self,link,category):
        '''
        Constructor for IES_Thesis calls parents IES_Web constructor first,
        where self.link, self.request and self.soup are created
        
        Then unique id, name and characteristics are generated as IES_Person attributes
        '''
        
        # calling a parents IES_Web constructor
        super().__init__(link)
        
        # store thesis-specific information
        self.category = category
        self.id = self.getThesisID(link)
        self.name = self.parseH3()
        
        # parse more complicated characteristics
        self.characteristics = self.parseCharacteristics()
    
    def getThesisID(self, link):
        '''
        ThesisID is stored inside the link right after the '/id/' substring
        '''
        llink = link.split('/')
        ind = llink.index('id')
        return int(llink[ind+1])
    
    def parseCharacteristics(self):
        '''
        returns pandas series with IES_Thesis characteristics
        
        See documentation of individual methods methods for details
        and example page: http://ies.fsv.cuni.cz/work/index/show/id/1112/lang/cs
        '''
        # parse all attributes from table inside the <section class="content"> element
        ser = self.parseThsAndTdsFromEl('section[class=content]')
        
        # get all links inside  <section class="content"> element containg substring 'staff',
        # e.g.: http://ies.fsv.cuni.cz/cs/staff/barunik
        supervisorlinks = self.getLinksWithStringFromEl('section[class=content]','staff')
        
        # get supervisor ids as a last part of a link
        supervisorlinks = [l.split('/')[-1] for l in supervisorlinks]
        ser.loc['supervisor-id'] = supervisorlinks
        
        # add object attributes 
        ser.loc['id'] = self.id
        ser.loc['name'] = self.name
        
        return ser
    
class IES_Course(IES_Web):
    '''
    Class representing an IES course webpage
    '''
    def __init__(self,link):
        
        # calling a parents IES_Web constructor
        super().__init__(link)
        
        # parsing object specific features
        self.name = self.parseH2()
        self.id = link.split('/')[-1]
        
        # parsing more specific characteristics
        self.characteristics = self.parseCharacteristics()
    
    def parseCharacteristics(self):
        '''
        returns pandas series with IES_Course characteristics
        
        See documentation of individual methods methods for details
        and example page: http://ies.fsv.cuni.cz/en/syllab/JEM207
        '''

        # parse table inside <section class='content'> element
        ser = self.parseThsAndTdsFromEl('section[class=content]')
        
        # add object attributes
        ser.loc['name'] = self.name
        ser.loc['id'] = self.id
        
        # find supervisors ids:
        supervisors = self.getTdForCorrespondingTh('section[class=content]','Course supervisors:')
        if supervisors:
            supervisors = [a['href'].split('/')[-1] for a in supervisors.findAll('a')]
        
        ser.loc['supervisors'] = supervisors
        return ser