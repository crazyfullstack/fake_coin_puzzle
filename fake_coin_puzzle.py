import random
from typing import List

def get_n() -> int:
    """Prompt the user to enter the number of coins."""
    while True:
        try:
            n = int(input("Enter the number of coins (must be greater than 2): "))
            if n > 2:
                return n
            else:
                print("Please enter a number greater than 2.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_fake_no(n) -> int:
    while True:
        try:
            fake_no = int(input(f"Enter the number of the counterfeit coin (0 to {n-1}): "))
            if 0 <= fake_no <= n-1:
                return fake_no
            else:
                print(f"Please enter a number between 1 and {n}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            
def get_fake_weight():
    while True:
        try:
            fake_weight = int(input("Enter 0 if the fake coin is lighter and 1 if it is heavier: "))
            if fake_weight not in [0, 1]:
                print("Invalid input. Please enter 0 or 1.")
            else:
                return fake_weight
        except ValueError:
            print("Invalid input. Please enter an integer.")

def makeRandomCoins(n: int, fake_no: int, fake_weight: int) -> List[int]:
    print(f"Generating {n} coins with {'heavier' if fake_weight == 1 else 'lighter'} fake coin in position of {fake_no}")
    randomCoins = [2*fake_weight if i == fake_no else 1 for i in range(n)]
    return randomCoins

def weigh(coinWeights: List[int], group1: List[int], group2: List[int]) -> int:
    weight_left = sum([coinWeights[i] for i in group1])
    weight_right = sum([coinWeights[i] for i in group2])
    if weight_left > weight_right:
        print("The left group is heavier.")
        return 1
    elif weight_left == weight_right:
        print("Both groups are equal in weight.")
        return 0
    else:
        print("The left group is lighter.")
        return -1

def chooseNextStrategy(status: List[List[int]], m: int) -> str:
    if m == 1:
        return "init"
    elif status[0] == []:
        return "first"
    else:
        return "second"

def divideInGroups(status: List[List[int]], strategy: str) -> List[List[int]]:
    if strategy == "init":
        u = len(status[0])
        left = u // 3
        right = left
        group_left = status[0][:left]
        group_right = status[0][left:left + right]
        group_rest = status[0][left + right:]
        return [group_left, group_right, group_rest]
    
    if strategy == "first":
        h = len(status[1])
        l = len(status[2])
        heavy = (h + l) // 3
        light = (h + l + 1) // 3
        rest = (h + l + 2) // 3
        left_h = h // 3
        right_h = (h + 1) // 3
        rest_h = (h + 2) // 3
        left_l = heavy - right_h
        right_l = light - left_h
        rest_l = rest - rest_h
        
        group_left = status[1][:left_h] + status[2][:left_l]
        group_right = status[1][left_h:left_h + right_h] + status[2][left_l:left_l + right_l]
        group_rest = status[1][left_h + right_h:] + status[2][left_l + right_l:]

        if len(group_left) > len(group_right):
            group_right = group_right + status[3][:len(group_left) - len(group_right)]
        else:
            group_left = group_left + status[3][:len(group_right) - len(group_left)]
        
        return [group_left, group_right, group_rest]
    
    if strategy == "second":
        u = len(status[0])
        left = (u) // 3
        right = (u + 1) // 3
        rest = (u + 2) // 3
        less = right - left
        group_left = status[0][:left] + status[3][:less]
        group_right = status[0][left:left + right]
        group_rest = status[0][left + right:]
        return [group_left, group_right, group_rest]

def getNextStatus(coinWeights: List[int], status: List[List[int]], group_left: List[int], group_right: List[int], group_rest: List[int]) -> List[List[int]]:
    scale_result = weigh(coinWeights, group_left, group_right)
    n = len(coinWeights)
    nextStatus = [[], [], [], []]
    
    if scale_result == 1:
        nextStatus[0] = []
        nextStatus[1] = [i for i in group_left if i in status[0] or i in status[1]]
        nextStatus[2] = [i for i in group_right if i in status[0] or i in status[2]]
        nextStatus[3] = [i for i in range(n) if i not in nextStatus[1] and i not in nextStatus[2]]
        
    if scale_result == 0:
        nextStatus[0] = [i for i in group_rest if i in status[0]]
        nextStatus[1] = [i for i in group_rest if i in status[1]]
        nextStatus[2] = [i for i in group_rest if i in status[2]]
        nextStatus[3] = [i for i in range(n) if i not in nextStatus[0] and i not in nextStatus[1] and i not in nextStatus[2]]
        
    if scale_result == -1:
        nextStatus[0] = []
        nextStatus[1] = [i for i in group_right if i in status[0] or i in status[1]]
        nextStatus[2] = [i for i in group_left if i in status[0] or i in status[2]]
        nextStatus[3] = [i for i in range(n) if i not in nextStatus[1] and i not in nextStatus[2]]
    
    return nextStatus

def printStatus(status: List[List[int]]) -> None:
    print("\nCurrent progress:")
    print("Coins that could be fake (unknown if heavier or lighter):", status[0])
    print("Coins that could be fake (heavier if fake):", status[1])
    print("Coins that could be fake (lighter if fake):", status[2])
    print("Coins that are normal:", status[3])

n = get_n()  # Get the number of coins from the user
fake_no = get_fake_no(n) # Get the number of the fake coin from user
fake_weight = get_fake_weight()
coinWeights = makeRandomCoins(n, fake_no, fake_weight)
status = [[i for i in range(n)], [], [], []]
print("This is the list of coin weights:")
print(coinWeights)
printStatus(status)

m = 0

while len(status[0]) + len(status[1]) + len(status[2]) > 1:
    m += 1
    print(f"\nStep {m} ------------------------------------------")
    strategy = chooseNextStrategy(status, m)
    group_left, group_right, group_rest = divideInGroups(status, strategy)
    print(f"Comparing groups: Left group size = {len(group_left)}, Right group size = {len(group_right)}")
    print(f"Group Left: {group_left}")
    print(f"Group Right: {group_right}")
    status = getNextStatus(coinWeights, status, group_left, group_right, group_rest)
    printStatus(status)

found_no = (status[0] + status[1] + status[2])[0]

print(f"\nThe fake coin has been identified from {n} coins after {m} weighings.")
print(f"The fake coin is located at position: {found_no}.")