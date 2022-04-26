# -*- coding: utf-8 -*-
import sqlite3
import time


class dbSqlite:
    def __init__(self):
        self.sqliteConnection=sqlite3.connect('database/db.sql')

    def insertDB(self, query):
        try:
            cur=self.sqliteConnection.cursor()
            self.sqliteConnection.commit()
            return 'out: Insert success'
        except:
            return 'error: query not found'

    def selectDB(self, query):
        print(query)
        try:
            cur=self.sqliteConnection.cursor()
            cur.execute(query)
            return cur.fetchall()
        except:
            return 'error: query not found'

    def updateDB(self, query):
        try:
            cur=self.sqliteConnection.cursor()
            cur.execute(query)
            self.sqliteConnection.commit()
            return 'out: Update success'
        except:
            return 'error: query not found'
    def getCodeSTock(self):
        getCodes="select * from Stock;"
        cur=self.sqliteConnection.cursor()
        cur.execute(getCodes)
        code=[code[1] for code in cur.fetchall()]
        return code


    def deleteDB(self, query):
        try:
            cur=self.sqliteConnection.cursor()
            cur.execute(query)
            self.sqliteConnection.commit()
            return 'out: Delete success'
        except:
            return 'error: query not found'

    def updateStock(self, producto):
        print('Productos desde Update')
        print(producto)
        cur=self.sqliteConnection.cursor()
        updateQuery='update Stock set Stock=%s, Precio=%s, Descripcion=\'%s\' where Codigo=%s;'%(producto['stock'], producto['precio'], producto['descripcion'], producto['codigo'])
        print(updateQuery)
        cur.execute(updateQuery)
        self.sqliteConnection.commit()
        return 'out: Update success'

    def putVentas(self, productos):
        dateVenta=time.strftime("%d%m%Y")
        cur=self.sqliteConnection.cursor()
        for item in productos:
            precioTotal=item[3]*float(item[6])
            query='insert into Ventas (Codigo, Producto, Precio, Fecha, Cantidad) values (%s, %s, %s, %s, %s)'%(item[5], item[1], precioTotal, dateVenta, item[6])
            cur.execute(query)
            self.sqliteConnection.commit()
        return 'Insert Succes'

    def deleteItemStock(self, item):
        cur=self.sqliteConnection.cursor()
        delItem="delete from Stock where Codigo=%s"%(item)
        cur.execute(delItem)
        self.sqliteConnection.commit()
        return 'out: delete success'

    def addItemStock(self, item):
        print(type(item))
        print(item)
        cur=self.sqliteConnection.cursor()
        addItem="insert into Stock (Codigo, Stock, Precio, Descripcion) values (%s, %s, %s, '%s')"%(item['codigo'], item['stock'], item['precio'], item['descripcion'])
        print(addItem)
        cur.execute(addItem)
        self.sqliteConnection.commit()
        return 'out: stock added'
