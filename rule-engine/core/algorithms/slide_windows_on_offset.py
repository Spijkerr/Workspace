# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 11:22:35 2016

@author: Thomas
"""

from numpy import searchsorted
from numpy import append 
def slide_windows(*series, offset, mode):

    """
    You have the discrete chunks and the continuous chunks.
    Let's say you have a list [100, 100, 101, 108, 109, 109].
    The discrete chunks are:
    [0,1], [2], [3], [4, 5]
    
    If you want to get everything within a 5% range, the continuous ranges are:
    Base    Comp
    [0,1] - [0,1,2]
    [2]   - [2]
    [3]   - [3, 4,5]
    [4,5] - [4,5]
    
    Every element in base needs to be compared to every element in comp. 
    That's why all the elements in base are also present in comp.
    """
    
    #What happens when series is size 0 TO DO
    if len(series) == 2:
        #If the input is base/comp you will split the comp into groups that are
        #candidates for the discrete chunks in base. So first discrete chunk base.
        base, comp = series
        sorted_base = base.sort_values()
        sorted_comp = comp.sort_values()
        
        discrete_chunks = get_discrete_chunks(sorted_base)
        cont_chunks = get_cont_chunks(sorted_comp, sorted_base, offset, mode)

    else:
        sorted_series = series[0].sort_values()
        
        discrete_chunks = get_discrete_chunks(sorted_series)
        cont_chunks = get_cont_chunks(sorted_series, sorted_series, offset, mode)
    return list(zip(discrete_chunks, cont_chunks))

def get_discrete_chunks(sorted_series):
    #First we create the discrete chunks
    sorted_index = sorted_series.index
    sorted_values = sorted_series.values
    
    chunk_starts, chunk_ends = get_chunk_indices(sorted_values)

    discrete_chunks = [sorted_index[s:e] for s,e in zip(chunk_starts, chunk_ends)] 
    print(discrete_chunks)
    return discrete_chunks

def get_cont_chunks(series, search_series, offset, mode):
    sorted_index = series.index
    sorted_values = series.values
    
    search_starts, search_ends = get_chunk_indices(search_series)
    search_values = search_series[search_starts]
    offsetted_search_values = create_offset(search_values, offset, mode)

    
    chunk_starts = searchsorted(sorted_values, search_series)
    chunk_starts = chunk_starts[search_starts]
    
    chunk_ends = searchsorted(sorted_values, offsetted_search_values, side = 'right')

    return [sorted_index[s:e] for s,e in zip(chunk_starts, chunk_ends)]
    

def get_chunk_indices(sorted_series):
    from numpy import where, diff, add, insert
    chunks = where(diff(sorted_series))
    chunks = add(chunks[0], 1)
    chunks = insert(chunks, 0, 0)

    if chunks[-1] < len(sorted_series):
        chunks = append(chunks,(len(sorted_series)))
        
    chunk_ends = chunks[1:]
    chunk_starts = chunks[0:-1]
    
    return chunk_starts, chunk_ends

def create_offset(arraylike, offset, mode):
    
    if mode == 'percentage':
        offset = float(offset) / 100
        return arraylike + abs(arraylike * offset)
        
    elif mode == 'absolute':
        return arraylike + offset


import unittest
from pandas import DataFrame
from functools import partial
from pandas import Index

class WindowSliderBase():
    def get_result(frame, column, offset):
        series = frame[column]
        result = self.slide(series, offset)
        
        result = [list(map(list, n)) for n in result]
        
        return result

class testPercentageWindowSlider(unittest.TestCase):
    a = [100, 100, 102, 102, 103, 105, 105, 106, 109, 110, 111]
    b = [105, 110, 111, 111, 112, 120, 120, 125, 130, 131, 141]
    c = [200, 100, 150, 100, 200, 150, 130, 130, 150, 140, 205]
    
    total = DataFrame(data = list(zip(a, b, c)), columns = ['A', 'B', 'C'])
    total.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    print(total)
    
    slide = partial(slide_windows, mode = 'percentage')
    
    def test_total_input(self):
        series = self.total['A']
        
        result = self.slide(series, offset = 5)

        result = [list(map(list, n)) for n in result]
        
        test = [[['A', 'B'], ['A', 'B', 'C', 'D', 'E', 'F', 'G']],
                [['C', 'D'], ['C', 'D', 'E', 'F', 'G', 'H']], 
                [['E'], ['E', 'F', 'G', 'H']],
                [['F', 'G'], ['F', 'G', 'H', 'I', 'J']],
                [['H'], ['H', 'I', 'J', 'K']],
                [['I'], ['I', 'J', 'K']],
                [['J'], ['J', 'K']],
                [['K'], ['K']]]
        self.assertEqual(result,test )
        
        
    def test_basecomp_input(self):
        base = self.total['B'].loc[['A', 'B']]
        comp = self.total['B'].loc[['A', 'B', 'C', 'D', 'E', 'F', 'G']]
        

        result = self.slide(base, comp, offset = 5)
        result = [list(map(list, n)) for n in result]

        test = [[['A'], ['A', 'B']],
                [['B'], ['B', 'C', 'D','E']]]
                
        self.assertEqual(result, test)
        
if __name__ == '__main__':
    test_classes_to_run = [testPercentageWindowSlider]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
