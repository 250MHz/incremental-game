"""
Incremental game - GUI project
Layout idea and concepts are modeled on https://kittensgame.com/web/#
"""
import tkinter as tk
from tkinter import ttk
from tkinter import font

from tooltip import Hovertip


class Resource:

    def __init__(self, frame, row, name, style='TLabel'):
        self.resource = tk.DoubleVar()
        self.per_second = tk.StringVar()
        self.text_visible = False # True if the label is visible
        self.frame = frame
        self.row = row
        self.name = name
        self.style = style

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
        total = round(p, 2)
        if total > 0:
            self.per_second.set(f'+{total}/s')
        elif total < 0:
            self.per_second.set(f'{total}/s')
        else:
            self.per_second.set('')


class ResourceFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

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

    # have the buttons in control panel call a different function. that function calls the methods in the Resource class
    # and you can put all the label stuff there
    # labels like 'Milk' can be written in the Resource class, the stuff that enables other buttons needs to be in ControlFrame class

    # def update_milk(self, p):
    #     self.milk.set(round(self.milk.get() + p, 2))
    #     if not self.milk_text_visible:
    #         # milk label
    #         ttk.Label(self, text='Milk').grid(column=0, row=1, sticky='W')
    #         self.milk_label = ttk.Label(self, textvariable=self.milk)
    #         self.milk_label.grid(column=1, row=1, sticky='W')
    #         # milk per second label
    #         self.milk_per_second_lb = ttk.Label(self, textvariable=self.milk_per_second)
    #         self.milk_per_second_lb.grid(column=2, row=1, sticky='W')
    #         self.milk_text_visible = True
    #     if not self.c_frame.cow_button_visible and self.milk.get() >= 3:
    #         # make cow button visible
    #         self.c_frame.cow.grid()
    #         self.cow_button_visible = True

    # def update_milk_per_second(self):
    #     total = round(self.c_frame.cow_num * 0.63 + self.c_frame.factory_activated_num * -self.c_frame.factory_conversion_cost, 2) # first argument needs to expand as we add more buildings
    #     if total > 0:
    #         self.milk_per_second.set(f'+{total}/s')
    #     elif total < 0:
    #         self.milk_per_second.set(f'{total}/s')
    #     else:
    #         self.milk_per_second.set('')

    # def update_ice_cream(self, p):
    #     self.ice_cream.set(round(self.ice_cream.get() + p, 2))
    #     if not self.ice_cream_text_visible:
    #         # ice cream label
    #         ttk.Label(self, text='Ice Cream').grid(column=0, row=2, sticky='W')
    #         self.ice_cream_label = ttk.Label(self, textvariable=self.ice_cream)
    #         self.ice_cream_label.grid(column=1, row=2, sticky='W')
    #         # ice cream per second label
    #         self.ice_cream_per_second_lb = ttk.Label(self, textvariable=self.ice_cream_per_second)
    #         self.ice_cream_per_second_lb.grid(column=2, row=2, sticky='W')
    #         self.ice_cream_text_visible = True
    #     if not self.c_frame.factory_button_visible and self.ice_cream.get() >= 1:
    #         self.c_frame.factory.grid()
    #         self.c_frame.factory_activated_up_b.grid() # goes along with factory
    #         self.c_frame.factory_activated_down_b.grid() # goes along with factory
    #         self.c_frame.vanilla_plantation.grid() # available at the same time as the factory
    #         self.factory_button_visible = True

    # def update_ice_cream_per_second(self):
    #     total = round(self.c_frame.factory_activated_num * 0.1, 2) # first argument expands as we add more stuff
    #     if total > 0:
    #         self.ice_cream_per_second.set(f'+{total}/s') 
    #     elif total < 0:
    #         self.ice_cream_per_second.set(f'{total}/s')
    #     else:
    #         self.ice_cream_per_second.set('')

    # def update_vanilla_i_c(self, p):
    #     self.vanilla_i_c.set(round(self.vanilla_i_c.get() + p, 2))
    #     if not self.vanilla_i_c_text_visible:
    #         # vanilla ice cream label
    #         self.style.configure('Vanilla.TLabel', font=('TkTextFont', self.text_font['size'], 'bold'), foreground='#D1BEA8') # bold b/c color is hard to read
    #         ttk.Label(self, text='    Vanilla', style='Vanilla.TLabel').grid(column=0, row=3, sticky='W')
    #         self.vanilla_i_c_label = ttk.Label(self, textvariable=self.vanilla_i_c)
    #         self.vanilla_i_c_label.grid(column=1, row=3, sticky='W')
    #         self.vanilla_i_c_text_visible = True

    # def update_strawberry_i_c(self, p):
    #     self.strawberry_i_c.set(round(self.strawberry_i_c.get() + p, 2))
    #     if not self.strawberry_i_c_text_visible:
    #         # strawberry ice cream label
    #         self.style.configure('Strawberry.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#FC5A8D')
    #         ttk.Label(self, text='    Strawberry', style='Strawberry.TLabel').grid(column=0, row=4, sticky='W')
    #         self.strawberry_i_c_label = ttk.Label(self, textvariable=self.strawberry_i_c)
    #         self.strawberry_i_c_label.grid(column=1, row=4, sticky='W')
    #         self.strawberry_i_c_text_visible = True

    # def update_chocolate_i_c(self, p):
    #     self.chocolate_i_c.set(round(self.chocolate_i_c.get() + p, 2))
    #     if not self.chocolate_i_c_text_visible:
    #         # chocolate ice cream label
    #         self.style.configure('Chocolate.TLabel', font=('TkTextFont', self.text_font['size']), foreground='#7B3F00')
    #         ttk.Label(self, text='    Chocolate', style='Chocolate.TLabel').grid(column=0, row=5, sticky='W')
    #         self.chocolate_i_c_label = ttk.Label(self, textvariable=self.chocolate_i_c)
    #         self.chocolate_i_c_label.grid(column=1, row=5, sticky='W')
    #         self.chocolate_i_c_text_visible = True

    # def update_neapolitan_i_c(self, p):
    #     self.neapolitan_i_c.set(round(self.neapolitan_i_c.get() + p, 2))
    #     if not self.neapolitan_i_c_text_visible:
    #         # neapolitan ice cream label
    #         self.style.configure('Neapolitan.TLabel', font=('TkTextFont', self.text_font['size'], 'bold'), foreground='#808080')
    #         ttk.Label(self, text='    Neapolitan', style='Neapolitan.TLabel').grid(column=0, row=6, sticky='W')
    #         self.neapolitan_i_c_label = ttk.Label(self, textvariable=self.neapolitan_i_c)
    #         self.neapolitan_i_c_label.grid(column=1, row=6, sticky='W')
    #         self.neapolitan_i_c_text_visible = True


# IngredientFrame is just another ResourceFrame. Same thing as methods above, we need to define the specifics of changing labels
# in MainApplication or ControlFrame

class IngredientFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # ingredients label !!!!(IMPORTANT: make the game so that vanilla is always the first ingredient obtained)!!!!
        self.ingredient_lb = ttk.Label(self, text='Ingredients', width=45)
        self.ingredient_lb.grid(column=0, row=0, columnspan=3, sticky='W')
        self.ingredient_lb.grid_remove() # show this after Vanilla (spice) is first obtained
        
        # .grid() for ingredients are called when ingredients increment for the very first time
        # vanilla (spice)
        self.vanilla_spice = Resource(frame=self, row=1, name='Vanilla (spice)')
        # strawberry (fruit)
        self.strawberry_fruit = Resource(frame=self, row=2, name='Strawberry (fruit)')
        # chocolate (food)
        self.chocolate_food = Resource(frame=self, row=3, name='Chocolate (food)')

    # def update_vanilla_spice(self, p):
    #     self.vanilla_spice.set(round(self.vanilla_spice.get() + p, 2))
    #     if not self.vanilla_spice_text_visible:
    #         # ingredients label !!!!(IMPORTANT: make the game so that vanilla is always the first ingredient obtained)!!!!
    #         ttk.Label(self, text='Ingredients', width=45).grid(column=0, row=0, columnspan=3, sticky='W')
    #         # vanilla (spice) label
    #         ttk.Label(self, text='Vanilla (spice)').grid(column=0, row=1, sticky='W')
    #         self.vanilla_spice_label = ttk.Label(self, textvariable=self.vanilla_spice)
    #         self.vanilla_spice_label.grid(column=1, row=1, sticky='W')
    #         # vanilla (spice) per second label
    #         self.vanilla_spice_per_second_lb = ttk.Label(self, textvariable=self.vanilla_spice_per_second)
    #         self.vanilla_spice_per_second_lb.grid(column=2, row=1, sticky='W')
    #         self.vanilla_spice_text_visible = True
    #     if not self.c_frame.strawberry_field_button_visible and self.vanilla_spice.get() > 0:
    #         self.c_frame.strawberry_field.grid()
    #         self.c_frame.chocolate_processor.grid()
    #         self.strawberry_field_button_visible = True
    #     if not self.main.i_c_tab_visible:
    #         self.main.nb.tab(1, state='normal')
    #         self.i_c_tab_visible = True

    # def update_vanilla_spice_per_second(self):
    #     total = round(self.c_frame.vanilla_plantation_num * 0.26, 2) # first argument expands as we add more stuff
    #     if total > 0:
    #         self.vanilla_spice_per_second.set(f'+{total}/s')
    #     elif total < 0:
    #         self.vanilla_spice_per_second.set(f'{total}/s')
    #     else:
    #         self.vanilla_spice_per_second.set('')

    # def update_strawberry_fruit(self, p):
    #     self.strawberry_fruit.set(round(self.strawberry_fruit.get() + p, 2))
    #     if not self.strawberry_fruit_text_visible:
    #         # strawberry (fruit) label
    #         ttk.Label(self, text='Strawberry (fruit)').grid(column=0, row=2, sticky='W')
    #         self.strawberry_fruit_label = ttk.Label(self, textvariable=self.strawberry_fruit)
    #         self.strawberry_fruit_label.grid(column=1, row=2, sticky='W')
    #         # strawberry (fruit) per second label
    #         self.strawberry_fruit_per_second_lb = ttk.Label(self, textvariable=self.strawberry_fruit_per_second)
    #         self.strawberry_fruit_per_second_lb.grid(column=2, row=2, sticky='W')
    #         self.strawberry_fruit_text_visible = True

    # def update_strawberry_fruit_per_second(self):
    #     total = round(self.c_frame.strawberry_field_num * 0.35, 2) # first argument expands as we add more stuff
    #     if total > 0:
    #         self.strawberry_fruit_per_second.set(f'+{total}/s')
    #     elif total < 0:
    #         self.strawberry_fruit_per_second.set(f'{total}/s')
    #     else:
    #         self.strawberry_fruit_per_second.set('')

    # def update_chocolate_food(self, p):
    #     self.chocolate_food.set(round(self.chocolate_food.get() + p, 2))
    #     if not self.chocolate_food_text_visible:
    #         # chocolate (food) label
    #         ttk.Label(self, text='Chocolate (food)').grid(column=0, row=3, sticky='W')
    #         self.chocolate_food_label = ttk.Label(self, textvariable=self.chocolate_food)
    #         self.chocolate_food_label.grid(column=1, row=3, sticky='W')
    #         # chocolate (food) per second label
    #         self.chocolate_food_per_second_lb = ttk.Label(self, textvariable=self.chocolate_food_per_second)
    #         self.chocolate_food_per_second_lb.grid(column=2, row=3, sticky='W')
    #         self.chocolate_food_text_visible = True

    # def update_chocolate_food_per_second(self):
    #     total = round(self.c_frame.chocolate_processor_num * 0.15, 2) # first argument expands as we add more stuff
    #     if total > 0:
    #         self.chocolate_food_per_second.set(f'+{total}/s')
    #     elif total < 0:
    #         self.chocolate_food_per_second.set(f'{total}/s')
    #     else:
    #         self.chocolate_food_per_second.set('')


class Building:

    def __init__(self, parent, r_frame, resource, num, cost, cost_mult, update_val, name, col, row):
        self.parent = parent
        self.r_frame = r_frame
        self.resource = resource
        self.num = num
        self.cost = cost
        self.cost_mult = cost_mult
        self.update_val = update_val
        self.name = name
        self.col = col
        self.row = row
        self.button = ttk.Button(self.parent, text=self.name, state='disabled', width=25, command=self.buy)
        self.button.grid(column=self.col, row=self.row, padx=5, pady=5, sticky='WE')
        self.button.grid_remove() # hide the button until certain requirements are met

    # need to implement buy() modifying selling stuff

    def buy(self):
        self.resource.update(-self.cost) # deduct cost from Resource
        self.num = self.num + 1 # increase the number of this Building
        self.button['text'] = f'{self.name} ({self.num})' # update quantity on this Building's button
        self.cost = round(self.cost * self.cost_mult, 2) # increase cost by cost_mult
        self.update_resource_per_second(self.num * self.update_val)

    def update_resource_per_second(self):





class ControlPanelFrame(ttk.Frame):

    def __init__(self, parent, main):
        ttk.Frame.__init__(self, parent)
        self.main = main
        self.r_frame = main.r_frame
        self.i_frame = main.i_frame

        self.cow_button_visible = False
        self.factory_button_visible = False
        self.strawberry_field_button_visible = False

        # button for collecting milk
        self.collect_b = ttk.Button(self, text='Collect', width=25, command=lambda: self.r_frame.update_milk(1))
        self.collect_b.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        self.collect_b_hovertip = Hovertip(self.collect_b, 'Collect some milk...', hover_delay=10)
        # cow
        self.cow_num = 0
        self.cow_cost = 10 # default cost is 10 milk
        # self.cow = Building(parent=self, r_frame=self.r_frame, resource=self.r_frame.milk, num=0, cost=10, cost_mult=1.12, name='Cow', col=0, row=1)
        # self.cow_hovertip = Hovertip(self.cow.button, f'Get a cow\nCost:\n{self.cow_cost} milk\nEffects:\nIncrease milk per second: +0.63/s', hover_delay=10))
        self.cow = ttk.Button(self, text='Cow', state='disabled', width=25, command=self.get_cow)
        self.cow.grid(column=0, row=1, padx=5, pady=5, sticky='WE')
        self.cow.grid_remove() # hide the button, show it when the player reaches 3 milk for the first time
        self.cow_hovertip = Hovertip(self.cow, f'Get a cow\nCost:\n{self.cow_cost} milk\nEffects:\nIncrease milk per second: +0.63/s', hover_delay=10)
        # convert milk to ice cream
        self.convert_cost = 50 # default cost is 50 milk
        self.convert_b = ttk.Button(self, text='Make ice cream', width=25, command=self.convert_milk)
        self.convert_b.grid(column=3, row=0, columnspan=3, padx=5, pady=5, sticky='WE')
        self.convert_b_hovertip = Hovertip(self.convert_b, f'Uses milk to create plain ice cream\nCost:\n{self.convert_cost} milk', hover_delay=10)
        # TODO: add way to convert more milk at a time
        # factory, automatic converter for ice cream
        self.factory_num = 0
        self.factory_cost = 5 # default cost is 5 ice cream
        self.factory_conversion_cost = self.convert_cost / 10
        self.factory = ttk.Button(self, text='Factory', state='disabled', command=self.get_factory)
        self.factory.grid(column=3, row=1, padx=(5, 0), pady=5, sticky='WE')
        self.factory.grid_remove() # hide the button, show it after the player has 1 ice cream for the first time
        self.factory_hovertip = Hovertip(self.factory, f"Converts milk to ice cream. Factories stop running\nif you don't have enough milk and continue\nrunning when you have enough.\nCost:\n{self.factory_cost} ice cream\nEffects:\nMilk conversion: -{self.factory_conversion_cost}/s\nIce cream conversion: +0.1/s", hover_delay=10)
        # buttons for managing number of activated factories
        self.factory_activated_num = 0
        self.factory_activated_up_b = ttk.Button(self, text='+', state='disabled', width=1, command=lambda: self.factory_activated_increase(1))
        self.factory_activated_up_b.grid(column=4, row=1, sticky='WE')
        self.factory_activated_up_b.grid_remove() # hide and show at same time a factory is available
        self.factory_activated_down_b = ttk.Button(self, text='-', state='disabled', width=1, command=lambda: self.factory_activated_increase(-1))
        self.factory_activated_down_b.grid(column=5, row=1, padx=(0, 5), sticky='WE')
        self.factory_activated_down_b.grid_remove() # hide and show at same time a factory is available
        # vanilla plantation
        self.vanilla_plantation_num = 0
        self.vanilla_plantation_cost = 10 # default cost is 10 ice cream
        self.vanilla_plantation = ttk.Button(self, text='Vanilla Plantation', state='disabled', width=25, command=self.get_vanilla_plantation)
        self.vanilla_plantation.grid(column=0, row=2, padx=5, pady=5, sticky='WE')
        self.vanilla_plantation.grid_remove() # hide the button, show it alongside the factory
        self.vanilla_plantation_hovertip = Hovertip(self.vanilla_plantation, f'Plantation for growing Vanilla planifolia\nCost:\n{self.vanilla_plantation_cost} ice cream\nEffects:\nIncrease vanilla (spice) per second: +0.26/s', hover_delay=10)
        # strawberry field
        self.strawberry_field_num = 0
        self.strawberry_field_cost = 10 # default cost is 10 ice cream
        self.strawberry_field = ttk.Button(self, text='Strawberry Field', state='disabled', width=25, command=self.get_strawberry_field)
        self.strawberry_field.grid(column=3, row=2, columnspan=3, padx=5, pady=5, sticky='WE')
        self.strawberry_field.grid_remove() # hide the button, show it after a vanilla plantation has been made
        self.strawberry_field_hovertip = Hovertip(self.strawberry_field, f'Produces strawberries\nCost:\n{self.strawberry_field_cost} ice cream\nEffects:\nIncrease strawberry (fruit) per second: +0.35/s', hover_delay=10)
        # chocolate processor
        self.chocolate_processor_num = 0
        self.chocolate_processor_cost = 10 # default cost is 10 ice cream
        self.chocolate_processor = ttk.Button(self, text='Chocolate Processor', state='disabled', width=25, command=self.get_chocolate_processor)
        self.chocolate_processor.grid(column=0, row=3, padx=5, pady=5, sticky='WE')
        self.chocolate_processor.grid_remove() # hide the button, show it after a vanilla plantation has been made
        self.chocolate_processor_hovertip = Hovertip(self.chocolate_processor, f'Build facilities to order and process cocoa beans\nCost:\n{self.chocolate_processor_cost} ice cream\nEffects:\nIncrease chocolate (food) per second: +0.15/s', hover_delay=10)
        # TODO: add more stuff to buy here!!

    def get_cow(self):
        self.r_frame.update_milk(-self.cow_cost) # milk will be deducted
        self.cow_num = self.cow_num + 1
        self.cow['text'] = f'Cow ({self.cow_num})'
        self.cow_cost = round(self.cow_cost * 1.12, 2)
        self.main.available_sell()
        self.main.sell_cow_sp['to'] = self.cow_num # update selling spinboxes
        self.r_frame.update_milk_per_second()
        self.main.update_hovertips()
        self.cow_hovertip.showtip()
    
    def convert_milk(self):
        self.r_frame.update_milk(-50)
        self.r_frame.update_ice_cream(1)

    def get_factory(self):
        self.r_frame.update_ice_cream(-self.factory_cost) # ice cream will be deducted
        self.factory_num = self.factory_num + 1
        self.factory_activated_increase(1)
        self.factory['text'] = f'Factory ({self.factory_activated_num}/{self.factory_num})'
        self.factory_cost = round(self.factory_cost * 1.2, 2)
        self.main.available_sell()
        self.main.sell_factory_sp['to'] = self.factory_num # update selling spinboxes
        self.r_frame.update_milk_per_second()
        self.r_frame.update_ice_cream_per_second()
        self.update_hovertips()
        self.factory_hovertip.showtip()

    def factory_activated_increase(self, i):
        self.factory_activated_num = self.factory_activated_num + i
        self.factory['text'] = f'Factory ({self.factory_activated_num}/{self.factory_num})'
        self.r_frame.update_milk_per_second()
        self.r_frame.update_ice_cream_per_second()

    def get_vanilla_plantation(self):
        self.r_frame.update_ice_cream(-self.vanilla_plantation_cost) # ice cream will be deducted
        self.vanilla_plantation_num = self.vanilla_plantation_num + 1
        self.vanilla_plantation['text'] = f'Vanilla Plantation ({self.vanilla_plantation_num})'
        self.vanilla_plantation_cost = round(self.vanilla_plantation_cost * 1.24, 2)
        self.main.available_sell()
        self.main.sell_vanilla_plantation_sp['to'] = self.vanilla_plantation_num # update selling spinboxes
        self.i_frame.update_vanilla_spice_per_second()
        self.main.update_hovertips()
        self.vanilla_plantation_hovertip.showtip()

    def get_strawberry_field(self):
        self.r_frame.update_ice_cream(-self.strawberry_field_cost) # ice cream will be deducted
        self.strawberry_field_num = self.strawberry_field_num + 1
        self.strawberry_field['text'] = f'Strawberry Field ({self.strawberry_field_num})'
        self.strawberry_field_cost = round(self.strawberry_field_cost * 1.19, 2)
        self.main.available_sell()
        self.main.sell_strawberry_field_sp['to'] = self.strawberry_field_num # update selling spinboxes
        self.i_frame.update_strawberry_fruit_per_second()
        self.main.update_hovertips()
        self.strawberry_field_hovertip.showtip()

    def get_chocolate_processor(self):
        self.r_frame.update_ice_cream(-self.chocolate_processor_cost) # ice cream will be deducted
        self.chocolate_processor_num = self.chocolate_processor_num + 1
        self.chocolate_processor['text'] = f'Chocolate Processor ({self.chocolate_processor_num})'
        self.chocolate_processor_cost = round(self.chocolate_processor_cost * 1.29, 2)
        self.main.available_sell()
        self.main.sell_chocolate_processor_sp['to'] = self.chocolate_processor_num # update selling spinboxes
        self.i_frame.update_chocolate_food_per_second()
        self.main.update_hovertips()
        self.chocolate_processor_hovertip.showtip()

    


class MainApplication:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Simple incremental game')
        self.parent.eval('tk::PlaceWindow . center')
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.style = ttk.Style()
        self.text_font = font.nametofont('TkTextFont')

        # resource label booleans
        

        # resources frame
        self.r_frame = ResourceFrame(self.parent, self)
        self.r_frame.grid(column=0, row=0, padx=10, pady=5, sticky='NWES')

        # ingredient label booleans
        self.ingredients_text_visible = False
        self.vanilla_spice_text_visible = False
        self.strawberry_fruit_text_visible = False
        self.chocolate_food_text_visible = False

        # ingredients frame
        self.i_frame = IngredientFrame(self.r_frame, self)
        self.i_frame.grid(column=0, row=98, columnspan=3, pady=5, sticky='NWES')
        
        # create a notebook for holding tabs
        self.nb = ttk.Notebook(self.parent)
        self.nb.grid(column=1, row=0, rowspan=3, padx=10, pady=5, sticky='NE')

        self.cow_button_visible = False
        self.factory_button_visible = False
        self.strawberry_field_button_visible = False

        # control panel frame
        self.c_frame = ControlPanelFrame(self.nb, self)
        self.nb.add(self.c_frame, text='Control Panel')

        # TODO: powerup / bonuses frame? thinking of having these special upgrades to be in a separate frame, but
        #       they can still be in the control panel frame...

        # keeping ice cream buttons hidden until certain requirements are met
        self.i_c_tab_visible = False

        # ice cream frame
        self.i_c_frame = ttk.Frame(self.nb)
        self.nb.add(self.i_c_frame, text='Ice Cream', state='hidden') # unlock after getting fist vanilla (spice)
        # vanilla ice cream button
        self.vanilla_i_c_cost = 5 # default cost is 5 ice cream and
        self.vanilla_i_c_spice_cost = 3 # 3 vanilla spices
        self.vanilla_i_c_b = ttk.Button(self.i_c_frame, text='Vanilla Ice Cream', state='disabled', width=25, command=self.get_vanilla_i_c)
        self.vanilla_i_c_b.grid(column=0, row=1, padx=5, pady=5, sticky='W')
        self.vanilla_i_c_b_hovertip = Hovertip(self.vanilla_i_c_b, f'Produce vanilla ice cream\nCost:\n{self.vanilla_i_c_cost} ice cream\n{self.vanilla_i_c_spice_cost} vanilla (spice)', hover_delay=10)
        # strawberry ice cream button
        self.strawberry_i_c_cost = 5 # default cost is 5 ice cream and
        self.strawberry_i_c_fruit_cost = 4 # 4 strawberrry fruits
        self.strawberry_i_c_b = ttk.Button(self.i_c_frame, text='Strawberry Ice Cream', state='disabled', width=25, command=self.get_strawberry_i_c)
        self.strawberry_i_c_b.grid(column=0, row=2, padx=5, pady=5, sticky='W')
        self.strawberry_i_c_b_hovertip = Hovertip(self.strawberry_i_c_b, f'Produce strawberry ice cream\nCost:\n{self.strawberry_i_c_cost} ice cream\n{self.strawberry_i_c_fruit_cost} strawberry (fruit)', hover_delay=10)
        # chocolate ice cream button
        self.chocolate_i_c_cost = 5 # default cost is 5 ice cream and
        self.chocolate_i_c_food_cost = 5 # 5 chocolate food
        self.chocolate_i_c_b = ttk.Button(self.i_c_frame, text='Chocolate Ice Cream', state='disabled', width=25, command=self.get_chocolate_i_c)
        self.chocolate_i_c_b.grid(column=0, row=3, padx=5, pady=5, sticky='W')
        self.chocolate_i_c_b_hovertip = Hovertip(self.chocolate_i_c_b, f'Produce chocolate ice cream\nCost:\n{self.chocolate_i_c_cost} ice cream\n{self.chocolate_i_c_food_cost} chocolate (food)', hover_delay=10)
        # neapolitan ice cream button
        self.neapolitan_i_c_vanilla_cost = 3 # default costs 3 vanilla ice cream and
        self.neapolitan_i_c_strawberry_cost = 3 # 3 strawberry ice cream and
        self.neapolitan_i_c_chocolate_cost = 3 # 3 chocolate ice cream
        self.neapolitan_i_c_b = ttk.Button(self.i_c_frame, text='Neapolitan Ice Cream', state='disabled', width=25, command=self.get_neapolitan_i_c)
        self.neapolitan_i_c_b.grid(column=0, row=4, padx=5, pady=5, sticky='W')
        self.neapolitan_i_c_b_hovertip = Hovertip(self.neapolitan_i_c_b, f'Produce neapolitan ice cream\nCost\n{self.neapolitan_i_c_vanilla_cost} vanilla ice cream\n{self.neapolitan_i_c_strawberry_cost} strawberry ice cream\n{self.neapolitan_i_c_chocolate_cost} chocolate ice cream', hover_delay=10)

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

        # use buildings
        self.use_buildings()
        # keeping track of what is available to buy
        self.available_buy()

        # cheat button for testing new features, delete in final version
        self.cheat_b = ttk.Button(self.parent, text='Cheat increase', command=self.cheat)
        self.cheat_b.grid()

    # resource and ingredient related functions

    # hovertips

    def update_hovertips(self):
        # add more tips as we add more buldings
        # TODO: .showtip() is called in the function for the bulding after the new hovertip has been created
        #       .showtip() has to be called in the create function because the sell Button also uses .update_hovertips()
        #       This could be improved by having .showtip() be called here instead. The issue is how do we do that without
        #       the hovertip appearing when the sell Button is invoked?
        # c_frame hovertips
        self.c_frame.cow_hovertip.hidetip()
        self.c_frame.factory_hovertip.hidetip()
        self.c_frame.vanilla_plantation_hovertip.hidetip()
        self.c_frame.strawberry_field_hovertip.hidetip()
        self.c_frame.chocolate_processor_hovertip.hidetip()
        self.c_frame.cow_hovertip = Hovertip(self.c_frame.cow, f'Get a cow\nCost:\n{self.c_frame.cow_cost} milk\nEffects:\nIncrease milk per second: +0.63/s', hover_delay=10)
        self.c_frame.factory_hovertip = Hovertip(self.c_frame.factory, f"Converts milk to ice cream. Factories stop running\nif you don't have enough milk and continue\nrunning when you have enough.\nCost:\n{self.c_frame.factory_cost} ice cream\nEffects:\nMilk conversion: -{self.c_frame.factory_conversion_cost}/s\nIce cream conversion: +0.1/s", hover_delay=10)
        self.c_frame.vanilla_plantation_hovertip = Hovertip(self.c_frame.vanilla_plantation, f'Plantation for growing Vanilla planifolia\nCost:\n{self.c_frame.vanilla_plantation_cost} ice cream\nEffects:\nIncrease vanilla (spice) per second: +0.26/s', hover_delay=10)
        self.c_frame.strawberry_field_hovertip = Hovertip(self.c_frame.strawberry_field, f'Produces strawberries\nCost:\n{self.c_frame.strawberry_field_cost} ice cream\nEffects:\nIncrease strawberry (fruit) per second: +0.35/s', hover_delay=10)
        self.vchocolate_processor_hovertip = Hovertip(self.c_frame.chocolate_processor, f'Build facilities to order and process cocoa beans\nCost:\n{self.c_frame.chocolate_processor_cost} ice cream\nEffects:\nIncrease chocolate (food) per second: +0.15/s', hover_delay=10)
        # i_c_frame hovertips
        self.vanilla_i_c_b_hovertip.hidetip()
        self.strawberry_i_c_b_hovertip.hidetip()
        self.chocolate_i_c_b_hovertip.hidetip()
        self.neapolitan_i_c_b_hovertip.hidetip()
        self.vanilla_i_c_b_hovertip = Hovertip(self.vanilla_i_c_b, f'Produce vanilla ice cream\nCost:\n{self.vanilla_i_c_cost} ice cream\n{self.vanilla_i_c_spice_cost} vanilla (spice)', hover_delay=10)
        self.strawberry_i_c_b_hovertip = Hovertip(self.strawberry_i_c_b, f'Produce strawberry ice cream\nCost:\n{self.strawberry_i_c_cost} ice cream\n{self.strawberry_i_c_fruit_cost} strawberry (fruit)', hover_delay=10)
        self.chocolate_i_c_b_hovertip = Hovertip(self.chocolate_i_c_b, f'Produce chocolate ice cream\nCost:\n{self.chocolate_i_c_cost} ice cream\n{self.chocolate_i_c_food_cost} chocolate (food)', hover_delay=10)
        self.neapolitan_i_c_b_hovertip = Hovertip(self.neapolitan_i_c_b, f'Produce neapolitan ice cream\nCost\n{self.neapolitan_i_c_vanilla_cost} vanilla ice cream\n{self.neapolitan_i_c_strawberry_cost} strawberry ice cream\n{self.neapolitan_i_c_chocolate_cost} chocolate ice cream', hover_delay=10)

    # building / c_frame related functions

    

    def use_buildings(self):
        if self.c_frame.cow_num > 0:
            self.r_frame.update_milk(self.c_frame.cow_num * 0.63)
        if (self.c_frame.factory_activated_num > 0) and (self.r_frame.milk.get() >= self.c_frame.factory_activated_num * self.c_frame.factory_conversion_cost):
            self.r_frame.update_milk(self.c_frame.factory_activated_num * -self.c_frame.factory_conversion_cost)
            self.r_frame.update_ice_cream(self.c_frame.factory_activated_num * 0.1)
        if self.c_frame.vanilla_plantation_num > 0:
            self.i_frame.update_vanilla_spice(self.c_frame.vanilla_plantation_num * 0.26)
        if self.c_frame.strawberry_field_num > 0:
            self.i_frame.update_strawberry_fruit(self.c_frame.strawberry_field_num * 0.35)
        if self.c_frame.chocolate_processor_num > 0:
            self.i_frame.update_chocolate_food(self.c_frame.chocolate_processor_num * 0.15)
        self.parent.after(1000, self.use_buildings)

    # ice cream frame related functions

    def get_vanilla_i_c(self):
        self.r_frame.update_ice_cream(-self.vanilla_i_c_cost) # deduct ice cream
        self.i_frame.update_vanilla_spice(-self.vanilla_i_c_spice_cost) # deduct vanilla (spice)
        self.r_frame.update_vanilla_i_c(1)

    def get_strawberry_i_c(self):
        self.r_frame.update_ice_cream(-self.strawberry_i_c_cost) # deduct ice cream
        self.i_frame.update_strawberry_fruit(-self.strawberry_i_c_fruit_cost) # deduct strawberry (fruit)
        self.r_frame.update_strawberry_i_c(1)

    def get_chocolate_i_c(self):
        self.r_frame.update_ice_cream(-self.chocolate_i_c_cost) # deduct ice cream
        self.i_frame.update_chocolate_food(-self.chocolate_i_c_food_cost) # deduct chocolate (food)
        self.r_frame.update_chocolate_i_c(1)
    
    def get_neapolitan_i_c(self):
        self.r_frame.update_vanilla_i_c(-self.neapolitan_i_c_vanilla_cost) # deduct vanilla ice cream
        self.r_frame.update_strawberry_i_c(-self.neapolitan_i_c_strawberry_cost) # deduct strawberry ice cream
        self.r_frame.update_chocolate_i_c(-self.neapolitan_i_c_chocolate_cost) # deduct chocolate ice cream
        self.r_frame.update_neapolitan_i_c(1)

    # availability stuff

    def available_buy(self):
        # disable the buttons that are too expensive
        # add an if-else statement for every new thing that we create
        # c_frame
        # std gen
        if self.r_frame.milk.get() >= self.c_frame.cow_cost:
            self.c_frame.cow.state(['!disabled'])
        else:
            self.c_frame.cow.state(['disabled'])
        # convert milk
        if self.r_frame.milk.get() >= 50:
            self.c_frame.convert_b.state(['!disabled'])
        else:
            self.c_frame.convert_b.state(['disabled'])
        # factory
        if self.r_frame.ice_cream.get() >= self.c_frame.factory_cost:
            self.c_frame.factory.state(['!disabled'])
        else:
            self.c_frame.factory.state(['disabled'])
        if self.c_frame.factory_num > 0 and self.c_frame.factory_activated_num < self.c_frame.factory_num:
            # maximum number of factories activated
            self.c_frame.factory_activated_up_b.state(['!disabled'])
        elif self.c_frame.factory_num > 0 and self.c_frame.factory_activated_num >= self.c_frame.factory_num:
            # maximum number of factories activated not reached yet
            self.c_frame.factory_activated_up_b.state(['disabled'])
        if self.c_frame.factory_num > 0 and self.c_frame.factory_activated_num > 0:
            # more than 0 activated factories
            self.c_frame.factory_activated_down_b.state(['!disabled'])
        elif self.c_frame.factory_num > 0 and self.c_frame.factory_activated_num <= 0:
            # 0 activated factories
            self.c_frame.factory_activated_down_b.state(['disabled'])
        # vanilla plantation
        if self.r_frame.ice_cream.get() >= self.c_frame.vanilla_plantation_cost:
            self.c_frame.vanilla_plantation.state(['!disabled'])
        else:
            self.c_frame.vanilla_plantation.state(['disabled'])
        # strawberry field
        if self.r_frame.ice_cream.get() >= self.c_frame.strawberry_field_cost:
            self.c_frame.strawberry_field.state(['!disabled'])
        else:
            self.c_frame.strawberry_field.state(['disabled'])
        # chocolate processor
        if self.r_frame.ice_cream.get() >= self.c_frame.chocolate_processor_cost:
            self.c_frame.chocolate_processor.state(['!disabled'])
        else:
            self.c_frame.chocolate_processor.state(['disabled'])

        # i_c_frame
        # vanilla ice cream
        if (self.r_frame.ice_cream.get() >= self.vanilla_i_c_cost) and (self.i_frame.vanilla_spice.get() >= self.vanilla_i_c_spice_cost):
            self.vanilla_i_c_b.state(['!disabled'])
        else:
            self.vanilla_i_c_b.state(['disabled'])
        # strawberry ice crema
        if (self.r_frame.ice_cream.get() >= self.strawberry_i_c_cost) and (self.i_frame.strawberry_fruit.get() >= self.strawberry_i_c_fruit_cost):
            self.strawberry_i_c_b.state(['!disabled'])
        else:
            self.strawberry_i_c_b.state(['disabled'])
        # chocolate ice cream
        if (self.r_frame.ice_cream.get() >= self.chocolate_i_c_cost) and (self.i_frame.chocolate_food.get() >= self.chocolate_i_c_food_cost):
            self.chocolate_i_c_b.state(['!disabled'])
        else:
            self.chocolate_i_c_b.state(['disabled'])
        # neapolitan ice cream
        if (self.r_frame.vanilla_i_c.get() >= self.neapolitan_i_c_vanilla_cost and self.r_frame.strawberry_i_c.get() >= self.neapolitan_i_c_strawberry_cost and
                self.r_frame.chocolate_i_c.get() >= self.neapolitan_i_c_chocolate_cost):
            self.neapolitan_i_c_b.state(['!disabled'])
        else:
            self.neapolitan_i_c_b.state(['disabled'])
    
        self.parent.after(10, self.available_buy)

    # sell_frame stuff

    def available_sell(self):
        # called when a new building that can be sold is bought
        # makes Sell tab visible and makes selling spinboxes visible
        # labels and spinboxes - everytime we add a new building, we need to add a new spinbox in its get function
        # in the future, the state of the Spinboxes can be changed if validation is implemented
        if not self.sell_tab_visible:
            self.nb.tab(2, state='normal')
            self.sell_tab_visible = True
        if not self.sell_cow_sp_visible and self.c_frame.cow_num > 0:
            ttk.Label(self.sell_frame, text='Cow').grid(column=0, row=0)
            self.sell_cow_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.c_frame.cow_num, textvariable=self.sell_cow_num, state=['readonly'])
            self.sell_cow_sp.grid(column=1, row=0, padx=5, pady=5)
            self.sell_cow_sp_visible = True
        if not self.sell_factory_sp_visible and self.c_frame.factory_num > 0:
            ttk.Label(self.sell_frame, text='Factory').grid(column=0, row=1)
            self.sell_factory_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.c_frame.factory_num, textvariable=self.sell_factory_num, state=['readonly'])
            self.sell_factory_sp.grid(column=1, row=1, padx=5, pady=5)
            self.sell_factory_sp_visible = True
        if not self.sell_vanilla_plantation_sp_visible and self.c_frame.vanilla_plantation_num > 0:
            ttk.Label(self.sell_frame, text='Vanilla Plantation').grid(column=0, row=2)
            self.sell_vanilla_plantation_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.c_frame.vanilla_plantation_num, textvariable=self.sell_vanilla_plantation_num, state=['readonly'])
            self.sell_vanilla_plantation_sp.grid(column=1, row=2, padx=5, pady=5)
            self.sell_vanilla_plantation_sp_visible = True
        if not self.sell_strawberry_field_sp_visible and self.c_frame.strawberry_field_num > 0:
            ttk.Label(self.sell_frame, text='Strawberry Field').grid(column=0, row=3)
            self.sell_strawberry_field_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.c_frame.strawberry_field_num, textvariable=self.sell_strawberry_field_num, state=['readonly'])
            self.sell_strawberry_field_sp.grid(column=1, row=3, padx=5, pady=5)
            self.sell_strawberry_field_sp_visible = True
        if not self.sell_chocolate_processor_sp_visible and self.c_frame.chocolate_processor_num > 0:
            ttk.Label(self.sell_frame, text='Chocolate Processor').grid(column=0, row=4)
            self.sell_chocolate_processor_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.c_frame.chocolate_processor_num, textvariable=self.sell_chocolate_processor_num, state=['readonly'])
            self.sell_chocolate_processor_sp.grid(column=1, row=4, padx=5, pady=5)
            self.sell_chocolate_processor_sp_visible = True

    def sell(self):
        # current plan is to add a for loop for every new building we think of, but
        # this seems really inefficient, there must be a better way of doing this
        for i in range(self.sell_cow_num.get()):
            self.c_frame.cow_cost = round(self.c_frame.cow_cost / 1.12, 2) # update the cost
            self.c_frame.cow_num = self.c_frame.cow_num - 1 # update number of cows
            if self.c_frame.cow_num != 0:
                self.c_frame.cow['text'] = f'Cow ({self.c_frame.cow_num})'
            else:
                self.c_frame.cow['text'] = 'Cow'
            self.sell_cow_sp['to'] = self.c_frame.cow_num
            self.sell_cow_sp.set(0)
            self.r_frame.update_milk(self.c_frame.cow_cost) # update number of milk
        for i in range(self.sell_factory_num.get()):
            self.c_frame.factory_cost = round(self.c_frame.factory_cost / 1.2, 2) # update the cost
            self.c_frame.factory_num = self.c_frame.factory_num - 1 # update number of factories
            if self.c_frame.factory_activated_num > self.c_frame.factory_num:
                self.c_frame.factory_activated_num = self.c_frame.factory_activated_num - 1
            if self.c_frame.factory_num != 0:
                self.c_frame.factory['text'] = f'Factory ({self.c_frame.factory_activated_num}/{self.c_frame.factory_num})'
            else:
                self.c_frame.factory['text'] = 'Factory'
            self.sell_factory_sp['to'] = self.c_frame.factory_num
            self.sell_factory_sp.set(0)
            self.r_frame.update_ice_cream(self.c_frame.factory_cost) # update number of ice cream
        for i in range(self.sell_vanilla_plantation_num.get()):
            self.c_frame.vanilla_plantation_cost = round(self.c_frame.vanilla_plantation_cost / 1.24, 2) # update the cost
            self.c_frame.vanilla_plantation_num = self.c_frame.vanilla_plantation_num - 1 # update number of vanilla plantations
            if self.c_frame.vanilla_plantation_num != 0:
                self.c_frame.vanilla_plantation['text'] = f'Vanilla Plantation ({self.c_frame.vanilla_plantation_num})'
            else:
                self.c_frame.vanilla_plantation['text'] = 'Vanilla Plantation'
            self.sell_vanilla_plantation_sp['to'] = self.c_frame.vanilla_plantation_num
            self.sell_vanilla_plantation_sp.set(0)
            self.r_frame.update_ice_cream(self.c_frame.vanilla_plantation_cost) # update number of ice cream
        for i in range(self.sell_strawberry_field_num.get()):
            self.c_frame.strawberry_field_cost = round(self.c_frame.strawberry_field_cost / 1.19, 2) # update the cost
            self.c_frame.strawberry_field_num = self.c_frame.strawberry_field_num - 1 # update number of vstrawberry fields
            if self.c_frame.strawberry_field_num != 0:
                self.c_frame.strawberry_field['text'] = f'Strawberry Field ({self.c_frame.strawberry_field_num})'
            else:
                self.c_frame.strawberry_field['text'] = 'Strawberry Field'
            self.sell_strawberry_field_sp['to'] = self.c_frame.strawberry_field_num
            self.sell_strawberry_field_sp.set(0)
            self.r_frame.update_ice_cream(self.c_frame.strawberry_field_cost) # update number of ice cream
        for i in range(self.sell_chocolate_processor_num.get()):
            self.c_frame.chocolate_processor_cost = round(self.c_frame.chocolate_processor_cost / 1.29, 2) # update the cost
            self.c_frame.chocolate_processor_num = self.c_frame.chocolate_processor_num - 1 # update number of chocolate processors
            if self.c_frame.chocolate_processor_num != 0:
                self.c_frame.chocolate_processor['text'] = f'Chocolate Processor ({self.c_frame.chocolate_processor_num})'
            else:
                self.c_frame.chocolate_processor['text'] = 'Chocolate Processor'
            self.sell_chocolate_processor_sp['to'] = self.c_frame.chocolate_processor_num
            self.sell_chocolate_processor_sp.set(0)
            self.r_frame.update_ice_cream(self.c_frame.chocolate_processor_cost) # update number of ice cream
        self.r_frame.update_milk_per_second()
        self.r_frame.update_ice_cream_per_second()
        self.i_frame.update_vanilla_spice_per_second()
        self.i_frame.update_strawberry_fruit_per_second()
        self.i_frame.update_chocolate_food_per_second()
        self.update_hovertips()
    
    def cheat(self):
        i = 100
        self.r_frame.update_milk(i)
        self.r_frame.update_ice_cream(i)
        self.i_frame.update_vanilla_spice(i)
        self.i_frame.update_strawberry_fruit(i)
        self.i_frame.update_chocolate_food(i)


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()