# test script for a bifurcation algorithm

# class Bifurcator():
#     def __init__(self, arr: [str]):
#         self.arr = arr # arr will house the characters
#
#     def bifurcate(self):

def birfucate(arr):
    split = int(len(arr) / 2)
    return (arr[0:split], arr[split:])

arr = ['a', 'b', 'c', 'd','e','f']

one_level = birfucate(arr)
print(one_level)
second_level = birfucate(one_level[0])
print(second_level)
third_level = birfucate(second_level[0])
print(third_level)