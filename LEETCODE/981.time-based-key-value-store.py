# https://leetcode.com/problems/time-based-key-value-store/
# @lc app=leetcode id=981 lang=python3
#
# [981] Time Based Key-Value Store
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (53.13%)	3748	358
# Tags
# greedy

# Companies
# Unknown

# Design a time-based key-value data structure that can store multiple values 
# for the same key at different time stamps and retrieve the key's value at a certain timestamp.

# Implement the TimeMap class:

# TimeMap() Initializes the object of the data structure.
# void set(String key, String value, int timestamp) Stores the key key with 
# the value value at the given time timestamp.
# String get(String key, int timestamp) Returns a value such that set was 
# called previously, with timestamp_prev <= timestamp. If there are multiple 
# such values, it returns the value associated with the largest timestamp_prev. 
# If there are no values, it returns "".
 

# Example 1:

# Input
# ["TimeMap", "set", "get", "get", "set", "get", "get"]
# [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
# Output
# [null, null, "bar", "bar", null, "bar2", "bar2"]

# Explanation
# TimeMap timeMap = new TimeMap();
# timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
# timeMap.get("foo", 1);         // return "bar"
# timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
# timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
# timeMap.get("foo", 4);         // return "bar2"
# timeMap.get("foo", 5);         // return "bar2"
 

# Constraints:

# 1 <= key.length, value.length <= 100
# key and value consist of lowercase English letters and digits.
# 1 <= timestamp <= 107
# All the timestamps timestamp of set are strictly increasing.
# At most 2 * 105 calls will be made to set and get.
# @lc code=start
from bisect import bisect_right


class TimeMap:
    """ Actually, the value stored doesn't matter since we retrieve
        based solely on the timestamp. So we can just store the timestamp.
        Beats 97% cpu, 65% memory 
    """
    def __init__(self):
        self.schedule = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.schedule.setdefault(key, []).append((timestamp,value))
        
    def get1(self, key: str, timestamp: int) -> str:
        """ The timestamps are always increasing so no need to sort here
            use bisect_right to find the max timestamp in O(log) time
            bisect_right returns the index of the last element <= timestamp
            which is perfect for our use case 
        """
        timestamps_values = self.schedule.get(key, "")
        # here I will compare the tuples (timestamp, value) with (timestamp,~)
        # ~ is the last character in the ascii table so it will always be > any string
        # so if timestamp is in the list, he will be at idx-1
        # and if idx == 0, then for sure all the timestamps are > timestamp
        idx = bisect_right(timestamps_values, (timestamp, "~"))

        if idx == 0:
            # if idx is 0, then all the timestamps are > timestamp
            # so there is no value for this timestamp
            return ""
        
        return timestamps_values[idx-1][1]
    
    def get(self, key: str, timestamp: int) -> str:
        """ To speed things up, let's test if timestamp id < the first timestamp
            or > the last timestamp, to avoid bisect_right
            Improved by 30ms (well, Leetcode is not very reliable, but 
            it has to be faster anyway)
        """
        timestamps_values = self.schedule.get(key, "")
        if not timestamps_values or timestamp < timestamps_values[0][0]:
            return ""
        if timestamp >= timestamps_values[-1][0]:
            return timestamps_values[-1][1]

        
        # here I will compare the tuples (timestamp, value) with (timestamp,~)
        # ~ is the last character in the ascii table so it will always be > any string
        # so if timestamp is in the list, he will be at idx-1
        # and if idx == 0, then for sure all the timestamps are > timestamp
        idx = bisect_right(timestamps_values, (timestamp, "~"))
        
        return timestamps_values[idx-1][1]
        
class TimeMap2:
    """ This is from Leetcode: 617ms instead of my 677ms """
    def __init__(self):
        self.dict = collections.defaultdict(dict)
        self.time_list = collections.defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.dict[key][timestamp] = value
        self.time_list[key].append(timestamp)

    def get(self, key: str, timestamp: int) -> str:
        index = 0
        if key not in self.dict:
            return ""
        if timestamp > self.time_list[key][-1]:
            return self.dict[key][self.time_list[key][-1]]
        elif timestamp < self.time_list[key][0]:
            return ""
        elif timestamp in self.dict[key]:
            return self.dict[key][timestamp]
        else:
            while index < len(self.time_list[key]):
                if self.time_list[key][index + 1] > timestamp:
                    return self.dict[key][self.time_list[key][index]]
                index += 1


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
# @lc code=end


def test_timemap(instructions, data):
    tm = TimeMap()
    ans = []
    for ins, d in zip(instructions[1:], data[1:]):
        if ins == "set":
            tm.set(d[0], d[1], d[2])
            ans.append(None)
        elif ins == "get":
            ans.append(tm.get(d[0], d[1]))
    return ans

instructions = ["TimeMap","set","get","get","set","get","get"]
data = [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]

# print(test_timemap(instructions, data))
assert test_timemap(instructions, data) == [None,"bar", "bar", None, "bar2", "bar2"]

instructions = ["TimeMap","set","set","get","get","get","get","get"]
data = [[],["love","high",10],["love","low",20],["love",5],["love",10],["love",15],["love",20],["love",25]]

# print(test_timemap(instructions, data))
assert test_timemap(instructions, data) == [None,None,"","high","high","low","low"]

instructions = ["TimeMap","set","set","get","set","get","get"]
data = [[],["a","bar",1],["x","b",3],["b",3],["foo","bar2",4],["foo",4],["foo",5]]
# print(test_timemap(instructions, data))
test_timemap(instructions, data) == [None, None, '', None, 'bar2', 'bar2']

print("TESTS PASSED")