"""
An interval tree implementation based on avl tree
Intreval is given in python list (or numpy array), e.g., [20, 23]
Can also define an Interval class with interval.low, interval.high
"""


class Node():
    def __init__(self, interval):
        self.low = interval[0]
        self.high = interval[1]
        self.max = interval[1]
        self.left = None
        self.right = None
        self.height = 0

class IntervalTree():
    def __init__(self) -> None:
        pass

    def interval_search(self, root, interval):
        while (root is not None
                and (interval[0] > root.high
                    or interval[1] < root.low)):
            if root.left is not None and interval[0] < root.left.max:
                root = root.left
            else:
                root = root.right
        if root is None:
            print("No overlapping interval with [%d, %d]"%(interval[0], interval[1]))
        else:
            print("Overlapping interval with [%d, %d]: [%d, %d]"\
                  %(interval[0], interval[1], root.low, root.high))
        return root

    def insert(self, root, interval):
        if root is None:
            return Node(interval)
        elif interval[0] < root.low:
            root.left = self.insert(root.left, interval)
        else:
            root.right = self.insert(root.right, interval)

        root.max = max(root.max, interval[1])
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
    
    def delete(self, root, interval):
        if root is None:
            return root
        elif interval[0] < root.low:
            root.left = self.delete(root.left, interval)
        elif interval[0] > root.low:
            root.right = self.delete(root.right, interval)
        else:
            if interval[1] != root.high:
                print("Interval does not match!")
                return root
            if root.left is None:
                ret = root.right
                root = None
                return ret
            if root.right is None:
                ret = root.left
                root = None
                return ret
            new_root = self.find_min_node(root.right)
            root.low = new_root.low
            root.high = new_root.high
            # root.max = new_root.max
            root.right = self.delete(root.right, [new_root.low, new_root.high])

        root.max = max(root.high, self.get_max(root.left), self.get_max(root.right))
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

        # update max, x depends on y
        y.max = max(y.max, self.get_max(y.left), self.get_max(y.right))
        x.max = max(x.high, self.get_max(x.left), self.get_max(x.right))

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

        # update max, y depends on x
        x.max = max(x.high, self.get_max(x.left), self.get_max(x.right))
        y.max = max(y.max, self.get_max(y.left), self.get_max(y.right))

        # return new children to the calling parent
        return x

    def get_max(self, node):
        # NIL has no max attribute
        # assume all interval endpoints are non-negative
        if node is None:
            return -1
        return node.max

    def get_height(self, node):
        # NIL has height -1
        if node is None:
            return -1
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def find_min_node(self, root):
        if root is None or root.left is None:
            return root
        return self.find_min_node(root.left)
    
    def pre_order(self, root):
        if root is None:
            return
        print(root.low, root.high, root.max)
        self.pre_order(root.left)
        self.pre_order(root.right)

if __name__ == "__main__":
    root = None
    my_interval_tree = IntervalTree()
    intervals = [[17, 19], [5, 11], [22, 23], [4, 8], [15, 18], [7, 10]]
    for interval in intervals:
        root = my_interval_tree.insert(root, interval)
    my_interval_tree.pre_order(root)

    my_interval_tree.interval_search(root, [14, 16])
    my_interval_tree.interval_search(root, [12, 14])

    