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

        self._entries = list()

        self._vars = {
            "title": StringVar(),
            "ISBN": StringVar(),
            "author": StringVar(),
            "year": StringVar()
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

        bt_search = Button(master=self.master, text="Search entry", width=12, command=self.search)
        bt_search.grid(row=3, column=3)

        bt_add = Button(master=self.master, text="Add entry", width=12, command=self.insert_entry)
        bt_add.grid(row=4, column=3)

        bt_update = Button(master=self.master, text="Update", width=12, command=self.update)
        bt_update.grid(row=5, column=3)

        bt_del = Button(master=self.master, text="Delete", width=12, command=self.delete)
        bt_del.grid(row=6, column=3)

        bt_close = Button(master=self.master, text="Close", width=12, command=self.close)
        bt_close.grid(row=7, column=3)

    def _print_message(self, msg, error = False):
        """

        :param msg:         The message to print
        :param error:       True - if it is an error message
                            False - otherwise
        :return:
        """
        if error:
            showerror("ERROR", msg)
        else:
            showinfo("INFO", msg)

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
        self._list_box.delete(0, END) #clearing the list
        idx = 1

        #putting the new elements in
        for entry in new_list:
            string = "(" + str(idx) + ") " + \
                str(entry[1]) + ", " + \
                str(entry[2]) + ", " + \
                str(entry[3]) + "," + \
                str(entry[4])
            self._list_box.insert(END, string)
            idx += 1

    def _get_entries(self, all_mandatory=True):
        """
            Processes the entries from the edit boxes and returns a dictionary to be sent to the db
        :param all_mandatory:   True if we want all the entries
                                False otherwise

        :return:    The required dictionary in the format :
                         <column_name> : <value>, if everything is ok

                    None, otherwise
        """
        result = dict()

        for key in self._vars:
            if key != "year":
                if self._vars[key].get() != "":
                    result[key] = self._vars[key].get()
                elif all_mandatory:
                    self._print_message("The " + key + " field must not be empty", error=True)
                    return None

        try:
            year = int(self._vars["year"].get())
            result["year"] = year
        except ValueError:
            if (self._vars["year"].get() == "" and all_mandatory) \
                    or (self._vars["year"].get()!="" and not all_mandatory):
                self._print_message("The given year is not in a valid format. Please review.", error=True)
                return None

        if len(result) == 0:
            self._print_message("Please specify entries in the provided fields and try again")
            return None

        return result

    def view_all(self):
        """
            uses the Database object to read all the entries and then display them
        in the list box
        :return:    -
        """
        self._entries = list()
        self._entries = self._db.fetch()
        self._update_list_box(new_list=self._entries)

    def insert_entry(self):
        """
            Processes the inputs and sends them to the db
        :return: -
        """

        to_insert = self._get_entries()
        if to_insert is None:
            return

        success = self._db.insert(to_insert)

        if (success):
            self._reset_fields()
            self._print_message("Entry inserted successfully!")
        else:
            self._print_message("Something went wrong. Please review your entries to make sure they"
                                "are in the required format and try again.", error=True)

    def delete(self):
        """
            Deletes the selected entry from the database
        :return:    Nothing
        """
        # getting the selected entry
        no = self._list_box.get(ACTIVE)

        idx = int(no.split(" ")[0].replace("(", "").replace(")", "")) - 1

        to_delete = {
            "id": self._entries[idx][0]
        }

        #deleting from the db
        success = self._db.delete(to_delete)

        if (not success):
            self._print_message("The delete failed", error=True)
            return
        else:
            self._print_message("Delete successful")

        #deleting from the listbox
        self._entries.remove(self._entries[idx])
        self._update_list_box(new_list=self._entries)

    def close(self):
        """
            Closes the window
        :return:     -
        """
        if askyesno("Quit?", "Are you sure you want to quit?"):
            sys.exit(0)

    def search(self):
        """
            Function that takes care of the search
        :return:    -
        """
        #setting up the condtions
        cond = dict()

        for key in self._vars:
            if (self._vars[key].get() != ""):
                if key == "year":
                    try :
                        cond["year"] = int(self._vars["year"].get())
                    except ValueError:
                        self._print_message("The given year is not in a valid format. Please review.", error=True)
                        return

                else:
                    cond[key] = self._vars[key].get()

        if len(cond) == 0:
            self._print_message("You have to enter at least a keyword for the search to work.", error=True)
            return


        self._entries = list(self._db.fetch(conds=cond))
        if len(self._entries) == 0:
            self._print_message("There were no results for the given search")

        self._update_list_box(new_list=self._entries)

    def update(self):
        """
            Updates a selected entry
        :return:  -
        """

        #getting the index
        no = self._list_box.get(ACTIVE)

        idx = int(no.split(" ")[0].replace("(", "").replace(")", "")) - 1

        to_update = {
            "id": self._entries[idx][0]
        }

        #getting the new values
        new_vals = self._get_entries(all_mandatory=False)
        if new_vals is None:
            return

        success = self._db.update(to_update, new_vals)

        if success:
            self._print_message("Element updated successfully.")
            self._entries[idx] = self._db.fetch(conds=to_update)[0]
            self._update_list_box(new_list=self._entries)
            self._reset_fields()
        else:
            self._print_message("Something went wrong when updating. Please revise your"
                                "fields and try again.")

if __name__ == "__main__":
    # I run the app
    root = Tk()
    gui = BookshopGUI(root)
    root.mainloop()
