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
from tkinter.messagebox import *
import back_end as be

class BookshopGUI:

    def __init__(self, master):
        """
                CONSTRUCTOR
        :param master:      The Tk object that we use to build our GUI
        """
        self.master = master
        self._db = be.Database("bookshop.db")

        self._vars = {
            "title" : StringVar(),
            "ISBN" : StringVar(),
            "author" : StringVar(),
            "year" : StringVar()
        }

        self._list_box = Listbox(master=self.master, height=6, width=35)

        self._init_objects()

    def _init_objects(self):
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

        bx_title = Entry(master=self.master, textvariable=self._vars["title"])
        bx_title.grid(row=0, column=1)

        bx_year= Entry(master=self.master, textvariable=self._vars["year"])
        bx_year.grid(row=1, column=1)

        bx_author = Entry(master=self.master, textvariable=self._vars["author"])
        bx_author.grid(row=0, column=3)

        bx_ISBN = Entry(master=self.master, textvariable=self._vars["ISBN"])
        bx_ISBN.grid(row=1, column=3)

        # adding the listbox
        self._list_box.grid(row=2, column=0, rowspan=6, columnspan=2)

        #creating the scrollbar
        scroll_bar = Scrollbar()
        scroll_bar.grid(row=2, column=2, rowspan=6)

        #connecting the listbox and the scrollbar
        self._list_box.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.configure(command=self._list_box.yview )

        #setting up the buttons
        bt_view = Button(master=self.master, text="View all", width=12, command=self.view_all)
        bt_view.grid(row=2, column=3)

        bt_search = Button(master=self.master, text="Search entry", width=12)
        bt_search.grid(row=3, column=3)

        bt_add = Button(master=self.master, text="Add entry", width=12, command=self.insert_entry)
        bt_add.grid(row=4, column=3)

        bt_update = Button(master=self.master, text="Update", width=12)
        bt_update.grid(row=5, column=3)

        bt_del = Button(master=self.master, text="Delete", width=12)
        bt_del.grid(row=6, column=3)

        bt_close = Button(master=self.master, text="Close", width=12)
        bt_close.grid(row=7, column=3)

    def _print_message(self, msg, error = False):
        """

        :param msg:         The message to print
        :param error:       True - if it is an error message
                            False - otherwise
        :return:
        """
        showerror("ERROR", msg)

    def _reset_fields(self):
        """
            function that resets the input fields
        :return:
        """
        for key in self._vars:
            self._vars[key].set("")

    def _update_list_box(self, new_list):
        """
            Updates the listbox with the contents of the new list
        :param new_list:        The new contents to be written in the listbox
        :return:                -
        """
        self._list_box.delete(0) #clearing the list

        #putting the new elements in
        for entry in new_list:
            string = "(" + str(entry[0]) + ") " + \
                str(entry[1]) + ", " + \
                str(entry[2]) + ", " + \
                str(entry[3]) + "," + \
                str(entry[4])
            self._list_box.insert(END, string)

    def view_all(self):
        """
            uses the Database object to read all the entries and then display them
        in the list box
        :return:    -
        """
        entries = self._db.fetch()
        self._update_list_box(new_list=entries)

    def insert_entry(self):
        """
            Processes the inputs and sends them to the db
        :return: -
        """
        self._print_message("This is just a test message")
        to_insert = dict()
        try:
            year = int(self._vars["year"].get())
            to_insert["year"] = year
        except ValueError:
            print("error")
            return

        for key in self._vars:
            if key != "year":
                if self._vars[key].get() != "":
                    to_insert[key] = self._vars[key].get()
                else:
                    print("error")
                    return

        success = self._db.insert(to_insert)

        if (success):
            self._reset_fields()
        else:
            print("error")

if __name__ == "__main__":
    # I run the app
    root = Tk()
    gui = BookshopGUI(root)
    root.mainloop()
