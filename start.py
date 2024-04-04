import tkinter
from tkinter import *
from tkinter import ttk

from core.services.binance.binance_service import BinanceService
from ui.theme.style import Style

binance_service = BinanceService()
root = Tk()
root.title("Tranquill")
root.option_add("*tearOff", False)

Style.apply_style(root)

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.columnconfigure(index=3, weight=1)
root.columnconfigure(index=4, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
root.rowconfigure(index=3, weight=1)
root.rowconfigure(index=4, weight=1)


def draw_portfolio_content():
    portfolio_paned_window = ttk.PanedWindow(root)
    portfolio_paned_window.grid(row=1, column=0, pady=(25, 5), sticky="nsew", rowspan=3)

    # Pane #1
    portfolio_frame = ttk.Frame(portfolio_paned_window)
    portfolio_paned_window.add(portfolio_frame, weight=1)

    # Create a Frame for the Treeview
    portfolio_tree_frame = ttk.Frame(portfolio_frame)
    portfolio_tree_frame.pack(expand=True, fill="both")

    # Scrollbar
    portfolio_tree_scroll = ttk.Scrollbar(portfolio_tree_frame)
    portfolio_tree_scroll.pack(side="right", fill="y")

    # Treeview
    portfolio_tree_view = ttk.Treeview(portfolio_tree_frame,
                                       selectmode="extended",
                                       yscrollcommand=portfolio_tree_scroll.set,
                                       columns=(1, 2, 3, 4, 5, 6, 7),
                                       height=12)
    portfolio_tree_view.pack(expand=True, fill="both")
    portfolio_tree_scroll.config(command=portfolio_tree_view.yview)

    # Treeview columns
    portfolio_tree_view.column("#0", width=120)
    portfolio_tree_view.column(1, anchor=tkinter.W, width=120)
    portfolio_tree_view.column(2, anchor=tkinter.W, width=120)
    portfolio_tree_view.column(3, anchor=tkinter.W, width=120)
    portfolio_tree_view.column(4, anchor=tkinter.W, width=120)
    portfolio_tree_view.column(5, anchor=tkinter.W, width=120)
    portfolio_tree_view.column(6, anchor=tkinter.W, width=120)
    portfolio_tree_view.column(7, anchor=tkinter.W, width=120)

    # Treeview headings
    portfolio_tree_view.heading("#0", text="Asset", anchor=tkinter.W)
    portfolio_tree_view.heading(1, text="Free", anchor=tkinter.W)
    portfolio_tree_view.heading(2, text="Locked", anchor=tkinter.W)
    portfolio_tree_view.heading(3, text="In USDT", anchor=tkinter.W)
    portfolio_tree_view.heading(4, text="Avg Price", anchor=tkinter.W)
    portfolio_tree_view.heading(5, text="Current Price", anchor=tkinter.W)
    portfolio_tree_view.heading(6, text="PNL (%)", anchor=tkinter.W)
    portfolio_tree_view.heading(7, text="Profit (USDT)", anchor=tkinter.W)

    binance_data = binance_service.get_assets()

    for asset in binance_data:
        portfolio_tree_view.insert(parent='', index='end', iid=asset['index'], text=asset['text'], values=asset['values'])
    # Insert treeview data
    # for item in treeview_data:
    #     treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
    #     if item[0] == "" or item[2] in (8, 12):
    #         treeview.item(item[2], open=True) # Open parents

    # Select and scroll
    portfolio_tree_view.selection_set(0)
    portfolio_tree_view.see(0)


def draw_left_panel():
    tabs_paned_window = ttk.PanedWindow(root)
    tabs_paned_window.grid(row=0, column=0, sticky="nsew")
    tabs_frame = ttk.Frame(tabs_paned_window)
    tabs_paned_window.add(tabs_frame, weight=3)

    tabs_notebook = ttk.Notebook(tabs_frame)
    # Tab #1
    tab_11 = ttk.Frame(tabs_notebook)
    tab_11.columnconfigure(index=0, weight=1)
    tab_11.columnconfigure(index=1, weight=1)
    tab_11.rowconfigure(index=0, weight=1)
    tab_11.rowconfigure(index=1, weight=1)
    tabs_notebook.add(tab_11, text="Portfolio")

    draw_portfolio_content()

    # Tab #2
    tab_21 = ttk.Frame(tabs_notebook)
    tabs_notebook.add(tab_21, text="Tab C")

    # Tab #3
    tab_31 = ttk.Frame(tabs_notebook)
    tabs_notebook.add(tab_31, text="Tab V")

    tabs_notebook.pack(expand=True, fill="both")


draw_left_panel()

# Sizegrip
sizegrip = ttk.Sizegrip(root)
sizegrip.grid(row=300, column=500, padx=(0, 5), pady=(0, 5))

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# Start the main loop
root.mainloop()
