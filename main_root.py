from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import time
import pizza_backend

# making database for the users if it doesnt exist
with sqlite3.connect('pizza.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL ,password TEXT NOT NULL);')
c.execute('CREATE TABLE IF NOT EXISTS user_orders (username TEXT NOT NULL, pizza_id  TEXT NOT NULL,price INT);')
db.commit()
db.close()

#main class
class main:
    def __init__(self,mainscreen):
        #creating main screen part
        self.mainscreen = mainscreen
        self.mainscreen.title("ZakaPizza")
        self.mainscreen.geometry("750x750")
        self.mainscreen.configure(bg = "yellow")
        

        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        #Creating Widgets
        self.widgets()

    #Login Function
    def login(self):
        with sqlite3.connect('pizza.db') as db:
            c = db.cursor()

        find_user = ('SELECT * FROM users WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        #username and password of admin
        if self.username.get()=="admin" and self.password.get()=="admin":
            self.logf.pack_forget()
            self.admin_b_seeorders.place(x=100,y=150)
            self.admin_b_income.place(x=350,y=150)
            
            
        elif result:
            #login page for  the user
            self.logf.pack_forget()
            self.label_main.place(x=25,y=100)
            self.label2_main.place(x=380,y=100)
            self.p1.place(x=200,y=290)
            self.p2.place(x=380,y=290)
            self.l1.place(x=240,y=350)
            self.b1.place(x=180,y=400)
            self.b2.place(x=370,y=400)
            self.label_extention.place(x=250,y=450)
            self.b_tomato.place(x=170,y=490)
            self.b_cheese.place(x=420,y=490)
            self.b_mushroom.place(x=280,y=490)
            self.b_order.place(x=290,y=550)
            self.b_prev.place(x=230,y=600)
            
            
            
        else:
            ms.showerror('Error','Username Not Found!!!')
    
    #income of admin        
    def ad_income(self):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        result = [x[0] for x in c.execute("SELECT price FROM user_orders")]
        count=0
        for i in result:
            count+=i
        string="Your income is "+str(count)+ " manats"
        self.admin_l1=Label(self.mainscreen,text=string,bg = "SeaGreen1",font=("arial",20))
        self.admin_l1.place(x=200,y=250)

    #orders of admin       
    def ad_orders(self):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        result1=[x[0] for x in c.execute('SELECT username FROM user_orders')]
        result2=[x[0] for x in c.execute('SELECT pizza_id FROM user_orders')]

        for i in range(len(result1)):
            print(result1[i],result2[i])
            
        
    #pizza creator   
    def create_pizza(self,a):
        if a=="Pepperoni":
            self.pizza=pizza_backend.PizzaBuilder(a)
        elif a=="Barbeque":
            self.pizza=pizza_backend.PizzaBuilder(a)



    #function for adding or removing extensions to the pizza
    def add_remove(self,pizza_type,extention,choice):
        if choice=="add":
            self.pizza.add_extention(extention)
        elif choice=="remove":
            self.pizza.remove_extention(extention)
            
    #order's total price
    def order_price(self,pizza):
        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        insert='INSERT INTO user_orders(username,pizza_id,price) VALUES(?,?,?)'
        c.execute(insert,[(self.username.get()),(self.pizza.get_status()),(self.pizza.get_price())])
        db.commit()
        ms.showinfo('Price','Your order is {} manats'.format(self.pizza.get_price()))
        


    #see user's previous orders
    def previous_order(self):

        with sqlite3.connect('pizza.db') as db:
            c=db.cursor()
        find_user=('SELECT * FROM user_orders WHERE username=?')
        c.execute(find_user,[(self.username.get())])
        result=c.fetchall()
        print("Username is",result[0][0])
        for i in result:
            print("Order:",i[1],end="|")
            print("Price:",i[2],"manat")
       
                  
    
            
    def new_user(self):

        with sqlite3.connect('pizza.db') as db:
            c = db.cursor()

        #Find Existing username if any take proper action
        find_user = ('SELECT * FROM users WHERE username = ?')
        c.execute(find_user,[(self.username.get())])        
        if c.fetchall():
            ms.showerror('Username Is Already Taken, Please Try With a Diffrent One.')
        else:
            ms.showinfo('Success!','Your Account is  Created!')
            self.log()
        #Create New Account 
        insert = 'INSERT INTO users(username,password) VALUES(?,?)'
        c.execute(insert,[(self.n_username.get()),(self.n_password.get())])
        db.commit()


    #
    def log(self):
        self.username.set('')
        self.password.set('')
        self.reg.pack_forget()
        self.head['text'] = 'Zeka Pizza House'
        self.logf.pack()
    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.reg.pack()

    
        
    def widgets(self):
        self.head = Label(self.mainscreen,text = 'Zeka Pizza House',font = ('',35),pady = 10)
        self.head.pack()
        
        self.logf = Frame(self.mainscreen,padx =20,pady = 20)
        Label(self.logf,text = 'Username: ',bg = "dark turquoise",font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',bg = "dark turquoise",font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logf,text = ' Login ',bg = "dark orange",bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid()
        Button(self.logf,text = ' Create Account ',bg = "dark orange",bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
        self.logf.pack()
        
        self.reg = Frame(self.mainscreen,padx =10,pady = 10)
        Label(self.reg,text = 'E-mail: ',bg = "dark turquoise",font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.reg,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.reg,text = 'Username: ',bg = "dark turquoise",font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.reg,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=1,column=1)
        Label(self.reg,text = 'Password: ',bg = "dark turquoise",font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.reg,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=2,column=1)
        Button(self.reg,text = 'Create Account',bg = "dark orange",bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid()
        Button(self.reg,text = 'Go to Login',bg = "dark orange",bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=3,column=1)








        

        #main page widgets    
        self.label_main=Label(self.mainscreen)
        self.label_main.img=ImageTk.PhotoImage(file="pizz2.jpg")
        self.label_main.config(image=self.label_main.img)
        self.label_main.pack_forget()

        self.label2_main=Label(self.mainscreen)
        self.label2_main.img=ImageTk.PhotoImage(file="pizz1.jpg")
        self.label2_main.config(image=self.label2_main.img)
        self.label2_main.pack_forget()

        self.p1=Label(self.mainscreen,text="Pepperoni",font=("arial",16),bg="orange")
        self.p1.pack_forget()
        self.p2=Label(self.mainscreen,text="Barbeque",font=("arial",16),bg="orange")
        self.p2.pack_forget()
        self.l1=Label(self.mainscreen,text="Choose your order",font=("arial",20))
        self.l1.pack_forget()

        self.v=IntVar()
        self.b1=Radiobutton(self.mainscreen,variable=self.v,value=1,bg = 'spring green',text="Pepperoni",font=('',15),command=lambda:self.create_pizza("Pepperoni"))
        self.b2=Radiobutton(self.mainscreen,variable=self.v,value=2,bg = 'spring green',text="Barbeque",font=('',15),command=lambda:self.create_pizza("Barbeque"))
        self.b1.pack_forget()
        self.b2.pack_forget()
        self.label_extention=Label(self.mainscreen,text="Add extention:",bg = 'green yellow',font=("arial",20))
        self.label_extention.pack_forget()
        self.b_tomato=Button(self.mainscreen,text="Tomato",bg = 'gold',bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Tomato","add"))
        self.b_tomato.pack_forget()
        self.b_cheese=Button(self.mainscreen,text="Cheese",bg = 'orchid1',bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Cheese","add"))
        self.b_cheese.pack_forget()
        self.b_mushroom=Button(self.mainscreen,text="Mushroom",bg = 'tan1',bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Mushroom","add"))
        self.b_mushroom.pack_forget()
        self.b_order=Button(self.mainscreen,text="order",bg = 'chocolate1',bd=3,font=('',15),command=lambda:self.order_price(self.pizza))
        self.b_order.pack_forget()
        self.b_prev=Button(self.mainscreen,text="See previous orders",bd=3,font=('',15),command=lambda:self.previous_order())
        self.b_prev.pack_forget()
        self.admin_b_seeorders=Button(self.mainscreen,text="See all orders",bd=3,font=('arial',20),bg="orange",command=lambda:self.ad_orders())
        self.admin_b_seeorders.pack_forget()
        self.admin_b_income=Button(self.mainscreen,text="Income",bd=3,font=('arial',20),bg="orange",command=lambda:self.ad_income())
        self.admin_b_income.pack_forget()




    
#create window and application object
root = Tk()
root.geometry("1000x1000")

main(root)
root.mainloop()
