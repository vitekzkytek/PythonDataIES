import pandas as pd
from .IES_Page import IES_Page


class IES_Person(IES_Page):
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
