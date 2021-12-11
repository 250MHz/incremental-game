# incremental-game
An incremental game about ice cream for GUI project by Section 4's Group 10.  

## Installing

This project is written in Python 3 and uses Tkinter from the Python standard library.  
The game uses a widget added in Tk 8.6. Follow [this tutorial](https://tkdocs.com/tutorial/install.html) to install Tcl/Tk if you don't have Tcl/Tk or have an older version.

## Running

Start the game with `py game.py` in the directory where both `game.py` and `tooltip.py` are located.

## Playing

* Click on the "Collect" button under the Control Panel to start collecting resources. Hover over buttons to see the cost needed to use a button and the effect of buying something.  
* Upon making your first ice cream, an "Ice Cream" tab will appear. Different ice cream flavors require different resources and ingredients to create. The radiobuttons under "Controls" control the number of ice creams to be converted at a time.  
* Upon buying a building that can be sold, a "Sell" tab will appear. Set the spinboxes to the value you want to sell for each building, then click on "Sell".  
* The achievement tab displays possible achievements. Reaching an achievement will automatically show that it has been reached. Each achievement increases the "achievement bonus" by a small percentage. This bonus increases the number of ice cream you get from converting ingredients and resources to ice cream.

New buildings to buy and ice creams to create will be available as you progress.

## Credits

* General concept of the game, the layout, and the buildings are heavily inspired from ideas in [Kittens Game by bloodrizer](https://kittensgame.com/web/)  
* Achievement tab is modeled off the "Achievements" menu in [PokéClicker](https://www.pokeclicker.com/)  
* `tooltip.py` is modified from [idlelib's `tooltip.py`](https://github.com/python/cpython/blob/main/Lib/idlelib/tooltip.py) in the Python Standard Library
