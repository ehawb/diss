# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:21:18 2020

@author: Emily Smith
"""

import random
import string

def random_string(num_letters, num_digits):
    string_ID = ''.join((random.choice(string.ascii_letters) for i in range(num_letters)))
    string_ID += ''.join((random.choice(string.digits) for i in range(num_digits)))
    string_list = list(string_ID)
    random.shuffle(string_list)
    final_string = ''.join(string_list)
    return final_string