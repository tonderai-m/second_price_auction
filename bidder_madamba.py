""""This is my bidder fuction"""
import random
import itertools
import numpy as np
class Bidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    id_iter = itertools.count()
    def __init__(self, num_users, num_rounds):
        '''Setting initial balance to 0, number of users, number of rounds, and round counter'''
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.round_counter = 0
        self.balance = 0
        self.history = {}
        self.arr_scoreboard = {}
        self.scores = {}

    def __repr__(self):
        '''Return Bidder object with balance'''
        return str(self.balance)

    def __str__(self):
        '''Return Bidder object with balance'''
        return str(self.balance)
    def average_bid(self):
        """Return Average Bid"""
        return  np.mean(self.arr_scoreboard[self.user_id][:,2])
    def std_bid(self):
        """Return std"""
        return  np.std(self.arr_scoreboard[self.user_id][:,2])
    def last_7_bid_mean(self):
        """Return last 7 Bid"""
        return np.mean(self.arr_scoreboard[self.user_id][:,2][-20:])
    def last_7_bid_std(self):
        """Return last 7 Bid"""
        return  np.std(self.arr_scoreboard[self.user_id][:,2][-20:])
    def count_bid(self):
        """Return Count Bid"""
        return np.sum(self.arr_scoreboard[self.user_id][:,1])
    def count_click(self):
        """Return Count Clicked"""
        return sum([ i for i in self.arr_scoreboard[self.user_id][:,3] if i is not None])
    def winning_percentage(self):
        """Return winning percentage"""
        try:
            ratio = self.count_click() / self.count_bid()
        except :
            ratio = 0
        return ratio

    def bid(self, user_id):
        '''Returns a non-negative bid amount''' 
        self.current_round = next(self.id_iter)
        self.user_id = user_id
        if self.user_id not in self.scores:
            bid = random.uniform(0, 1)
        else:
            a = np.random.uniform(0,0.0005)
            if self.scores[self.user_id][1] < 5:
                bid = min(1 + self.scores[self.user_id][-1],
                          self.scores[self.user_id][0][0] + self.scores[self.user_id][0][1])
            elif self.scores[self.user_id][1] < 20 and self.scores[self.user_id][-1] > 0.55:
                bid = min(self.scores[self.user_id][0][0] + self.scores[self.user_id][-1],
                          1 + self.scores[self.user_id][-1],
                          self.scores[self.user_id][0][0] + self.scores[self.user_id][0][1])
            elif self.scores[self.user_id][1] < 20 and self.scores[self.user_id][-1] < 0.55:
                bid = min(self.scores[self.user_id][0][0] + self.scores[self.user_id][-1],
                          self.scores[self.user_id][-1],
                          self.scores[self.user_id][0][0] + self.scores[self.user_id][0][1])
            elif  self.scores[self.user_id][1] < 20 and self.scores[self.user_id][-1] > 0.55:
                bid = min(1 + self.scores[self.user_id][-1],
                          self.scores[self.user_id][-2][0] + self.scores[self.user_id][-1] - a,
                          1 + self.scores[self.user_id][-1],
                          self.scores[self.user_id][-2][0] + self.scores[self.user_id][-2][1])
            else:
                bid = min(1 + self.scores[self.user_id][-1], self.scores[self.user_id][-1] - a,
                          1 + self.scores[self.user_id][-1],
                          self.scores[self.user_id][-2][0] + self.scores[self.user_id][-2][1])
        self.my_bid = bid
        return bid
    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        if auction_winner:
            if clicked:
                self.balance -= self.my_bid - price - 1
            self.balance -= self.my_bid - price

        if self.user_id in self.history:
            self.history[self.user_id] += [[self.my_bid, auction_winner,
                                            price,clicked,self.current_round]]
        else:
            self.history[self.user_id] = [[self.my_bid, auction_winner,price,
                                           clicked,self.current_round]]
        self.arr_scoreboard[self.user_id] = np.array(self.history[self.user_id])
        self.scores[self.user_id] = [(self.average_bid(),self.std_bid()),
                                     self.count_bid(),
                                     self.count_click(),
                                     (self.last_7_bid_mean(),self.std_bid()),
                                     self.winning_percentage()]