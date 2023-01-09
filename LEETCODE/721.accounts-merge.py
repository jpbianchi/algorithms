# https://leetcode.com/problems/accounts-merge/
# @lc app=leetcode id=721 lang=python3
#
# [721] Accounts Merge
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (56.35%)	5175	890
# Tags
# depth-first-search | union-find

# Companies
# facebook

# Given a list of accounts where each element accounts[i] is a list of strings, 
# where the first element accounts[i][0] is a name, and the rest of the elements 
# are emails representing emails of the account.

# Now, we would like to merge these accounts. Two accounts definitely belong to 
# the same person if there is some common email to both accounts. Note that even 
# if two accounts have the same name, they may belong to different people as people could 
# have the same name. A person can have any number of accounts initially, but all of their 
# accounts definitely have the same name.

# After merging the accounts, return the accounts in the following format: the 
# first element of each account is the name, and the rest of the elements are 
# emails in sorted order. The accounts themselves can be returned in any order.

 

# Example 1:

# Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
# Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
# Explanation:
# The first and second John's are the same person as they have the common email "johnsmith@mail.com".
# The third John and Mary are different people as none of their email addresses are used by other accounts.
# We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], 
# ['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.
# Example 2:

# Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
# Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
 

# Constraints:

# 1 <= accounts.length <= 1000
# 2 <= accounts[i].length <= 10
# 1 <= accounts[i][j].length <= 30
# accounts[i][0] consists of English letters.
# accounts[i][j] (for j > 0) is a valid email.
from typing import List
# @lc code=start
class Solution:
    def accountsMerge1(self, accounts: List[List[str]]) -> List[List[str]]:
        """ Let's use sets since we can easily find if two sets have one element in common
            Since there can be multiple accounts with the same name, we need to use a 2nd dictionary
            as the value to store the accounts with the same name, but with some Id to differentiate them
        """
        all_accounts = {}
        for account in accounts:
            name = account[0]
            if name not in all_accounts:
                all_accounts[name] = {}                
                all_accounts[name][0] = set(account[1:]) 
                # we store a set already so we don't have to do it over and over if we find a similar name
            else:
                # if an account is already in the dictionary, let's find out if it's the same person
                emails = set(account[1:])
                ids = []
                for id in all_accounts[name]:
                    new_set = all_accounts[name][id]
                    new_emails = all_accounts[name][id] | emails  # let's merge only once
                    if len(new_emails) < len(new_set) + len(emails):  
                        # the two sets have at least one email in common, merge them
                        # but it's possible we can merge with more than one account
                        # so we need to merge all of them
                        emails = new_emails
                        ids.append(id)
                if ids:
                    # let's delete all the accounts we merged and but one to save merged emails
                    for id in ids[1:]:
                        del all_accounts[name][id]
                    all_accounts[name][ids[0]] = emails
                else:
                    # we didn't find a match, so let's add a new account
                    id = max(all_accounts[name])+1
                    all_accounts[name][id] = emails
                    
        # now let's create the output
        ans = []
        for name in [account[0] for account in accounts]: # replace list with all_accounts for leetcode
            for id in all_accounts[name]:
                ans.extend([[name] + sorted(all_accounts[name][id])])
                
        return ans 
                    
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """ There are solutions on Leetcode 10 times faster, I am wasting time
            by testing if an email exists in 2 accounts by merging sets when there
            is a way to do that in O(1) time by using a dictionary
            We could do a 2nd dictionary to reverse encode emails:name just to find duplicates
            or, better, use key (name,email) as a key in a dictionary
            We assume two users can't have the same email address
            I'll use the same dict since it's O(1) anyway
        """
        all_accounts = {}
        ids = []
        for id, (name, *emails) in enumerate(accounts):
            
            duplicates = set()
            for email in emails:
                if (name,email) in all_accounts:
                    duplicates.add(all_accounts[(name,email)])
                # we must go through all emails before we can decide if we have (several) duplicates

            # now let's merge the duplicate accounts
            if duplicates:
                id0 = duplicates.pop()
                # do not add id0 to ids, it's already in it
                all_accounts[id0].extend(emails)
                for idup in duplicates:
                    all_accounts[id0].extend(all_accounts[idup][1:])  
                    # I could improve by eliminating duplicates here, but I want to restrict the use of sets
                    # since it will force to go through every element every time we extend 
                    del all_accounts[idup] 
                    ids.remove(idup)
            else:
                ids.append(id)
                id0 = id
                all_accounts[id] = [name] + emails
                
            # now let's (re)set each (name,email) to the (new) id0
            # since we may have merged several ids, the (name,email) point
            # to the wrong id (in duplicates)
            for email in all_accounts[id0][1:]:
                all_accounts[(name,email)] = id0
                
        # now let's create the output
        return [ [all_accounts[id][0]] + sorted(set(all_accounts[id][1:])) for id in ids]
            
    def accountsMerge99(self, accounts: List[List[str]]) -> List[List[str]]:
        """ Solution from Leetcode that is 6 times faster than mine 
            But it pretty much does the same, except it uses 2 dictionaries ??? 
        """
        
        class Account:
            def __init__(self, name):
                self.name = name
                self.emails = set()
        
        account_objects = {}
        account_objects_by_email = {}
        
        for name, *emails in accounts:
            account = None
            for email in emails:
                if email not in account_objects_by_email:  # looks for existing email
                    continue
                
                if not account:  
                    # if we don't have an account yet, let's use the existing one
                    # now, all emails must point to this account, so let make them do that
                    account = account_objects_by_email[email]
                    
                elif account != account_objects_by_email[email]:
                    # if we have an account, but it's not the same as the existing one, let's merge them
                    account_to_merge = account_objects_by_email[email]
                    
                    for merged_email in account_to_merge.emails:
                        account_objects_by_email[merged_email] = account
                        
                    account.emails.update(account_to_merge.emails)
                    
                    del account_objects_by_email[email]
                    del account_objects[id(account_to_merge)]
                    
            if not account:
                account = Account(name)
                account_objects[id(account)] = account
                
            for email in emails:
                account_objects_by_email[email] = account
                
            account.emails.update(emails)

        return [[account.name] + sorted(account.emails) for account in account_objects.values()]            

# @lc code=end

accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],
            ["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],
            ["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],
            ["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],
            ["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]

ans = [["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],
       ["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],
       ["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],
       ["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],
       ["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]

# print(Solution().accountsMerge1(accounts))
assert Solution().accountsMerge1(accounts) == ans

# print(Solution().accountsMerge(accounts))
assert Solution().accountsMerge(accounts) == ans

accounts.extend([["Gabe","Gabe5@m.co","Gabe7@m.co","Gabe1@m.co"]])
ans[0] = ["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co","Gabe5@m.co","Gabe7@m.co"]

# print(Solution().accountsMerge1(accounts)[:-1])
assert Solution().accountsMerge1(accounts)[:-1] == ans  # to remove the 2nd 'gabe' account

# print(Solution().accountsMerge(accounts))
assert Solution().accountsMerge(accounts) == ans

accounts.extend([["Gabe","gabe@gmail.com"]])
ans.insert(1, ["Gabe","gabe@gmail.com"])

# print(Solution().accountsMerge1(accounts)[:-4])
assert Solution().accountsMerge1(accounts)[:-4] == ans  # each gabe generates 2 outputs now

# print(Solution().accountsMerge(accounts))
ans.pop(1)
ans.extend([["Gabe","gabe@gmail.com"]])  # to account for differences between my 2 implementations
assert Solution().accountsMerge(accounts) == ans

accounts2 = [["David","David0@m.co","David1@m.co"],
             ["David","David3@m.co","David4@m.co"],
             ["David","David4@m.co","David5@m.co"],
             ["David","David2@m.co","David3@m.co"],
             ["David","David1@m.co","David2@m.co"]]

ans2 = [["David","David0@m.co","David1@m.co","David2@m.co","David3@m.co","David4@m.co","David5@m.co"]]

# print(Solution().accountsMerge1(accounts2)[0])
assert Solution().accountsMerge1(accounts2)[0] == ans2[0]

accounts3 = [["Hanzo","Hanzo2@m.co","Hanzo3@m.co"],
             ["Hanzo","Hanzo4@m.co","Hanzo5@m.co"],
             ["Hanzo","Hanzo0@m.co","Hanzo1@m.co"],
             ["Hanzo","Hanzo3@m.co","Hanzo4@m.co"],
             ["Hanzo","Hanzo7@m.co","Hanzo8@m.co"],
             ["Hanzo","Hanzo1@m.co","Hanzo2@m.co"],
             ["Hanzo","Hanzo6@m.co","Hanzo7@m.co"],
             ["Hanzo","Hanzo5@m.co","Hanzo6@m.co"]]

ans3 = [["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo2@m.co","Hanzo3@m.co","Hanzo4@m.co","Hanzo5@m.co","Hanzo6@m.co","Hanzo7@m.co","Hanzo8@m.co"]]


# print(Solution().accountsMerge1(accounts3)[0])
assert Solution().accountsMerge1(accounts3)[0] == ans3[0]

# print(Solution().accountsMerge(accounts3))
assert Solution().accountsMerge(accounts3) == ans3
assert Solution().accountsMerge99(accounts3) == ans3


print("TESTS PASSED")