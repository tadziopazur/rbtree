import rbtree as rb

def orNil(x):
  return x.value if x else "(nil)"

def main():
  rbt = rb.RBTree()

  values = [1, 7, 3, 5, 6, 9, 2, 4, 8, 0, 12, 11, 10, 14, 17, 13, 15, 16, 19, 20, 18]
  rbt.debug = False
#rbt.debug = True
  xin = []
  for v in values:
    print("Insert ", v)
    xin.append(v)
    rbt.insert(v)
    for x in xin:
      node = rbt.find(x)
      if not node:
        raise KeyError(x)
#      else:
#        print(x, "red" if node.red else "black", 'L:', orNil(node.child[0]), 'R:', orNil(node.child[1]))
  rbt.dump()
  rbt.validate()

#  n20 = rbt.find(20)
#  n20.value = 15
#
# rbt.validate()

if __name__ == '__main__':
  main()
