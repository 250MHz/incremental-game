"""
Incremental game - GUI project
Layout idea and concepts are modeled on https://kittensgame.com/web/#
"""
import tkinter as tk
from tkinter import ttk

from tooltip import Hovertip


class MainApplication:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Simple incremental game')
        self.parent.eval('tk::PlaceWindow . center')
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.milk_text_visible = False
        self.ice_cream_text_visible = False
        self.strawberry_fruit_text_visible = False
        self.chocolate_food_text_visible = False

        # resources frame
        self.r_frame = ttk.Frame(self.parent)
        self.r_frame.grid(column=0, row=0, padx=10, pady=5, sticky='NWES')
        # resources
        ttk.Label(self.r_frame, text='Resources', width=45).grid(column=0, row=0, columnspan=3, sticky='W')
        # .grid() for resources are called when the resources increment for the very first time
        # milk
        self.milk = tk.DoubleVar()
        # milk per second
        self.milk_per_second = tk.StringVar()
        # ice cream
        self.ice_cream = tk.DoubleVar()
        # ice cream per second
        self.ice_cream_per_second = tk.StringVar()
        # TODO: maybe make a hovertip over the per second labels to show where the per seconds are coming from
        # bonuses / combos
        # TODO: add new labels for combos or bonuses
        
        self.ingredients_text_visible = False
        self.vanilla_spice_text_visible = False

        # ingredients frame
        self.i_frame = ttk.Frame(self.r_frame)
        self.i_frame.grid(column=0, row=3, columnspan=3, pady=5, sticky='NWES')
        # .grid() for ingredients are called when ingredients increment for the very first time
        # vanilla (spice)
        self.vanilla_spice = tk.DoubleVar()
        # vanilla (spice) per second
        self.vanilla_spice_per_second = tk.StringVar()
        # strawberry (fruit)
        self.strawberry_fruit = tk.DoubleVar()
        # strawberry (fruit) per second
        self.strawberry_fruit_per_second = tk.StringVar()
        # chocolate (food)
        self.chocolate_food = tk.DoubleVar()
        # chocolate (food) per second
        self.chocolate_food_per_second = tk.StringVar()
        
        # create a notebook for holding tabs
        self.nb = ttk.Notebook(self.parent)
        self.nb.grid(column=1, row=0, rowspan=3, padx=10, pady=5, sticky='NE')

        self.cow_button_visible = False
        self.factory_button_visible = False
        self.strawberry_field_button_visible = False

        # control panel frame
        self.c_frame = ttk.Frame(self.nb)
        self.nb.add(self.c_frame, text='Control Panel')
        # button for collecting milk
        self.collect_b = ttk.Button(self.c_frame, text='Collect', width=25, command=lambda: self.update_milk(1))
        self.collect_b.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        self.collect_b_hovertip = Hovertip(self.collect_b, 'Collect some milk...', hover_delay=10)
        # cow
        self.cow_num = 0
        self.cow_cost = 10 # default cost is 10 milk
        self.cow = ttk.Button(self.c_frame, text='Cow', state='disabled', width=25, command=self.get_cow)
        self.cow.grid(column=0, row=1, padx=5, pady=5, sticky='W')
        self.cow.grid_remove() # hide the button, show it when the player reaches 3 milk for the first time
        self.cow_hovertip = Hovertip(self.cow, f'Get a cow\nCost: {self.cow_cost} milk\nIncrease milk per second: +0.63/s', hover_delay=10)
        # convert milk to ice cream
        self.convert_b = ttk.Button(self.c_frame, text='Make ice cream', width=25, command=self.convert_milk)
        self.convert_b.grid(column=1, row=0, padx=5, pady=5, sticky='E')
        self.convert_b_hovertip = Hovertip(self.convert_b, 'Uses milk to create plain ice cream\nCost: 50 milk', hover_delay=10)
        # TODO: add way to convert more milk at a time
        # factory, slow generator for ice cream
        self.factory_num = 0
        self.factory_cost = 5 # default cost is 5 ice cream
        self.factory = ttk.Button(self.c_frame, text='Factory', state='disabled', width=25, command=self.get_factory)
        self.factory.grid(column=1, row=1, padx=5, pady=5, sticky='E')
        self.factory.grid_remove() # hide the button, show it after the player has 1 ice cream for the first time
        self.factory_hovertip = Hovertip(self.factory, f'Build a regular ice cream factory\nCost: {self.factory_cost} ice cream\nIncrease ice cream per second: +0.4/s', hover_delay=10)
        # vanilla plantation
        self.vanilla_plantation_num = 0
        self.vanilla_plantation_cost = 10 # default cost is 10 ice cream
        self.vanilla_plantation = ttk.Button(self.c_frame, text='Vanilla Plantation', state='disabled', width=25, command=self.get_vanilla_plantation)
        self.vanilla_plantation.grid(column=0, row=2, padx=5, pady=5, sticky='W')
        self.vanilla_plantation.grid_remove() # hide the button, show it alongside the factory
        self.vanilla_plantation_hovertip = Hovertip(self.vanilla_plantation, f'Plantation for growing Vanilla planifolia\nCost: {self.vanilla_plantation_cost} ice cream\nIncrease vanilla (spice) per second: +0.26/s', hover_delay=10)
        # strawberry field
        self.strawberry_field_num = 0
        self.strawberry_field_cost = 10 # default cost is 10 ice cream
        self.strawberry_field = ttk.Button(self.c_frame, text='Strawberry Field', state='disabled', width=25, command=self.get_strawberry_field)
        self.strawberry_field.grid(column=1, row=2, padx=5, pady=5, sticky='E')
        self.strawberry_field.grid_remove() # hide the button, show it after a vanilla plantation has been made
        self.strawberry_field_hovertip = Hovertip(self.strawberry_field, f'Produces strawberries\nCost: {self.strawberry_field_cost} ice cream\nIncrease strawberry (fruit) per second: +0.35/s', hover_delay=10)
        # chocolate processor
        self.chocolate_processor_num = 0
        self.chocolate_processor_cost = 10 # default cost is 10 ice cream
        self.chocolate_processor = ttk.Button(self.c_frame, text='Chocolate Processor', state='disabled', width=25, command=self.get_chocolate_processor)
        self.chocolate_processor.grid(column=0, row=3, padx=5, pady=5, sticky='E')
        self.chocolate_processor.grid_remove() # hide the button, show it after a vanilla plantation has been made
        self.chocolate_processor_hovertip = Hovertip(self.chocolate_processor, f'Build facilities to order and process cocoa beans\nCost: {self.chocolate_processor_cost} ice cream\nIncrease chocolate (food) per second: +0.15/s', hover_delay=10)
        # TODO: add more stuff to buy here!!

        # use buildings
        self.use_buildings()
        # keeping track of what is available to buy
        self.available_buy()

        # TODO: powerup / bonuses frame? thinking of having these special upgrades to be in a separate frame, but
        #       they can still be in the control panel frame...

        # keep selling spinboxes hidden until building is acquired for the first time
        self.sell_tab_visible = False
        self.sell_cow_sp_visible = False
        self.sell_factory_sp_visible = False
        self.sell_vanilla_plantation_sp_visible = False
        self.sell_strawberry_field_sp_visible = False
        self.sell_chocolate_processor_sp_visible = False

        # selling frame
        self.sell_frame = ttk.Frame(self.nb)
        self.nb.add(self.sell_frame, text='Sell', state='hidden')
        # IntVar to count the number of each building to sell
        self.sell_cow_num = tk.IntVar() # cow
        self.sell_factory_num = tk.IntVar() # factory
        self.sell_vanilla_plantation_num = tk.IntVar() # vanilla plantation
        self.sell_strawberry_field_num = tk.IntVar() # strawberry field
        self.sell_chocolate_processor_num = tk.IntVar() # chocoalte processor
        # sell button
        self.sell_button = ttk.Button(self.sell_frame, text='Sell', command=self.sell)
        self.sell_button.grid(column=1, row=99, pady=5) # if there are >99 things to sell, then row # needs to increase

        # cheat button for testing new features, delete in final version
        self.cheat_b = ttk.Button(self.parent, text='Cheat increase', command=self.cheat)
        self.cheat_b.grid()

    def update_milk(self, p):
        self.milk.set(round(self.milk.get() + p, 2))
        if not self.milk_text_visible:
            # milk label
            ttk.Label(self.r_frame, text='Milk').grid(column=0, row=1, sticky='W')
            self.milk_label = ttk.Label(self.r_frame, textvariable=self.milk)
            self.milk_label.grid(column=1, row=1, sticky='W')
            # milk per second label
            self.milk_per_second_lb = ttk.Label(self.r_frame, textvariable=self.milk_per_second)
            self.milk_per_second_lb.grid(column=2, row=1, sticky='W')
            self.milk_text_visible = True
        if not self.cow_button_visible and self.milk.get() >= 3:
            self.cow.grid()
            self.cow_button_visible = True

    def update_milk_per_second(self):
        total = round(self.cow_num * 0.63, 2) # first argument needs to expand as we add more buildings
        if total > 0:
            self.milk_per_second.set(f'+{total}/s')
        elif total < 0:
            self.milk_per_second.set(f'{total}/s')
        else:
            self.milk_per_second.set('')

    def update_ice_cream(self, p):
        self.ice_cream.set(round(self.ice_cream.get() + p, 2))
        if not self.ice_cream_text_visible:
            # ice cream label
            ttk.Label(self.r_frame, text='Ice Cream').grid(column=0, row=2, sticky='W')
            self.ice_cream_label = ttk.Label(self.r_frame, textvariable=self.ice_cream)
            self.ice_cream_label.grid(column=1, row=2, sticky='W')
            # ice cream per second label
            self.ice_cream_per_second_lb = ttk.Label(self.r_frame, textvariable=self.ice_cream_per_second)
            self.ice_cream_per_second_lb.grid(column=2, row=2, sticky='W')
            self.ice_cream_text_visible = True
        if not self.factory_button_visible and self.ice_cream.get() >= 1:
            self.factory.grid()
            self.vanilla_plantation.grid() # available at the same time as the factory
            self.factory_button_visible = True

    def update_ice_cream_per_second(self):
        total = round(self.factory_num * 0.4, 2) # first argument expands as we add more stuff
        if total > 0:
            self.ice_cream_per_second.set(f'+{total}/s') 
        elif total < 0:
            self.ice_cream_per_second.set(f'{total}/s')
        else:
            self.ice_cream_per_second.set('')

    def update_vanilla_spice(self, p):
        self.vanilla_spice.set(round(self.vanilla_spice.get() + p, 2))
        if not self.vanilla_spice_text_visible:
            # ingredients label !!!!(IMPORTANT: make the game so that vanilla is always the first ingredient obtained)!!!!
            ttk.Label(self.i_frame, text='Ingredients', width=45).grid(column=0, row=0, columnspan=3, sticky='W')
            # vanilla (spice) label
            ttk.Label(self.i_frame, text='Vanilla (spice)').grid(column=0, row=1, sticky='W')
            self.vanilla_spice_label = ttk.Label(self.i_frame, textvariable=self.vanilla_spice)
            self.vanilla_spice_label.grid(column=1, row=1, sticky='W')
            # vanilla (spice) per second label
            self.vanilla_spice_per_second_lb = ttk.Label(self.i_frame, textvariable=self.vanilla_spice_per_second)
            self.vanilla_spice_per_second_lb.grid(column=2, row=1, sticky='W')
            self.vanilla_spice_text_visible = True
        if not self.strawberry_field_button_visible and self.vanilla_spice.get() > 0:
            self.strawberry_field.grid()
            self.chocolate_processor.grid()
            self.strawberry_field_button_visible = True

    def update_vanilla_spice_per_second(self):
        total = round(self.vanilla_plantation_num * 0.26, 2) # first argument expands as we add more stuff
        if total > 0:
            self.vanilla_spice_per_second.set(f'+{total}/s')
        elif total < 0:
            self.vanilla_spice_per_second.set(f'{total}/s')
        else:
            self.vanilla_spice_per_second.set('')

    def update_strawberry_fruit(self, p):
        self.strawberry_fruit.set(round(self.strawberry_fruit.get() + p, 2))
        if not self.strawberry_fruit_text_visible:
            # strawberry (fruit) label
            ttk.Label(self.i_frame, text='Strawberry (fruit)').grid(column=0, row=2, sticky='W')
            self.strawberry_fruit_label = ttk.Label(self.i_frame, textvariable=self.strawberry_fruit)
            self.strawberry_fruit_label.grid(column=1, row=2, sticky='W')
            # strawberry (fruit) per second label
            self.strawberry_fruit_per_second_lb = ttk.Label(self.i_frame, textvariable=self.strawberry_fruit_per_second)
            self.strawberry_fruit_per_second_lb.grid(column=2, row=2, sticky='W')
            self.strawberry_fruit_text_visible = True

    def update_strawberry_fruit_per_second(self):
        total = round(self.strawberry_field_num * 0.35, 2) # first argument expands as we add more stuff
        if total > 0:
            self.strawberry_fruit_per_second.set(f'+{total}/s')
        elif total < 0:
            self.strawberry_fruit_per_second.set(f'{total}/s')
        else:
            self.strawberry_fruit_per_second.set('')

    def update_chocolate_food(self, p):
        self.chocolate_food.set(round(self.chocolate_food.get() + p, 2))
        if not self.chocolate_food_text_visible:
            # chocolate (food) label
            ttk.Label(self.i_frame, text='Chocolate (food)').grid(column=0, row=3, sticky='W')
            self.chocolate_food_label = ttk.Label(self.i_frame, textvariable=self.chocolate_food)
            self.chocolate_food_label.grid(column=1, row=3, sticky='W')
            # chocolate (food) per second label
            self.chocolate_food_per_second_lb = ttk.Label(self.i_frame, textvariable=self.chocolate_food_per_second)
            self.chocolate_food_per_second_lb.grid(column=2, row=3, sticky='W')
            self.chocolate_food_text_visible = True

    def update_chocolate_food_per_second(self):
        total = round(self.chocolate_processor_num * 0.15, 2) # first argument expands as we add more stuff
        if total > 0:
            self.chocolate_food_per_second.set(f'+{total}/s')
        elif total < 0:
            self.chocolate_food_per_second.set(f'{total}/s')
        else:
            self.chocolate_food_per_second.set('')

    def update_hovertips(self):
        # add more tips as we add more buldings
        # TODO: .showtip() is called in the function for the bulding after the new hovertip has been created
        #       .showtip() has to be called in the create function because the sell Button also uses .update_hovertips()
        #       This could be improved by having .showtip() be called here instead. The issue is how do we do that without
        #       the hovertip appearing when the sell Button is invoked?
        self.cow_hovertip.hidetip()
        self.factory_hovertip.hidetip()
        self.vanilla_plantation_hovertip.hidetip()
        self.strawberry_field_hovertip.hidetip()
        self.chocolate_processor_hovertip.hidetip()
        self.cow_hovertip = Hovertip(self.cow, f'Get a cow\nCost: {self.cow_cost} milk\nIncrease milk per second: +0.63/s', hover_delay=10)
        self.factory_hovertip = Hovertip(self.factory, f'Build a regular ice cream factory\nCost: {self.factory_cost} ice cream\nIncrease ice cream per second: +0.4/s', hover_delay=10)
        self.vanilla_plantation_hovertip = Hovertip(self.vanilla_plantation, f'Plantation for growing Vanilla planifolia\nCost: {self.vanilla_plantation_cost} ice cream\nIncrease vanilla (spice) per second: +0.26/s', hover_delay=10)
        self.strawberry_field_hovertip = Hovertip(self.strawberry_field, f'Produces strawberries\nCost: {self.strawberry_field_cost} ice cream\nIncrease strawberry (fruit) per second: +0.35/s', hover_delay=10)
        self.chocolate_processor_hovertip = Hovertip(self.chocolate_processor, f'Build facilities to order and process cocoa beans\nCost: {self.chocolate_processor_cost} ice cream\nIncrease chocolate (food) per second: +0.15/s', hover_delay=10)

    def get_cow(self):
        self.update_milk(-self.cow_cost) # milk will be deducted
        self.cow_num = self.cow_num + 1
        self.cow['text'] = f'Cow ({self.cow_num})'
        self.cow_cost = round(self.cow_cost * 1.12, 2)
        self.available_sell()
        self.sell_cow_sp['to'] = self.cow_num # update selling spinboxes
        self.update_milk_per_second()
        self.update_hovertips()
        self.cow_hovertip.showtip()
    
    def convert_milk(self):
        self.update_milk(-50)
        self.update_ice_cream(1)

    def get_factory(self):
        self.update_ice_cream(-self.factory_cost) # ice cream will be deducted
        self.factory_num = self.factory_num + 1
        self.factory['text'] = f'Factory ({self.factory_num})'
        self.factory_cost = round(self.factory_cost * 1.2, 2)
        self.available_sell()
        self.sell_factory_sp['to'] = self.factory_num # update selling spinboxes
        self.update_ice_cream_per_second()
        self.update_hovertips()
        self.factory_hovertip.showtip()

    def get_vanilla_plantation(self):
        self.update_ice_cream(-self.vanilla_plantation_cost) # ice cream will be deducted
        self.vanilla_plantation_num = self.vanilla_plantation_num + 1
        self.vanilla_plantation['text'] = f'Vanilla Plantation ({self.vanilla_plantation_num})'
        self.vanilla_plantation_cost = round(self.vanilla_plantation_cost * 1.24, 2)
        self.available_sell()
        self.sell_vanilla_plantation_sp['to'] = self.vanilla_plantation_num # update selling spinboxes
        self.update_vanilla_spice_per_second()
        self.update_hovertips()
        self.vanilla_plantation_hovertip.showtip()

    def get_strawberry_field(self):
        self.update_ice_cream(-self.strawberry_field_cost) # ice cream will be deducted
        self.strawberry_field_num = self.strawberry_field_num + 1
        self.strawberry_field['text'] = f'Strawberry Field ({self.strawberry_field_num})'
        self.strawberry_field_cost = round(self.strawberry_field_cost * 1.19, 2)
        self.available_sell()
        self.sell_strawberry_field_sp['to'] = self.strawberry_field_num # update selling spinboxes
        self.update_strawberry_fruit_per_second()
        self.update_hovertips()
        self.strawberry_field_hovertip.showtip()

    def get_chocolate_processor(self):
        self.update_ice_cream(-self.chocolate_processor_cost) # ice cream will be deducted
        self.chocolate_processor_num = self.chocolate_processor_num + 1
        self.chocolate_processor['text'] = f'Chocolate Processor ({self.chocolate_processor_num})'
        self.chocolate_processor_cost = round(self.chocolate_processor_cost * 1.29, 2)
        self.available_sell()
        self.sell_chocolate_processor_sp['to'] = self.chocolate_processor_num # update selling spinboxes
        self.update_chocolate_food_per_second()
        self.update_hovertips()
        self.chocolate_processor_hovertip.showtip()

    def use_buildings(self):
        if self.cow_num > 0:
            self.update_milk(self.cow_num * 0.63)
        if self.factory_num > 0:
            self.update_ice_cream(self.factory_num * 0.4)
        if self.vanilla_plantation_num > 0:
            self.update_vanilla_spice(self.vanilla_plantation_num * 0.26)
        if self.strawberry_field_num > 0:
            self.update_strawberry_fruit(self.strawberry_field_num * 0.35)
        if self.chocolate_processor_num > 0:
            self.update_chocolate_food(self.chocolate_processor_num * 0.15)
        self.parent.after(1000, self.use_buildings)

    def available_buy(self):
        # disable the buttons that are too expensive
        # add an if-else statement for every new thing that we create
        # std gen
        if self.milk.get() >= self.cow_cost:
            self.cow.state(['!disabled'])
        else:
            self.cow.state(['disabled'])
        # convert milk
        if self.milk.get() >= 50:
            self.convert_b.state(['!disabled'])
        else:
            self.convert_b.state(['disabled'])
        # factory
        if self.ice_cream.get() >= self.factory_cost:
            self.factory.state(['!disabled'])
        else:
            self.factory.state(['disabled'])
        # vanilla plantation
        if self.ice_cream.get() >= self.vanilla_plantation_cost:
            self.vanilla_plantation.state(['!disabled'])
        else:
            self.vanilla_plantation.state(['disabled'])
        # strawberry field
        if self.ice_cream.get() >= self.strawberry_field_cost:
            self.strawberry_field.state(['!disabled'])
        else:
            self.strawberry_field.state(['disabled'])
        # chocolate processor
        if self.ice_cream.get() >= self.chocolate_processor_cost:
            self.chocolate_processor.state(['!disabled'])
        else:
            self.chocolate_processor.state(['disabled'])
        self.parent.after(10, self.available_buy)

    def available_sell(self):
        # called when a new building that can be sold is bought
        # makes Sell tab visible and makes selling spinboxes visible
        # labels and spinboxes - everytime we add a new building, we need to add a new spinbox in its get function
        # in the future, the state of the Spinboxes can be changed if validation is implemented
        if not self.sell_tab_visible:
            self.nb.tab(1, state='normal')
            self.sell_tab_visible = True
        if not self.sell_cow_sp_visible and self.cow_num > 0:
            ttk.Label(self.sell_frame, text='Cow').grid(column=0, row=0)
            self.sell_cow_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.cow_num, textvariable=self.sell_cow_num, state=['readonly'])
            self.sell_cow_sp.grid(column=1, row=0, padx=5, pady=5)
            self.sell_cow_sp_visible = True
        if not self.sell_factory_sp_visible and self.factory_num > 0:
            ttk.Label(self.sell_frame, text='Factory').grid(column=0, row=1)
            self.sell_factory_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.factory_num, textvariable=self.sell_factory_num, state=['readonly'])
            self.sell_factory_sp.grid(column=1, row=1, padx=5, pady=5)
            self.sell_factory_sp_visible = True
        if not self.sell_vanilla_plantation_sp_visible and self.vanilla_plantation_num > 0:
            ttk.Label(self.sell_frame, text='Vanilla Plantation').grid(column=0, row=2)
            self.sell_vanilla_plantation_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.vanilla_plantation_num, textvariable=self.sell_vanilla_plantation_num, state=['readonly'])
            self.sell_vanilla_plantation_sp.grid(column=1, row=2, padx=5, pady=5)
            self.sell_vanilla_plantation_sp_visible = True
        if not self.sell_strawberry_field_sp_visible and self.strawberry_field_num > 0:
            ttk.Label(self.sell_frame, text='Strawberry Field').grid(column=0, row=3)
            self.sell_strawberry_field_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.strawberry_field_num, textvariable=self.sell_strawberry_field_num, state=['readonly'])
            self.sell_strawberry_field_sp.grid(column=1, row=3, padx=5, pady=5)
            self.sell_strawberry_field_sp_visible = True
        if not self.sell_chocolate_processor_sp_visible and self.chocolate_processor_num > 0:
            ttk.Label(self.sell_frame, text='Chocolate Processor').grid(column=0, row=4)
            self.sell_chocolate_processor_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.chocolate_processor_num, textvariable=self.sell_chocolate_processor_num, state=['readonly'])
            self.sell_chocolate_processor_sp.grid(column=1, row=4, padx=5, pady=5)
            self.sell_chocolate_processor_sp_visible = True

    def sell(self):
        # current plan is to add a for loop for every new building we think of, but
        # this seems really inefficient, there must be a better way of doing this
        for i in range(self.sell_cow_num.get()):
            self.cow_cost = round(self.cow_cost / 1.12, 2) # update the cost
            self.cow_num = self.cow_num - 1 # update number of cows
            if self.cow_num != 0:
                self.cow['text'] = f'Cow ({self.cow_num})'
            else:
                self.cow['text'] = 'Cow'
            self.sell_cow_sp['to'] = self.cow_num
            self.sell_cow_sp.set(0)
            self.update_milk(self.cow_cost) # update number of milk
        for i in range(self.sell_factory_num.get()):
            self.factory_cost = round(self.factory_cost / 1.2, 2) # update the cost
            self.factory_num = self.factory_num - 1 # update number of factories
            if self.factory_num != 0:
                self.factory['text'] = f'Factory ({self.factory_num})'
            else:
                self.factory['text'] = 'Factory'
            self.sell_factory_sp['to'] = self.factory_num
            self.sell_factory_sp.set(0)
            self.update_ice_cream(self.factory_cost) # update number of ice cream
        for i in range(self.sell_vanilla_plantation_num.get()):
            self.vanilla_plantation_cost = round(self.vanilla_plantation_cost / 1.24, 2) # update the cost
            self.vanilla_plantation_num = self.vanilla_plantation_num - 1 # update number of vanilla plantations
            if self.vanilla_plantation_num != 0:
                self.vanilla_plantation['text'] = f'Vanilla Plantation ({self.vanilla_plantation_num})'
            else:
                self.vanilla_plantation['text'] = 'Vanilla Plantation'
            self.sell_vanilla_plantation_sp['to'] = self.vanilla_plantation_num
            self.sell_vanilla_plantation_sp.set(0)
            self.update_ice_cream(self.vanilla_plantation_cost) # update number of ice cream
        for i in range(self.sell_strawberry_field_num.get()):
            self.strawberry_field_cost = round(self.strawberry_field_cost / 1.19, 2) # update the cost
            self.strawberry_field_num = self.strawberry_field_num - 1 # update number of vstrawberry fields
            if self.strawberry_field_num != 0:
                self.strawberry_field['text'] = f'Strawberry Field ({self.strawberry_field_num})'
            else:
                self.strawberry_field['text'] = 'Strawberry Field'
            self.sell_strawberry_field_sp['to'] = self.strawberry_field_num
            self.sell_strawberry_field_sp.set(0)
            self.update_ice_cream(self.strawberry_field_cost) # update number of ice cream
        for i in range(self.sell_chocolate_processor_num.get()):
            self.chocolate_processor_cost = round(self.chocolate_processor_cost / 1.29, 2) # update the cost
            self.chocolate_processor_num = self.chocolate_processor_num - 1 # update number of chocolate processors
            if self.chocolate_processor_num != 0:
                self.chocolate_processor['text'] = f'Chocolate Processor ({self.chocolate_processor_num})'
            else:
                self.chocolate_processor['text'] = 'Chocolate Processor'
            self.sell_chocolate_processor_sp['to'] = self.chocolate_processor_num
            self.sell_chocolate_processor_sp.set(0)
            self.update_ice_cream(self.chocolate_processor_cost) # update number of ice cream
        self.update_milk_per_second()
        self.update_ice_cream_per_second()
        self.update_vanilla_spice_per_second()
        self.update_strawberry_fruit_per_second()
        self.update_chocolate_food_per_second()
        self.update_hovertips()
    
    def cheat(self):
        i = 100000
        self.update_milk(i)
        self.update_ice_cream(i)
        self.update_vanilla_spice(i)
        self.update_strawberry_fruit(i)
        self.update_chocolate_food(i)


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()