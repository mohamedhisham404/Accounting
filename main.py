from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3

class Accounting:
    def __init__(self,root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1919x1079+0+0")

        #====================================================Variables====================================================
        self.var_month = StringVar()
        self.var_year = StringVar()
        self.var_revenues = StringVar()
        self.var_expenses = StringVar()
        self.var_paid = StringVar()

        # ====================== title ======================
        lbl_title=Label(text="Accounting",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE) 
        lbl_title.place(x=0,y=0,width=1919,height=50)

        # ====================== label frame ======================
        labelframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,text="Accounting Details",font=("times new roman",12,"bold"),fg="black")
        labelframeleft.place(x=0,y=50,width=600,height=900)

        # ====================== labels and entrys ======================
        #month
        lbl_name=Label(labelframeleft,text="Month",font=("times new roman",12,"bold")).grid(row=0,column=0,padx=10,pady=10,sticky="w")

        combo_month=ttk.Combobox(labelframeleft,textvariable=self.var_month,width=58,font=("times new roman",12,"bold"),state="readonly")
        combo_month["values"]=("1","2","3","4","5","6","7","8","9","10","11","12")
        combo_month.current(0)
        combo_month.grid(row=0,column=1,padx=10,pady=10)

        #entryyear
        lbl_year=Label(labelframeleft,text="Year",font=("times new roman",12,"bold")).grid(row=2,column=0,padx=10,pady=10,sticky="w")

        entry_year=Entry(labelframeleft,textvariable=self.var_year,width=60,font=("times new roman",12,"bold"),bd=2,relief=GROOVE)
        entry_year.grid(row=2,column=1,padx=10,pady=10)
        #Revenues
        lbl_revenues=Label(labelframeleft,text="Revenues",font=("times new roman",12,"bold")).grid(row=4,column=0,padx=10,pady=10,sticky="w")

        self.txt_revenues=Entry(labelframeleft,textvariable=self.var_revenues,width=60,font=("times new roman",12,"bold"),bg="white")
        self.txt_revenues.grid(row=4,column=1,padx=10,pady=10,sticky="w")

        #Expenses
        lbl_expenses=Label(labelframeleft,text="Expenses",font=("times new roman",12,"bold")).grid(row=6,column=0,padx=10,pady=10,sticky="w")        

        self.txt_expenses=Entry(labelframeleft,textvariable=self.var_expenses,width=60,font=("times new roman",12,"bold"),bg="white")
        self.txt_expenses.grid(row=6,column=1,padx=10,pady=10,sticky="w")
        
        #paid
        lbl_paid=Label(labelframeleft,text="Paid",font=("times new roman",12,"bold")).grid(row=8,column=0,padx=10,pady=10,sticky="w")

        self.txt_paid=Entry(labelframeleft,textvariable=self.var_paid,width=60,font=("times new roman",12,"bold"),bg="white")
        self.txt_paid.grid(row=8,column=1,padx=10,pady=10,sticky="w")
        
        
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

        combo_searchby=ttk.Combobox(Table_frame,font=("times new roman",12,"bold"),width=29)
        combo_searchby["values"]=("month","year")
        combo_searchby.current(0)
        combo_searchby.grid(row=0,column=1,padx=10,pady=10,sticky="w")

        txtsearch=Entry(Table_frame,width=29,font=("times new roman",12,"bold"),bd=5)
        txtsearch.grid(row=0,column=2,padx=10,pady=10,sticky="w")

        btnsearch=Button(Table_frame,text="Search",width=8,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=3,padx=10,pady=10)

        btnShowall=Button(Table_frame,text="Show All",width=8,font=("times new roman",11,"bold"),bg="black",fg="gold").grid(row=0,column=4,padx=10,pady=10)
        
        #total
        lbl_total=Label(Table_frame,text="Total",font=("times new roman",12,"bold"),fg="black").grid(row=1,column=0,padx=2,pady=10,sticky="w")

        self.txt_total=Entry(Table_frame,width=29,font=("times new roman",12,"bold"),bg="white",state="readonly")
        self.txt_total.grid(row=1,column=1,padx=10,pady=10,sticky="w")
    # ====================== show data table ======================
        details_table=Frame(Table_frame,bd=2,relief=RIDGE)
        details_table.place(x=0,y=95,width=1300,height=750)

        scroll_x=Scrollbar(details_table,orient=HORIZONTAL)
        scroll_y=Scrollbar(details_table,orient=VERTICAL)

        self.details_Table_frame=ttk.Treeview(details_table,columns=("Month","Year","Revenues","Expenses","Paid"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y) 

        scroll_x.config(command=self.details_Table_frame.xview)
        scroll_y.config(command=self.details_Table_frame.yview)

        self.details_Table_frame.heading("Month",text="Month")   
        self.details_Table_frame.heading("Year",text="Year") 
        self.details_Table_frame.heading("Revenues",text="Revenues")
        self.details_Table_frame.heading("Expenses",text="Expenses")
        self.details_Table_frame.heading("Paid",text="Paid")
        
        self.details_Table_frame["show"]="headings"
        self.details_Table_frame.pack(fill=BOTH,expand=1)
        self.details_Table_frame.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()


# ====================== add data table ======================
    def add_data(self):
        if self.var_month.get()=="" or self.var_expenses.get()==""or self.var_year.get()=="" or self.var_paid.get()=="" or self.var_revenues.get()=="":
            messagebox.showerror("Error","All fields are required")
        else:
            try:
                conn=sqlite3.connect('database.db')
                cursor=conn.cursor()
                sqlite_insert_with_param='''INSERT INTO Accounting(Month,Year,Revenues,Expenses,Paid)
                                                                VALUES(?,?,?,?,?);'''

                data_tuble=(self.var_month.get(),
                            self.var_year.get(),
                            self.var_revenues.get(),
                            self.var_expenses.get(),
                            self.var_paid.get(),
                            )
                cursor.execute(sqlite_insert_with_param,data_tuble)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Accounting details added successfully",parent=self.root)
            except sqlite3.Error as error:
                messagebox.showerror("Error",f"Error due to {error}",parent=self.root)

    def fetch_data(self):
        conn=sqlite3.connect('database.db')
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Accounting")
        rows=cursor.fetchall()
        if len(rows)!=0:
            self.details_Table_frame.delete(*self.details_Table_frame.get_children())
            for row in rows:
                self.details_Table_frame.insert('',END,values=row)
            conn.commit()
        conn.close()

    def get_cursor(self,evnet=""):
        cursor_row=self.details_Table_frame.focus()
        contents=self.details_Table_frame.item(cursor_row)
        row=contents['values']
        self.var_month.set(row[0])
        self.var_year.set(row[1])
        self.var_revenues.set(row[2])
        self.var_expenses.set(row[3])
        self.var_paid.set(row[4])

    def update(self):
        if self.var_month.get()=="" or self.var_expenses.get()==""or self.var_year.get()=="" or self.var_paid.get()=="" or self.var_revenues.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            conn=sqlite3.connect('database.db')
            cursor=conn.cursor()
            cursor.execute("update Accounting set Month=?,Year=?,Revenues=?,Expenses=?,Paid=?",(self.var_month.get(),
                                                                                                self.var_year.get(),
                                                                                                self.var_revenues.get(),
                                                                                                self.var_expenses.get(),
                                                                                                self.var_paid.get(),))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Accounting updated successfully",parent=self.root)

    def delete(self):
        mDelete=messagebox.askyesno("Delete","Do you want to delete?",parent=self.root)
        if mDelete>0:
            conn=sqlite3.connect('database.db')
            cursor=conn.cursor()
            cursor.execute("delete from Accounting where Month=?,Year=?,Revenues=?,Expenses=?,Paid=?",(self.var_month.get(),
                                                                                                self.var_year.get(),
                                                                                                self.var_revenues.get(),
                                                                                                self.var_expenses.get(),
                                                                                                self.var_paid.get(),))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Accounting details deleted successfully",parent=self.root)
        else:
            if not mDelete:
                return
        conn.commit()
        self.fetch_data()
        conn.close()

    def reset(self):
        self.var_month.set("")
        self.var_year.set("")
        self.var_revenues.set("")
        self.var_expenses.set("")
        self.var_paid.set("")  

if __name__=="__main__":
    root = Tk()
    obj=Accounting(root)
    root.mainloop()