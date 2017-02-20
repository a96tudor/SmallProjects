"""
This is a frontend for a bookshop application.

The user can :
    - View all records
    - Search an entry
    - Add entry
    - Update entry
    - Delete entry
"""

from tkinter import *

class BookshopGUI:

    def __init__(self, master):
        """
                CONSTRUCTOR
        :param master:      The Tk object that we use to build our GUI
        """
        self.master = master
        self.init_objects()

    def init_objects(self):
        """
            Initialises the initial states of the objects from the GUI
        :return:    -
        """

        # setting up labels
        lb_title = Label(master=self.master, text="Title")
        lb_title.grid(row=0, column=0)

        lb_year = Label(master=self.master, text="Year")
        lb_year.grid(row=1, column=0)

        lb_author = Label(master=self.master, text="Author")
        lb_author.grid(row=0, column=2)

        lb_ISBN = Label(master=self.master, text="ISBN")
        lb_ISBN.grid(row=1, column=2)

        # setting up edit boxes
        var_title = StringVar()
        bx_title = Entry(master=self.master, textvariable=var_title)
        bx_title.grid(row=0, column=1)

        var_year = StringVar()
        bx_year= Entry(master=self.master, textvariable=var_year)
        bx_year.grid(row=1, column=1)

        var_author = StringVar()
        bx_author = Entry(master=self.master, textvariable=var_author)
        bx_author.grid(row=0, column=3)

        var_ISBN = StringVar()
        bx_ISBN = Entry(master=self.master, textvariable=var_ISBN)
        bx_ISBN.grid(row=1, column=3)

        # adding the listbox
        list_box = Listbox(master=self.master, height=6, width=35)
        list_box.grid(row=2, column=0, rowspan=6, columnspan=2)

        #creating the scrollbar
        scroll_bar = Scrollbar()
        scroll_bar.grid(row=2, column=2, rowspan=6)

        #connecting the listbox and the scrollbar
        list_box.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.configure(command=list_box.yview )

        #setting up the buttons
        bt_view = Button(master=self.master, text="View all", width=12)
        bt_view.grid(row=2, column=3)

        bt_search = Button(master=self.master, text="Search entry", width=12)
        bt_search.grid(row=3, column=3)

        bt_add = Button(master=self.master, text="Add entry", width=12)
        bt_add.grid(row=4, column=3)

        bt_update = Button(master=self.master, text="Update", width=12)
        bt_update.grid(row=5, column=3)

        bt_del = Button(master=self.master, text="Delete", width=12)
        bt_del.grid(row=6, column=3)

        bt_close = Button(master=self.master, text="Close", width=12)
        bt_close.grid(row=7, column=3)


if __name__ == "__main__":
    # I run the app
    root = Tk()
    gui = BookshopGUI(root)
    root.mainloop()