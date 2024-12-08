import mysql.connector as s
import random
import csv
import time
import smtplib 
import getpass as gt
ms=s.connect(host="localhost",
          user="vijay",
          password="ckav",
          database="project_test")



c=ms.cursor()
if ms.is_connected():
    print("\n\t-----------SQL is connected------------")
def sign_up():
        print("\n\t*Create new User ID and Password*")
        c.execute("select * from user")
        data=[]
        for i in c.fetchall():
            data.append(i[0])
        while True:
            u=input("\n\tENTER USERNAME: ") 
            p=input("\tENTER PASSWORD: ")
            if u in data:
                print("\n\tUser already Existing!\n\tPLease try again with different username. ")
            else:
                break
        query="insert into user values('{0}','{1}')".format(u,p)
        c.execute(query)
        c.execute("CREATE TABLE {0}(Fruit_Name varchar(20),Price float,Bill_No int,Date DATE)".format(u+"_cart"))
        ms.commit()
        print("\n\tYour account has been created successfully----")
def sign_in_user():
    print("\n\t*ENTER User ID and Password to LOGIN*")
    global u
    global p
    u=input("\n\tENTER USERNAME: ")
    p=input("\tENTER PASSWORD: ")
    c.execute("select * from user")
    data=(c.fetchall())
    l=(u,p)        
    if l in data:
        print("\n\t-----------Login successfully-----------------")
        return True
    else:
        print("\n\tInvalid username or password")
        return False

def sign_in_admin():
    print("\n\t*ENTER User ID and Password to LOGIN*")
    global u
    global p
    global type
    u=input("\n\tENTER USERNAME: ")
    p=input("\tENTER PASSWORD: ")
    c.execute("select * from admin")
    data=(c.fetchall())
    l=(u,p)
    if l in data:
        print("\n\t-----------Login successfully-----------------")
        return True
    else:
        print("\n\tInvalid username or password")
        return False
def delAccount():
    x=sign_in_user()
    if x==True:
        confirm=input('''\n\tAre you sure you want to delete your account?
\tEnter (y/n) to confirm your action: ''')
        if confirm=="y":
            c.execute("delete from user where user='{0}'".format(u))
            c.execute("drop table {0}".format(u+"_cart"))
            ms.commit()
            print("\n\t-----------Your account has been successfully deleted----------------")

def updatepass():
   x=sign_in_user()
   if x== True      :
       update=input("\n\tEnter new Password: ")
       query=("update user set pass='{0}' where user='{1}'".format(update,u))
       c.execute(query)
       ms.commit()
       print("\n\t-----------New password has been updated----------------")

def shop(c):
    print('''
            +------+---------------------+-------+
            | code | Fruit_Name          | Price |
            +------+---------------------+-------+
            |    1 | APPLE (1kg)         |   120 |
            |    2 | BANANA (12 pieces)  |    70 |
            |    3 | GRAPES (500g)       |    60 |
            |    4 | ORANGE (1kg)        |    70 |
            |    5 | PINEAPPLE (1 piece) |    65 |
            |    6 | STRAWBERRY (250g)   |    80 |
            |    7 | WATERMELON (1)      |    60 |
            +------+---------------------+-------+
            \n\t Enter the code number to add the corresponding item to your Cart
            \t or Press 0 to stop adding''')
    isValid = True
    fruits=['1','2','3','4','5','6','7']
    fruitsDict={'1' : "Apple",'2' : "Banana",'3' : "Grapes",'4' : "Orange",'5' :
                "Pineapple",'6' : "Strawberry",'7' : "Watermelon"}
    item=[]
    while isValid:
        add=input("\tEnter Item code or 0 to stop: ")
        if add.isnumeric():            
            if add== '0':
                print("All items has been added to your Cart")
                isValid = False
            elif add in fruits:
                item.append(add)
                print("\t{0} added ...".format(fruitsDict[add]))
            else:
                print("\n\tINVALID ITEM CODE! PLEASE ENTER AGAIN.\n ")
        else:
            print("\n\tINVALID ITEM CODE! PLEASE ENTER AGAIN.\n ")
    if add == '0':
        r=str(random.randint(0,1000000))
        ms.commit()
        for i in item:
            query="select Fruit_name,price from fruits where code={0}".format(i)
            c.execute(query)
            cart=c.fetchall()
            print(cart)
            i_f=cart[0][0]
            i_p=cart[0][1]
            c.execute("insert into {0} values('{1}',{2},{3},curdate())".format(u+"_cart",i_f,i_p,r))
            ms.commit()
        c.execute("select sum(price) from {0} where Bill_No={1}".format(u+"_cart",r))
        bill=c.fetchall()
        bill=bill[0][0] 
        print("\n\tTOTAL bill : Rs. ",bill)
        print('''\n\tAvailable Payment Options are :
               +---+--------------------------------------------+
               | 1 | Cash                                       |
               | 2 | Credit Card (*10% Discount of bill amount*)|
               | 3 | Debit  Card (*5%  Discount of bill amount*)|
               | 4 | Net-Banking (*2%  Discount of bill amount*)|
               +---+--------------------------------------------+''')
        payment=[1,2,3,4]
        p=5
        while p not in payment:
            p=int(input("\n\t Please select your payment option : "))
            if p==1:
                    m="Cash"
                    pm=bill
                    d=0
            elif p==2:
                    d=bill*(10/100)
                    m="Credit Card"
                    pm=bill - d
            elif p==3:
                    m="Debit Card"
                    d=bill*(5/100)
                    pm=bill - d
            elif p==4:
                    m="Net Banking"
                    d=bill*(2/100)
                    pm=bill - d
            else:   
                print("\n\tPlease enter appropriate Payment option!")
        from datetime import date
        today = date.today()
        indianformat=today.strftime("%d/%m/%y")
        printout="\n\t"+"-"*35+"\n\t Bill No: {0}".format(r)+"\n\t"+"-"*35+ "\n\t Date of Transaction: {0}".format(indianformat)+"\n\t"+"-"*35+"\n\t TOTAL: Rs. {0} ".format(bill)+"\n\t"+"-"*35+"\n\t Mode of Payment :  {0} ".format(m)+"\n\t"+("-"*35)+"\n\t You saved : Rs. {0}".format(d)+"\n\t"+("-"*35)+"\n\t Total Payable Amount : Rs. {0} ".format(pm) +"\n\t"+("-"*35)+"\n\n\t ------------ THANK YOU ------------"
        print(printout)
        query="insert into customers_data values('{0}',{1},{2},curdate())".format(u,r,pm)
        c.execute(query)
        ms.commit()
        
        d=input("\n\tDo you want to Download the data as text file? (y/n): ") #DOWNLOAD TEXT FILE
        if d=="y":
            c=ms.cursor()
            query="select fruit_name, count(fruit_name), sum(price) from {0} where bill_no={1} group by fruit_name".format(u+"_cart",r)
            c.execute(query)
            history=c.fetchall()
            f=open(u+"_bill.pdf","w")
            f.writelines("\n\t- - - - - - - V-Mart - - - - - - - \n ")
            f.writelines("\n\t\t----BILL MEMO----\n\n ")
            f.writelines("\n\tFRUIT : , QUANTITY : , COST : \n")    
            f.writelines("\t"+("-"*35))
            for i in history:
                itemlist="\n\t"+i[0]+" , "+str(i[1])+" , "+str(i[2])+"\n\t"
                f.writelines(itemlist)
            f.write(printout)
            f.close()
            print("\n\tDownloading",u+'_bill.txt',end="")
            for i in range (50):
                print("-",end="")
                time.sleep( 0.01)
            print("\n\tDownloaded successfully")
            
        ####Bill Throught Email #####
        d=input("\n\tDo you want to send the bill to your email address? (y/n): ")
        if d=="y" or "Y":
            l=[120,120,113,109,32,98,99,117,97,32,110,121,111,110,32,120,112,105,97]
            def hash(l):
                x=""
                for i in l:
                    x=x+chr(i)
                return x
            f=open(u+"_bill.pdf","r")
            email_bill=f.read()
            smtp_object=smtplib.SMTP('smtp.gmail.com',587)
            print(smtp_object.ehlo())
            print(smtp_object.starttls())
            y=[86,105,106,97,121,65,105]
            email="vijaygeneratedai@gmail.com" 
            print(smtp_object.login(email,hash(l)))
            print("\n-------------Login Successful!-------------\n")
            from_adress = email
            to_adress=input("To : ")
            subject= "Fruit Grocry Store - Bill_No: "+str(r)
            message=email_bill
            msg="Subject: "+subject+'\n'+message
            print("\n\n\tDo you want send this E-mail to",to_adress,"?")
            
            sure=input("\tPRESS ' Y ' or ' y ' TO CONFIRM : ")
            if sure=="Y" or sure=="y":
                
                print(smtp_object.sendmail(from_adress,to_adress,msg))
                print("Email sent successfully!")
            else:
                print("Discard!")
        else:
            print("Access Denied")

##### Main function ######

print("""\n\t-----------Welcome to V-Mart-----------""")
g="y"
while g=="y" or g=="Y" :
    print('''\n    Enter 1 to Sign-in and start Shopping
    Enter 2 to Sign-up for creating a new V-Mart account
    Enter 3 to Delete your account
    Enter 4 to Update your password
    Enter 5 to Check Ordered items (History)
''')
    ask=input("    Option: ")    
    if ask=='1':
        if sign_in_user():
            shop(c)
    elif ask == '2':
        sign_up()
    elif ask == '3':
        delAccount()
    elif ask == '4':
       updatepass()
    elif ask == '5':
        x=sign_in_user()
        if x==True:
            query="select * from {0}".format(u+"_cart")
            c.execute(query)
            history=c.fetchall()
            for h in history:
                print(h)
            d=input("\n\tDo you want to Download the history as csv file ? (y/n): ")
            if d=="y":                                                         #DOWNLOAD CSV FILE
                f=open(u+"_cart.csv","w")
                wr=csv.writer(f)
                wr.writerow(["Fruit","price","Bill_No","Date"])
                for i in history:
                    wr.writerow([i[0],i[1],i[2],i[3]])
                f.close()
                print("\n\tDownloading",u+'_cart.csv',end="")
                for i in range (50):
                    print("-",end="")
                    time.sleep(0.01)
                print("\n\tDownloaded successfully")
    elif ask == '6':
        x=sign_in_admin()
        if x==True:
            print('''\n\tWELCOME ADMIN
    Press 1 to get all Customer's History:
    Press 2 to get today's Total Earnings''')
            ask1=input("\n\tEnter : ")
            if ask1=='1':
                print("('USER', BILL_NO, BILL_PAID,------date(XXXX, XX, XX))")
                query="select* from customers_data"
                c.execute(query)
                history=c.fetchall()
                for i in history:
                    print(i)
            elif ask1=='2':
                c.execute("select sum(Bill_Paid) from customers_data where date= curdate()")
                e=c.fetchall()
                e=e[0][0]
                print("\n\t Today's Total Earning : ",e," Rs. ")
    else:
       print("\n\tInvalid input!")
    g=input("\n\n\t--------------------------------------\n\tGo back to Home page to try again? (y/n) :")
print("\n\t--------------Thank you!--------------")