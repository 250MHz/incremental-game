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

    def __init__(self, frame, row, name, style='TLabel'):
        self.resource = tk.DoubleVar()
        self.per_second = tk.StringVar()
        self.text_visible = False # True if the label is visible
        self.frame = frame
        self.row = row
        self.name = name
        self.style = style
        self.total = 0.0 # used in update_per_second

    def update(self, p):
        self.resource.set(round(self.resource.get() + p, 2))
        if not self.text_visible:
            # unchanging label, shows the name of the resource
            ttk.Label(self.frame, text=self.name, style=self.style).grid(column=0, row=self.row, sticky='W')
            # changing label, shows the amount of the resource
            ttk.Label(self.frame, textvariable=self.resource).grid(column=1, row=self.row, sticky='W')
            # changing label, shows the resource per second
            ttk.Label(self.frame, textvariable=self.per_second).grid(column=2, row=self.row, sticky='W')
            self.text_visible = True # label should now be visible

    def update_per_second(self, p):
        self.total = round(self.total + p, 2)
        if self.total > 0:
            self.per_second.set(f'+{self.total}/s')
        elif self.total < 0:
            self.per_second.set(f'{self.total}/s')
        else:
            self.per_second.set('')


class ResourceFrame(ttk.Frame):
    """
    Displays Labels that shows the name of Resources, the current value
    of those Resources, and per_second bonuses.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.style = ttk.Style()
        self.text_font = font.nametofont('TkTextFont')
        self.style.configure('Vanilla.TLabel', font=('TkTextFont', self.text_font['size'], 'bold'), foreground='#D1BEA8') # bold b/c color is hard to read
        self.style.configure('Strawberry.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#FC5A8D')
        self.style.configure('Chocolate.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#7B3F00')
        self.style.configure('Neapolitan.TLabel', font=('TkTextFont', self.text_font['size'], 'bold'), foreground='#808080')

        # resources
        ttk.Label(self, text='Resources', width=45).grid(column=0, row=0, columnspan=3, sticky='W')
        # .grid() for resources are called when the resources increment for the very first time
        # milk
        self.milk = Resource(frame=self, row=1, name='Milk')
        # ice cream
        self.ice_cream = Resource(frame=self, row=2, name='Ice Cream')
        # vanilla ice cream
        self.vanilla_i_c = Resource(frame=self, row=3, name='    Vanilla', style='Vanilla.TLabel')
        # strawberry ice cream
        self.strawberry_i_c = Resource(frame=self, row=4, name='    Strawberry', style='Strawberry.TLabel')
        # chocolate ice cream
        self.chocolate_i_c = Resource(frame=self, row=5, name='    Chocolate', style='Chocolate.TLabel')
        # neapolitan ice cream
        self.neapolitan_i_c = Resource(frame=self, row=6, name='    Neapolitan', style='Neapolitan.TLabel')
        # TODO: maybe make a hovertip over the per second labels to show where the per seconds are coming from
        # bonuses / combos
        # TODO: add new labels for combos or bonuses


class Ingredient(Resource):
    
    def __init__(self, frame, row, name, style='TLabel'):
        super().__init__(frame, row, name, style)
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

        # ingredients label
        self.ingredient_lb = ttk.Label(self, text='Ingredients', width=45)
        self.ingredient_lb.grid(column=0, row=0, columnspan=3, sticky='W')
        self.ingredient_lb.grid_remove()
        self.ingredient_lb_visible = False # change this when an Ingredient increases for the first time
        
        # .grid() for ingredients are called when ingredients increment for the very first time
        # vanilla (spice)
        self.vanilla_spice = Ingredient(frame=self, row=1, name='Vanilla (spice)')
        # strawberry (fruit)
        self.strawberry_fruit = Ingredient(frame=self, row=2, name='Strawberry (fruit)')
        # chocolate (food)
        self.chocolate_food = Ingredient(frame=self, row=3, name='Chocolate (food)')


class Building:
    """
    For buildings that can be bought and sold.
    Standard Building increases production of new_resource by +bonus_val/s
    """
    # TODO: is r_frame a necessary parameter? can it be deleted?
    def __init__(self, parent, r_frame, buy_resources, new_resource, costs, cost_mults, bonus_val, name, col, row, visible_resource, visible_value, colspan=3):
        self.parent = parent # frame Button will be on
        self.r_frame = r_frame # to access the ResourceFrame
        self.buy_resources = buy_resources # Resource(s) that are used to buy the building
        self.new_resource = new_resource # Resource that the building generates
        self.num = 0 # number of buildings owned
        self.costs = costs # cost to build a building
        self.cost_mults = cost_mults # how much the price increases each time a new bulding is bought
        self.bonus_val = bonus_val # the bonus the building applies
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

    def buy(self):
        # deduct cost from Resource(s) to buy building
        for buy_resource, cost in zip(self.buy_resources, self.costs):
            buy_resource.update(-cost)
        self.num = self.num + 1 # increase the number of this Building
        self.button['text'] = f'{self.name} ({self.num})' # update quantity on this Building's button
        for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
            self.costs[i] = round(cost * cost_mult, 2) # increase each cost by cost_mult
        self.new_resource.update_per_second(self.bonus_val) # increase the Resource the building generates
        self.update_hovertip()
        self.hovertip.showtip()

    def sell(self, s):
        # s is the number of things to sell
        for i in range(s):
            for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
                self.costs[i] = round(cost / cost_mult, 2) # update the cost
                self.buy_resources[i].update(self.costs[i]) # refund the user
                self.new_resource.update_per_second(-self.bonus_val) # update per second Label
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
        self.new_resource.update(self.num * self.bonus_val) # increase new_resource

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

    def __init__(self, parent, r_frame, buy_resources, old_resources, new_resource, costs, cost_mults, bonus_val, conversion_costs, name, col, row, visible_resource, visible_value, colspan=1):
        super().__init__(parent, r_frame, buy_resources, new_resource, costs, cost_mults, bonus_val, name, col, row, visible_resource, visible_value, colspan)
        self.old_resources = old_resources # Resource that gets converted into new_resource
        self.new_resource = new_resource # Resource converted from old_resource
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
            self.costs[i] = round(cost * cost_mult, 2) # increase each cost of Converter by cost_mult
        self.update_hovertip()
        self.hovertip.showtip()

    def sell(self, s):
        # s is the number of things to sell
        for i in range(s):
            for cost, cost_mult, i in zip(self.costs, self.cost_mults, range(len(self.costs))):
                self.costs[i] = round(cost / cost_mult, 2) # update the cost
                self.buy_resources[i].update(self.costs[i]) # refund the user
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
            if old_resource.resource.get() + (self.activated_num * -conversion_cost) >= 0:
                old_resource.update(self.activated_num * -conversion_cost)
            else:
                b = False
                break
        if b:
            self.new_resource.update(self.activated_num * self.bonus_val)

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
        else:
            self.activated_up_b.grid_remove()
            self.activated_down_b.grid_remove()
        diff = self.previous_activated_num - self.activated_num
        if diff > 0: # previous is higher than current
            sign = 1
        elif diff < 0: # previous is lower than current
            sign = -1
        for i in range(abs(diff)): # if diff == 0, then range(0)
            for old_resource, conversion_cost in zip(self.old_resources, self.conversion_costs):
                old_resource.update_per_second(sign * conversion_cost)
            self.new_resource.update_per_second(sign * -1 * self.bonus_val)
        self.previous_activated_num = self.activated_num # update for next time


class Convert:
    """Makes a Button that exchanges some old resource for a new resource."""

    def __init__(self, parent, text, buy_resources, new_resource, costs, reward, col, row, colspan=1):
        self.buy_resources = buy_resources # Resource(s) that gets converted into new_resource
        self.new_resource = new_resource # Resource converted from buy_resource
        self.costs = costs # number of buy_resources spent for each conversion
        self.reward = reward # number of new_resources received for each conversion
        self.button = ttk.Button(parent, text=text, state='disabled', width=25, command=self.convert)
        self.button.grid(column=col, row=row, columnspan=colspan, padx=5, pady=5, sticky='WE')

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
        self.convert_milk_i_c = Convert(self, 'Make ice cream', (self.r_frame.milk,), self.r_frame.ice_cream, [25], 1, 3, 0, 3)
        self.convert_milk_i_c.create_hovertip('Uses milk to create plain ice cream')
        # cow
        self.cow = Building(self, self.r_frame, (self.r_frame.milk,), self.r_frame.milk, [10], [1.12], 0.63, 'Cow', 0, 1, self.r_frame.milk, 3)
        self.cow.create_hovertip('Get a cow')
        # factory
        self.factory = Converter(self, self.r_frame, (self.r_frame.ice_cream,), (self.r_frame.milk,), self.r_frame.ice_cream, [5], [1.2], 1, (self.convert_milk_i_c.costs[0]/10,), 'Factory', 3, 1, self.r_frame.ice_cream, 1)
        self.factory.create_hovertip("Converts milk to ice cream. Factories stop running\nif you don't have enough milk and continue\nrunning when you have enough.")
        # vanilla plantation
        self.vanilla_plantation = Building(self, self.r_frame, (self.r_frame.ice_cream,), self.i_frame.vanilla_spice, [10], [1.29], 0.15, 'Vanilla Plantation', 0, 2, self.r_frame.ice_cream, 1)
        self.vanilla_plantation.create_hovertip('Plantation for growing Vanilla planifolia')
        # strawberry field
        self.strawberry_field = Building(self, self.r_frame, (self.r_frame.ice_cream,), self.i_frame.strawberry_fruit, [10], [1.3], 0.15, 'Strawberry Field', 3, 2, self.r_frame.ice_cream, 1)
        self.strawberry_field.create_hovertip('Produces strawberries')
        # chocolate processor
        self.chocolate_processor = Building(self, self.r_frame, (self.r_frame.ice_cream,), self.i_frame.chocolate_food, [10], [1.31], 0.15, 'Chocolate Processor', 0, 3, self.r_frame.ice_cream, 1)
        self.chocolate_processor.create_hovertip('Build facilities to order and process cocoa beans')
        # TODO: add more buildings here

        # keep list of Buildings/Converters
        self.buildings = [
            self.cow, self.factory, self.vanilla_plantation, self.strawberry_field, self.chocolate_processor,
        ]


class IceCreamFrame(ttk.Frame):
    """Contains Buttons used for converting Ingredients to Ice Cream"""

    def __init__(self, parent, main):
        super().__init__(parent)
        self.r_frame = main.r_frame
        self.i_frame = main.i_frame

        # vanilla ice cream
        self.vanilla_i_c_convert = Convert(self, 'Vanilla Ice Cream', (self.r_frame.ice_cream, self.i_frame.vanilla_spice), self.r_frame.vanilla_i_c, [3, 8], 1, 0, 1)
        self.vanilla_i_c_convert.create_hovertip('Produce vanilla ice cream')
        # strawberry ice cream
        self.strawberry_i_c_convert = Convert(self, 'Strawberry Ice Cream', (self.r_frame.ice_cream, self.i_frame.strawberry_fruit), self.r_frame.strawberry_i_c, [3, 8], 1, 0, 2)
        self.strawberry_i_c_convert.create_hovertip('Produce strawberry ice cream')
        # chocolate ice cream
        self.chocolate_i_c_convert = Convert(self, 'Chocolate Ice Cream', (self.r_frame.ice_cream, self.i_frame.chocolate_food), self.r_frame.chocolate_i_c, [3, 8], 1, 0, 3)
        self.chocolate_i_c_convert.create_hovertip('Produce chocolate ice cream')
        # neapolitan ice cream
        self.neapolitan_i_c_convert = Convert(self, 'Neapolitan Ice Cream', (self.r_frame.vanilla_i_c, self.r_frame.strawberry_i_c, self.r_frame.chocolate_i_c), self.r_frame.neapolitan_i_c, [3, 3, 3], 1, 0, 4)
        self.neapolitan_i_c_convert.create_hovertip('Produce neapolitan ice cream')

        # keep list of ice creams
        self.i_c_converts = [
            self.vanilla_i_c_convert, self.strawberry_i_c_convert, self.chocolate_i_c_convert, self.neapolitan_i_c_convert,
        ]


class SellObject:
    """
    Creates Labels and Spinboxes for SellFrame. 
    Has methods to update, show, and hide the Spinboxes.
    """

    def __init__(self, parent, building, row):
        self.parent = parent # Frame that widgets will be on
        self.building = building
        self.sell_num = tk.IntVar() # count the number of things to sell
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
        self.sell_button.grid(column=1, row=99, pady=5) # if there are >99 things to sell, then row # needs to increase

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

    def __init__(self, thing, description):
        self.thing = thing
        self.description = description
        text = self.produce_text(thing, description)
        super().__init__(thing.button, text, hover_delay=10)

    def produce_text(self, thing, description):
        text = description + '\n' # string to be inputted
        text += '—————\nCost:'
        for buy_resource, cost in zip(thing.buy_resources, thing.costs):
            text += f'\n{cost} {buy_resource.name.strip()}'
        if isinstance(thing, (Converter, Building)):
            text += '\n—————\nEffects:\n'
        if isinstance(thing, Converter):
            for old_resource, conversion_cost in zip(thing.old_resources, thing.conversion_costs):
                text += f'{old_resource.name} conversion: -{conversion_cost}/sec\n'
            text += f'{thing.new_resource.name} conversion: {thing.bonus_val}/sec'
        elif isinstance(thing, Building):
            text += f'{thing.new_resource.name} production: {thing.bonus_val}/sec'
        return text


class MainApplication:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Simple incremental game')
        self.parent.eval('tk::PlaceWindow . center')
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.style = ttk.Style()
        self.text_font = font.nametofont('TkTextFont')

        # resources frame
        self.r_frame = ResourceFrame(self.parent)
        self.r_frame.grid(column=0, row=0, padx=10, pady=5, sticky='NWES')

        # ingredients frame
        self.i_frame = IngredientFrame(self.r_frame)
        self.i_frame.grid(column=0, row=98, columnspan=3, pady=5, sticky='NWES')
        
        # create a notebook for holding tabs
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
        # make Convert buttons available/visible
        self.c_frame.convert_milk_i_c.available() # copnvert_milk_i_c is not in i_c_frame
        for ice_cream in self.i_c_frame.i_c_converts:
            ice_cream.available()
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


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()