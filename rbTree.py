# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from matplotlib.pyplot import arrow
'''
    red-black Btree test
    current is binary tree
'''
class node(object):
    def __init__(self, content, _parent=None, color='red'):
        self._color =color 
        self.right = None
        self.left = None
        self.content = content
        self._parent = _parent

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, newParent):
        self._parent = newParent

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, newColor):
        self._color = newColor


    def __str__(self):
        d = None
        if self == self.parent.left:
            d = 'left'
        elif self == self.parent.right:
            d = 'right'
        return str( ( self.content, self.color, d, self.parent ) ) 

    '''
        __repr__ vs __str__???
    '''
    def __repr__(self):
        return str( ( self.content, self.color ) ) 

class rbTree(object):
    def __init__(self):
        self.root = None 
        self.nil = node( -1, None, 'black' ) #null節點，用來當葉節點與根節點的父親
        self.treeSize = 0 #總共幾個節點


    def __str__(self):
        output = []
        self.DFS( self.root, output )
        return str( output )

    def __len__(self):
        return self.treeSize

    def DFS( self, curNode, output):
        if self.nil == curNode:
            return
        else:
            self.DFS(curNode.left, output)
            self.DFS(curNode.right, output)
            output.append( str(curNode) )
        return
            
    def insert(self, content):
        self.treeSize += 1

        thisNode = node( content )
        thisNode.left = self.nil
        thisNode.right = self.nil
        if None == self.root:
            self.root = thisNode 
            self.root.color = 'black'
            self.root.parent = self.nil
            self.root.left = self.nil
            self.root.right = self.nil
        else:
            currentNode = self.root
            insertSuccess = False
            while not insertSuccess:
                if content < currentNode.content:
                    if self.nil == currentNode.left:
                        thisNode.parent = currentNode
                        thisNode.left = self.nil
                        thisNode.right = self.nil
                        currentNode.left = thisNode
                        insertSuccess = True
                    else:
                        currentNode = currentNode.left
                else:
                    if self.nil == currentNode.right:
                        thisNode.parent = currentNode
                        thisNode.left = self.nil
                        thisNode.right = self.nil
                        currentNode.right = thisNode 
                        insertSuccess = True
                    else:
                        currentNode = currentNode.right
        self.rb_insert_fixup( thisNode )

    def binarySearch(self, current, content):
        if None == current: # empty tree
            return None

        if content < current.content: 
            return self.binarySearch( current.left, content )
        elif content > current.content:
            return self.binarySearch( current.right, content )
        else:
            print 'find: ',current
            return current
    '''
        確認在插入node後，是否違反紅黑樹的性質
        若有則依照性質（LLr, LRr, RRb, RLb）行動
        性質定義出自"Fundamentals of Data Structures in C" 這本書
    '''
    def rb_insert_fixup(self, node ):
        while 'red' == node.parent.color:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if 'red' == uncle.color:
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent # 往上檢查
                else: 
                    if node == node.parent.right:
                        node = node.parent # 是否具備改變while loop的意義？
                        self.left_rotate( node.content )
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.right_rotate( node.parent.content )
            else:
                uncle = node.parent.parent.left
                if 'red' == uncle.color:
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent # 往上檢查
                else:
                    if node == node.parent.left:
                        node = node.parent # 是否具備改變while loop的意義？
                        self.left_rotate( node.content )
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    #這行是否該改成left_rotate
                    self.left_rotate( node.parent.content )
        self.root.color = 'black'

    def left_rotate(self, target):
        print '-----------'
        # 連結斷了？？
        print 'left_rotate', target
        x = self.binarySearch(self.root, target)
        print x
        father = x.parent

        if self.nil != father:
            if father == father.parent.right:
                father.parent.right = x
            else:
                father.parent.left = x

            x.parent = father.parent
            father.right = x.left
            x.left.parent = father
            x.left = father
            father.parent = x

            if x.parent == self.nil:
                self.root = x

    def right_rotate(self, target):
        print '-----------'
        print 'right_rotate'
        x = self.binarySearch(self.root, target)
        father = x.parent

        if self.nil != father: #不是根
            if father == father.parent.right:
                father.parent.right = x
            else:
                father.parent.left = x
            x.parent = father.parent
            father.left = x.right
            x.right.parent = father
            x.right = father
            father.parent = x

            if x.parent == self.nil:
                self.root = x

'''
    畫出紅黑樹的簡單示意圖
    不然每次都要用樹的走訪來看紅黑樹內容，太不方便了
    尤其是現在紅黑樹還有bug！

    不會畫出nil節點
'''
def drawRbTree( tree ):
    scale = 0.8 #畫圖時的間距
    print tree.root

    rootNode = (0,0) #繪圖用的根節點 
    

    treeSize = len(tree)
    treeLevel = math.floor( math.log( treeSize*2, 2 ) )
    maxTreeLeaves = 2**treeLevel / 2

    print 'tree size: ', treeSize 
    print 'tree level: ', treeLevel 
    print 'tree leaves max amount: ',  maxTreeLeaves


    treeLevelOrder = []
    nodeCount = 0 # 用以知道是第幾個節點，才方便知道是第幾層的節點 

    treeLevelOrder.append( tree.root ) # 用來作level order的走訪
    drawTreeQueue = []
    drawTreeQueue.append( rootNode )  #存放節點的座標，用以繪圖，節點位置的新增同level order走訪

    '''
        樹的level order走訪
    '''
    while treeLevelOrder != []:
        node = treeLevelOrder.pop(0)
        nodePos = drawTreeQueue.pop(0)
        text( nodePos[0], nodePos[1], node.content, color=node.color, size=20 )
        fX, fY = nodePos[0], nodePos[1] #紀錄本次節點的位置，用在調整它的子節點的位置

        if node.left != tree.nil:
            treeLevelOrder.append( node.left )
            nodeCount += 1
            '''
                左節點的位置微調是考慮到以父親的位置往左微調，微調幅度則是以位於第幾層控制
                math.log( (nodeCount+1), 2 )是用來算第幾層，階層越往下，偏移程度越低
            '''
            fX_shift = fX - scale/math.floor( math.log( (nodeCount+1), 2 ) )
            fY_shift = fY-0.5
            drawTreeQueue.append( ( fX_shift, fY_shift  ) )
            plt.plot( [ fX, fX_shift ], [ fY, fY_shift ], 'k-'  )
        if node.right != tree.nil:
            treeLevelOrder.append( node.right )
            nodeCount += 1
            '''
                右節點的位置微調是考慮到以父親的位置往右微調，微調幅度則是以位於第幾層控制
                math.log( (nodeCount+1), 2 )是用來算第幾層，階層越往下，偏移程度越低
            '''
            fX_shift = fX + scale/math.floor( math.log( (nodeCount+1), 2 ) )
            fY_shift = fY-0.5
            drawTreeQueue.append( ( fX_shift, fY_shift  ) )
            plt.plot( [ fX, fX_shift ], [ fY, fY_shift ], 'k-'  )

    plt.xticks(range(-2,3))
    plt.yticks(range(-2,1))
    plt.show()
    

if __name__ == '__main__':
   tree = rbTree()
   #這個例子似乎違反紅黑樹的不能有重複紅色節點
   #且DFS 順序好像怪怪的
   a = [13,11,8,6,14,4,9,10]
   #a = [13,11,8,6,1,17,15,25,22,27]
   #a = [13,8,17,1,11,15,25,6,22,27]
    # 70-60-65: LRb error?
   #a = [50,10,80,90,70,60]
   #a = [ 50, 10, 80 ]

   for i in a:
       tree.insert(i)
   print '---DFS---'
   print tree
   drawRbTree( tree )
   '''
   print 'left rotate in node 13'
   tree.left_rotate(13)
   print tree
   '''


