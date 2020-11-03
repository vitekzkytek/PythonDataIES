import requests
from bs4 import BeautifulSoup
import pandas as pd

class IES_Page:
    '''
    Class containing methods for parsing IES websites from self.soup attribute.
    It is designed as a parent class for specific pages
    '''
    
    def __init__(self,link):
        '''
        Constructor only converts link into a BeatifulSoup object
        '''

        self.link = link
        r = requests.get(link)
        r.encoding='UTF-8'
        if r.status_code == 200:
            self.soup = BeautifulSoup(r.text,'lxml')
        else: 
            print('Requesting website {} failed'.format(link))
    
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
        breakpoint()
        return pd.Series({key:self._siblingOfStrong(key) for key in strongTexts})
    
    def _siblingOfStrong(self,strongText):
        '''
        for the following structure:
        <strong>strongText</strong> valueText 
        
        takes strongText as an input and returns ValueText (stripped) or None, if StrongText or valueText does not exist
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
        
        returns (number1,number2) or (None,None)
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
