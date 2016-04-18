# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 19:29:40 2016

@author: Thomas
"""


def process_two_args(args):
    first_arg, *other_args = args
    if isinstance(first_arg, (tuple, list)):
        operand_tuple = first_arg
        assert len(operand_tuple) == 2, "Not enough or too much values passed."
        
        operand1 = operand_tuple[0]
        operand2 = operand_tuple[1]
        
    else:    
        assert len(other_args) == 1
        operand1 = first_arg
        operand2 = other_args[0]
        
    return operand1, operand2


def not_between(val, *comparisons):
    return not(between(val, *comparisons))
    
def between(val, *comparisons):
    operand1, operand2 = process_two_args(comparisons)
    return operand1 <= val <= operand2
