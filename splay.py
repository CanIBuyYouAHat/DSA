from __future__ import annotations
import json
from typing import List

verbose = False

class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent


class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------

    def rotate_right(self, root: Node) -> Node:
        parent = root.parent
        temp = root.leftchild.rightchild
        newRoot = root.leftchild
        root.leftchild = temp
        newRoot.rightchild = root 
        
        # Set parents
        if (root.leftchild is not None):
            root.leftchild.parent = root
        newRoot.parent = root.parent    
        root.parent = newRoot    
        
        # set children
        if (parent is not None):
            if (root == parent.leftchild):
                parent.leftchild = newRoot
            else:
                parent.rightchild = newRoot
         
        return newRoot
    
    def rotate_left(self, root: Node) -> Node:
        # print(f"curr: {root.key}")
        
        parent = root.parent
        temp = root.rightchild.leftchild  
        newRoot = root.rightchild
        root.rightchild = temp
        newRoot.leftchild = root
        
        # Set parents
        if (root.rightchild is not None):
            root.rightchild.parent = root
        newRoot.parent = root.parent
        root.parent = newRoot
        
        # set children
        if (parent is not None):
            if (root == parent.leftchild):
                parent.leftchild = newRoot
            else:
                parent.rightchild = newRoot
        
        return newRoot 

        
    def splay(self, curr):
        
        while (curr.parent is not None):
            parent = curr.parent
            gp = parent.parent
            
            if (gp is not None):
                if (parent == curr.parent.parent.leftchild):
                    if (curr == parent.leftchild):
                        parent = self.rotate_right(gp)
                        curr = self.rotate_right(parent)
                    else:
                        curr = self.rotate_left(parent)
                        # parent changed
                        curr = self.rotate_right(curr.parent)
                else:
                    if (curr == parent.rightchild):
                        parent = self.rotate_left(gp)
                        curr = self.rotate_left(parent)
                    else:
                        curr = self.rotate_right(parent)
                        # parent changed
                        curr = self.rotate_left(curr.parent)
            else:
                if (parent.leftchild == curr):
                    curr = self.rotate_right(self.root)
                else:
                    curr = self.rotate_left(self.root)  
        self.root = curr  
   
                
    def exists(self, curr, key) -> int:
        if (curr.key == key):
            return curr
        elif (key < curr.key):
            if (curr.leftchild is None):
                return curr
            else:
                return self.exists(curr.leftchild, key)
        else:
            if (curr.rightchild is not None):
                return self.exists(curr.rightchild, key)
            else:
                return curr

    # Search
    def search(self, key:int):
        self.splay(self.exists(self.root, key))

    # Insert Method 1
    def insert(self,key:int):
        
        if self.root is None:
            self.root = Node(key)

        # Call splay on IOS (or IOP) if key does not exist
        else:
            self.splay(self.exists(self.root, key))
            # print(f'new root {self.root.key}')
            newRoot = Node(key)
            # print(self.root.key, key)
            if self.root.key < key:
                newRoot.leftchild = self.root
                newRoot.rightchild = self.root.rightchild
                self.root.rightchild = None
            else:
                newRoot.rightchild = self.root
                newRoot.leftchild = self.root.leftchild
                self.root.leftchild = None
            
            if (newRoot.leftchild is not None):
                newRoot.leftchild.parent = newRoot
            if (newRoot.rightchild is not None):
                newRoot.rightchild.parent = newRoot
            self.root = newRoot    

    # Delete Method 1
    def delete(self,key:int):
        self.splay(self.exists(self.root, key))
        
        if (self.root.key == key):
            if (self.root.leftchild is None and self.root.rightchild is not None):
                self.root = self.root.rightchild
            elif (self.root.rightchild is None and self.root.leftchild is not None):
                self.root = self.root.leftchild
            else:
                temp = self.root.leftchild
                self.splay(self.exists(self.root.rightchild, key))
                self.root.leftchild = temp
                self.root.leftchild.parent = self.root
                
            self.root.parent = None
                
                