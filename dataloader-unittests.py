# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 10:25:52 2016

@author: OffermanTW1
"""

#Data Loader test cases 

import DataLoader3 as DL
import unittest
import os
import sys

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
#
#if sys.executable != 'J:\Applications\BB-Python\Python\python.exe':
#    raise Exception ('Python is run from the wrong location')

def locator(filename):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "Python/Testcases/" + filename
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path


class DataListLoaderTestCases(unittest.TestCase):
    
    """
    Create a test for empty headers. Thiw will, however, require the overhaul of quite a few tests.
    """
    dataloader = DL.DataListLoader()
    def test_datalistloader1(self):
        #Test 1: Check whether data is loaded properly
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
        
        self.assertEqual(result[0:2], [['Header1', 'Header2', 'Header3'],
                                  ['Regel1', 'Regel2', 'Regel3']])
                                       
    def test_datalistloader2(self):
        #Test 2: Check whether capitalized extension is still recognized. 
        result = self.dataloader.find_extension_and_load(locator('datalistloader2.TXT'))
        
        self.assertEqual(result, [['Header1', 'Header2', 'Header3'],
                                  ['Regel1', 'Regel2', 'Regel3']])        
                                  
    def test_datalistloader3(self):
        #Test 3: Empty dataset 
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
        
        self.assertEqual(result[3:8], [['','','',''],['','','',''],
                                  ['','','',''],['','','',''],['','','','']])   
                                 
    def test_datalistloader4(self):
        #Test 4: Check whether special characters are properly handled
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
        
        self.assertEqual(result[8], ['\'"%Regel7', "'Regel8#'", '&"Regel9"\''])   
                                   
    def test_datalistloader5(self):
        #Test 5: check whether empty rows and columns influence the data in between
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
        
        self.assertEqual(result[7:10], [['', '', '', ''], ['\'"%Regel7', "'Regel8#'", '&"Regel9"\''], ['', '', '', '']])           
                                                          
                                  
    def test_datalistloader6(self):
        #Test 6: Check whether data is loaded properly
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.xlsx'))
        
        self.assertEqual(result[0:3], [['Header1', 'Header2', 'Header3'], ['Regel1', 'Regel2', 'Regel3'], 
                                      ['"3454235', '&85674#', "'sadaf'"]])
                                       
    def test_datalistloader7(self):
        #Test 7: Check whether capitalized extension is still recognized. 
        result = self.dataloader.find_extension_and_load(locator('datalistloader2.XLSX'))
        
        self.assertEqual(result, [['Header1', 'Header2', 'Header3'],
                                  ['Regel1', 'Regel2', 'Regel3']])        
                                                                                                           
    def test_datalistloader8(self):
        #Test 8: Check how empty cells are handled 
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.xlsx'))
        
        self.assertEqual(result[3:8], [[None, None, None],[None, None, None],[None, None, None],
                                       [None, None, None],[None, None, None]])                                          
                                                                            
    def test_datalistloader9(self):
        #Test 9: Check empty file
        result = self.dataloader.find_extension_and_load(locator('datalistloader3.xlsx'))
        
        self.assertEqual(result, [[]])                              
                                  
#    def test_datalistloader10(self):
#        """
#        Seems to be an issue with my python formula, not the script
#        """
#        #Test 10: Check whether csv is not supported
#        self.assertRaises(NameError('CSV not yet supported'), self.dataloader.find_extension_and_load(locator('datalistloader1.csv')))       

#    def test_datalistloader11(self):
#        """
#        Seems to be an issue with my python formula, not the script
#        """
#        #Test 11: Check whether cvs is not supported
#        self.assertRaises(NameError('Extension of file is not recognized'), self.dataloader.find_extension_and_load(locator('datalistloader1.cvs')))    
#        
    def test_datalistloader12(self):
        #Test 12: Check loading with an empty first cell
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
        
        self.assertEqual(result[10], ['','Regel10','', ''])        
                      
    def test_datalistloader13(self):
        #Test 13: Check loading with only a filled first cell
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
        
        self.assertEqual(result[11], ['Regel11', '', '' , ''])                              
        
#    def test_datalistloader14(self):
#        """
#        Required? It would only matter when manually creating columns in a .txt. Still, it might be used at some point. 
#        Currently no support for changing column width as 1 invalid column screws up the entire datalist
#        """
#        #Test 14: Check how changing column widths are handled
#        result = self.dataloader.find_extension_and_load(locator('datalistloader1.txt'))
#        
#        self.assertEqual(result[13:15], [])       

    def test_datalistloader15(self):
        #Test 15: Checks special chartacters splt by an empty cell
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.xlsx'))
        
        self.assertEqual(result[12], ['""Regel5', None, '&"Regel6\''])  
                                       
#    def test_datalistloader16(self):
#        """
#        Right now returns the formula. Look for a way to return only the value
#        """
#        #Test 16: Check whether formulas return values rather than formulas
#        result = self.dataloader.find_extension_and_load(locator('datalistloader1.xlsx'))
#        
#        self.assertEqual(result[8], [18, None, None])       
                                       
    def test_datalistloader17(self):
        #Test 16: Check whether quoted formulas retain their value as such
        result = self.dataloader.find_extension_and_load(locator('datalistloader1.xlsx'))
        
        self.assertEqual(result[9], [None, '=17^6', "Regel4#'"])                                            
                                       
                                       
#    def test_datalistloader18(self):
#        """
#        Currency from Dutch to National usage is working as intended. However when importing a number using national notation
#        the number is handled as a string rather than an integer. input check when a comma is found to see whether the length is
#        3 or more. If so, remove comma and pass on the edited number
#        """
#        #Test 18: Check how formulas are handled
#        result = self.dataloader.find_extension_and_load(locator('datalistloader1.xlsx'))
#        
#        self.assertEqual(result[9], [147512.25, 147512.25, 147512.25])           
        
        
        
          
    
class DataCutterTestCases(unittest.TestCase):
    datacutter = DL.DataCutter(protect_cols = None, protect_rows = None, col_limit = 0.05, row_limit = 0.50)
    
    def test_datacutter1(self):
        dataset = [['Header1', 'Header2'], 
                   ['',''],
                   ['Data1', 'Data2']]
        
        cut_data = self.datacutter.cut_redundant_data(dataset)
        self.assertEqual(cut_data,[['Header1', 'Header2'], ['Data1', 'Data2']] )
        
    def test_datacutter2(self): 
        dataset = [['Header1', '', 'Header2'], 
                   ['', '',''],
                   ['Data1', '', 'Data2'], 
                   ['', '','']]
        
        cut_data = self.datacutter.cut_redundant_data(dataset)
        
        self.assertEqual(cut_data,[['Header1', 'Header2'], ['Data1', 'Data2']] )
        
class DataFrameTestCase(unittest.TestCase):
    """
    Expected defaults:
    data_location = None, cut_redundant_data = True, dtype_detection = True, protect_rows = None, 
    protect_cols = None, col_is_index = None, assign_dtype = None
    """

    """
    Device a test to check whether a loaded string gets referencded properly. see Dataloader3.py line 266
    """    
    
    dataframeloader = DL.DataFrameLoader()
    
    
    def test_dataframeloader1(self):
        #Test 1: Checks whether pandaframes handles basic data import correctly
        result = self.dataframeloader.load_data(data_location = locator('dataframeloader1.xlsx'))
      
        t = [['Regel1', 'Regel2', 'Regel3'], ['"3454235', '&85674#', "'sadaf'"]]
        df = DataFrame(t, columns = ['Header1', 'Header2', 'Header3'])    
        df.index.rename('ID', inplace = True)
        assert_frame_equal(result, df)
        
#    def test_dataframeloader2(self):
#        """
#        works as of 05-04, check regularely to ensure proper it keeps working
#        """
#        #Test 2: Checks whether file selection imports data properly
#        result = self.dataframeloader.load_data(data_location = None) #Select dataframeloader1.xlsx
#        
#        t = [['Regel1', 'Regel2', 'Regel3'], ['"3454235', '&85674#', "'sadaf'"]]
#        df = DataFrame(t, columns = ['Header1', 'Header2', 'Header3'])    
#        df.index.rename('ID', inplace = True)
#        assert_frame_equal(result, df)

    def test_dataframeloader3(self):
        #Test 3: Checks whether slicing works correctly when cutting redundant data has been set to false
        result = self.dataframeloader.load_data(data_location = locator('datalistloader1.xlsx'), cut_redundant_data = False)
        
        t = '""Regel5'
        result = result['Header1'].loc[11]

        self.assertEqual(result, t)
        
        
    def test_dataframeloader4(self):
        #Test 4: Checks whether cutting redundant data influences the data beyond removing rows
        result = self.dataframeloader.load_data(data_location = locator('datalistloader1.xlsx'))
        
        t = '""Regel5'
        result = result['Header1'].loc[5]

        self.assertEqual(result, t)        


#    def test_dataframloader5(self):
#        #Test 5: Check whether the dataframe returns values rather than formulas
#        result = self.dataframeloader.load_data(data_location = locator('datalistloader1.xlsx'))        
#        result = result['Header1'].loc[2]
#        t = 18
#
#        self.assertEqual(result, t)  
        
        
    def test_dataframeloader6(self):
        #Test 6: Check whether the dataframe structure retains quoted formulas
        result = self.dataframeloader.load_data(data_location = locator('datalistloader1.xlsx'))
        
        t = '=17^6'
        result = result['Header2'].loc[3]

        self.assertEqual(result, t)  


    def test_dataframeloader7(self):
        #Test 7: Checks whether slicing retains it's values
        result = self.dataframeloader.load_data(data_location = locator('dataframeloader1.xlsx'))
        
        t = [['Regel1', 'Regel2', 'Regel3'], ['"3454235', '&85674#', "'sadaf'"]]
        df = DataFrame(t, columns = ['Header1', 'Header2', 'Header3'])    
        df.index.rename('ID', inplace = True)
        
        assert_frame_equal(result.iloc[[1]], df.iloc[[1]])
        

    def test_dataframeloader8(self):
        #Test 8: Check whether the col_is_index function works properly
        result = self.dataframeloader.load_data(data_location = locator('datalistloader1.xlsx'), col_is_index = 'Header1')
        result = result['Header2'].loc['Regel1']
        
        self.assertEqual(result, 'Regel2')  
        
    def test_dataframeloader9(self):
        #Test 5: Check whether changing the index changes the usage of slicing 
        result = self.dataframeloader.load_data(data_location = locator('datalistloader1.xlsx'), col_is_index = 'Header1')
        Header1 = ['Regel1', '"3454235' ]        
        t = [['Regel2', 'Regel3'], ['&85674#', "'sadaf'"]]
        df = DataFrame(t, columns = ['Header2', 'Header3'], index = Header1)    
        df.index.rename('Header1', inplace = True)
            
        assert_frame_equal(result.iloc[[1]], df.iloc[[1]])          
      


#testchange



    
    
if __name__ == '__main__':
    test_classes_to_run = [DataListLoaderTestCases, DataCutterTestCases, DataFrameTestCase]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)


#        t = [['Regel1', 'Regel2', 'Regel3'],['"3454235', '&85674#', 'sadaf']]
#        df = DataFrame(t, columns = ['Header1', 'Header2', 'Header3'])
#        print(df)
#        print(result)





















































































































































































































































































































































































































































































































































































print ('woo')





















































































































































































































































































































































































































































































































































































































