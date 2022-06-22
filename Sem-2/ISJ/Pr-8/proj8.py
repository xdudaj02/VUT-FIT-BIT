#!/usr/bin/env python3


def first_with_given_key(iterable, key=lambda x: x):
    values = []
    return_list = []
    for i in iterable:
        if key(i) not in values:
            values.append(key(i))
            return_list.append(i)
    return return_list
