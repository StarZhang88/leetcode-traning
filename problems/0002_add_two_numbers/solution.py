"""
LC 0002 Add Two Numbers
Difficulty: medium
Tags: linked-list, math

Key:
- (write 1-2 key observations)

Pitfalls:
- (edge cases / common mistakes)

Complexity: O(?) time, O(?) space
"""

from typing import List, Optional, Tuple, Dict

class ListNode:
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

  

class Solution:
    def addTwoNumbers(self,l1:Optional[ListNode],l2:Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        curr = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            total = val1 + val2 + carry
            carry = total // 10
            curr.next = ListNode(total % 10)
            curr = curr.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next


if __name__ == "__main__":
    l1 = ListNode(2,ListNode(4,ListNode(3)))
    l2 = ListNode(5,ListNode(6,ListNode(4)))
    solution = Solution()
    result = solution.addTwoNumbers(l1,l2)
    while result:
        print(result.val,end=" ")
        result = result.next
    print() 
