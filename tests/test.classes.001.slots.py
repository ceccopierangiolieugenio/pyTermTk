#!/usr/bin/env python3
# vim:ts=4:sw=4:fdm=indent:cc=79:

import TermTk

def find_classes(cand_dict):
    '''
    find all classes in cand_dict.

    return (sorted) list of classes (not class names).
    '''
    found_classes = []
    for candidate in cand_dict.values():
        if isinstance(candidate, type):
            found_classes.append(candidate)

    found_classes.sort(key=lambda entry: entry.__name__)
    return found_classes

def check_slots(classes):
    '''
    check for every class in classes if it and its superclasses uses slots.
    '''
    for cls in classes:
        found_problem = None
        for test_class in cls.__mro__:
            if test_class.__module__.startswith('TermTk'):
                if '__slots__' not in test_class.__dict__:
                    found_problem = test_class
        if found_problem:
            print(f'class {cls.__name__} has superclass {found_problem} with missing __slots__')

found_classes = find_classes(TermTk.__dict__)
check_slots(found_classes)

