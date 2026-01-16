"""
LC 0001 Two Sum
Tags: hash, array
Key:
- one-pass hash map
Pitfalls:
- check before store
Complexity: O(n) time, O(n) space
"""

from typing import List

class Solution:
    def twoSum(self,nums:List[int],target:int) -> List[int]:
        num_map = {}
        for i, num in enumerate(nums):
            y = target - num
            if y in num_map:
                return [num_map[y],i]
            num_map[num] = i
        return []

    def twoSum2(self,nums:List[int],target:int) -> List[int]:
        hashtable = dict()
        for i,num in enumerate(nums):
          if target - num in hashtable:
            return [hashtable[target-num],i]
          hashtable[num] = i
        return []


        
