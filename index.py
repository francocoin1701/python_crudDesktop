from tkinter.ttk import *
from tkinter import *

import sqlite3

class Product:

    db_name = "database.db"

    def __init__(self,window):
        self.wind = window
        self.wind.title("products application")

        #creating a frame container
        frame = LabelFrame(self.wind, text = "Register a new product")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #imput name
        Label(frame, text = "Name: ").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 1)

        #price input
        Label(frame, text = "Price: ").grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        
        #button
        ttk.Button(frame, text = "save product", command = self.printInterface).grid(row = 3, columnspan = 2, sticky = W + E )
        
        #message
        self.message = Label(text = "", fg = "red")
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        # table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading("#0", text = "name product",anchor = CENTER)
        self.tree.heading("#1", text = "price product", anchor = CENTER)    
        self.get_product()

        #buttons delete and edit
        ttk.Button(text = "delete product", command = self.deleteProduct).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = "edid product", command = self.edid_product).grid(row = 5, column =1, sticky = W + E)

    #se establese la coneccion a base de datos
    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result 
    #se obtiene el producto
    def get_product(self):
        records = self.tree.get_children()
        for elements in records:
            self.tree.delete(elements)
        query = "SELECT * FROM product ORDER BY name DESC "       
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert("",0,tex = row[1],values = row[2])
   
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def printInterface(self):
        if self.validation():
            query = "INSERT INTO product VALUES(NULL,?,?)"
            parameters = (self.name.get(),self.price.get())
            self.run_query(query,parameters)
            self.message["text"] = "product {} add succefully".format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0,END)
        else:
            self.message["text"] = "porfavor llene ambos campos para continuar"    

        self.get_product()

    def deleteProduct(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]          
        except IndexError as identifier:
            self.message["text"] = "plese select a record"
            return
        self.message["text"] = ""    
        parameters = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM product WHERE name = ?"
        self.run_query(query,(parameters,))
        self.message["text"] = "product {} was delete successfully".format(parameters) 
        self.get_product()   
    def edid_product(self):
        self.message["text"]= ""
        try:
            self.tree.item(self.tree.selection())["text"]
        except IndexError as e:
            self.message["text"] = "plese select a record"
            return
        name = self.tree.item(self.tree.selection())["text"]
        old_price= self.tree.item(self.tree.selection())["values"][0]  
        self.edid_wind = Toplevel()
        self.edid_wind.title("edit product")

        Label(self.edid_wind, text = "old name").grid(row = 0 , column = 1)
        Entry(self.edid_wind, textvariable = StringVar(self.edid_wind, value= name), state = "readonly").grid(
            row = 0 , column = 2
        ) 
        Label(self.edid_wind, text = "new name").grid(row = 1, column = 1)
        Entry(self.edid_wind, text = "").grid(row = 1, column = 2)
        Label(self.edid_wind, text = "old price").grid(row = 2, column = 1)
        Entry(self.edid_wind, textvariable = StringVar(self.edid_wind,  value=old_price),state = "readonly").grid(
            row = 2, column = 2
        )
        Label(self.edid_wind, text = "new price").grid(row = 3, column = 1)
        Entry(self.edid_wind, text = "").grid(row = 3 , column = 2)

if __name__ == "__main__":
    window = Tk()
    aplication = Product(window)
    window.mainloop()

