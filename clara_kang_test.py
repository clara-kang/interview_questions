#!/usr/bin/env python

# question 1
# accepts two lines (x1,x2) and (x3,x4) on the x-axis
# returns whether they overlap

# assumption cases such as (1, 2), (2, 3) are considered overlapped
def overlap(x1, x2, x3, x4):
    s1_left = min(x1, x2)
    s1_right = max(x1, x2)
    s2_left = min(x3, x4)
    s2_right = max(x3, x4)

    if (s1_left < s2_left):
        l_s = [s1_left, s1_right]
        r_s = [s2_left, s2_right]
    else:
        l_s = [s2_left, s2_right]
        r_s = [s1_left, s1_right]

    # scenario 1: partially overlap
    if l_s[1] >= r_s[0] and l_s[1] <= r_s[1]:
        return True
    # scenario 2: completely overlap
    elif l_s[1] >= r_s[1]:
        return True
    # scenario 3: no overlap
    else:
        return False

# test scenario 1
result = overlap(1, 5, 2, 8)
assert result == True

# test scenario 1 with x1, x2 in reversed order
result = overlap(5, 1, 2, 8)
assert result == True

# test scenario 1 with seg1, seg2 in reversed order
result = overlap(2, 8, 5, 1)
assert result == True

# test scenario 2
result = overlap(1, 9, 3, 6)
assert result == True

# test scenario 3
result = overlap(2, 4, 5, 8)
assert result == False

# test scenario 3, corner case
result = overlap(2, 4, 4, 8)
assert result == True


# question 2
# accepts 2 version string
# returns the 0 is equal, -1 if s1 smaller, 1 if s1 bigger
def cmpString(s1, s2):
    s1_list = s1.split(".")
    s2_list = s2.split(".")

    def digit_check(s):
        return s.isdigit()

    if not ( all(list(map(digit_check, s1_list))) and all(list(map(digit_check, s2_list))) ):
        raise ValueError('invalid input')

    v_1 = list(map(int, s1_list))
    v_2 = list(map(int, s2_list))

    min_len = min(len(v_1), len(v_2))
    for i in range(0, min_len):
        if v_1[i] > v_2[i]:
            return 1
        elif v_1[i] < v_2[i]:
            return -1
    if i == min_len - 1:
        if len(v_1) > len(v_2):
            return 1
        elif len(v_1) == len(v_2):
            return 0
        else:
            return -1

# test invalid input
try:
    cmpString("1.a", "1.1.1")
    assert False # should have thrown value error already
except ValueError:
    assert True

# test equal input
assert cmpString("1.1.1", "1.1.1") == 0

# test s1 bigger with equal digits
assert cmpString("1.2.1", "1.1.1") == 1

# test s2 bigger with equal digits
assert cmpString("1.1.1", "1.2.1") == -1

# test s1 bigger with different digits
assert cmpString("1.2", "1.1.1") == 1

# test s2 bigger with different digits
assert cmpString("1.1", "1.3.1") == -1


# question 3
# Geo Distributed LRU cache with time expiration
# let each page be represented by integer

from datetime import datetime
from datetime import timedelta
# linked list node, for tracking how recently pages are accessed, and to hold content of page
class Node:
    def __init__(self, index, content, left=None, right=None):
        self.index = index
        self.content = content
        self.left = left
        self.right = right
        self.timestamp = datetime.now()

    def __repr__(self):
        return str(self.content)+" ["+str(self.timestamp) +"] "

class GeoLRUCache:
    # lifetime of nodes in caches is 6 hrs
    def __init__(self,capacity, life=6):
        # maps keys are indices of pages, en
        self.map = {}
        self.capacity = capacity
        self.start = None
        self.end = None
        self.life = life

    def addToStart(self, node):
        node.right = self.start
        # start's parent is now node
        if self.start != None:
            self.start.left = node
        # update start
        self.start = node
        # if node only node in list
        if self.end == None:
            self.end = self.start

    # helper function
    # find then removes node from linked list
    def removeNode(self, node):
        # parent not null, point parent to node's child
        if node.left != None:
            node.left.right = node.right
        # node has no parent, node must be start, start is now node's child
        else:
            self.start = node.right
        # child not null, point child to node's parent
        if node.right != None:
            node.right.left = node.left
        # no child, node is end, point end to node's parent
        else:
            self.end = node.left
        del node

    # extract content from LRU cache
    def get(self, key):
        # check if key exists
        if key in self.map.keys():
            node = self.map[key]
            self.removeNode(node)
            self.addToStart(node)
            return node.content
        else:
            return -1

    # insert page index&content into LRU cache
    def put(self, index, content):
        # key exists
        if index in self.map.keys():
            same_node = self.map[index]
            self.removeNode(same_node)
            self.addToStart(same_node)
            # update content
            same_node.content = content
        # key does not exist
        else:
            # initialize new node
            node = Node(index, content)
            # capacity exceeded, remove end
            if len(self.map) + 1 > self.capacity:
                self.rmEnd()
            self.addToStart(node)
            self.map[index] = node

    # helper function
    # remove the end node from map and linked list
    def rmEnd(self):
        del self.map[self.end.index]
        self.removeNode(self.end)

    # delete all expired pages (added life hours ago)
    def clearExpired(self):
        current_time = datetime.now()
        while self.end != self.start:
            # node expired
            if current_time - self.end.timestamp > timedelta(hours=self.life) :
                self.rmEnd()
            # all nodes before should be more recent, stop
            else:
                break

    # print the contents of the map
    def display(self):
        print(self.map)

# a simple test case
cache = GeoLRUCache(3)
cache.put(0, 100)
cache.put(4, 100)
cache.put(1, 100)

cache.put(4, 100)
cache.put(2, 100)
cache.put(4, 100)

cache.clearExpired()
cache.display()
