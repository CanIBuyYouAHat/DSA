from __future__ import annotations
import json
from typing import List

verbose = False

class Node():
    def  __init__(self,
                  key      : int,
                  value    : str,
                  toplevel : int,
                  pointers : List[Node] = None):
        self.key      = key
        self.value    = value
        self.toplevel = toplevel
        self.pointers = pointers

class SkipList():
    def  __init__(self,
                  maxlevel : int,
                  headnode : Node = None,
                  tailnode : Node = None):
        self.headnode  = headnode
        self.tailnode  = tailnode
        self.maxlevel = maxlevel

    # Return a reasonable-looking json.dumps of the object with indent=2.
    # For each node we show the key, the value, and the list of pointers and the key each points to.
    def dump(self) -> str:
        currentNode = self.headnode
        nodeList = []
        while currentNode is not self.tailnode:
            pointerList = str([n.key for n in currentNode.pointers])
            nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
            currentNode = currentNode.pointers[0]
        pointerList = str([None for n in currentNode.pointers])
        nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
        return json.dumps(nodeList,indent = 2)

    # Creates a pretty rendition of a skip list.
    # It's vertical rather than horizontal in order to manage different lengths more gracefully.
    # This will never be part of a test but you can put "pretty" as a single line in your tracefile
    # to see what the result looks like.
    def pretty(self) -> str:
        currentNode = self.headnode
        longest = 0
        while currentNode != None:
            if len(str(currentNode.key)) > longest:
                longest = len(str(currentNode.key))
            currentNode = currentNode.pointers[0]
        longest = longest + 2
        pretty = ''
        currentNode = self.headnode
        while currentNode != None:
            lineT = 'Key = ' + str(currentNode.key) + ', Value = ' + str(currentNode.value)
            lineB = ''
            for p in currentNode.pointers:
                if p is not None:
                    lineB = lineB + ('('+str(p.key)+')').ljust(longest)
                else:
                    lineB = lineB + ''.ljust(longest)
            pretty = pretty + lineT
            if currentNode != self.tailnode:
                pretty = pretty + "\n"
                pretty = pretty + lineB + "\n"
                pretty = pretty + "\n"
            currentNode = currentNode.pointers[0]
        return(pretty)

    # Initialize a skip list.
    # This constructs the headnode and tailnode each with maximum level maxlevel.
    # Headnode has key -inf, and pointers point to tailnode.
    # Tailnode has key inf, and pointers point to None.
    # Both have value None.
    def initialize(self,maxlevel):
        pointers = [None] * (1+maxlevel)
        tailnode = Node(key = float('inf'),value = None,toplevel = maxlevel,pointers = pointers)
        pointers = [tailnode] * (maxlevel+1)
        headnode = Node(key = float('-inf'),value = None, toplevel = maxlevel,pointers = pointers)
        self.headnode = headnode
        self.tailnode = tailnode
        self.maxlevel = maxlevel


    def makeSpace(self, a, newNode):
        a.reverse()
        
        newPtrs = []
        for ptr in a:
            if ptr[1] <= newNode.toplevel:
                # print(newNode.key, ptr[2].key)
                ptr[0].pointers[ptr[1]] = newNode
                newPtrs.append(ptr[2])
        # newPtrs.reverse()
        newNode.pointers = newPtrs

    # Create and insert a node with the given key, value, and toplevel.
    # The key is guaranteed to not be in the skiplist.
    def insert(self,key,value,toplevel):
        a = []
        curr = self.headnode

        for i in range(self.maxlevel, -1, -1):
            next = curr.pointers[i]
            
            while next.key != float('inf') and next.key < key:
                curr = next
                next = curr.pointers[i]

            a.append((curr, i, next))
        newNode = Node(key = key, value = value, toplevel = toplevel, pointers = None)
        self.makeSpace(a, newNode)

            # else:
            #     a.append((curr, i, next))
            #     while next.key is not None and next.key < key:
            #         curr = next
            #         next = curr.pointers[i]

        
    def splice(self, a, key):
        
        for ptr in a:
            if ptr[2].key == key:
                # print(ptr[0].pointers[ptr[1]].key, ptr[2].pointers[ptr[1]].key)
                ptr[0].pointers[ptr[1]] = ptr[2].pointers[ptr[1]]
            

    # Delete node with the given key.
    # The key is guaranteed to be in the skiplist.
    def delete(self,key):
        a = []
        
        for i in range(self.maxlevel, -1, -1):
            curr = self.headnode
            next = curr.pointers[i]
            
            while next.key != float('inf') and next.key != key:
                curr = next
                next = curr.pointers[i]

            a.append((curr, i, next))
        self.splice(a, key)

    # Search for the given key.
    # Construct a list of all the keys in all the nodes visited during the search.
    # Append the value associated to the given key to this list.
    def search(self,key) -> str:
        A = []
        curr = self.headnode
        A.append(curr.key)
        for i in range(self.maxlevel, -1, -1):
            next = curr.pointers[i]
            while next.key != float('inf') and next.key <= key:
                curr = next
                next = curr.pointers[i]

                A.append(curr.key)
        A.append(curr.value)
        return json.dumps(A,indent = 2)