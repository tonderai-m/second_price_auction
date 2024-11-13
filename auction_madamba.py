"""This is my first project done by Tonderai"""
import itertools
import random
import numpy as np

class User:
    '''Class to represent a user with a secret probability of clicking an ad.'''
    def __init__(self):
        '''Generating a probability between 0 and 1 from a uniform distribution'''
        self.__probability = random.uniform(0,1)

    def __repr__(self):
        '''User object with secret probability'''
        return str(self.__probability)

    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return str(self.__probability)

    def show_ad(self):
        '''Returns True to represent the user clicking on an ad or False otherwise'''
        return np.random.choice([True,False],p=[self.__probability, 1-self.__probability])
class Auction:
    '''Class to represent an online second-price ad auction'''
    round_iter = itertools.count()
    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary to store 
            balances for each bidder in the auction'''
        self.users = users
        self.bidders = bidders
        self.balances = {i:0 for i in self.bidders }
        self.round_history = []

    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return str([self.users, self.bidders])

    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return str([self.users, self.bidders])

    def execute_round(self):
        '''Executes a single round of an auction, completing the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - showing ad to user and finding out whether or not they click
            - notifying winning bidder of price and user outcome and updating balance
            - notifying losing bidders of price'''
        self.num_round = next(self.round_iter)
        user_id = random.choice(range(len(self.users)))
        bids = [(i.bid(user_id),i) for i in self.bidders if self.balances[i] > -1000]
        if len(bids) > 1:
            max_value = max(bids, key=lambda x : x[0])
            winning_bidder = random.choice([i for i in bids if max_value[1] == i[1]])
        else: winning_bidder = bids

        if len(bids) > 1:
            losing_bidders = [i for i in bids if i != winning_bidder]
            second_highest = max([i for i in bids if i != winning_bidder],key=lambda x : x[0])
            print(second_highest)
        else: second_highest = bids
        clicked = self.users[user_id].show_ad()
        if  len(bids) > 1:
            winning_bidder[1].notify(True, second_highest[0], clicked)
            b = 0
            if clicked:
                b = 1
                self.balances[winning_bidder[1]] -= second_highest[0] - b
            else:
                self.balances[winning_bidder[1]] -= second_highest[0] + b
            # Trigger multiple notification for losing bidders
            for i in losing_bidders:
                i[1].notify(False, second_highest[0], None)
        else:
            b = 0
            if clicked:
                b = 1
                self.balances[winning_bidder[0][1]] -= second_highest[0][0] - b
            else:
                self.balances[winning_bidder[0][1]] -= second_highest[0][0] + b
            winning_bidder[0][1].notify(True, second_highest[0][0], clicked)
