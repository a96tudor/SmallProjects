import sqlite3 as sql

class Database:

    """
        A custom database class for the bookshop application
    """

    def __init__(self, db_name):
        """
            CONSTRUCTOR
        :param db_name:     The name of the database we are going to use
        """
        self._dbName = db_name
        self._check_integrity()

    def _check_integrity(self):
        """
            Method that checks the integrity of the database (i.e. if it has the required tables, etc)
        :return:    -
        """
        #setting up the connection
        con = sql.connect(self._dbName)
        cur = con.cursor()

        #Creating the table, if it doesn't exist. This way we make sure that we have it in the correct format
        query = "CREATE TABLE IF NOT EXISTS " \
            "book (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "title VARCHAR(50) ," \
                "author VARCHAR(50)," \
                "'year' INT," \
                "isbn VARCHAR(13)" \
            ")"
        cur.execute(query)
        con.commit()

        #closing the connection
        con.close()

    def _get_query_format(self, d, keyword="AND", pre_word=" WHERE "):
        """
            Returns the query format from an dictionary of specs, d
        :param d:       A dictionary, holding specs, in the format :
                    <column_name> : <constraint>
        :param keyword:     The work that is used to connect the conditions
                    (i.e. AND or OR)
        :param pre_word:    The keyword that precedes the sequence of
                    equalities

        :return:        The query-format string
        """
        l_conds=list()
        #Setting up the conditions
        for key in d:
            if (key!="year" and key!="id"):
                l_conds.append(key + "='" + str(d[key]) + "'")
            else:
                l_conds.append(key + "=" + str(d[key]))
        condition=(" " + keyword + " ").join(l_conds)

        if condition!="":
            condition = pre_word + condition

        return condition

    def fetch(self, limit=-1, conds=dict()):
        """
            Method that reads all the entries from the table
        :param limit:       How many elements to fetch from the table

                Default: -1 = no limit (i.e. fetching all of them)
        :param condition:   The conditions used when we run the query
                    It is a dictionary with the format :
                        <column_name> : <condition>

                Default: {} = no conditions

        :return:    The entries from the table, as a list of tuples
        """


        condition = self._get_query_format(conds)

        #setting up the query
        query = "SELECT * FROM book" + condition
        if limit != -1:
            query += " LIMIT " + str(limit)

        #opening the connection
        con = sql.connect(self._dbName)
        cur = con.cursor()

        #running the query
        cur.execute(query)
        results = list(set(cur.fetchall()))

        #closing the connection
        con.close()

        return results

    def _get_entry(self, d, key):
        """

        :param d:       The dictionary
        :param key:     The key of the entry we want from the dictionary

        :return:         - The value at that specific key, if the key exists in the dictionary
                         - "NULL", otherwise
        """
        if key in d:
            return d[key]
        else:
            return "NULL"

    def insert(self, inputs):
        """

        :param inputs:      the new entries to be inserted into the db table, as a dictionary
                The dictionary has to be of the format :
                        <column_name> : <value>

        :return:    True : if the insert was successful
                    False : otherwise
        """
        #getting the data from the dictionary
        title = self._get_entry(inputs, "title")
        author = self._get_entry(inputs, "author")
        year = self._get_entry(inputs, "year")
        isbn = self._get_entry(inputs, "ISBN")

        #setting up the querry
        query = "INSERT INTO book" \
                "(title, author, 'year', isbn)" \
                " VALUES (?, ?, ?, ?)"

        #setting up the connection
        con = sql.connect(self._dbName)
        try:
            cur = con.cursor()
            cur.execute(query, (title, author, year, isbn))
            con.commit()
        except Exception:
            #it failed
            return False
        finally:
            con.close()

        return True

    def delete(self, cond):
        """
            Deletes the entries with the given specs
        :param cond:        The required specifications,
                in the format of a dictionary:

                    <column_name> : <constraint>

        :return:        True if successful,
                    false otherwise
        """

        condition = self._get_query_format(cond)

        #setting up the query

        query = "DELETE FROM book" + condition


        try:
            con = sql.connect(self._dbName)
            cur = con.cursor()

            cur.execute(query)

            con.commit()
        except Exception:
            return False
        finally:
            con.close()

        return True

    def update(self, id, new_data):
        """
        :param id:         The id of the element we want to update, as a dictionary
        :param new_data:   The new data for our element. Has to be a dictionary in the format:
                            <column_name> : <value>

        :return:            - True, if the update was successful
                            - False, otherwise
        """

        #setting up the query
        cond = self._get_query_format(id)
        set = self._get_query_format(new_data, pre_word=" SET ")

        query = "UPDATE book" + set + cond

        try:
            #setting up the connection
            con = sql.connect(self._dbName)
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except Exception:
            return False
        finally:
            con.close()

        return True

