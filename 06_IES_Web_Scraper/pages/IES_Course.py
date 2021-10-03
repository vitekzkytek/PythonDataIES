import pandas as pd
from .IES_Page import IES_Page

class IES_Course(IES_Page):
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