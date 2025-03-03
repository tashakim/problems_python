from heapq import heapq

class Solution:

    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Purpose: Returns the min. no. of conference rooms required, given an array 
        of meeting time  `intervals` where intervals[i] = [start_i, end_i].
        
        """
        if not intervals: return 0
        free_rooms = []

        intervals.sort(key= lambda x: x[0])
        heapq.heappush(free_rooms, intervals[0][1])

        for interval in intervals[1:]:
            if free_rooms[0] <= interval[0]:
                heapq.heappop(free_rooms)

            heapq.heappush(free_rooms, interval[1])

        return len(free_rooms)