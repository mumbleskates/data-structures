# -*- coding: utf-8 -*-
from linked_list import LinkedList


class Stack(LinkedList):
    # Using LinkedList __init__ for Stack init method

    # push() has the same functionality as insert()
    push = LinkedList.insert

    # pop() already has the desired functionality in LinkedList
