import json
from typing import List

class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)


def get_height(curr: Node) -> int:
    if curr is None:
        return 0
    else:
        return 1 + max(get_height(curr.rightchild), get_height(curr.leftchild))
    
def rotate_right(root: Node) -> Node:
    temp = root.leftchild.rightchild
    newRoot = root.leftchild
    root.leftchild = temp
    newRoot.rightchild = root
    return newRoot
    
def rotate_left(root: Node) -> Node:
    # print(f"curr: {root.key}")
    temp = root.rightchild.leftchild  
    newRoot = root.rightchild
    root.rightchild = temp
    newRoot.leftchild = root
    
    return newRoot 

def balance(root: Node) -> Node:
    if root is None:
        return None
    else:
        if root.rightchild is not None:
            root.rightchild = balance(root.rightchild)
        if root.leftchild is not None:
            root.leftchild = balance(root.leftchild)
        diff = get_height(root.rightchild) - get_height(root.leftchild)
        
        if diff == 2:
            rlHeavy = get_height(root.rightchild.rightchild) - get_height(root.rightchild.leftchild)
            if rlHeavy == 1:
                root = rotate_left(root)
            elif rlHeavy == -1:
                root.rightchild = rotate_right(root.rightchild)
                root = rotate_left(root)
            else:
                root.rightchild = balance(root.rightchild)
        elif diff == -2:
            lrHeavy = get_height(root.leftchild.rightchild) - get_height(root.leftchild.leftchild)
            if lrHeavy == 1:
                root.leftchild = rotate_left(root.leftchild)
                root = rotate_right(root)
            elif lrHeavy == -1:
                root = rotate_right(root)
            else:
                root.leftchild = balance(root.leftchild)
        
        return root

def insert_helper(curr: Node, key: int, word: str) -> Node:
    if key > curr.key:
        if curr.rightchild == None:
            newNode = Node(key, word, None, None)
            curr.rightchild = newNode
        else:
            insert_helper(curr.rightchild, key, word)
    elif key < curr.key:
        if curr.leftchild == None:
            newNode = Node(key, word, None, None)
            curr.leftchild = newNode
        else:
            insert_helper(curr.leftchild, key, word)

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def insert(root: Node, key: int, word: str) -> Node:
    # Fill in.
    if root == None:
        root = Node(key, word, None, None)
        return root
    else:   
        insert_helper(root, key, word)
        root = balance(root)
    return root

def preorder(curr: Node, list: str) -> str:
    list.append((curr.key, curr.word))
    if curr.leftchild != None:
        preorder(curr.leftchild, list)
    if curr.rightchild != None:
        preorder(curr.rightchild, list)
    return list

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    for node in items:
        if root == None:
            root = Node(int(node[0]), node[1], None, None)
        else:   
            insert_helper(root, int(node[0]), node[1])
        
    pre = preorder(root, [])
 
    newRoot = Node(pre[0][0], pre[0][1], None, None)
    for node in pre[1:]:
        newRoot = insert(newRoot, node[0], node[1])
        
    root = newRoot
    return root

def preorder_delete(curr: Node, list: str, keys: List[int]) -> str:
    if curr.key not in keys:
        list.append((curr.key, curr.word))
    if curr.leftchild != None:
        preorder_delete(curr.leftchild, list, keys)
    if curr.rightchild != None:
        preorder_delete(curr.rightchild, list, keys)
    return list

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    pre = preorder_delete(root, [], keys)
    
    newRoot = insert(None, pre[0][0], pre[0][1])
    for node in pre[1:]:
        newRoot = insert(newRoot, node[0], node[1])
    root = newRoot
        
    return root

def searcher(curr: Node, key: int, ret: str, replacement_word: str) -> str:
    while curr and curr.key != key:
        ret.append(curr.key)
        if key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild
    if curr != None:
        if replacement_word is not None:
            curr.word = replacement_word
        else:
            ret.append(curr.key)
            ret.append(curr.word)
        return ret
    else:
        return ret

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    path = searcher(root, search_key, [], None)
    return json.dumps(path,indent=2)

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> None:
    searcher(root, search_key, [], replacement_word)
    return root