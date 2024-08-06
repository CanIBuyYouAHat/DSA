import json
from typing import List

class Node():
    def  __init__(self,
                  key        = None,
                  keycount   = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.keycount   = keycount
        self.leftchild  = leftchild
        self.rightchild = rightchild

# For the tree rooted at root, dump the tree to stringified JSON object and return.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "keycount": node.keycount,
            "leftchild": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------
        
def insert_helper(curr: Node, key: int):
    if key == curr.key:
        curr.keycount += 1
    elif key > curr.key:
        if curr.rightchild == None:
            newNode = Node(key)
            newNode.keycount = 1
            curr.rightchild = newNode
        else:
            insert_helper(curr.rightchild, key)
    elif key < curr.key:
        if curr.leftchild == None:
            newNode = Node(key)
            newNode.keycount = 1
            curr.leftchild = newNode
        else:
            insert_helper(curr.leftchild, key)
        

# For the tree rooted at root and the key given:
# If the key is not in the tree, insert it with a keycount of 1.
# If the key is in the tree, increment its keycount.
def insert(root: Node, key: int) -> Node:
    # YOUR CODE GOES HERE.
    if root == None:
        root = Node(key)
        root.keycount = 1
        return root
    else:   
        insert_helper(root, key)  
        return root

def inOrderSucc(curr: Node) -> Node:
    while curr.leftchild:
        curr = curr.leftchild
    return curr

def inOrderPred(curr: Node) -> Node:
    while curr.rightchild:
        curr = curr.rightchild
    return curr


def deleter(root: Node, key: int, decr: bool) -> Node:
    parent = None
    curr = root

    while curr and curr.key != key:
        parent = curr
        if key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild
    
    if curr == None:
        return root
    
    if decr and curr.keycount > 1:
        curr.keycount -= 1
    else:
        if curr.leftchild == None and curr.rightchild == None:
            if curr != root:
                if parent.leftchild == curr:
                    parent.leftchild = None
                else:
                    parent.rightchild = None
            else:
                root = None

        elif curr.rightchild and curr.leftchild:
            succ = inOrderSucc(curr.rightchild)
            tempKey = succ.key
            tempKeyCount = succ.keycount
            
            deleter(root, tempKey, False)

            curr.key = tempKey
            curr.keycount = tempKeyCount
        
        else:
            if curr.leftchild:
                temp = curr.leftchild
            else:
                temp = curr.rightchild
          
            if curr != root:
                if curr == parent.leftchild:
                    parent.leftchild = temp
                else:
                    parent.rightchild = temp
            else:
                root = temp
    return root

# For the tree rooted at root and the key given:
# If the key is not in the tree, do nothing.
# If the key is in the tree, decrement its key count. If they keycount goes to 0, remove the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    root = deleter(root, key, True)
    return root

        
def searcher(curr: Node, key: int, ret: str) -> str:

    while curr and curr.key != key:
        ret.append(curr.key)
        if key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild
    if curr != None:
        ret.append(curr.key)
        return ret
    else:
        return ret
    
# For the tree rooted at root and the key given:
# Calculate the list of keys on the path from the root towards the search key.
# The key is not guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    path = searcher(root, search_key, [])
    return(json.dumps(path, indent=2))

def preorder_helper(curr: Node, list: str) -> str:
    list.append(curr.key)
    if curr.leftchild != None:
        preorder_helper(curr.leftchild, list)
    if curr.rightchild != None:
        preorder_helper(curr.rightchild, list)
    return list

# For the tree rooted at root, find the preorder traversal.
# Return the json.dumps of the list with indent=2.
def preorder(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    pre = preorder_helper(root, [])
    
    return(json.dumps(pre, indent=2))

def inorder_helper(curr: Node, list: str) -> str:
    if curr.leftchild != None:
        inorder_helper(curr.leftchild, list)
    list.append(curr.key)
    if curr.rightchild != None:
        inorder_helper(curr.rightchild, list)
    return list


# For the tree rooted at root, find the inorder traversal.
# Return the json.dumps of the list with indent=2.
def inorder(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    ord = inorder_helper(root, [])
    return(json.dumps(ord, indent=2))

def postorder_helper(curr: Node, list: str) -> str:
    if curr.leftchild != None:
        postorder_helper(curr.leftchild, list)
    if curr.rightchild != None:
        postorder_helper(curr.rightchild, list)
    list.append(curr.key)
    return list

# For the tree rooted at root, find the postorder traversal.
# Return the json.dumps of the list with indent=2.
def postorder(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    post = postorder_helper(root, [])
    return(json.dumps(post, indent=2))

def bft_helper(curr: Node, list: str) -> str:
    if curr != None:
        if curr.leftchild != None:
            list.append(curr.leftchild.key)
        if curr.rightchild != None:
            list.append(curr.rightchild.key)

# For the tree rooted at root, find the BFT traversal (go leftchild-to-rightchild).
# Return the json.dumps of the list with indent=2.
def bft(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    queue = [root]
    path = []
    while len(queue) != 0:
        curr = queue.pop(0)
        path.append(curr.key)

        if curr.leftchild != None:
            queue.append(curr.leftchild)
        if curr.rightchild != None:
            queue.append(curr.rightchild)

    return json.dumps(path, indent=2)