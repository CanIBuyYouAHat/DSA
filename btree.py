from __future__ import annotations
import json
from typing import List
import math

# Node Class.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  values   : List[str] = None,
                  children : List[Node] = [None, None],
                  parent   : Node = None):
        self.keys     = keys
        self.values   = values
        self.children = children
        self.parent   = parent

class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = root

    def dump(self) -> str:
        def _to_dict(node) -> dict:
            # print(f'keys: {node.keys}, values: {node.values}, children: {len(node.children)}')
            return {
                "keys": node.keys,
                "values": node.values,
                "children": [(_to_dict(child) if child is not None else None) for child in node.children],
            }
            
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    
    
    def setChildren(self, newParent: Node):
        if newParent.children[0] != None:
            for child in newParent.children:
                child.parent = newParent 
    
    def split(self, overfull: Node) -> Node:
        if self.m % 2 != 0:
            median = math.floor(self.m / 2)
        else:
            median = self.m // 2 - 1

        promote = overfull.keys[median]
        newChild1 = Node(overfull.keys[:median], overfull.values[:median], overfull.children[:median + 1], overfull.parent)
        newChild2 = Node(overfull.keys[median + 1:], overfull.values[median + 1:], overfull.children[median + 1:], overfull.parent)
        
        self.setChildren(newChild1)
        self.setChildren(newChild2)

        if overfull == self.root:
            newChild1.parent = overfull
            newChild2.parent = overfull
            overfull.keys = [promote]
            overfull.values = [overfull.values[median]]
            overfull.children = [newChild1, newChild2]
            overfull.parent = None
            return overfull
        else:
            overfull.parent.keys.append(promote)
            overfull.parent.keys.sort()
            overfull.parent.values.insert(overfull.parent.keys.index(promote), overfull.values[median])
            overfull.parent.children.remove(overfull)
            promotedIndex = overfull.parent.keys.index(promote)
            overfull.parent.children.insert(promotedIndex, newChild1)
            overfull.parent.children.insert(promotedIndex + 1, newChild2)

            if len(overfull.parent.keys) == self.m:
                if not self.rotateIns(overfull.parent):
                    if overfull.parent == self.root:
                        self.root = self.split(overfull.parent)
                    else:
                        overfull.parent.parent = self.split(overfull.parent)
        return overfull.parent

    def rotateIns(self, overfull: Node) -> bool:
        if overfull == self.root:
            return False
        else:
            siblings = overfull.parent.children
            childIndex = siblings.index(overfull)
      
            if childIndex > 0 and len(siblings[childIndex - 1].keys) < self.m - 1:
                parent = overfull.parent
                openSibling = siblings[childIndex - 1]
                if childIndex == len(siblings) - 1:
                    tempKey = parent.keys[-1]
                    tempVal = parent.values[-1]
                else:
                    tempKey = parent.keys[childIndex - 1]
                    tempVal = parent.values[childIndex - 1]
                 
                totalLen = len(openSibling.keys) + len(overfull.keys)
                newLen = math.ceil(totalLen / 2)
                
                while len(overfull.keys) > newLen:
                    # Largest value from sibling moving left, append to end
                    openSibling.keys.append(tempKey)
                    openSibling.values.append(tempVal)
                    openSibling.children.append(overfull.children[0])
                    
                    parent.keys.remove(tempKey)
                    parent.values.remove(tempVal)
                    
                    tempKey = overfull.keys[0]
                    tempVal = overfull.values[0]
                    
                    overfull.values.pop(0)
                    overfull.keys.pop(0)
                    overfull.children.pop(0)
                    
                    parent.keys.append(tempKey)
                    parent.keys.sort()
                    parent.values.insert(parent.keys.index(tempKey), tempVal)
                self.setChildren(openSibling)
                return True
                    
            elif childIndex < len(siblings) - 1 and len(siblings[childIndex + 1].keys) < self.m - 1:
                parent = overfull.parent
                openSibling = siblings[childIndex + 1]
                if childIndex == 0:
                    tempKey = parent.keys[0]
                    tempVal = parent.values[0]
                else:
                    tempKey = parent.keys[childIndex]
                    tempVal = parent.values[childIndex]
                tempKey = parent.keys[childIndex]
                tempVal = parent.values[childIndex]
                totalLen = len(openSibling.keys) + len(overfull.keys)
                newLen = math.ceil(totalLen / 2)
                
                while len(overfull.keys) > newLen:
                    # Largest value from sibling moving left, append to end
                    openSibling.keys.insert(0, tempKey)
                    openSibling.values.insert(0, tempVal)
                    openSibling.children.insert(0, overfull.children[-1])
                    
                    parent.keys.remove(tempKey)
                    parent.values.remove(tempVal)
                    
                    tempKey = overfull.keys[-1]
                    tempVal = overfull.values[-1]
                    overfull.values.pop(-1)
                    overfull.keys.pop(-1)
                    overfull.children.pop(-1)
                    
                    parent.keys.append(tempKey)
                    parent.keys.sort()
                    parent.values.insert(parent.keys.index(tempKey), tempVal)
                self.setChildren(openSibling)
                return True
            
            else:
                return False
            
    
    def findChild(self, curr: Node, key: int) -> Node:
        # print(len(curr.children), curr.keys, key)
        if curr is None or curr.children[0] == None:
            return curr
        else:
            child = -1
            for i in range(len(curr.keys)):
                if key < curr.keys[i]:
                    child = i
                    break
            if self.findChild(curr.children[child], key) is None:
                return curr
            else:
                return self.findChild(curr.children[child], key)
                    
    # Insert.
    # if not overfull, done
    # if overfull, split
    # check parent recursively
    def insert(self, key: int, value: str):
        # Fill in the details.
        # print(f'Insert: {key} {value}') # This is just here to make the code run, you can delete it.
        
        if self.root is None:
            self.root = Node([key], [value])
        else:
            curr = self.root
            curr = self.findChild(curr, key)
            
            curr.keys.append(key)
            curr.keys.sort()
            curr.values.insert(curr.keys.index(key), value)
            curr.children.append(None)
            
            # print(curr.keys)
            if len(curr.keys) == self.m:
                if not self.rotateIns(curr):
                    if curr == self.root:
                        self.root = self.split(curr)
                    else:
                        curr.parent = self.split(curr)

# -----------------------------------------------------------------------------------------------------

    def merge(self, underfull: Node):
        # TODO: implement merging node1 and node2
        parent = underfull.parent
        siblings = parent.children
        childIndex = siblings.index(underfull)

        if childIndex < len(siblings) - 1:
            if len(siblings[childIndex - 1].keys) == math.ceil(self.m / 2):
                openSibling = siblings[childIndex - 1]
                rotateRight = False
            else: 
                openSibling = siblings[childIndex + 1]
                rotateRight = True
        else: 
            openSibling = siblings[childIndex - 1]
            rotateRight = False
            
        # Merging underfull with right sibling
        if rotateRight:
            demoteKey = parent.keys[childIndex]
            demoteVal = parent.values[childIndex]

            underfull.keys.append(demoteKey)
            underfull.values.append(demoteVal)

            underfull.keys.extend(openSibling.keys)
            underfull.values.extend(openSibling.values)
            underfull.children.extend(openSibling.children)

            openSibling.keys = underfull.keys
            openSibling.values = underfull.values
            openSibling.children = underfull.children

        else:
            demoteKey = parent.keys[childIndex - 1]
            demoteVal = parent.values[childIndex -1]

            openSibling.keys.append(demoteKey)
            openSibling.values.append(demoteVal)

            openSibling.keys.extend(underfull.keys)
            openSibling.values.extend(underfull.values)
            openSibling.children.extend(underfull.children)

        parent.keys.remove(demoteKey)
        parent.values.remove(demoteVal)

        self.setChildren(openSibling)
        siblings.pop(siblings.index(underfull))

        if parent == self.root and len(parent.keys) == 0:
            self.root = openSibling
        
        elif underfull.parent != self.root and len(underfull.parent.keys) < math.ceil(self.m / 2) - 1:
                    if not self.rotateDel(underfull.parent):
                        underfull.parent.parent = self.merge(underfull.parent)
        
        return parent
        
    def rotateDel(self, underfull: Node) -> bool:
        siblings = underfull.parent.children
        childIndex = siblings.index(underfull)

        # Determine which sibling to use for rotation
        if childIndex > 0 and len(siblings[childIndex - 1].keys) > (math.ceil(self.m / 2) - 1):
            openSibling = siblings[childIndex - 1]
            rotateRight = True
        elif childIndex < len(siblings) - 1 and len(siblings[childIndex + 1].keys) > (math.ceil(self.m / 2) - 1):
            openSibling = siblings[childIndex + 1]
            rotateRight = False
        else:
            return False  # No rotation possible

        totalLen = len(openSibling.keys) + len(underfull.keys)
        newLen = math.floor(totalLen / 2)
        
        # Determine the demote key and value
        if rotateRight:
            demoteKey = underfull.parent.keys[childIndex - 1]
            demoteValue = underfull.parent.values[childIndex - 1]
        else:
            demoteKey = underfull.parent.keys[childIndex]
            demoteValue = underfull.parent.values[childIndex]

        if rotateRight:
            # Rotate keys, values, and children from the left sibling
            while len(underfull.keys) < newLen:
                underfull.keys.insert(0, demoteKey)
                underfull.values.insert(0, demoteValue)
                underfull.children.insert(0, openSibling.children.pop())

                underfull.parent.keys[childIndex - 1] = openSibling.keys.pop()
                underfull.parent.values[childIndex - 1] = openSibling.values.pop()
                
                demoteKey = underfull.parent.keys[childIndex - 1]
                demoteValue = underfull.parent.values[childIndex - 1]
        else:
            # Rotate keys, values, and children from the right sibling
            while len(underfull.keys) < newLen:
                underfull.keys.append(demoteKey)
                underfull.values.append(demoteValue)
                underfull.children.append(openSibling.children.pop(0))

                underfull.parent.keys[childIndex] = openSibling.keys.pop(0)
                underfull.parent.values[childIndex] = openSibling.values.pop(0)

                demoteKey = underfull.parent.keys[childIndex]
                demoteValue = underfull.parent.values[childIndex]
            
        return True
    
   
    def findIOS(self, curr: Node):
        if curr.children[0] == None:
            return [curr.keys[0], curr.values[0]]
        else:
            return self.findIOS(curr.children[0])
        
    def delChild(self, curr: Node, key: int) -> Node:
        # print(len(curr.children), curr.keys, key)
        if curr.children[0] == None and key in curr.keys:
            curr.values.pop(curr.keys.index(key))
            curr.keys.remove(key)
            curr.children.pop(0)

            return curr
        elif key in curr.keys:
            keyIndex = curr.keys.index(key)
            keyVal = self.findIOS(curr.children[keyIndex + 1])
            curr.keys[keyIndex] = keyVal[0]
            curr.values[keyIndex] = keyVal[1]
        
            return self.delChild(curr.children[keyIndex + 1], keyVal[0])
        else:
            child = -1
            for i in range(len(curr.keys)):
                if key < curr.keys[i]:
                    child = i
                    break
            return self.delChild(curr.children[child], key)          
            
    # Delete.
    def delete(self, key: int):
        # Fill in the details.
        curr = self.root
        curr = self.delChild(curr, key)
        
        # print(curr.keys, key, curr.parent.keys)
        if curr != self.root:
            if len(curr.keys) < (math.ceil(self.m / 2) - 1):
                if not self.rotateDel(curr):
                    curr.parent = self.merge(curr)

# --------------------------------------------------------------------------------------------

    def searchChild(self, curr: Node, key: int, path) -> list:
        # print(len(curr.children), curr.keys, key)
        # print(len(curr.children), path, curr.values)
        child = -1
        for i in range(len(curr.keys)):
            if key < curr.keys[i]:
                child = i
                break
            
        if key in curr.keys:
            path.append(str(curr.values[curr.keys.index(key)]))
            return path

        else:
            if child == -1:
                path.append(len(curr.children) - 1)
            else:
                path.append(child)
            return self.searchChild(curr.children[child], key, path)

    # Search
    def search(self,key) -> str:
        path = self.searchChild(self.root, key, [])
        return json.dumps(path)