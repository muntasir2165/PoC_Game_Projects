"""
ClickerState() class "test suite"
"""

"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        #pass
        self.total_cookies = 0.0
        self.current_cookies = 0.0
        self.current_time = 0.0
        self.current_cps = 1.0
        self.current_item = None
        self.cost_item = 0.0
        #history = [(0.0, None, 0.0, 0.0)]
        self.history = [(self.current_time, self.current_item,
                         self.cost_item, self.total_cookies)]
        
    def __str__(self):
        """
        Return human readable state
        """
        #state = "Time: " + str(self.get_time()) + "; item bought: " + str(self.current_item) + "; item cost: " + str(self.cost_item) + "; total cookies: " + str(self.total_cookies)
        #print type(state)
        state = "Time: " + str(self.get_time()) + "\nCurrent Cookies: " + str(self.get_cookies()) + "\nCurrent CPS: " + str(self.get_cps()) + "\nTotal Cookies: " + str(self.total_cookies) + "\n"
        return state
                
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self.history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        #time_required = 0.0
        time_required = cookies/self.get_cps()
        return math.ceil(time_required)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        #pass
        if time <= 0:
            pass
        else:
            self.current_time = self.get_time() + time
            self.current_cookies = time * self.get_cps()
            self.total_cookies += self.get_cookies()
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        #pass
        if self.get_cookies() < cost:
            pass
        else:
            self.current_cookies -= cost
            self.current_cps = self.get_cps() + additional_cps
            self.current_item = item_name
            self.item_cost = cost
            self.history.append((self.get_time(), self.current_item, 
                                 self.item_cost, self.total_cookies))
            
#testing the ClickerState() class            
x = ClickerState()
print x
print x.get_cookies()
print x.get_cps()
print x.get_time()
print x.get_history()
print x.time_until(100)
print
x.wait(10)
print x.get_cookies()
print x.get_cps()
print x.get_time()
print x.get_history()
print
x.buy_item("grandma", 5, 1)
print x.get_cookies()
print x.get_cps()
print x.get_time()
print x.get_history()
print x

