# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        """Purpose: Iteratively merges two linked lists l1, l2.
        """
        dummy_head = ListNode(-1)
        prev = dummy_head
        while l1 and l2:
            if l1.val <=  l2.val:
                prev.next = l1
                l1 = l1.next
            else:
                prev.next = l2
                l2 = l2.next
            prev = prev.next
            
        if l1 is None:
            prev.next = l2
        else:
            prev.next = l1
        return dummy_head.next