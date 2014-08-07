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
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._current_item = None
        self._cost_item = 0.0
        self._history = [(self._current_time, self._current_item,
                         self._cost_item, self._total_cookies)]
        
    def __str__(self):
        """
        Return human readable state
        """
        state = "Time: " + str(self.get_time()) + "\nCurrent Cookies: " + str(self.get_cookies()) + "\nCurrent CPS: " + str(self.get_cps()) + "\nTotal Cookies: " + str(self._total_cookies) + "\n"
        return state
                       
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        difference = (cookies-self.get_cookies())
        if difference < 0:
            return 0.0
        else:
            time_required = (cookies-self.get_cookies())/self.get_cps()
            return math.ceil(time_required)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            pass
        else:
            self._current_time = self.get_time() + time
            cookies_generated = time * self.get_cps()
            self._current_cookies += cookies_generated
            self._total_cookies += cookies_generated
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        #pass
        if self.get_cookies() < cost:
            pass
        else:
            self._current_cookies -= cost
            self._current_cps = self.get_cps() + additional_cps
            self._current_item = item_name
            self._cost_item = cost
            self._history.append((self.get_time(), self._current_item, 
                                 self._cost_item, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    copy = build_info.clone()
    clickerstate_object = ClickerState()
    present_time = 0.0
    while True:
        if present_time > duration:
            break
        else:
            item = strategy(clickerstate_object.get_cookies(),
                                   clickerstate_object.get_cps(),
                                   duration - present_time, copy)
            if item == None:
                break
            else:
                cookies_needed = copy.get_cost(item)
                item_cps = copy.get_cps(item)
                time_needed = clickerstate_object.time_until(cookies_needed)
                if (present_time + time_needed) > duration:
                    break
                else:
                    clickerstate_object.wait(time_needed)
                    present_time += time_needed
                    clickerstate_object.buy_item(item, cookies_needed,
                                                item_cps)
                    copy.update_item(item)
    
    # Further, after you have exited the loop, if there is
    #time left, you should allow cookies to accumulate for
    #the remainder of the time left. 
    if present_time < duration:
        time_remaining = duration - present_time
        clickerstate_object.wait(time_remaining)
        present_time += time_remaining
                                               
    # Replace with your code
    return clickerstate_object


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Identify and return the item that would be the cheapest option
    to buy given the parameters: cookies, cps, and time_left. 
    
    If there is no cheap option, return None.
    """
    total_cookies = cookies + (cps * time_left)
    minval = total_cookies
    item_name = None
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost <= minval:
            minval = item_cost
            item_name = item
    return item_name

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Identify and return the item that would be the most expensive
    option to buy given the parameters: cookies, cps, and time_left. 
    
    If there is no expensive option, return None.
    """
    total_cookies = cookies + (cps * time_left)
    maxval = float('-inf')
    item_name = None
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost <= total_cookies:
            if item_cost > maxval:
                maxval = item_cost
                item_name = item
    return item_name

def strategy_best(cookies, cps, time_left, build_info):
    """
    Identify and return the item that would be the best option
    to buy (in terms of cps) given the parameters: cookies, cps,
    and time_left. 
    
    If the best option is None, check for the most expensive option. If the most
    expensive option is None, return the cheapest option. Otherwise, return the
    most expensive option.
    """
    total_cookies = cookies + (cps * time_left)
    best_cps_to_cost_ratio = float('-inf')
    item_name = None
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost <= total_cookies:
            cps_to_cost_ratio = build_info.get_cps(item)/(item_cost*1.0)
            if cps_to_cost_ratio >= best_cps_to_cost_ratio:
                best_cps_to_cost_ratio = cps_to_cost_ratio
                item_name = item
    return item_name
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    
    #"undefined: TypeError: Cannot read property 'document' of undefined"
    #That error is Chrome blocking the pop-up window for simpleplot. Click the
    #red X in the right portion of the URL bar to unblock.
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

