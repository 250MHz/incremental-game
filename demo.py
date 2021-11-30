"""
Demo for our incremental game showing basic layout and mechanics
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
        # points
        self.points = tk.DoubleVar()
        ttk.Label(self.r_frame, text='Points').grid(column=0, row=1, sticky='W')
        self.points_label = ttk.Label(self.r_frame, textvariable=self.points)
        self.points_label.grid(column=1, row=1, sticky='W')
        # points per second
        self.points_per_second = tk.StringVar()
        self.points_per_second_lb = ttk.Label(self.r_frame, textvariable=self.points_per_second)
        self.points_per_second_lb.grid(column=2, row=1, sticky='W')
        # TODO: maybe make a hovertip over the points per second label to show where the points per second are coming from
        # bonuses / combos
        # TODO: add new labels for combos or bonuses

        # create a notebook for holding tabs
        self.nb = ttk.Notebook(self.parent)
        self.nb.grid(column=1, row=0, padx=10, pady=5, sticky='NE')

        # control panel frame
        self.c_frame = ttk.Frame(self.nb)
        self.nb.add(self.c_frame, text='Control Panel')
        # button for gathering points
        self.gather_b = ttk.Button(self.c_frame, text='Gather', width=25, command=lambda: self.update_points(1))
        self.gather_b.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        # standard point generator
        self.std_gen_num = 0
        self.std_gen_cost = 10 # default cost is 10
        self.std_gen = ttk.Button(self.c_frame, text='Standard Generator', state='disabled', width=25, command=self.create_std_gen)
        self.std_gen.grid(column=1, row=0, padx=5, pady=5, sticky='E')
        self.std_gen_hovertip = Hovertip(self.std_gen, f'Create a standard point generator\nCost: {self.std_gen_cost}\nIncrease points per second: +0.63/s', hover_delay=10)
        self.use_std_gen()
        # TODO: add more stuff to buy here!!

        # keeping track of what is available to buy
        self.available_buy()

        # TODO: powerup / bonuses frame? thinking of having these special upgrades to be in a separate frame, but
        #       they can still be in the control panel frame...

        # selling frame
        self.sell_frame = ttk.Frame(self.nb)
        self.nb.add(self.sell_frame, text='Sell')
        # labels and spinboxes - everytime we add a new building, we need to add a new spinbox
        ttk.Label(self.sell_frame, text='Standard Generator').grid(column=0, row=0)
        self.sell_std_gen_num = tk.IntVar()
        self.sell_std_gen_sp = ttk.Spinbox(self.sell_frame, from_=0.0, to=self.std_gen_num, textvariable=self.sell_std_gen_num)
        self.sell_std_gen_sp.grid(column=1, row=0, padx=5, pady=5)
        # sell button
        self.sell_button = ttk.Button(self.sell_frame, text='Sell', command=self.sell)
        self.sell_button.grid(column=1, row=1, pady=5) # every time we add a new spinbox, this row number needs to increase

    def update_points(self, p):
        self.points.set(round(self.points.get() + p, 2))

    def update_points_per_second(self):
        total = round(self.std_gen_num * 0.63, 2) # this number needs to expand as we add more buildings
        if total != 0:
            self.points_per_second.set(f'+{total}/s')
        else:
            self.points_per_second.set('')

    def update_hovertips(self):
        # add more tips as we add more buldings
        # TODO: .showtip() is called in the function for the bulding after the new hovertip has been created
        #       .showtip() has to be called in the create function because the sell Button also uses .update_hovertips()
        #       This could be improved by having .showtip() be called here instead. The issue is how do we do that without
        #       the hovertip appearing when the sell Button is invoked?
        self.std_gen_hovertip.hidetip()
        self.std_gen_hovertip = Hovertip(self.std_gen, f'Create a standard point generator\nCost: {self.std_gen_cost}\nIncrease points per second: +0.63/s', hover_delay=10)

    def create_std_gen(self):
        self.update_points(-self.std_gen_cost) # points will be deducted
        self.std_gen_num = self.std_gen_num + 1
        self.std_gen['text'] = f'Standard Generator ({self.std_gen_num})'
        self.std_gen_cost = round(self.std_gen_cost * 1.12, 2)
        self.sell_std_gen_sp['to'] = self.std_gen_num # update selling spinboxes
        self.update_points_per_second()
        self.update_hovertips()
        self.std_gen_hovertip.showtip()

    def use_std_gen(self):
        self.update_points(self.std_gen_num * 0.63)
        self.parent.after(1000, self.use_std_gen)

    def available_buy(self):
        # disable the buttons that are too expensive
        # add an if-else statement for every new thing that we create
        if self.points.get() >= self.std_gen_cost:
            self.std_gen.state(['!disabled'])
        else:
            self.std_gen.state(['disabled'])
        self.parent.after(10, self.available_buy)

    def sell(self):
        # current plan is to add a for loop for every new building we think of, but
        # this seems really inefficient, there must be a better way of doing this
        for i in range(self.sell_std_gen_num.get()):
            self.std_gen_cost = round(self.std_gen_cost / 1.12, 2) # update the cost
            self.std_gen_num = self.std_gen_num - 1 # update number of standard generators
            self.std_gen['text'] = f'Standard Generator ({self.std_gen_num})'
            self.sell_std_gen_sp['to'] = self.std_gen_num
            self.sell_std_gen_sp.set(0)
            self.update_points(self.std_gen_cost) # update number of points
        self.update_points_per_second()
        self.update_hovertips()


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()