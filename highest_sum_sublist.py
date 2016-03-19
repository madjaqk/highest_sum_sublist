from time import time

start = time()

"""
Problem: Find the highest-value consecutive sublist in a list that could
contain positive and/or negative elements

My idea: First, pool together all adjacent positive and negative values (so
[1,2,-3,-4,5] would become [3,-7,5]).  Then, for each negative value, check if
its absolute value is less than the minimum of its two neighbors, or,
equivalently, if the sum of the negative and adjacent positives is greater than
either positive on its own; if this is the case, pool all three together, and
keep iterating through the list until you can pool no longer.

Time complexity: The first while loop is clearly O(n) time.  I suspect the
second while loop is at most O(n log n), as each merger removes two elements
from the list, but I'm not positive.
"""

def sign(num):
    return int(num >= 0)
    # It's weird that Python doesn't have a sign function, right?  This kludge
    # is based on doing math on boolean vaules

def highest_sum_subseries(arr):
    # Build a dictionary where "start" and "end" represent indices into arr and
    # val the total of elements in that range (sum(arr[start:end])
    condensed = [{"val": val,
                 "start": index,
                 "end": index+1}
                 for index, val in enumerate(arr)]

    # Combine all adjacent positives or negatives
    i = 1
    while i < len(condensed):
        if sign(condensed[i]["val"]) == sign(condensed[i-1]["val"]):
            condensed[i-1]["val"] += condensed[i]["val"]
            condensed[i-1]["end"] = condensed[i]["end"]
            condensed.pop(i)
        else:
            i += 1

    # Look for cases three consecutive elements can be combined
    keepgoing = True
    while keepgoing:
        keepgoing = False
        j = 1
        while j < len(condensed) - 1:
            if abs(condensed[j]["val"]) < min(condensed[j-1]["val"], condensed[j+1]["val"]):
                condensed[j-1]["val"] += condensed[j]["val"] + condensed[j+1]["val"]
                condensed[j-1]["end"] = condensed[j+1]["end"]
                condensed.pop(j+1)
                condensed.pop(j)
                keepgoing = True
            else:
                j += 1

    # I suspect the two while loops could be combined, but everything broke the
    # first time I tried it, so I rolled back to the version I know works.
    final_range = max(condensed, key=lambda x: x["val"])

    return arr[final_range["start"]:final_range["end"]]


tests = [
    [[-7,-1,3,2,9,-6], [3,2,9]],
    [[7,-1,3,2,9,-6], [7,-1,3,2,9]],
    [[2,1], [2,1]],
    [[1,1,1,1,1,1,-20,5,-20], [1,1,1,1,1,1]]
    ]

# TDD (kind of)
for test in tests:
    assert highest_sum_subseries(test[0]) == test[1], "Failed {}".format(test[0])
    #print(highest_sum_subseries(test[0]))

print("All done")
print(time() - start)



