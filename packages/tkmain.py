# -*- coding: utf-8 -*-
import json
import sys
import sqlite3
import os
import time
from tkinter import ttk
from tkinter import *
from packages.dbSqlite import dbSqlite
import tkinter.font as tkFont

class stockWindow:
    def __init__(self, window):
        self.window=window
        self.window.title("Stock Manage")
        # frames
        #
        frame=LabelFrame(self.window, text="Administrar")
        frame.grid(row=0, column=0, columnspan=1, pady=10, padx=10)
        #
        frameButtons=LabelFrame(self.window, text="Acciones")
        frameButtons.grid(row=0, column=2, columnspan=2, pady=10)
        #
        frameTable=LabelFrame(self.window, text="Stock")
        frameTable.grid(row=6, column=0, columnspan=6, pady=10, padx=5)
        #
        #
        # buttons for actions
        ttk.Button(frameButtons, text='Agregar', command=self.addStock, width=30).grid(row=0, column=1, columnspan=2, sticky= W + E)
        ttk.Button(frameButtons, text='Editar', command=self.updateStock).grid(row=1, column=1, columnspan=2, sticky= W + E)
        ttk.Button(frameButtons, text='Borrar', command=self.deleteStock).grid(row=2, column=1, columnspan=2, sticky= W + E)
        #
        # create the table for the items
        frameTable.grid(row=7, column=0, columnspan=6, pady=5)
        self.tree = ttk.Treeview(frameTable, column=("c0", "c1", "c2", "c3"), show='headings', height=20)
        self.tree.grid(row=0)
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="Producto")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Cantidad")
        self.tree.column("# 3", anchor=CENTER)
        self.tree.heading("# 3", text="Precio")
        self.tree.column("# 4", anchor=CENTER)
        self.tree.heading("# 4", text="Codigo")
        ttk.Button(frameTable, text='Actualizar lista de stock', command=self.loadStock, width=30).grid(row=2, column=0, columnspan=2, pady=10)
        #
        #
        # items stock
        self.stockItems=[] # list of items will get from data bases
        self.loadStock() # load items from data base in the table
        self.loadItems()




    def alertMessage(self, messageAlert):
        # message alert for errors
        self.alertwindow=Toplevel()
        self.alertwindow.title="Alerta"
        self.message = Label(self.alertwindow, text = messageAlert, pady=20, padx=20, fg = 'red')
        self.message.grid(row=9, column=1, columnspan=3, sticky = W + E)
        ttk.Button(self.alertwindow, text='Aceptar', command=self.closeAlertWindow, width=20).grid(row=10, column=1, columnspan=3, pady=10, padx=70)

        return 'out: alert'

    def closeAlertWindow(self):
        self.alertwindow.destroy()
        self.alertwindow.update()
        return 'out: close window'

    def getItems(self):
        dataBase=dbSqlite()
        for item in dataBase.selectDB("select * from Stock;"):
            self.stockItems.append(item)
        return 'out: stock list update'

    def loadStock(self):
        self.getItems()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.stockItems:
            self.tree.insert('', 1, text='', value=(item[4], item[2], item[3], item[1]))
        self.stockItems=[]
        return 'ok'

    def updateStock(self):
        if len(self.tree.item(self.tree.selection())['values'])<1:
            self.alertMessage('Error: no seleccionaste ningun item de la lista.')
            return 'Error: no seleccionaste ningun item de la lista.'
        print(self.tree.item(self.tree.selection())['values'])
        self.updateWindow = Toplevel()
        self.updateWindow.title="Actualizar Item"
        frameUpdate=LabelFrame(self.updateWindow, text="Actualizar stock")
        frameUpdate.grid(row=0, column=0, columnspan=6, pady=10, padx=5)
        # formulario para stock
        Label(frameUpdate, text="Codigo").grid(row=1, column=0)
        self.inputCode=Entry(frameUpdate)
        self.inputCode.grid(row=1, column=1, columnspan=2)
        self.inputCode.insert(10, self.tree.item(self.tree.selection())['values'][3])
        self.inputCode.focus()
        #
        #
        Label(frameUpdate, text="Stock").grid(row=2, column=0)
        self.inputStock=Entry(frameUpdate)
        self.inputStock.grid(row=2, column=1)
        self.inputStock.insert(10, self.tree.item(self.tree.selection())['values'][1])
        #
        #
        Label(frameUpdate, text="Precio").grid(row=3, column=0)
        self.inputPrecio=Entry(frameUpdate)
        self.inputPrecio.grid(row=3, column=1)
        self.inputPrecio.insert(10, self.tree.item(self.tree.selection())['values'][2])
        #
        #
        Label(frameUpdate, text="Descripcion").grid(row=4, column=0)
        self.inputDescripcion=Entry(frameUpdate)
        self.inputDescripcion.grid(row=4, column=1)
        self.inputDescripcion.insert(10, self.tree.item(self.tree.selection())['values'][0])
        ttk.Button(frameUpdate, text='Guardar', command=self.syncStock, width=30).grid(row=5, column=0, columnspan=2, sticky= W + E)
        return 'out: stock update success'

    def syncStock(self):
        if int(self.inputCode.get())<=0 or int(self.inputStock.get())<=0 or float(self.inputPrecio.get())<=0 or str(self.inputDescripcion.get())=='':
            self.alertMessage('Error: Existen campos vacios update.')
            return 'Error: Existen campos vacios.'

        item={
                'codigo':self.inputCode.get(),
                'stock':self.inputStock.get(),
                'precio':self.inputPrecio.get(),
                'descripcion':self.inputDescripcion.get()
                }
        print(item)
        database=dbSqlite()
        database.updateStock(item)
        self.updateWindow.destroy()
        self.updateWindow.update()
        self.loadStock()
        return 'out: product added'

    def loadItems(self):
        deleteItem=self.tree.item(self.tree.selection())['values']
        print(deleteItem)
        #self.inputCode.insert(10, 1)
        #self.inputStock.insert(10, 2)
        #self.inputPrecio.insert(10, 3)
        #self.inputDescripcion.insert(10, 4)
        return 'ok'

    def addStock(self):
        self.addWindow = Toplevel()
        self.addWindow.title="Actualizar Item"
        frameUpdate=LabelFrame(self.addWindow, text="Actualizar stock")
        frameUpdate.grid(row=0, column=0, columnspan=6, pady=10, padx=5)
        # formulario para stock
        Label(frameUpdate, text="Codigo").grid(row=1, column=0)
        self.inputCode=Entry(frameUpdate)
        self.inputCode.grid(row=1, column=1, columnspan=2)
        self.inputCode.insert(10, 0)
        self.inputCode.focus()
        #
        #
        Label(frameUpdate, text="Stock").grid(row=2, column=0)
        self.inputStock=Entry(frameUpdate)
        self.inputStock.grid(row=2, column=1)
        self.inputStock.insert(10, 0)
        #
        #
        Label(frameUpdate, text="Precio").grid(row=3, column=0)
        self.inputPrecio=Entry(frameUpdate)
        self.inputPrecio.grid(row=3, column=1)
        self.inputPrecio.insert(10, 0)
        #
        #
        Label(frameUpdate, text="Descripcion").grid(row=4, column=0)
        self.inputDescripcion=Entry(frameUpdate)
        self.inputDescripcion.grid(row=4, column=1)
        #self.inputCount.insert(10, 1)
        ttk.Button(frameUpdate, text='Cargar', command=self.putStock, width=30).grid(row=5, column=0, columnspan=2, sticky= W + E)
        return 'out: add stock success'

    def putStock(self):
        dataBase=dbSqlite()
        codes=dataBase.getCodeSTock()
        print(codes)
        if int(self.inputCode.get())<=0:
            self.alertMessage('Error: Existen campos vacios.')
            return 'Error: Existen campos vacios.'
        elif int(self.inputStock.get())<=0:
            self.alertMessage('Error: Existen campos vacios.')
            return 'Error: Existen campos vacios.'
        elif float(self.inputPrecio.get())<=0:
            self.alertMessage('Error: Existen campos vacios.')
            return 'Error: Existen campos vacios.'
        elif not str(self.inputDescripcion.get()):
            self.alertMessage('Error: Existen campos vacios.')
            return 'Error: Existen campos vacios.'
        elif int(self.inputCode.get()) in codes:
            self.alertMessage('Error: Existen campos vacios.')
            return 'Error: Existen campos vacios.'

        item={
                'codigo':self.inputCode.get(),
                'stock':self.inputStock.get(),
                'precio':self.inputPrecio.get(),
                'descripcion':self.inputDescripcion.get()
                }
        print(item)
        database=dbSqlite()
        database.addItemStock(item)
        self.addWindow.destroy()
        self.addWindow.update()
        self.loadStock()
        return 'out: product added'

    def deleteStock(self):
        if len(self.tree.item(self.tree.selection())['values'])<1:
            self.alertMessage('Error: no seleccionaste ningun item de la lista.')
            return 'Error: no seleccionaste ningun item de la lista.'
        # traigo item seleccionado de la lista
        #
        deleteItem=self.tree.item(self.tree.selection())['values'][3]
        # envio codigo de item para borrar item de la base
        #
        dataBase=dbSqlite()
        dataBase.deleteItemStock(deleteItem)
        #
        # recargo vista
        self.loadStock()
        return 'ok'
