# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countNodes(self, root: TreeNode) -> int:
        self.count = 0
        def traverse(node):
            if node:
                # visit node
                self.count +=1 
                traverse(node.left)
                traverse(node.right)
                
        traverse(root)
        return self.count