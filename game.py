"""
Incremental game - GUI project
Layout idea and the standard points generator is modeled on https://kittensgame.com/web/#
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

        # resources frame
        self.r_frame = ttk.Frame(self.parent)
        self.r_frame.grid(column=0, row=0, padx=10, pady=5, sticky='NWES')
        # resources
        ttk.Label(self.r_frame, text='Resources', width=30).grid(column=0, row=0, columnspan=3)
        # milk
        self.milk = tk.DoubleVar()
        ttk.Label(self.r_frame, text='Milk').grid(column=0, row=1, sticky='W')
        self.milk_label = ttk.Label(self.r_frame, textvariable=self.milk)
        self.milk_label.grid(column=1, row=1, sticky='W')
        # milk per second
        self.milk_per_second = tk.StringVar()
        self.milk_per_second_lb = ttk.Label(self.r_frame, textvariable=self.milk_per_second)
        self.milk_per_second_lb.grid(column=2, row=1, sticky='W')
        # ice cream
        self.ice_cream = tk.DoubleVar()
        ttk.Label(self.r_frame, text='Ice Cream').grid(column=0, row=2, sticky='W')
        self.ice_cream_label = ttk.Label(self.r_frame, textvariable=self.ice_cream)
        self.ice_cream_label.grid(column=1, row=2, sticky='W')
        # TODO: maybe make a hovertip over the milk per second label to show where the milk per second are coming from
        # bonuses / combos
        # TODO: add new labels for combos or bonuses

        # create a notebook for holding tabs
        self.nb = ttk.Notebook(self.parent)
        self.nb.grid(column=1, row=0, padx=10, pady=5, sticky='NE')

        # control panel frame
        self.c_frame = ttk.Frame(self.nb)
        self.nb.add(self.c_frame, text='Control Panel')
        # button for collecting milk
        self.collect_b = ttk.Button(self.c_frame, text='Collect', width=25, command=lambda: self.update_milk(1))
        self.collect_b.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        self.collect_b_hovertip = Hovertip(self.collect_b, 'Collect some milk...', hover_delay=10)
        # cow
        self.cow_num = 0
        self.cow_cost = 10 # default cost is 10
        self.cow = ttk.Button(self.c_frame, text='Cow', state='disabled', width=25, command=self.get_cow)
        self.cow.grid(column=0, row=1, padx=5, pady=5, sticky='E')
        self.cow_hovertip = Hovertip(self.cow, f'Get a cow\nCost: {self.cow_cost}\nIncrease milk per second: +0.63/s', hover_delay=10)
        self.use_cow()
        # convert milk to ice cream
        self.convert_b = ttk.Button(self.c_frame, text='Make ice cream', width=25, command=self.convert_milk)
        self.convert_b.grid(column=1, row=0, padx=5, pady=5, sticky='E')
        self.convert_b_hovertip = Hovertip(self.convert_b, 'Uses milk to create ice cream\nCost: 50', hover_delay=10)
        # TODO: add more stuff to buy here!!

        # keeping track of what is available to buy
        self.available_buy()

        # TODO: powerup / bonuses frame? thinking of having these special upgrades to be in a separate frame, but
        #       they can still be in the control panel frame...

        # selling frame
        self.sell_frame = ttk.Frame(self.nb)
        self.nb.add(self.sell_frame, text='Sell')
        # labels and spinboxes - everytime we add a new building, we need to add a new spinbox
        ttk.Label(self.sell_frame, text='Cow').grid(column=0, row=0)
        self.sell_cow_num = tk.IntVar()
        self.sell_cow_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.cow_num, textvariable=self.sell_cow_num)
        self.sell_cow_sp.grid(column=1, row=0, padx=5, pady=5)
        # sell button
        self.sell_button = ttk.Button(self.sell_frame, text='Sell', command=self.sell)
        self.sell_button.grid(column=1, row=1, pady=5) # every time we add a new spinbox, this row number needs to increase

    def update_milk(self, p):
        self.milk.set(round(self.milk.get() + p, 2))

    def update_milk_per_second(self):
        total = round(self.cow_num * 0.63, 2) # this number needs to expand as we add more buildings
        if total != 0:
            self.milk_per_second.set(f'+{total}/s')
        else:
            self.milk_per_second.set('')

    def update_hovertips(self):
        # add more tips as we add more buldings
        # TODO: .showtip() is called in the function for the bulding after the new hovertip has been created
        #       .showtip() has to be called in the create function because the sell Button also uses .update_hovertips()
        #       This could be improved by having .showtip() be called here instead. The issue is how do we do that without
        #       the hovertip appearing when the sell Button is invoked?
        self.cow_hovertip.hidetip()
        self.cow_hovertip = Hovertip(self.cow, f'Get a cow\nCost: {self.cow_cost}\nIncrease milk per second: +0.63/s', hover_delay=10)

    def get_cow(self):
        self.update_milk(-self.cow_cost) # milk will be deducted
        self.cow_num = self.cow_num + 1
        self.cow['text'] = f'Cow ({self.cow_num})'
        self.cow_cost = round(self.cow_cost * 1.12, 2)
        self.sell_cow_sp['to'] = self.cow_num # update selling spinboxes
        self.update_milk_per_second()
        self.update_hovertips()
        self.cow_hovertip.showtip()

    def use_cow(self):
        self.update_milk(self.cow_num * 0.63)
        self.parent.after(1000, self.use_cow)
    
    def convert_milk(self):
        self.update_milk(-50)
        self.ice_cream.set(self.ice_cream.get() + 1)


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
        self.parent.after(10, self.available_buy)

    def sell(self):
        # current plan is to add a for loop for every new building we think of, but
        # this seems really inefficient, there must be a better way of doing this
        for i in range(self.sell_cow_num.get()):
            self.cow_cost = round(self.cow_cost / 1.12, 2) # update the cost
            self.cow_num = self.cow_num - 1 # update number of cows
            self.cow['text'] = f'Cow ({self.cow_num})'
            self.sell_cow_sp['to'] = self.cow_num
            self.sell_cow_sp.set(0)
            self.update_milk(self.cow_cost) # update number of milk
        self.update_milk_per_second()
        self.update_hovertips()


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()