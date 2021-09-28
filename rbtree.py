#!/bin/python

import math

class RBTree:
  class Node:
    def __init__(self, value, parent=None, left=None, right=None):
      self.parent = parent
      self.value = value
      self.red = True
      self.child = [left, right]

    def dump(self):
      if self:
        print("N(", self.value, " red" if self.red else " black", " <",
              self.child[0].value if self.child[0] else "nil", ", ",
              self.child[1].value if self.child[1] else "nil", ">)", sep='')
      else:
        print("(nil)")

  def __init__(self, root=None):
    self.root = root

  def insert(self, value):
    if not self.root:
      self.root = self.Node(value)
      self.root.red = False
      return

    node, parent = self.doFind(value, self.root, None)
    while node:
      node, parent = self.doFind(value, node, parent)

    childNo = 0 if parent.value > value else 1
    node = self.Node(value, parent)
    parent.child[childNo] = node
    self.fixInsert(node)

  def addChild(self, parent, childNo, node):
    if self.debug:
      print("Add", parent.value, "L" if childNo == 0 else "R", node.value if node else "nil")
    parent.child[childNo] = node
    if node:
      node.parent = parent

  def upRotate(self, node, rotDir):
    if self.debug:
      print("ROT", "LEFT" if rotDir == 0 else "RIGHT")
      node.dump()
      node.parent.dump()

    # rotate(node.parent, rotDir)

    oldparent = node.parent
    grandpa = oldparent.parent
    self.addChild(oldparent, 1-rotDir, node.child[rotDir])
    self.addChild(node, rotDir, oldparent)
    if not grandpa:
      node.parent = None
      self.root = node
    else:
      childNo = 0 if grandpa.child[0] == oldparent else 1
      self.addChild(grandpa, childNo, node)

  def rotate(dself, oldparent, rotDir):
    granpa = oldparent.parent
    newparent = oldparet.child[1-rotDir]

    self.addChild(oldparent, 1-rotDir, newparent.child[rotDir])
    self.addChild(newparent, rotDir, oldparent)
    if not grandpa:
      newparent.parent = None
      self.root = newparent
    else:
      childNo = 0 if grandpa.child[0] == oldparent else 1
      self.addChild(grandpa, childNo, newparent)

  def rotateLeft(self, node):
    self.upRotate(node, 0)

  def rotateRight(self, node):
    self.upRotate(node, 1)

  def sibling(self, node):
    childNo = 0 if node.parent.child[0] == node else 1
    return node.parent.child[1-childNo]

  def fixInsert(self, node):
    # node.red == True
    while node != self.root and node.parent.red == True:
      parent = node.parent
      if self.debug:
        print("F", node.value, "R" if node.red else "B", ", P", parent.value, "R" if parent.red else "B") 
      grandChildNo = 0 if parent.parent.child[0] == parent else 1
      uncle = parent.parent.child[1-grandChildNo]
      if uncle and uncle.red:
        if self.debug:
          print("R1")
          node.dump()
          parent.dump()
          uncle.dump()
        uncle.red = False
        parent.red = False
        node = parent.parent
        node.red = True
      else:
        childNo = 0 if node == parent.child[0] else 1
        if childNo != grandChildNo:
          if self.debug:
            print("R2", "left" if childNo == 1 else "right", node.value, parent.value)
          self.upRotate(node, 1-childNo)
          parent = node
          node = node.child[1-childNo]

        if self.debug:
          print("R3", "left" if grandChildNo == 1 else "right", node.value, parent.value)

        node = parent
        parent = parent.parent

        node.red = False
        parent.red = True
        self.upRotate(node, 1-grandChildNo)
    self.root.red = False

  def remove(self, value):
    node, parent = self.doFind(value, self.root, None)
    if not node:
      raise KeyError(value)
    self.deleteNode(node)

  def swapNodeValues(self, node1, node2):
    tmp = node1.value
    node1.value = node2.value
    node2.value = tmp

  def successor(self, node):
    parent = node
    while node:
      parent = node
      node = node.child[0]
    return parent

  def findReplacement(self, node):
    left = node.child[0] 
    rigtht = node.child[1]

    if left and right:
      return successor(node)

    return left if left else right

  def deleteNode(self, node):
    replacement = self.findReplacement(node)
    bothBlack = not node.red and (not replacement or not replacement.red)
    if not replacement:
      if node == self.root:
        self.root = None
      else:
        if bothBlack:
          self.propagateBlack(node)
        else:
          sibling = self.sibling(node)
          if sibling:
            sibling.red = True

      childNo = 0 if node == parent.child[0] else 1
      node.parent.child[childNo] = None
      return

    else:
      if not node.child[0] or not node.child[1]:
        if node == self.root:
          replacement.parent = None
          replacement.red = True
          self.root = replacement
        else:
          parent = node.parent
          childNo = 0 if node == parent.child[0] else 1
          parent.child[childNo] = replacement
          replacement.parent = parent
          if bothBlack:
            self.propagateBlack(replacement)
          else:
            replacement.red = False
        return

      else:
        self.swapNodeValues(node, replacement)
        self.remove(replacement)

  def isRed(self, node):
    return node and node.red

  def propagateBlack(self, node):
    if self.root == node:
      return
    parent = node.parent
    childNo = 0 if parent.child[0]  == node else 1
    sibling = parent[1-childNo]

    if not sibling:
      propagateBlack(parent)
    elif sibling.red:
      parent.red = True
      sibling.red = False
      self.upRotate(node, 1-childNo)
      propagateBlack(node)
    else:
      closeNephewRed = isRed(sibling.child[childNo])
      distantNephewRed = isRed(sibling.child[1-childNo])
      if closeNephewRed or distantNephewRed:
        if closeNephewRed:
          sibling.red = True
          sibling.child[childNo].red = False
          self.rotate(sibling, childNo)
          self.propagateBlack(node)
        else:
          sibling.red = parent.red
          parent.red = False
          sibling.child[1-childNo].red = True
          self.rotate(parent, childNo)
      else:
        sibling.red = True
        if parent.red:
          parent.red = False
        else:
          propagateBlack(parent)

  def doFind(self, value, node=None, parent=None):
    if not node or node.value == value:
      return (node, parent)
    if node.value < value:
      return self.doFind(value, node.child[1], node)
    if node.value > value:
      return self.doFind(value, node.child[0], node)

  def find(self, value):
    return self.doFind(value, self.root, None)[0]

  def doDump(self, node):
    if node:
      node.dump()
      if node.child[0]:
        self.doDump(node.child[0])
      if node.child[1]:
        self.doDump(node.child[1])

  def dump(self):
    if self.root:
      self.doDump(self.root)
      print()
    else:
      print("Empty tree")

  def doValidate(self, node, parentRed, lowerBound, upperBound):
    if node:
      if node.red and parentRed:
        raise Exception('Double red')
      if node.value < lowerBound:
        raise Exception('BST order violated ({} < {})'.format(node.value, lowerBound))
      if node.value > upperBound:
        raise Exception('BST order violated ({} > {})'.format(node.value, upperBound))
      
      depthL = self.doValidate(node.child[0], node.red, lowerBound, node.value)
      depthR = self.doValidate(node.child[1], node.red, node.value, upperBound)
      if depthL != depthR:
        raise Exception('Black depth imbalance at node {}: L {}, R {}'.format(node.value, depthL, depthR))
      return depthL + (0 if node.red else 1)
    else:
      return 1

  def validate(self):
    if self.root:
      self.doValidate(self.root, False, -math.inf, math.inf)

