"""
An AVL tree is a self-balancing binary search tree (BST) 
where the difference between heights of left and right subtrees of any node cannot be larger than one. 
This invariant ensures the height of the tree is O(log n) where n is the number of nodes in the tree. 
Tree operations (insertion, deletion...) take O(log n) time.
After insertion or deletion, the tree may become unbalanced. 
The invariant can be restored through one or more tree rotations.
"""

class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

class AVLTree():
    def __init__(self) -> None:
        pass

    def AVL_insert(self, root, key):
        '''
        insert key into an AVL tree rooted at node root.
        1. first do a normal BST insertion
        2. update height
        3. calculate balance factor
        4. handle unbalance if necessay
            let z be the lowest node violating the invariant, 
            we have 4 cases:
            * right-right: z's right child y is higher (heavy) than left child, 
                and y is right-heavy or balanced -- left-rotate z.
            * right-left: z is right-heavy, its right child y is left-heavy
                -- right-rotate y then left-rotate z.
            * left-left: z is left-heavy, its left child y is left-heavy or balanced 
                -- right-rotate z.
            * left-right: z is left-heavy, its left child y is right-heavy
                -- left-rotate y then right-rotate z.
        '''
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.AVL_insert(root.left, key)
        else:
            root.right = self.AVL_insert(root.right, key)

        # update height and calculate balance factor
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))     
        
        balance = self.get_height(root.left) - self.get_height(root.right)

        # handle unbalance
        # right-right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # right-left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        # left-left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # left-right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        return root

    def AVL_delete(self, root, key):
        # normal BST deletion
        if not root:
            return root
        elif key < root.key:
            root.left = self.AVL_delete(root.left, key)
        elif key > root.key:
            root.right = self.AVL_delete(root.right, key)
        else:
            if not root.left:
                ret = root.right
                root = None
                return ret
            if not root.right:
                ret = root.left
                root = None
                return ret
            new_root = self.find_min_node(root.right)
            root.key = new_root.key
            root.right = self.AVL_delete(root.right, new_root.key)

        if not root:
            return root

        # update height and calculate balance factor
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))     
        
        balance = self.get_height(root.left) - self.get_height(root.right)
            
        # handle unbalance
        # right-right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # right-left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        # left-left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # left-right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        return root

    '''
    Rotations to handle tree acrobatics
             y       right-rotate(y)        x
           /   \     --------------->     /   \ 
          x    T3    <---------------    T1    y
        /   \          left-rotate(x)        /   \ 
       T1   T2                              T2   T3  
    '''
    def left_rotate(self, x):
        '''
        left-rotate node x
        '''
        # rotate
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2

        # update height
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # return new children to the calling parent
        return y

    def right_rotate(self, y):
        '''
        right-rotate node y
        '''
        # rotate
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2

        # update height
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # return new children to the calling parent
        return x

    def get_height(self, node):
        # NIL has height -1
        if not node:
            return -1
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def find_min_node(self, root):
        if not root or not root.left:
            return root
        return self.find_min_node(root.left)

    def pre_order(self, root):
        if not root:
            return
        print(root.key, end=' ')
        self.pre_order(root.left)
        self.pre_order(root.right)   

    def AVL_min(self, root):
        return self.find_min_node(root)

    def AVL_extract_min(self, root):
        ret = self.AVL_min(root)
        return self.AVL_delete(root, ret.key), ret

    def AVL_find(self, root, key):
        # find the node with given key
        if not root:
            return None
        if key < root.key:
            return self.AVL_find(root.left, key)
        if key > root.key:
            return self.AVL_find(root.right, key)
        return root

    def AVL_successor(self, root, key):
        # find the successor node of given key
        # assume key exists in the tree
        traversed = []
        while root:
            if key == root.key:
                break
            if key < root.key:
                traversed.append([root, 'left'])
                root = root.left
            else:
                traversed.append([root, 'right'])
                root = root.right
        if not root:
            return Node(None)
        if root.right != None:
            return self.find_min_node(root.right)
        for i in reversed(range(len(traversed))):
            if traversed[i][1] == 'left':
                return traversed[i][0]
        return Node(None)
    
if __name__ == "__main__":
    root = None
    my_avl_tree = AVLTree()
    root = my_avl_tree.AVL_insert(root, 1)
    root = my_avl_tree.AVL_insert(root, 2)
    root = my_avl_tree.AVL_insert(root, 3)
    root = my_avl_tree.AVL_insert(root, 4)
    my_avl_tree.pre_order(root)
    root, min = my_avl_tree.AVL_extract_min(root)
    print()
    my_avl_tree.pre_order(root)