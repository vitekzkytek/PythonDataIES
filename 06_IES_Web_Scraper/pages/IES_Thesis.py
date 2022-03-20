import pandas as pd
from .IES_Page import IES_Page

class IES_Thesis(IES_Page):
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
