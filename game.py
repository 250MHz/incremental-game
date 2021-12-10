"""
Incremental game - GUI project
Layout idea and concepts are modeled on https://kittensgame.com/web/#
"""
import tkinter as tk
from tkinter import ttk
from tkinter import font

from tooltip import Hovertip


class Resource:
    """
    A Resource represnts a resource used to build / create stuff.
    self.resource counts the quantity of the resource
    self.per_second counds the per/second increase of the resource
    """

    def __init__(self, frame, row, name, max_num, style='TLabel'):
        self.resource = tk.DoubleVar()
        self.per_second = tk.StringVar()
        self.text_visible = False # True if the label is visible
        self.frame = frame
        self.row = row
        self.name = name
        self.style = style
        self.total = 0.0 # used in update_per_second
        self.max_num_var = tk.StringVar() # the maximum value that self.resource can be
        self.max_num = 0
        self.update_max_num(max_num) # set the default max_num as the argument max_num
        self.efficiency_bonus_var = tk.StringVar()
        self.current_efficiency_bonus = 0.0 # used to keep track of what's displayed by efficiency_bonus_var

    def update(self, p):
        if round(self.resource.get() + p, 2) < 0:
            self.resource.set(0)
        else:
            self.resource.set(min(round(self.resource.get() + p, 2), self.max_num))
        if not self.text_visible:
            # unchanging label, shows the name of the resource
            ttk.Label(self.frame, text=self.name, style=self.style).grid(column=0, row=self.row, sticky='W')
            # changing label, shows the amount of the resource
            ttk.Label(self.frame, textvariable=self.resource).grid(column=1, row=self.row, padx=(10, 0), sticky='E')
            # changing label, shows the max number of the resource
            ttk.Label(self.frame, textvariable=self.max_num_var, foreground='#7d7d7d').grid(column=2, row=self.row, sticky='W')
            # changing label, shows the resource per second
            ttk.Label(self.frame, textvariable=self.per_second).grid(column=3, row=self.row, padx=(0, 5), sticky='W')
            # changing label, shows the efficiency bonus
            self.efficiency_bonus_label = ttk.Label(self.frame, textvariable=self.efficiency_bonus_var)
            self.efficiency_bonus_label.grid(column=4, row=self.row, sticky='W')
            self.text_visible = True # label should now be visible

    def update_per_second(self, p):
        self.total = self.total + p
        # update the label showing the resource per second
        if self.total > 0.0 and round(self.total, 2) > 0.0:
            self.per_second.set(f'+{round(self.total, 2)}/s')
        elif self.total < 0.0 and round(self.total, 2) < 0.0:
            self.per_second.set(f'{round(self.total, 2)}/s')
        else:
            self.per_second.set('')

    def update_max_num(self, p):
        # update label showing the max number of the resource
        self.max_num = int(self.max_num + p)
        self.max_num_var.set(f'/{self.max_num}')
    
    def update_efficiency_bonus(self, p):
        # update label showing the efficiency bonus
        self.current_efficiency_bonus = self.current_efficiency_bonus + p
        percentage = int(round(self.current_efficiency_bonus, 2) * 100)
        if self.current_efficiency_bonus > 0:
            self.efficiency_bonus_var.set(f'[+{percentage}%]')
            self.efficiency_bonus_label.config(foreground='#008000')
        elif self.current_efficiency_bonus < 0:
            self.efficiency_bonus_var.set(f'[{percentage}%]')
            self.efficiency_bonus_label.config(foreground='#ff0000')
        else:
            self.efficiency_bonus_var.set('')


class ResourceFrame(ttk.Frame):
    """
    Displays Labels that shows the name of Resources, the current value
    of those Resources, and per_second bonuses.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(1, minsize=60)

        self.style = ttk.Style()
        self.text_font = font.nametofont('TkTextFont')
        self.style.configure('Vanilla.TLabel', font=('TkTextFont', self.text_font['size'], 'bold'), foreground='#D1BEA8') # bold b/c color is hard to read
        self.style.configure('Strawberry.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#FC5A8D')
        self.style.configure('Chocolate.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#7B3F00')
        self.style.configure('Neapolitan.TLabel', font=('TkTextFont', self.text_font['size'], 'bold'), foreground='#808080')
        self.style.configure('MintChip.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#3EB489')
        self.style.configure('Cherry.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#DE3163')

        # resources
        ttk.Label(self, text='Resources').grid(column=0, row=0, columnspan=3, sticky='W')
        # .grid() for resources are called when the resources increment for the very first time
        # milk
        self.milk = Resource(frame=self, row=1, name='Milk', max_num=5000)
        # ice cream
        self.ice_cream = Resource(frame=self, row=2, name='Ice Cream', max_num=800)
        # vanilla ice cream
        self.vanilla_i_c = Resource(frame=self, row=3, name='    Vanilla', max_num=400, style='Vanilla.TLabel')
        # strawberry ice cream
        self.strawberry_i_c = Resource(frame=self, row=4, name='    Strawberry', max_num=400, style='Strawberry.TLabel')
        # chocolate ice cream
        self.chocolate_i_c = Resource(frame=self, row=5, name='    Chocolate', max_num=400, style='Chocolate.TLabel')
        # neapolitan ice cream
        self.neapolitan_i_c = Resource(frame=self, row=6, name='    Neapolitan', max_num=400, style='Neapolitan.TLabel')
        # mint chocolate chip ice cream
        self.mint_chip_i_c = Resource(frame=self, row=7, name='    Mint Chip', max_num=400, style='MintChip.TLabel')
        # cherry ice cream
        self.cherry_i_c = Resource(frame=self, row=8, name='    Cherry', max_num=400, style='Cherry.TLabel')
        # TODO: add more resources here

        # TODO: maybe make a hovertip over the per second labels to show where the per seconds are coming from
        # bonuses / combos
        # TODO: add new labels for combos or bonuses

        # keep a list of all resources
        self.resource_list = [
            self.milk, self.ice_cream, self.vanilla_i_c, self.strawberry_i_c, self.chocolate_i_c,
            self.neapolitan_i_c, self.mint_chip_i_c, self.cherry_i_c,
        ]


class Ingredient(Resource):
    
    def __init__(self, frame, row, name, max_num, style='TLabel'):
        super().__init__(frame, row, name, max_num, style)
        self.frame = frame

    def update(self, p):
        if not self.frame.ingredient_lb_visible:
            self.frame.ingredient_lb.grid()
            self.frame.ingredient_lb_visible = True
        super().update(p)


class IngredientFrame(ttk.Frame):
    """Basically another ResourceFrame."""

    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(1, minsize=60)

        # ingredients label
        self.ingredient_lb = ttk.Label(self, text='Ingredients')
        self.ingredient_lb.grid(column=0, row=0, sticky='W')
        self.ingredient_lb.grid_remove()
        self.ingredient_lb_visible = False # change this when an Ingredient increases for the first time
        
        # .grid() for ingredients are called when ingredients increment for the very first time
        # vanilla (spice)
        self.vanilla_spice = Ingredient(frame=self, row=1, name='Vanilla (spice)', max_num=500)
        # strawberry (fruit)
        self.strawberry_fruit = Ingredient(frame=self, row=2, name='Strawberry (fruit)', max_num=500)
        # chocolate (food)
        self.chocolate_food = Ingredient(frame=self, row=3, name='Chocolate (food)', max_num=500)
        # peppermint
        self.peppermint = Ingredient(frame=self, row=4, name='Peppermint', max_num=500)
        # cherry (fruit)
        self.cherry_fruit = Ingredient(frame=self, row=5, name='Cherry (fruit)', max_num=500)
        # TODO: add more ingredients here

        self.ingredient_list = [
            self.vanilla_spice, self.strawberry_fruit, self.chocolate_food, self.peppermint,
            self.cherry_fruit,
        ]


class Building:
    """
    For buildings that can be bought and sold.
    Standard Building increases production of new_resource by +bonus_val/s
    """
    # TODO: is r_frame a necessary parameter? can it be deleted?
    # TODO: make new_resource and bonus_val into sequence types
    def __init__(self, parent, r_frame, buy_resources, new_resources, costs, cost_mults, bonus_vals, name, col, row, visible_resource, visible_value, colspan=3):
        self.parent = parent # frame Button will be on
        self.r_frame = r_frame # to access the ResourceFrame
        self.buy_resources = buy_resources # Resource(s) that are used to buy the building
        self.new_resources = new_resources # Resource(s) that the building generates
        self.num = 0 # number of buildings owned
        self.costs = costs # cost to build a building
        self.cost_mults = cost_mults # how much the price increases each time a new bulding is bought
        self.bonus_vals = bonus_vals # the bonus the building applies to each resource in new_resources, every new_resource has an associated bonus_val, same index
        self.name = name # name of building
        self.col = col
        self.row = row
        self.colspan = colspan
        self.button = ttk.Button(self.parent, text=self.name, state='disabled', width=25, command=self.buy)
        self.button.grid(column=self.col, row=self.row, columnspan=self.colspan, padx=5, pady=5, sticky='WE')
        self.button.grid_remove() # hide the button until certain requirements are met
        self.button_visible = False # True if the Button for the Building is visible
        self.visible_resource = visible_resource # the Resource used to tell if the button should be visible
        self.visible_value = visible_value # number of visible_resources needed to make button visible
        self.efficiency_bonus = 1.0 # modify the bonus given to use(), this bonus applies to the building as a whole, all things the buliding produces is affected
        # TODO: use the efficiency_bonus value to add a [+x%] in ResourceFrame

    def buy(self):
        # deduct cost from Resource(s) to buy building
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            buy_resource.update(-cost)
        self.num = self.num + 1 # increase the number of this Building
        self.button['text'] = f'{self.name} ({self.num})' # update quantity on this Building's button
        for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
            self.costs[i] = cost * cost_mult # increase each cost by cost_mult
        for new_resource, bonus_val in zip(self.new_resources, self.bonus_vals):
            new_resource.update_per_second(bonus_val * self.efficiency_bonus) # increase each Resource the building generates
        self.update_hovertip()
        self.hovertip.showtip()

    def sell(self, s):
        # s is the number of hosts to sell
        for j in range(s):
            for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
                self.costs[i] = cost / cost_mult # update the cost
                self.buy_resources[i].update(cost / cost_mult) # refund the user
            for new_resource, bonus_val in zip(self.new_resources, self.bonus_vals):
                new_resource.update_per_second(-bonus_val * self.efficiency_bonus) # update per second Label
            self.num = self.num - 1 # update the number of Building
        if self.num != 0:
            self.button['text'] = f'{self.name} ({self.num})'
        else:
            self.button['text'] = self.name # Button doesn't show quantity if quantity is 0

    def available(self):
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            if (buy_resource.resource.get() < cost):
                self.button.state(['disabled'])
                break
        else:
            self.button.state(['!disabled'])

    def use(self):
        for new_resource, bonus_val in zip(self.new_resources, self.bonus_vals):
            new_resource.update(self.num * bonus_val * self.efficiency_bonus) # increase each new_resource

    def create_hovertip(self, description):
        self.description = description
        self.hovertip = HovertipButtons(self, description)

    def update_hovertip(self):
        self.hovertip.hidetip()
        self.hovertip = HovertipButtons(self, self.description)

    def make_visible(self):
        self.button.grid()
        self.button_visible = True


class Converter(Building):
    """
    Buildings but the number of buildings activated can be changed
    by the user.

    While activated, a Converter deducts from old_resource to add
    some value to the new_resource.
    """
    # TODO: modify Converter to allow converting old_resources into multiple new_resources
    def __init__(self, parent, r_frame, buy_resources, old_resources, new_resources, costs, cost_mults, bonus_vals, conversion_costs, name, col, row, visible_resource, visible_value, colspan=1):
        super().__init__(parent, r_frame, buy_resources, new_resources, costs, cost_mults, bonus_vals, name, col, row, visible_resource, visible_value, colspan)
        self.old_resources = old_resources # Resource that gets converted into new_resource
        self.new_resources = new_resources # Resources converted from old_resource
        self.conversion_costs = conversion_costs # number(s) of old_resources spent for each conversion
        # Building Button
        self.button.grid(column=col, row=row, padx=(5, 0), pady=5, sticky='WE')
        self.button.grid_remove()
        self.activated_num = 0 # number of Converters activated
        # increase the number of Converters activated
        self.activated_up_b = ttk.Button(self.parent, text='+', state='disabled', width=1, command=lambda: self.activated_increase(1))
        self.activated_up_b.grid(column=col+1, row=row, sticky='WE')
        self.activated_up_b.grid_remove() # show when at least 1 Converter is owned
        # decrease the number of Converters activated
        self.activated_down_b = ttk.Button(self.parent, text='-', state='disabled', width=1, command=lambda: self.activated_increase(-1))
        self.activated_down_b.grid(column=col+2, row=row, padx=(0, 5), sticky='WE')
        self.activated_down_b.grid_remove() # show at same time as activated_up_b

        self.previous_activated_num = self.activated_num # used in available()

    def activated_increase(self, i):
        self.activated_num = self.activated_num + i
        self.button['text'] = f'{self.name} ({self.activated_num}/{self.num})'

    def buy(self):
        # deduct cost from Resource(s) to buy building
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            buy_resource.update(-cost)
        self.num = self.num + 1 # increase the number of this Converter
        self.activated_increase(1) # when buying a new Converter, it is activated by default
        self.button['text'] = f'{self.name} ({self.activated_num}/{self.num})' # update button's text to show number activated & total quantity
        self.activated_up_b.grid()
        self.activated_down_b.grid()
        for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
            self.costs[i] = cost * cost_mult # increase each cost of Converter by cost_mult
        self.update_hovertip()
        self.hovertip.showtip()

    def sell(self, s):
        # s is the number of hosts to sell
        for i in range(s):
            for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
                self.costs[i] = cost / cost_mult # update the cost
                self.buy_resources[i].update(cost / cost_mult) # refund the user
            self.num = self.num - 1 # update the number of Building
            if self.activated_num > self.num: # when maxmium Converters are being used
                self.activated_num = self.activated_num - 1
        if self.num != 0:
            self.button['text'] = f'{self.name} ({self.activated_num}/{self.num})'
        else:
            self.button['text'] = self.name # Button doesn't show quantity if quantity is 0

    def use(self):
        b = True # make this False if there are not enough Resources to convert
        for old_resource, conversion_cost in zip(self.old_resources, self.conversion_costs):
            if old_resource.resource.get() + (self.activated_num * -conversion_cost) <= 0:
                b = False
                break
        # if there is ever not enough old_resources for the full conversion, stop the conversion
        if b:
            for old_resource, conversion_cost in zip(self.old_resources, self.conversion_costs):
                # no need to check if updating results in neagtive old_resource b/c it was done above
                old_resource.update(self.activated_num * -conversion_cost)
            for new_resource, bonus_val in zip(self.new_resources, self.bonus_vals):
                new_resource.update(self.activated_num * bonus_val * self.efficiency_bonus) # add each new_resource for a conversion

    def available(self):
        # whether or not the Converter can be bought
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            if (buy_resource.resource.get() < cost):
                self.button.state(['disabled'])
                break
        else:
            self.button.state(['!disabled'])
        
        if self.num > 0:
            # activated up button
            if self.activated_num < self.num:
                # less than maximum number of Converters activated
                self.activated_up_b.state(['!disabled'])
            else:
                # maximum number of Converters activated
                self.activated_up_b.state(['disabled'])
            # activated down Button
            if self.activated_num > 0:
                # more than 0 activated Converters
                self.activated_down_b.state(['!disabled'])
            else:
                # 0 activated Converters
                self.activated_down_b.state(['disabled'])
        else: # if there are no Converters, hide the '+' and '-' Buttons
            self.activated_up_b.grid_remove()
            self.activated_down_b.grid_remove()
        # update the per second labels 
        diff = self.previous_activated_num - self.activated_num
        if diff > 0: # previous is higher than current
            sign = 1
        elif diff < 0: # previous is lower than current
            sign = -1
        for i in range(abs(diff)): # if diff == 0, then range(0)
            for old_resource, conversion_cost in zip(self.old_resources, self.conversion_costs):
                old_resource.update_per_second(sign * conversion_cost) # update to show lower/higher cost
            for new_resource, bonus_val in zip(self.new_resources, self.bonus_vals):
                new_resource.update_per_second(sign * -1 * bonus_val * self.efficiency_bonus) # update to show lower/higher increase
        self.previous_activated_num = self.activated_num # update for next time


class StorageBuilding(Building):

    def __init__(self, parent, r_frame, buy_resources, costs, cost_mults, name, col, row, visible_resource, visible_value, expand_resources, expand_vals, colspan=3):
        # TODO: is there a way to do this w/o sending self.r_frame.milk? Maybe there should be an even simpler class than Buliding
        #       that doesn't take a new_resource 
        # new_resource and bonus_val won't be used. send self.r_frame.milk as new_resource
        # and have bonus_val as 0, so Building's buy(), sell(), and use() won't change self.r_frame.milk
        super().__init__(parent, r_frame, buy_resources, (r_frame.milk,), costs, cost_mults, [0], name, col, row, visible_resource, visible_value, colspan)
        self.expand_resources = expand_resources # sequence of resources whos max_num is to be expanded
        self.expand_vals = expand_vals # sequence of values to expand each resource by

    def buy(self):
        for expand_resource, expand_val in zip(self.expand_resources, self.expand_vals):
            expand_resource.update_max_num(expand_val)
        super().buy()

    def sell(self, s):
        for i in range(s):
            for expand_resource, expand_val in zip(self.expand_resources, self.expand_vals):
                expand_resource.update_max_num(-expand_val)
        super().sell(s)


class EfficiencyBuilding(Building):
    # improve productivity of a Resource
    # we do the math differently than kittensgame
    # pass as an argument, a tuple of all Buildings that give a +/s for a particular Resource
    # we apply this bonus to all of these Buildings' use() function
    # keep a double in each Building's __init__, when an EfficiencyBuilding is built,
    # this double increases
    # e.g., double starts at 1.0 and EffciencyBuilding improwves by 20%, then 
    # double becomes 1.2, another one is built, then double becomes 1.4
    # if efficiency buliding is sold, then decrease by 20%, so 1.4 -> 1.2
    # if bonus_val is 0.63, then 20% increase is, 0.63 * 1.2

    def __init__(self, parent, r_frame, buy_resources, costs, cost_mults, name, col, row, visible_resource, visible_value, applied_buildings, efficiency_increases, colspan=3):
        # simlar to StorageBuilding, a Resource is not being directly increased because of this Building
        # this Building only modifies the production of other Buildings
        self.applied_buildings = applied_buildings
        self.efficiency_increases = efficiency_increases
        self.new_resources = []
        self.bonus_vals = []
        # add every new_resource and bonus_val from every applied_building to new_resources and bonus_vals
        for building in applied_buildings:
            for new_resource, bonus_val in zip(building.new_resources, building.bonus_vals):
                self.new_resources.append(new_resource)
                self.bonus_vals.append(bonus_val)
        super().__init__(parent, r_frame, buy_resources, self.new_resources, costs, cost_mults, self.bonus_vals, name, col, row, visible_resource, visible_value, colspan)
        

    def buy(self):
        # deduct cost from Resource(s) to buy building
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            buy_resource.update(-cost)
        self.num = self.num + 1 # increase the number of this Building
        self.button['text'] = f'{self.name} ({self.num})' # update quantity on this Building's button
        for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
            self.costs[i] = cost * cost_mult # increase each cost by cost_mult
        for building, efficiency_increase in zip(self.applied_buildings, self.efficiency_increases): # increase efficiency_bonus of every Building in self.applied_buildings
            building.efficiency_bonus += efficiency_increase # increase efficiency_bonus
            for new_resource, bonus_val in zip(building.new_resources, building.bonus_vals):
                new_resource.update_efficiency_bonus(efficiency_increase) # update the [+x%] label
                new_resource.update_per_second(building.num * bonus_val * efficiency_increase) # update per second label
        self.update_hovertip()
        self.hovertip.showtip()

    def sell(self, s):
        # s is the number of hosts to sell
        for i in range(s):
            for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
                self.costs[i] = cost / cost_mult # update the cost
                self.buy_resources[i].update(self.costs[i]) # refund the user
            for building, efficiency_increase in zip(self.applied_buildings, self.efficiency_increases): # decrease efficiency_bonus of every Building in self.applied_buildings
                building.efficiency_bonus -= efficiency_increase # decrease efficiency_bonus
                for new_resource, bonus_val in zip(building.new_resources, building.bonus_vals):
                    new_resource.update_efficiency_bonus(-efficiency_increase) # update the [+%] label
                    new_resource.update_per_second(building.num * bonus_val * -efficiency_increase) # update per second label
            self.num = self.num - 1 # update the number of Building
        if self.num != 0:
            self.button['text'] = f'{self.name} ({self.num})'
        else:
            self.button['text'] = self.name # Button doesn't show quantity if quantity is 0

    def use(self):
        pass # do nothing


class Convert:
    """Makes a Button that exchanges some old resource for a new resource."""

    def __init__(self, parent, text, buy_resources, new_resource, costs, reward, col, row, visible_resource, visible_value, colspan=1):
        self.buy_resources = buy_resources # Resource(s) that gets converted into new_resource
        self.new_resource = new_resource # Resource converted from buy_resource
        self.costs = costs # number of buy_resources spent for each conversion
        self.reward = reward # number of new_resources received for each conversion
        self.button = ttk.Button(parent, text=text, state='disabled', width=25, command=self.convert)
        self.button.grid(column=col, row=row, columnspan=colspan, padx=5, pady=5, sticky='WE')
        self.button.grid_remove() # hide the button until certain requirements are met
        self.button_visible = False # True if the Button for the Building is visible
        self.visible_resource = visible_resource # the Resource used to tell if the button should be visible
        self.visible_value = visible_value # number of visible_resources needed to make button visible

    def convert(self):
        # send buy_resources as a tuple e.g. (ice_cream, vanilla_spice)
        # send costs as a tuple e.g. (3, 10)
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            buy_resource.update(-cost)
        self.new_resource.update(self.reward)

    def available(self):
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            if (buy_resource.resource.get() < cost):
                self.button.state(['disabled'])
                break
        else:
            self.button.state(['!disabled'])

    def create_hovertip(self, description):
        self.hovertip = HovertipButtons(self, description)

    def make_visible(self):
        self.button.grid()
        self.button_visible = True


class ControlPanelFrame(ttk.Frame):
    """Contains Buttons used for buying Buildings."""

    def __init__(self, parent, main):
        super().__init__(parent)
        self.r_frame = main.r_frame
        self.i_frame = main.i_frame

        # button for collecting milk
        self.collect_b = ttk.Button(self, text='Collect', width=25, command=lambda: self.r_frame.milk.update(1))
        self.collect_b.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        self.collect_b_hovertip = Hovertip(self.collect_b, 'Collect some milk...', hover_delay=10)
        # convert milk to ice cream
        self.convert_milk_i_c = Convert(self, 'Make ice cream', (self.r_frame.milk,), self.r_frame.ice_cream, [25], 1, 3, 0, self.r_frame.milk, 0, 3)
        self.convert_milk_i_c.make_visible() # make this button visible immediately
        self.convert_milk_i_c.create_hovertip('Uses milk to create plain ice cream')
        # cow
        self.cow = Building(self, self.r_frame, (self.r_frame.milk,), (self.r_frame.milk,), [10], [1.12], [0.63], 'Cow', 0, 1, self.r_frame.milk, 3)
        self.cow.create_hovertip('Get a cow')
        # factory
        self.factory = Converter(self, self.r_frame, (self.r_frame.ice_cream,), (self.r_frame.milk,), (self.r_frame.ice_cream,), [5], [1.2], [1], (self.convert_milk_i_c.costs[0]/10,), 'Factory', 3, 1, self.r_frame.ice_cream, 1)
        self.factory.create_hovertip("Converts milk to ice cream. Factories stop running\nif you don't have enough milk and continue\nrunning when you have enough.")
        # vanilla plantation
        self.vanilla_plantation = Building(self, self.r_frame, (self.r_frame.ice_cream,), (self.i_frame.vanilla_spice,), [10], [1.29], [0.15], 'Vanilla Plantation', 0, 2, self.r_frame.ice_cream, 1)
        self.vanilla_plantation.create_hovertip('Plantation for growing Vanilla planifolia')
        # strawberry field
        self.strawberry_field = Building(self, self.r_frame, (self.r_frame.ice_cream,), (self.i_frame.strawberry_fruit,), [10], [1.3], [0.15], 'Strawberry Field', 3, 2, self.r_frame.ice_cream, 1)
        self.strawberry_field.create_hovertip('Produces strawberries')
        # chocolate processor
        self.chocolate_processor = Building(self, self.r_frame, (self.r_frame.ice_cream,), (self.i_frame.chocolate_food,), [10], [1.31], [0.15], 'Chocolate Processor', 0, 3, self.r_frame.ice_cream, 1)
        self.chocolate_processor.create_hovertip('Build facilities to order and process cocoa beans')
        # peppermint farm
        self.peppermint_farm = Building(self, self.r_frame, (self.r_frame.neapolitan_i_c,), (self.i_frame.peppermint,), [3], [1.14], [0.22], 'Peppermint Farm', 3, 3, self.r_frame.neapolitan_i_c, 1)
        self.peppermint_farm.create_hovertip('Cultivate peppermint (Mentha x piperita)')
        # cold storage
        cold_expand_vals = [] # contains amount to increase each resource in resource_list by
        for resource in self.r_frame.resource_list:
            cold_expand_vals.append(resource.max_num) # double the max amount of each resource
        self.cold_storage = StorageBuilding(self, self.r_frame, (self.r_frame.ice_cream, self.r_frame.mint_chip_i_c), [50, 10], [1.75, 1.25], 'Cold Storage', 0, 4, self.r_frame.mint_chip_i_c, 1, self.r_frame.resource_list, cold_expand_vals)
        self.cold_storage.create_hovertip('Provides space to store all cold resources.')
        # milking machine
        self.milking_machine = EfficiencyBuilding(self, self.r_frame, (self.r_frame.ice_cream, self.r_frame.neapolitan_i_c), [100, 6], [1.15, 1.5], 'Milking Machine', 3, 4, self.r_frame.mint_chip_i_c, 1, [self.cow], [0.20])
        self.milking_machine.create_hovertip('Each machine improves the milk output of your cows by 20%')
        # cherry orchard
        self.cherry_orchard = Building(self, self.r_frame, (self.r_frame.neapolitan_i_c, self.r_frame.mint_chip_i_c), (self.i_frame.cherry_fruit,), [5, 7], [1.2, 1.18], [0.18], 'Cherry Orchard', 0, 5, self.r_frame.mint_chip_i_c, 1)
        self.cherry_orchard.create_hovertip('Plantation for growing cherries')
        # warehouse
        warehouse_expand_vals = [] # contains amount to increase each ingredient in ingredient_list by
        for ingredient in self.i_frame.ingredient_list:
            warehouse_expand_vals.append(ingredient.max_num) # double the max amount of each ingredient
        self.warehouse = StorageBuilding(self, self.r_frame, (self.r_frame.ice_cream, self.r_frame.strawberry_i_c, self.r_frame.cherry_i_c), [125, 15, 5], [1.5, 1.2, 1.15], 'Warehouse', 3, 5, self.r_frame.cherry_i_c, 1, self.i_frame.ingredient_list, warehouse_expand_vals)
        self.warehouse.create_hovertip('Provides space to store your ingredients')
        # TODO: add more buildings here

        # keep list of Buildings/Converters, when you add a new Bulding, you need to add it here
        self.buildings = [
            self.cow, self.factory, self.vanilla_plantation, self.strawberry_field, self.chocolate_processor,
            self.peppermint_farm, self.cold_storage, self.milking_machine, self.cherry_orchard, self.warehouse,
        ]


class IceCreamFrame(ttk.Frame):
    """Contains Buttons used for converting Ingredients to Ice Cream"""

    def __init__(self, parent, main):
        super().__init__(parent)
        self.r_frame = main.r_frame
        self.i_frame = main.i_frame

        # vanilla ice cream
        self.vanilla_i_c_convert = Convert(self, 'Vanilla', (self.r_frame.ice_cream, self.i_frame.vanilla_spice), self.r_frame.vanilla_i_c, [3, 8], 1, 0, 1, self.r_frame.milk, 0)
        self.vanilla_i_c_convert.create_hovertip('Produce vanilla ice cream')
        # strawberry ice cream
        self.strawberry_i_c_convert = Convert(self, 'Strawberry', (self.r_frame.ice_cream, self.i_frame.strawberry_fruit), self.r_frame.strawberry_i_c, [3, 8], 1, 0, 2, self.r_frame.milk, 0)
        self.strawberry_i_c_convert.create_hovertip('Produce strawberry ice cream')
        # chocolate ice cream
        self.chocolate_i_c_convert = Convert(self, 'Chocolate', (self.r_frame.ice_cream, self.i_frame.chocolate_food), self.r_frame.chocolate_i_c, [3, 8], 1, 0, 3, self.r_frame.milk, 0)
        self.chocolate_i_c_convert.create_hovertip('Produce chocolate ice cream')
        # neapolitan ice cream
        self.neapolitan_i_c_convert = Convert(self, 'Neapolitan', (self.r_frame.vanilla_i_c, self.r_frame.strawberry_i_c, self.r_frame.chocolate_i_c), self.r_frame.neapolitan_i_c, [3, 3, 3], 1, 0, 4, self.r_frame.milk, 0)
        self.neapolitan_i_c_convert.create_hovertip('Produce neapolitan ice cream')
        # mint chocolate chip ice cream
        self.mint_chip_i_c_convert = Convert(self, 'Mint Chocolate Chip', (self.r_frame.ice_cream, self.i_frame.chocolate_food, self.i_frame.peppermint), self.r_frame.mint_chip_i_c, [3, 4, 5], 1, 0, 5, self.r_frame.neapolitan_i_c, 1)
        self.mint_chip_i_c_convert.create_hovertip('Produce mint chocolate chip ice cream')
        # cherry ice cream
        self.cherry_i_c_convert = Convert(self, 'Cherry', (self.r_frame.ice_cream, self.i_frame.cherry_fruit), self.r_frame.cherry_i_c, [3, 8], 1, 0, 6, self.r_frame.mint_chip_i_c, 1)
        self.cherry_i_c_convert.create_hovertip('Produce cherry ice cream')
        # keep list of ice creams, when you add a new ice cream, you need to add it here
        self.i_c_converts = [
            self.vanilla_i_c_convert, self.strawberry_i_c_convert, self.chocolate_i_c_convert, self.neapolitan_i_c_convert,
            self.mint_chip_i_c_convert, self.cherry_i_c_convert,
        ]


class SellObject:
    """
    Creates Labels and Spinboxes for SellFrame. 
    Has methods to update, show, and hide the Spinboxes.
    """

    def __init__(self, parent, building, row):
        self.parent = parent # Frame that widgets will be on
        self.building = building
        self.sell_num = tk.IntVar() # count the number of hosts to sell
        self.sp_label = ttk.Label(parent, text=self.building.name)
        self.sp_label.grid(column=0, row=row)
        self.sp_label.grid_remove()
        self.sp = ttk.Spinbox(parent, from_=0, to=self.building.num, textvariable=self.sell_num, state=['readonly'])
        self.sp.grid(column=1, row=row, padx=5, pady=5)
        self.hide_sp() # keep Spinbox hidden until at least 1 building is owned

    def sell_(self):
        self.building.sell(self.sell_num.get()) # sell the amount currently selected
        self.sp['to'] = self.building.num
        self.sp.set(0)
        self.building.update_hovertip()

    def update_sp(self):
        self.sp['to'] = self.building.num
        self.sp.set(0)

    def show_sp(self):
        self.sp_label.grid()
        self.sp.grid()

    def hide_sp(self):
        self.sp_label.grid_remove()
        self.sp.grid_remove()


class SellFrame(ttk.Frame):
    """
    SellFrame contains Labels and Spinboxes. The value of the Spinboxes
    is how much of each Building as marked by Label should be sold.
    The sell Button sells the number of Buildings currently set by the
    Spinboxes.
    """

    def __init__(self, parent, main):
        super().__init__(parent)
        self.c_frame = main.c_frame

        # SellObject includes Labels and Spinboxes
        self.sell_object_list = [] # keep track of SellObjects
        row = 0
        for building in self.c_frame.buildings:
            self.sell_object_list.append(SellObject(self, building, row))
            row = row + 1

        # sell button
        self.sell_button = ttk.Button(self, text='Sell', command=self.sell_all)
        self.sell_button.grid(column=1, row=99, pady=5) # if there are >99 hosts to sell, then row # needs to increase

    def sell_all(self):
        for sell_object in self.sell_object_list:
            sell_object.sell_()

    def sf_update_sp(self):
        for sell_object in self.sell_object_list:
            sell_object.update_sp()


class HovertipButtons(Hovertip):
    """
    Takes an object and a simple description, then generates the
    message to be used for Hovertip's text.
    """

    def __init__(self, host, description):
        self.host = host # the Building instance to make a Hovertip for
        self.description = description
        text = self.produce_text(host, description)
        super().__init__(host.button, text, hover_delay=10)

    def produce_text(self, host, description):
        text = description + '\n' # string to be inputted
        text += '—————\nCost:'
        for buy_resource, cost in zip(host.buy_resources, host.costs):
            text += f'\n{round(cost, 2)} {buy_resource.name.strip()}'
        if isinstance(host, Building):
            text += '\n—————\nEffects:'
        if isinstance(host, Converter):
            for old_resource, conversion_cost in zip(host.old_resources, host.conversion_costs):
                text += f'\n{old_resource.name} conversion: -{round(conversion_cost, 2)}/sec'
            for new_resource, bonus_val in zip(host.new_resources, host.bonus_vals):
                text += f'\n{new_resource.name} production: {bonus_val}/sec'
        elif isinstance(host, StorageBuilding):
            # exception b/c we don't want every value listed for cold storages
            if host.name == 'Cold Storage':
                for i in range(2):
                    text += f'\nMax {host.expand_resources[i].name}: +{host.expand_vals[i]}'
                text += f'\nMax Ice Cream (flavored): +{host.expand_vals[2]}'
                return text
            # exception b/c we don't want every value listed for warehouses
            if host.name == 'Warehouse':
                text += f'\nMax Ingredient (every): +{host.expand_vals[0]}'
                return text
            for expand_resource, expand_val in zip(host.expand_resources, host.expand_vals):
                text += f'\nMax {expand_resource.name.strip()}: +{expand_val}'
        elif isinstance(host, EfficiencyBuilding):
            for building, efficiency_increase in zip(host.applied_buildings, host.efficiency_increases):
                text += f'\n{building.name} production bonus: {int(efficiency_increase * 100)}%'
        elif isinstance(host, Building):
            for new_resource, bonus_val in zip(host.new_resources, host.bonus_vals):
                text += f'\n{new_resource.name} production: {bonus_val}/sec'
        return text


class MainApplication:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Simple incremental game')
        self.parent.eval('tk::PlaceWindow . center')
        self.parent.columnconfigure(0, minsize=300)
        self.parent.columnconfigure(1, weight=1, minsize=300)
        self.parent.rowconfigure(0, weight=1)

        self.style = ttk.Style()
        self.text_font = font.nametofont('TkTextFont')

        # resources frame
        self.r_frame = ResourceFrame(self.parent)
        self.r_frame.grid(column=0, row=0, padx=10, pady=5, sticky='NWES')

        # ingredients frame
        self.i_frame = IngredientFrame(self.r_frame)
        self.i_frame.grid(column=0, row=99, columnspan=4, padx=0, pady=(5, 0), sticky='WS')
        
        # create a notebook for holding tabs
        #self.frame_for_nb = ttk.Frame()
        #self.frame_for_nb.grid(column=1, row=0, rowspan=3, padx=10, pady=5, sticky='NE')
        self.nb = ttk.Notebook(self.parent)
        self.nb.grid(column=1, row=0, rowspan=3, padx=10, pady=5, sticky='NE')

        # control panel frame
        self.c_frame = ControlPanelFrame(self.nb, self)
        self.nb.add(self.c_frame, text='Control Panel')

        # TODO: powerup / bonuses frame? thinking of having these special upgrades to be in a separate frame, but
        # they can still be in the control panel frame...

        self.i_c_tab_visible = False

        # ice cream frame
        self.i_c_frame = IceCreamFrame(self.nb, self)
        self.nb.add(self.i_c_frame, text='Ice Cream', state='hidden') # unlock after getting first Vanilla (spice)

        # sell frame
        self.sell_frame = SellFrame(self.nb, self)
        self.nb.add(self.sell_frame, text='Sell', state='hidden') # unlock after getting first Building
        self.nb.bind('<<NotebookTabChanged>>', lambda e: self.sell_frame.sf_update_sp())
        # keep selling spinboxes hidden until building is acquired for the first time
        self.sell_tab_visible = False

        # use buildings
        self.use_buildings()

        # see if buttons are available and visible
        self.available()

        # cheat button for testing new features, delete in final version
        self.cheat_b = ttk.Button(self.parent, text='Cheat increase', command=self.cheat)
        self.cheat_b.grid()

    def use_buildings(self):
        """Increase the value of Resources every second."""
        for building in self.c_frame.buildings:
            if building.num > 0:
                building.use()
        self.parent.after(1000, self.use_buildings)

    def available(self):
        """Makes buttons available and visible."""
        t = []
        # make Bulidings available
        for sell_object in self.sell_frame.sell_object_list:
            # make sell tab available
            if not self.sell_tab_visible and sell_object.building.num > 0:
                self.nb.tab(2, state='normal')
                self.sell_tab_visible = True
            t.append(sell_object.building.num)
            # make buttons for Buildings visible
            if not sell_object.building.button_visible and sell_object.building.visible_resource.resource.get() >= sell_object.building.visible_value:
                sell_object.building.make_visible()
            sell_object.building.available() # see if Button is available
            # make sell Spinboxes visible
            if sell_object.building.num > 0:
                sell_object.show_sp()
            else:
                sell_object.hide_sp()
        if not any(t): # hide the sell tab if there are no more buildings
            # if currently on sell tab, select Control Panel
            if self.nb.index('current') == 2:
                self.nb.select(0)
            self.nb.tab(2, state='hidden') 
            self.sell_tab_visible = False

        self.c_frame.convert_milk_i_c.available() # copnvert_milk_i_c is not in i_c_frame
        for ice_cream in self.i_c_frame.i_c_converts: 
            ice_cream.available() # make Convert buttons available
            if not ice_cream.button_visible and ice_cream.visible_resource.resource.get() >= ice_cream.visible_value:
                ice_cream.make_visible() # make Convert button visible
        # make ice cream tab visible
        if not self.i_c_tab_visible and self.r_frame.ice_cream.resource.get() > 0:
            self.nb.tab(1, state='normal')
            self.i_c_tab_visible = True

        self.parent.after(10, self.available)
    
    def cheat(self):
        i = 100
        self.r_frame.milk.update(i)
        self.r_frame.ice_cream.update(i)
        self.i_frame.vanilla_spice.update(i)
        self.i_frame.strawberry_fruit.update(i)
        self.i_frame.chocolate_food.update(i)
        self.i_frame.peppermint.update(i)
        self.i_frame.cherry_fruit.update(i)


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()