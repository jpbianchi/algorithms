#%% https://codinginterviewsmadesimple.substack.com/p/solutionproblem-69-generate-random
# Problem 69: Generate Random Numbers According to Probability

from random import random
from bisect import bisect_left
from matplotlib import pyplot as plt
#%% 
def preprocess(probs):
    lst = []

    current_val = 0
    for p in probs:
        current_val += p
        lst.append(current_val)

    return lst

def distribute(nums, arr):
    r = random()
    i = bisect_left(arr, r)
    return nums[i]

def solution_Devansh(nums, arr):
    times=int(input("Enter number of random numbers generated"))
    lst=preprocess(arr)
    ma={}
    for _ in range(times):
       rand=distribute(nums,lst)
       if rand not in ma:
           ma[rand]=1
       else:
            ma[rand]+=1
    #   print(rand)
    print(ma)

#%% see my article about another solution
# https://aiandbrains.substack.com/p/how-to-modify-a-probability-distribution
def solution(nums, probs, k=100000):
    """ I think we can improve by using a dictionary instead of a binary tree
        We create a dict rnd_smpl where each num is present as a value n times,
        n being its probability * 10
        PS: if the probabilities have two decimals, we would have to create a dict
            with 100 keys
    """
    all_nums = []
    # let's first create [1,2,3,3,3,4,5,5,5]
    for n,p in zip(nums, probs):
        all_nums += [n]*int(p*10)
            
    rnd_smpl = dict(enumerate(all_nums))        # our sampling dictionary
    
    sampling = dict(zip(nums,[0]*len(nums)))    # {1:0, 2:0, etc}
    
    for _ in range(k):
        sample = rnd_smpl[int(random()*10)]
        sampling[sample] += 1

    print(sampling)

solution([1,2,3,4,5],[0.1,0.2,0.3,0.1,0.3])
# {1: 9906, 2: 20063, 3: 30151, 4: 9916, 5: 29964}
#%% To generate the plots in the substack article

#%%
# PDF wanted
values = [1, 2, 3, 4, 5]
probabilities = [0.1, 0.2, 0.3, 0.1, 0.3]

plt.bar(values, probabilities, width=[0.9,0.9,0.9,0.9,0.9])
plt.xlabel('Fig 1 - Values')
plt.ylabel('Probabilities')

plt.show()

#%%
# Uniform PDF with buckets of varying widths
values = [0.5,2,4.5,6.5,8.5]
probabilities = [0.1, 0.1, 0.1, 0.1, 0.1]
buck_x = [0, 1, 2, 3, 4, 5,6,7,8,9, 10]
buckets = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

bars = plt.bar(values, probabilities, width=[0.95,1.95,2.95,0.95,2.95])
for bar, n in zip(bars,[1,2,3,4,5]):
    h = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, h*0.7, f'{n:.0f}', ha='center', va='bottom')
    
plt.xlabel('Fig 2  -  random.random() output')
# plt.ylabel('Probabilities')
plt.xticks(buck_x, buckets)
plt.yticks([],[])
plt.title("Bucket numbers")

plt.show()
#%%
# Uniform PDF with buckets of similar widths
values = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
probabilities = [0.1]*10
buck_x = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
buckets = [0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

bars = plt.bar(values, probabilities, width=[0.9]*10)
for bar, n in zip(bars,[1,2,2,3,3,3,4,5,5,5]):
    h = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, h * 0.7, f'{n:.0f}', ha='center', va='bottom')

plt.xlabel('Fig 3  -  random.random() output (1 decimal)')
# plt.ylabel('Probabilities')
plt.xticks(buck_x, buckets)
plt.yticks([],[])
plt.title("Bucket numbers")

plt.show()

