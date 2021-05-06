# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return True
        return self.recurse(root.left, root.right)
        
    def recurse(self, left, right):
        if left is None and right is None:
            return True

        if left is None or right is None:
            return False
        if left.val != right.val:
            return False
        return (self.recurse(left.right, right.left) and self.recurse(left.left, right.right))
     