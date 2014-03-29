'''
    red-black Btree test
    current is binary tree
'''
class node(object):
    def __init__(self, content, _parent=None):
        self.color ='black' 
        self.right = None
        self.left = None
        self.content = content
        self._parent = _parent

    @property
    def parent(self):
        return self._parent
    @parent.getter
    def parent(self):
        if self._parent:
            return self._parent.content
        else:
            return None

    def __str__(self):
        return str( ( self.content, self.color, self.parent ) )

class rbTree(object):
    def __init__(self):
        self.root = None 

    def __str__(self):
        output = []
        self.DFS(self.root, output)
        return str( output )

    def DFS(self, curNode, output):
        if None == curNode:
            return
        else:
            self.DFS(curNode.left, output)
            self.DFS(curNode.right, output)
            output.append( str(curNode) )
        return 
            
    def addNode(self, content):
        self.binary(self.root, content)

    def binarySearch(self, current, content):
        if None == current: # empty tree
            return None

        if content < current.content: 
            self.binarySearch( current.left, content )
        elif content > current.content:
            self.binarySearch( current.right, content )
        else:
            print 'find: ',current
            return current


    def binary(self, current, content):
        if None == current: # empty tree
            self.root = node(content)
            return

        if content < current.content: 
            if None == current.left:
                current.left = node(content, current)
            else:
                self.binary( current.left, content )
        else:
            if None == current.right:
                current.right = node(content, current)
            else:
                self.binary( current.right, content )
        return 


    def left_rotate(self, target):
        x = self.binarySearch(self.root, target)
        rightTree = x.right # x's right tree
        parent = x.parent

        if None != parent:
            if None != rightTree and None != rightTree.left:
                leftTree = rightTree.left # the leftTree of x's right tree
                if parent.right == x:
                    parent.right = rightTree
                    rightTree.left = x
                    x.right = leftTree
                else:
                    parent.left = rightTree
                    rightTree.left = x
                    x.right = leftTree
        else: #rotate in root
            leftTree = rightTree.left
            rightTree.left = x
            x.right = leftTree
            self.root = rightTree 

if __name__ == '__main__':
   tree = rbTree()
   a = [13,11,6,8,1,17,15,25]

   for i in a:
       tree.addNode(i)
   print tree
   print 'left rotate in node 13'
   tree.left_rotate(17)
   print tree


