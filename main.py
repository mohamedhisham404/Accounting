from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import sqlite3
import random

class Accounting:
    def __init__(self,root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1919x1079+0+0")

        #====================================================Variables====================================================
        self.var_date=StringVar()
        self.var_month = StringVar()
        self.var_year = StringVar()
        self.var_revenues = StringVar()
        self.var_expenses = StringVar()
        self.var_paid = StringVar()
        self.var_ref=StringVar()

        x=random.randint(1000,9999)
        self.var_ref.set(str(x))

        # ====================== title ======================
        lbl_title=Label(text="Accounting",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE) 
        lbl_title.place(x=0,y=0,width=1919,height=50)

        # ====================== label frame ======================
        labelframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,text="Accounting Details",font=("times new roman",12,"bold"),fg="black")
        labelframeleft.place(x=0,y=50,width=600,height=900)

        # ====================== labels and entrys ======================
        #ref
        lbl_ref=Label(labelframeleft,text="Ref",font=("times new roman",12,"bold")).grid(row=0,column=0,padx=10,pady=10,sticky="w")

        txt_ref=Entry(labelframeleft,width=30,textvariable=self.var_ref,font=("times new roman",12,"bold"),bd=5,relief=GROOVE,state='readonly')
        txt_ref.grid(row=0,column=1,padx=10,pady=10)
        #date 
        lbl_date=Label(labelframeleft,text="Date",font=("times new roman",12,"bold")).grid(row=1,column=0,padx=10,pady=10,sticky="w")

        txt_date=Entry(labelframeleft,width=30,textvariable=self.var_date,font=("times new roman",12,"bold"),bd=5,relief=GROOVE)
        txt_date.grid(row=1,column=1,padx=10,pady=10)
        #  #Revenues
        lbl_revenues=Label(labelframeleft,text="Revenues",font=("times new roman",12,"bold")).grid(row=2,column=0,padx=10,pady=10,sticky="w")

        txt_revenues=Entry(labelframeleft,width=30,textvariable=self.var_revenues,font=("times new roman",12,"bold"),bd=5,relief=GROOVE)
        txt_revenues.grid(row=2,column=1,padx=10,pady=10)
        #Expenses
        lbl_expenses=Label(labelframeleft,text="Expenses",font=("times new roman",12,"bold")).grid(row=3,column=0,padx=10,pady=10,sticky="w")

        txt_expenses=Entry(labelframeleft,width=30,textvariable=self.var_expenses,font=("times new roman",12,"bold"),bd=5,relief=GROOVE)
        txt_expenses.grid(row=3,column=1,padx=10,pady=10)
        #paid
        lbl_paid=Label(labelframeleft,text="Paid",font=("times new roman",12,"bold")).grid(row=4,column=0,padx=10,pady=10,sticky="w")

        txt_paid=Entry(labelframeleft,width=30,textvariable=self.var_paid,font=("times new roman",12,"bold"),bd=5,relief=GROOVE)
        txt_paid.grid(row=4,column=1,padx=10,pady=10)
        #===================== Buttons ======================
        btn_frame=Frame(labelframeleft,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=470,width=590,height=40)

        btnAdd=Button(btn_frame,text="Add",command=self.add_data,width=15,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=0,padx=1)

        btnUpdate=Button(btn_frame,text="Update",command=self.update,width=15,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=1,padx=1)

        btnDelete=Button(btn_frame,text="Delete",command=self.delete,width=15,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=2,padx=1)

        btnClear=Button(btn_frame,text="Clear",command=self.reset,width=15,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=3,padx=1)

         # ====================== tabel frame search sys ======================
        Table_frame=LabelFrame(self.root,bd=2,relief=RIDGE,text="View Details And search System",font=("times new roman",12,"bold"),padx=2)
        Table_frame.place(x=610,y=50,width=1300,height=900)

        lblseachby=Label(Table_frame,text="Search By",font=("times new roman",12,"bold"),bg="red",fg="white").grid(row=0,column=0,padx=2,pady=10,sticky="w")

        self.search_var=StringVar()    
        combo_searchby=ttk.Combobox(Table_frame,textvariable=self.search_var,font=("times new roman",12,"bold"),width=29)
        combo_searchby["values"]=("month","year")
        combo_searchby.current(0)
        combo_searchby.grid(row=0,column=1,padx=10,pady=10,sticky="w")

        self.txt_search=StringVar()
        txtsearch=Entry(Table_frame,textvariable=self.txt_search,width=29,font=("times new roman",12,"bold"),bd=5)
        txtsearch.grid(row=0,column=2,padx=10,pady=10,sticky="w")

        btnsearch=Button(Table_frame,command=self.search,text="Search",width=8,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=3,padx=10,pady=10)

        btnShowall=Button(Table_frame,text="Show All",command=self.fetch_data,width=8,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=4,padx=10,pady=10)
        
        #total
        lbl_total=Label(Table_frame,text="Total",font=("times new roman",12,"bold"),fg="black").grid(row=1,column=0,padx=2,pady=10,sticky="w")

        self.txt_total=Entry(Table_frame,width=29,font=("times new roman",12,"bold"),bg="white",state="readonly")
        self.txt_total.grid(row=1,column=1,padx=10,pady=10,sticky="w")
        # ====================== show data table ======================
        Table_frame1=LabelFrame(self.root,bd=2,relief=RIDGE,text="Show Details And View System",font=("times new roman",12,"bold"),padx=2)
        Table_frame1.place(x=610,y=200,width=1300,height=750)

        scroll_x=Scrollbar(Table_frame1,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_frame1,orient=VERTICAL)

        self.Table_frame1=ttk.Treeview(Table_frame1,columns=("Date","Month","Year","Revenues","Expenses","Paid","Ref"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Table_frame1.xview)
        scroll_y.config(command=self.Table_frame1.yview)

        self.Table_frame1.heading("Date",text="Date")
        self.Table_frame1.heading("Month",text="Month")
        self.Table_frame1.heading("Year",text="Year")
        self.Table_frame1.heading("Revenues",text="Revenues")
        self.Table_frame1.heading("Expenses",text="Expenses")
        self.Table_frame1.heading("Paid",text="Paid")
        self.Table_frame1.heading("Ref",text="Ref")

        self.Table_frame1["show"]="headings"
        self.Table_frame1.pack(fill=BOTH,expand=1)

        self.Table_frame1.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

        
        

# ====================== add data table ======================
    def add_data(self):
        if self.var_expenses.get()==""or self.var_paid.get()=="" or self.var_revenues.get()=="":
            messagebox.showerror("Error","All fields are required")
        else:
            try:
                date1=str(self.var_date.get()) 
                date_obj=datetime.strptime(date1,"%d-%m-%Y") 
                self.var_month.set(date_obj.month) 
                self.var_year.set(date_obj.year)
                conn=sqlite3.connect('database')
                cursor=conn.cursor()

                sqlite_insert_with_param='''INSERT INTO Accounting(Date,Month,Year,Revenues,Expenses,Paid,Ref)
                                                                VALUES(?,?,?,?,?,?,?);'''

                data_tuble=(self.var_date.get(),
                            self.var_month.get(),
                            self.var_year.get(),
                            self.var_revenues.get(),
                            self.var_expenses.get(),
                            self.var_paid.get(),
                            self.var_ref.get()
                            )
                cursor.execute(sqlite_insert_with_param,data_tuble)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Accounting details added successfully",parent=self.root)
            except sqlite3.Error as error:
                messagebox.showerror("Error",f"Error due to {error}",parent=self.root)

    def fetch_data(self):
        conn=sqlite3.connect('database')
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Accounting")
        rows=cursor.fetchall()
        if len(rows)!=0:
            self.Table_frame1.delete(*self.Table_frame1.get_children())
            for row in rows:
                self.Table_frame1.insert('',END,values=row)
            conn.commit()
        conn.close()

    def get_cursor(self,evnet=""):
        cursor_row=self.Table_frame1.focus()
        contents=self.Table_frame1.item(cursor_row)
        row=contents["values"]
        self.var_date.set(row[0])
        self.var_month.set(row[1])
        self.var_year.set(row[2])
        self.var_revenues.set(row[3])
        self.var_expenses.set(row[4])
        self.var_paid.set(row[5])
        self.var_ref.set(row[6])

    def update(self):
        if self.var_month.get()=="" or self.var_expenses.get()==""or self.var_year.get()=="" or self.var_paid.get()=="" or self.var_revenues.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            conn=sqlite3.connect('database')
            cursor=conn.cursor()
            cursor.execute("update Accounting set Date=?,Month=?,Year=?,Revenues=?,Expenses=?,Paid=? where Ref=?",(
                self.var_date.get(),
                self.var_month.get(),
                self.var_year.get(),
                self.var_revenues.get(),
                self.var_expenses.get(),
                self.var_paid.get(),
                self.var_ref.get()

            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Accounting details updated successfully",parent=self.root)

    def delete(self):
        mDelete=messagebox.askyesno("Delete","Do you want to delete this room?",parent=self.root)
        if mDelete>0:
            conn=sqlite3.connect('database')
            cursor=conn.cursor()
            cursor.execute("delete from Accounting where Ref=?",(self.var_ref.get(),))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Accounting details deleted successfully",parent=self.root)
        else:
            if not mDelete:
                return


    def reset(self):
        self.var_date.set("")
        self.var_month.set("")
        self.var_year.set("")
        self.var_revenues.set("")
        self.var_expenses.set("")
        self.var_paid.set("") 

        x=random.randint(1000,9999)
        self.var_ref.set(str(x)) 

    def search(self):
        conn=sqlite3.connect('database')
        cursor=conn.cursor()

        cursor.execute("select * from Accounting where "+str(self.search_var.get())+" LIKE '%"+str(self.txt_search.get())+"%'")
        rows=cursor.fetchall()
        if len(rows)!=0:
            self.details_Table_frame.delete(*self.details_Table_frame.get_children())
            for row in rows:
                self.details_Table_frame.insert('',END,values=row)
            conn.commit()
        else:
            messagebox.showerror("Error","No data found",parent=self.root)    
        conn.close()

if __name__=="__main__":
    root = Tk()
    obj=Accounting(root)
    root.mainloop()


    
