"""
Created on 10-23-2022
author@ Jonathan Estrada

"""

import tkinter as tk
from decimal import Decimal
from tkinter import ttk
import sqlite3 
import getpass
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# FUNCTION FOR MAIN MENU --- 

def main(sql, usr, pass_):
    # STARTING CURSOR TO ACCESS "LGUP" TABLE --- 

    lgupc = sql.cursor()

    # FETCHING "LGUP" TABLE TO LOGIN TO MAIN MENU --- 

    lgup = lgupc.execute("SELECT rowid, * FROM LGUP").fetchall()

    for lg in lgup:
        if usr == lg[1] and pass_ == lg[2]:
            # FUNCTION FOR SUBMITING ACCOUNT INFORMATION --- 

            def subM():
                # STARTING BNK DATABASE CURSOR --- 

                sbmC = sql.cursor()

                # FETCHING "BALANCE" TABLE IN BNK DATABASE --- 

                try:
                    subal = sbmC.execute("SELECT rowid, * FROM BALANCE").fetchall()

                except:
                    # ERRASING INPUT BOX FOR AMOUNT AND DESCRIPTION --- 

                    efa.delete(0, "end")
                    etbfd.delete('1.0', 'end')

                    # CLOSING THE ERROR WINDOW FOR NO BALANCE TO DEDUCT FROM  --- 

                    def cwb(clse):
                        clse.destroy()


                    # ERROR MESSAGE FOR NO BALANCE TO DEDUCT FROM --- 

                    emnb = tk.Toplevel()

                    # Gets the requested values of the height and widht.

                    emnbwW = emnb.winfo_reqwidth()
                    emnbwH = emnb.winfo_reqheight()
                     
                    # Gets both half the screen width/height and window width/height

                    emnbpR = int(emnb.winfo_screenwidth()/2 - emnbwW/2)
                    emnbpD = int(emnb.winfo_screenheight()/2 - emnbwH/2)
                     
                    # Positions the window in the center of the page.

                    emnb.geometry("+{}+{}".format(emnbpR, emnbpD))
                    emnb.title("Error")
                    emnb.geometry("300x150")

                    # FRAME FOR ERROR IN NO BALANCE TO DEDUCT FROM --- 

                    fenb = tk.Label(
                        emnb, bg='#F7F6EE', 
                        text='There is no balance to duduct from\nplease input balance before you input item', anchor='c')
                    fenb.place(relx=.1, rely=.1, relwidth=.8, relheight=.3)

                    # "OK" BUTTON --- 

                    okbtt = ttk.Button(emnb, text='OK', command=lambda:cwb(emnb))
                    okbtt.place(relx=.17, rely=.55, relwidth=.31, relheight=.2)

                    # "CANCEL" BUTTON --- 

                    cnclbtt = ttk.Button(emnb, text='Cancel', command=lambda:cwb(emnb))
                    cnclbtt.place(relx=.52, rely=.55, relwidth=.31, relheight=.2)

                    emnb.mainloop()

                    return

                # ACCOUNT DATETIME SAVED TO "ACCOUNT" TABLE --- 

                adsbt = datetime.now().strftime("%m-%d-%Y")

                # ITEMS SAVED TO "ACCOUNT" TABLE IN BNK DATABASE --- 

                isbtbd = obfsi_str.get()

                # AMOUNT SPENT SAVED TO "ACCOUNT" TABLE --- 

                try:
                    assbt = Decimal(efa.get())
                    efa.delete(0, "end")

                except:
                    # CLOSING THE ERROR WINDOW FOR WRONG AMOUNT INPUT --- 

                    def cwa(clse):
                        clse.destroy()


                    # ERROR MESSAGE FOR WRONG AMOUNT INPUT --- 

                    emnab = tk.Toplevel()

                    # Gets the requested values of the height and widht.

                    emnabwW = emnab.winfo_reqwidth()
                    emnabwH = emnab.winfo_reqheight()
                     
                    # Gets both half the screen width/height and window width/height

                    emnabpR = int(emnab.winfo_screenwidth()/2 - emnabwW/2)
                    emnabpD = int(emnab.winfo_screenheight()/2 - emnabwH/2)
                     
                    # Positions the window in the center of the page.

                    emnab.geometry("+{}+{}".format(emnabpR, emnabpD))
                    emnab.title("Error")
                    emnab.geometry("300x150")

                    # FRAME FOR ERROR IN WRONG AMOUNT INPUT --- 

                    fea = tk.Label(
                        emnab, bg='#F7F6EE', 
                        text='Amount must be an integer', anchor='c')
                    fea.place(relx=.1, rely=.1, relwidth=.8, relheight=.3)

                    # "OK" BUTTON --- 

                    okbtt = ttk.Button(emnab, text='OK', command=lambda:cwa(emnab))
                    okbtt.place(relx=.17, rely=.55, relwidth=.31, relheight=.2)

                    # "CANCEL" BUTTON --- 

                    cnclbtt = ttk.Button(emnab, text='Cancel', command=lambda:cwa(emnab))
                    cnclbtt.place(relx=.52, rely=.55, relwidth=.31, relheight=.2)

                    emnab.mainloop()

                    return 

                # CREATING TABLE CALLLED "ACCOUNT" SAVED TO BNK DATABASE ---

                ctcasbd = """CREATE TABLE ACCOUNT(

                    "DATES" DATE, 
                    "ITEMS" TEXT, 
                    "AMOUNT" INTEGER,
                    "BALANCE" INTEGER,
                    "DESCRIPTION" TEXT

                     )"""

                try:
                    sbmC.execute(ctcasbd)

                except:
                    time.sleep(.1)

                # DESCRIPTION SAVED TO "ACCOUNT" TABLE --- 

                dsbt = etbfd.get('1.0', 'end')
                etbfd.delete('1.0', 'end')

                # SUBTRACTING THE AMOUNT FROM BALANCE --- 

                for sbl in subal:
                    dsbl = sbl[0]
                    sbl1 = sbl[1]

                stafb = Decimal(sbl1) - assbt

                # DELETING ROW IN "BALANCE" TABLE BNK DATABASE ---

                sbmC.execute("DELETE FROM BALANCE WHERE rowid = "+str(dsbl))

                # STORING NEW BALANCE INSIDE "BALANCE" TABLE IN BNK DATABASE --- 

                bal_tbl = {

                "balance": [float(stafb)]

                }

                baldf = pd.DataFrame(bal_tbl)

                for bfl in range(len(baldf)):
                    bfl1 = baldf.iloc[bfl]
                    sbmC.execute("INSERT INTO BALANCE VALUES(?)", bfl1)

                # CREATING DICTIONARY TO STORE INSIDE "ACCOUNT" TABLE --- 

                cdsiat = {

                "DATES": [adsbt],
                "ITEMS": [isbtbd],
                "AMOUNT": [float(assbt)],
                "BALANCE": [float(stafb)],
                "DESCRIPTION": [dsbt]

                }

                # CREATING DATAFRAME FOR "ACCOUNT" TABLE --- 

                dFcdat = pd.DataFrame(cdsiat)

                # SAVING DATA TO "ACCOUNT" TABLE IN BNK DATABASE --- 

                for sdatbd in range(len(dFcdat)):
                    sdaR = dFcdat.iloc[sdatbd]
                    sbmC.execute("INSERT INTO ACCOUNT VALUES(?, ?, ?, ?, ?)", sdaR)

                sql.commit()


            # ROOT MENU FRAME --- 

            # ROOT BACKGROUND IMAGE --- 

            rbi = tk.PhotoImage(file="bnk_bc1.png")
            rbi2 = tk.Label(root, image=rbi)
            rbi2.place(relwidth=1, relheight=1)

            # ROOT MENU TITLE IMAGE --- 

            rmtifrm = tk.Frame(root, bg="black")
            rmtifrm.place(relx=.13, rely=.05, relwidth=.73, relheight=.22)
            rmti = tk.PhotoImage(file="bnk_.png")
            rmti2 = tk.Label(rmtifrm, image=rmti)
            rmti2.place(relwidth=1, relheight=1)

            rmf = tk.Frame(root, bg="#712F2F", bd=4)
            rmf.place(relx=.1, rely=.35, relwidth=.8, relheight=.5)

            # SUNKEN LABEL FOR INPUT SPENT --- 

            slfis = tk.Label(rmf, bg="#8D7070", bd=3, relief="sunken")
            slfis.place(relwidth=.6, relheight=1)

            # LABEL RIDGE FOR FILTER AMOUNT AND ENTRY --- 

            lrffae = tk.Label(slfis, bg="#8D7070", relief="ridge")
            lrffae.place(relx=.2, rely=.16, relwidth=.6, relheight=.2)

            # OPTION BOX FOR SPENT ITEMS --- 

            obfsi_lst = [

            "Items", "Food", "Phone", "Rent", "School", "Bills", "Other"

            ]

            obfsi_str = tk.StringVar(slfis)

            obfsi = ttk.OptionMenu(slfis, obfsi_str, *obfsi_lst)
            obfsi.place(relx=.35, rely=.1, relwidth=.3, relheight=.08)

            # ENTRY FOR AMOUNT --- 

            efa = tk.Entry(lrffae, bd=3, relief="sunken")
            efa.config(font=("Calibri", 15))
            efa.place(relx=.03, rely=.15, relwidth=.94, relheight=.7)

            # LABEL RIDGE FOR DESCRITION --- 

            lrfd = tk.Label(slfis, bg="#8D7070", relief="ridge")
            lrfd.place(relx=.05, rely=.42, relwidth=.9, relheight=.3)

            # LABEL TEXT "DESCRIPTION" --- 

            ltd = tk.Label(slfis, bg="#8D7070", text="Description")
            ltd.place(relx=.08, rely=.38)

            # ENTER TEXT BOX FOR DESCRIPTION --- 

            etbfd = tk.Text(lrfd)
            etbfd.config(font=("Calibri", 10))
            etbfd.place(relx=.03, rely=.13, relwidth=.93, relheight=.77)

            # BUTTON TO SUBMIT SUBJECT / AMOUNT / DESCRIPTION --- 

            bssad = ttk.Button(slfis, text="Submit", command=lambda: subM())
            bssad.place(relx=.3, rely=.7, relwidth=.4, relheight=.12)

            # LABEL SUNKEN FOR CHECK BALANCE AND ANALYSIS --- 

            lscba = tk.Label(rmf, bg="#712F2F", bd=3, relief="sunken")
            lscba.place(relx=.61, relwidth=.39, relheight=1)

            # BUTTON FOR ADDING NEW BALANCE MENU --- 

            banb = ttk.Button(lscba, text="Add New Balance", command=lambda: anb(bnkDc))
            banb.place(relx=.15, rely=.1, relwidth=.7, relheight=.2)

            # BUTTON TO CHECK BALANCE --- 

            btcb = ttk.Button(lscba, text="Check Balance", command=lambda: chkb(bnkDc))
            btcb.place(relx=.15, rely=.4, relwidth=.7, relheight=.2)

            # BUTTON FOR ANALYSIS MENU --- 

            bfam = ttk.Button(lscba, text="Analytics", command=lambda: analytics(bnkDc, usr, pass_))
            bfam.place(relx=.15, rely=.7, relwidth=.7, relheight=.2)

            # BUTTON TO LOGOUT --- 

            brbmm = ttk.Button(root, text="Logout", command=lambda: login())
            brbmm.place(relx=.35, rely=.88, relwidth=.3, relheight=.07)

            root.mainloop()
            break

        else:
            # WRONG USERNAME AND PASSWORD LABEL TEXT --- 

            wuplt = tk.Label(root, text="Wrong Username or Password", bg="black", fg="red")
            wuplt.place(relx=.35, rely=.55)

            root.mainloop()
            break


# FUNCTION FOR SMALL MENU SHOWING BALANCE --- 

def chkb(sqlB):
    try:
        # CLOSING THE BALANCE WINDOW --- 
        def cbw(clse):
            clse.destroy()


        # STARTING BNK DATABASE CURSOR --- 

        chkbSql = sqlB.cursor()

        # GRABBING BALANCE FROM DATABASE --- 

        bal = chkbSql.execute("SELECT rowid, * FROM BALANCE").fetchall()

        for bl in bal:
            blc = bl[1]

        # MENU FOR CHECKING BALANCE --- 

        smsb = tk.Toplevel()

        # Gets the requested values of the height and widht.

        smsbwW = smsb.winfo_reqwidth()
        smsbwH = smsb.winfo_reqheight()
         
        # Gets both half the screen width/height and window width/height

        smsbpR = int(smsb.winfo_screenwidth()/2 - smsbwW/2)
        smsbpD = int(smsb.winfo_screenheight()/2 - smsbwH/2)
         
        # Positions the window in the center of the page.

        smsb.geometry("+{}+{}".format(smsbpR, smsbpD))
        smsb.title("Balance")
        smsb.geometry("300x150")

        # FRAME FOR BALANCE --- 

        ffb = tk.Label(
            smsb, bg='#F7F6EE', 
            text='Your Current Balance is $'+f"{blc:,.2f}", anchor='c')
        ffb.place(relx=.1, rely=.1, relwidth=.8, relheight=.3)

        # "OK" BUTTON --- 

        okbtt = ttk.Button(smsb, text='OK', command=lambda:cbw(smsb))
        okbtt.place(relx=.17, rely=.55, relwidth=.31, relheight=.2)

        # "CANCEL" BUTTON --- 

        cnclbtt = ttk.Button(smsb, text='Cancel', command=lambda:cbw(smsb))
        cnclbtt.place(relx=.52, rely=.55, relwidth=.31, relheight=.2)

        smsb.mainloop()

    except:
        # CLOSING THE ERROR WINDOW FOR NO AVAILABLE BALANCE --- 

        def cwnab(clse):
            clse.destroy()


        # ERROR MESSAGE FOR NO AVAILABLE BALANCE --- 

        emia = tk.Toplevel()

        # Gets the requested values of the height and widht.

        emiawW = emia.winfo_reqwidth()
        emiawH = emia.winfo_reqheight()
         
        # Gets both half the screen width/height and window width/height

        emiapR = int(emia.winfo_screenwidth()/2 - emiawW/2)
        emiapD = int(emia.winfo_screenheight()/2 - emiawH/2)
         
        # Positions the window in the center of the page.

        emia.geometry("+{}+{}".format(emiapR, emiapD))
        emia.title("Error")
        emia.geometry("300x150")

        # FRAME FOR ERROR IN NO BALANCE --- 

        fenab = tk.Label(
            emia, bg='#F7F6EE', 
            text='No balance available', anchor='c')
        fenab.place(relx=.1, rely=.1, relwidth=.8, relheight=.3)

        # "OK" BUTTON --- 

        okbtt = ttk.Button(emia, text='OK', command=lambda:cwnab(emia))
        okbtt.place(relx=.17, rely=.55, relwidth=.31, relheight=.2)

        # "CANCEL" BUTTON --- 

        cnclbtt = ttk.Button(emia, text='Cancel', command=lambda:cwnab(emia))
        cnclbtt.place(relx=.52, rely=.55, relwidth=.31, relheight=.2)

        emia.mainloop()

        return 


# FUNCTION FOR ANALYSIS MENU --- 

def analytics(sql, usr, pass_):

    # FUNCTION FOR QUERYING ACCOUNT INTO TREEVIEW --- 

    def anqry():

        # FUNCTION FOR QUERYING DATES --- 

        def anins(anN, anvl):
            gd = {

                "DATES": [],
                "ITEMS": [],
                "AMOUNT": [],
                "BALANCE": [],
                "DESCRIPTION": []

                }

            for fld in anvl:
                # YEAR IN BNK DATABASE "ACCOUNT" TABLE--- 

                cdy = int(fld[1][6:])

                # MONTH IN BNK DATABASE "ACCOUNT" TABLE--- 

                cdm = int(fld[1][:-8])

                # DAY IN BNK DATABASE "ACCOUNT" TABLE--- 

                cdd = int(fld[1][3:-5])

                # YEAR IN "FROM" FILTER --- 

                try:
                    ffy = int(ofyamStr.get())

                except:
                    pass

                # MONTH IN "FROM" FILTER --- 

                try:
                    ffm = int(ofmamStr.get())

                except:
                    pass

                # DAY IN "FROM" FILTER --- 

                try:
                    ffd = int(ofdamStr.get())

                except:
                    pass

                # YEAR IN "TO" FILTER --- 

                try:
                    fty = int(obslfyStr.get())

                except:
                    pass

                # MONTH IN "TO" FILTER --- 

                try:
                    ftm = int(obslfmStr.get())

                except:
                    pass

                # DAY IN "TO" FILTER --- 

                try:
                    ftd = int(otdamStr.get())

                except:
                    pass

                # CONVERTING DATES TO DATETIME MOD IN BNK DATABASE "ACCOUNT" TABLE --- 

                cddm = datetime(cdy, cdm, cdd)

                # CONVERTING DATES TO DATETIME MOD IN "FROM" FILTER IN ANALYTICS PAGE --- 

                try:
                    cddf = datetime(ffy, ffm, ffd)

                except:
                    pass

                # CONVERTING DATES TO DATETIME MOD IN "TO" FILTER IN ANALYTICS PAGE --- 

                try:
                    cddt = datetime(fty, ftm, ftd)

                except:
                    pass
                        
                # CONDITION FOR QUERYING ITEMS --- 

                try:
                    if fld[2] == iobaStr.get() and cddf <= cddm <= cddt:
                        anN+=1
                        tvam.insert(
                        "", "end", values=(str(anN), fld[1], fld[2], '$'+f"{fld[3]:,.2f}", fld[5]))
                        gd["DATES"].append(fld[1])
                        gd["ITEMS"].append(fld[2])
                        gd["AMOUNT"].append(fld[3])
                        gd["BALANCE"].append(fld[4])
                        gd["DESCRIPTION"].append(fld[5])

                except:
                    pass

                try:
                    if "Items" == iobaStr.get() and cddf <= cddm <= cddt:
                        anN+=1
                        tvam.insert(
                        "", "end", values=(str(anN), fld[1], fld[2], '$'+f"{fld[3]:,.2f}", fld[5]))
                        gd["DATES"].append(fld[1])
                        gd["ITEMS"].append(fld[2])
                        gd["AMOUNT"].append(fld[3])
                        gd["BALANCE"].append(fld[4])
                        gd["DESCRIPTION"].append(fld[5])

                except:
                    pass

            df = pd.DataFrame(gd)
            
            # ITEMS DICTIONARY --- 

            ils = {
                
                "Dates": [],
                "Balance": [],
                "Amount": []
                
            }

            # GETTING RID OF DUPLICATES AND STORING THEM INSIDE OF DICTIONARY --- 

            for d in df["DATES"]:
                if d not in ils["Dates"]:
                    ils["Dates"].append(d)

            # APPENDING ALL ITEMS BALANCES AND AMOUNTS --- 
                
            for i in ils["Dates"]:
                result = df[(df['DATES'].str.contains(i))]
                
                # APPENDING BALANCE TO DICTIONARY
                
                balance = result["BALANCE"].iloc[-1]
                ils["Balance"].append(balance)
                
                # ALL ITEMS AMOUNT ADDED AND APPENDED TO DICTIONARY --- 
                
                amount = result["AMOUNT"].sum()
                ils["Amount"].append(amount)

            ipd = pd.DataFrame(ils)
            plt.style.use('dark_background')
            plt.bar(ipd["Dates"], ipd["Amount"])
            plt.xticks(rotation=45)
            plt.title("Amount Spent For Each Day")
            plt.ylabel("Amount")
            plt.show()


        for antredel in tvam.get_children():
            tvam.delete(antredel)

        # ACTIVATING SQL CURSOR --- 

        andb = sql.cursor()

        # ACCESSING "ACCOUNT" TABLE IN BNK DATABASE --- 

        try:
            antbl = andb.execute("SELECT rowid, * FROM ACCOUNT").fetchall()

        except:
            # CLOSING THE ERROR WINDOW FOR NO ITEMS AVAILABLE --- 

            def cwia(clse):
                clse.destroy()


            # ERROR MESSAGE FOR NO ITEMS AVAILABLE --- 

            emia = tk.Toplevel()

            # Gets the requested values of the height and widht.

            emiawW = emia.winfo_reqwidth()
            emiawH = emia.winfo_reqheight()
             
            # Gets both half the screen width/height and window width/height

            emiapR = int(emia.winfo_screenwidth()/2 - emiawW/2)
            emiapD = int(emia.winfo_screenheight()/2 - emiawH/2)
             
            # Positions the window in the center of the page.

            emia.geometry("+{}+{}".format(emiapR, emiapD))
            emia.title("Error")
            emia.geometry("300x150")

            # FRAME FOR NO ITEMS AVAILABLE --- 

            feia = tk.Label(
                emia, bg='#F7F6EE', 
                text='No items are available\nplease input items in main page', anchor='c')
            feia.place(relx=.1, rely=.1, relwidth=.8, relheight=.3)

            # "OK" BUTTON --- 

            okbtt = ttk.Button(emia, text='OK', command=lambda:cwia(emia))
            okbtt.place(relx=.17, rely=.55, relwidth=.31, relheight=.2)

            # "CANCEL" BUTTON --- 

            cnclbtt = ttk.Button(emia, text='Cancel', command=lambda:cwia(emia))
            cnclbtt.place(relx=.52, rely=.55, relwidth=.31, relheight=.2)

            emia.mainloop()

            return

        # TREEVIEW TO DISPLAY ACCOUNT INFORMATION --- 

        tvam['column'] = ("Index", "Date", "Item", "Amount", "Description")
        tvam['show'] = 'headings'

        for anclm in tvam['column']:
            tvam.heading(anclm, text=anclm)

        # FOR LOOP THROUGH DATES IN BNK DATABASE "ACCOUNT" TABLE--- 

        n1 = 0

        # QUERYING ITEMS AND DATES --- 

        anins(n1, antbl)


    # FRAME FOR DATE FILTERS FOR ANALYTICS MENU ---

    fdfam = tk.Frame(root, bg="#525C5D", bd=4)
    fdfam.place(relx=.1, rely=.35, relwidth=.8, relheight=.5)

    # SUNKEN LABEL FOR DATE FILTER "FROM" ANALYTICS MENU --- 

    fdffam = tk.Label(fdfam, bg="#738385", bd=3, relief="sunken")
    fdffam.place(relwidth=.55, relheight=.15)

    # OPTION FILTER FOR "FROM MONTH" ANALYTICS MENU --- 

    ofmamLs = [

    'Month', '1', '2', '3', '4',
    '5', '6', '7', '8', '9',
    '10', '11', '12'

    ]

    ofmamStr = tk.StringVar(fdffam)

    ofmam = ttk.OptionMenu(fdffam, ofmamStr, *ofmamLs)
    ofmam.place(relx=.03, rely=.15, relwidth=.30, relheight=.7)

    # OPTION FILTER FOR "FROM DAY" ANALYTICS MENU --- 

    ofdamLs = [

    "Day", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"

    ]

    ofdamStr = tk.StringVar(fdffam)

    ofdam = ttk.OptionMenu(fdffam, ofdamStr, *ofdamLs)
    ofdam.place(relx=.35, rely=.15, relwidth=.30, relheight=.7)

    # OPTION FILTER FOR "FROM YEARS" ANALYTICS MENU --- 

    ofyamLs = [

    'Year', "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"

    ]

    ofyamStr = tk.StringVar(fdffam)

    ofyam = ttk.OptionMenu(fdffam, ofyamStr, *ofyamLs)
    ofyam.place(relx=.67, rely=.15, relwidth=.30, relheight=.7)

    # LABEL RIDGE TO SEPERATE DATES --- 

    lrtsd = tk.Label(fdfam, bg="#525C5D", bd=2, relief="ridge")
    lrtsd.place(relx=.15, rely=.18, relwidth=.23, relheight=.01)

    # SUNKEN LABEL FOR DATE FILTER "TO" ANALYTICS MENU

    fdftan = tk.Label(fdfam, bg="#738385", bd=3, relief="sunken")
    fdftan.place(rely=.21, relwidth=.55, relheight=.15)

    # OPTION BOX IN 2ND SUNKEM LABEL FOR "TO MONTH" --- 

    obslfmLs = [

    'Month', '1', '2', '3', '4', 
    '5', '6', '7', '8', '9', 
    '10', '11', '12'

    ]

    obslfmStr = tk.StringVar(fdftan)

    obslfm = ttk.OptionMenu(fdftan, obslfmStr, *obslfmLs)
    obslfm.place(relx=.03, rely=.15, relwidth=.30, relheight=.7)

    # OPTION FILTER FOR "TO DAY" ANALYTICS MENU --- 

    otdamLs = [

    "Day", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"

    ]

    otdamStr = tk.StringVar(fdftan)

    otdam = ttk.OptionMenu(fdftan, otdamStr, *otdamLs)
    otdam.place(relx=.35, rely=.15, relwidth=.30, relheight=.7)

    # OPTION BOX IN 2ND SUNKEM LABEL FOR "TO YEAR" ---

    obslfyLs = [

    'Year', "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"

    ]    

    obslfyStr = tk.StringVar(fdftan)

    obslfy = ttk.OptionMenu(fdftan, obslfyStr, *obslfyLs)   
    obslfy.place(relx=.67, rely=.15, relwidth=.30, relheight=.7)

    # LABEL RIDGE FOR ITEM FILTER AND SERACH BUTTON --- 

    lrifsb = tk.Label(fdfam, bg="#525C5D", relief="ridge")
    lrifsb.place(relx=.57, relwidth=.41, relheight=.36)

    # LABEL RIDGE FOR ITEM OPTION BOX --- 

    lriob = tk.Label(lrifsb, bg="#525C5D", relief="ridge")
    lriob.place(relx=.05, rely=.2, relwidth=.9, relheight=.5)

    # ITEM OPTION BOX FOR ANALYTICS --- 

    iobaLs = [

    "Items", "Food", "Phone", "Rent", "School", "Bills", "Other"

    ]

    iobaStr = tk.StringVar(lriob)

    ioba = ttk.OptionMenu(lriob, iobaStr, *iobaLs)
    ioba.place(relx=.03, rely=.07, relwidth=.93)

    # BUTTON TO SEARCH BNK DATABASE --- 

    bsbd = ttk.Button(lrifsb, text="Search", command=lambda: anqry())
    bsbd.place(relx=.15, rely=.6, relwidth=.7)

    # TREE VIEW FOR ANALYTICS MENU --- 

    tvam = ttk.Treeview(fdfam)
    tvam.place(rely=.38, relwidth=.96, relheight=.57)

    # Y SCROLL BAR FOR TREE VIEW ANALYTICS --- 

    ysbtva = tk.Scrollbar(fdfam, orient="vertical", command=tvam.yview)
    tvam.config(yscrollcommand=ysbtva.set)
    ysbtva.place(relx=.96, rely=.38, relwidth=.04, relheight=.62)

    # X SCROLL BAR FOR TREE VIEW ANALYTICS --- 

    xsbtva = tk.Scrollbar(fdfam, orient="horizontal", command=tvam.xview)
    tvam.config(xscrollcommand=xsbtva.set)
    xsbtva.place(rely=.95, relwidth=.96, relheight=.05)

    # BUTTON TO TO RETURN TO MENU --- 

    brbmm = ttk.Button(root, text="Main Menu", command=lambda: main(bnkDc, usr, pass_))
    brbmm.place(relx=.35, rely=.88, relwidth=.3, relheight=.07)


# FUNCTION FOR ADD NEW BALANCE PAGE--- 

def anb(sqlanb):
    # FUNCTION TO SUBMIT NEW BALANCE --- 

    def anbq():
        # CURSOR FOR ACTIVATING DATABASE TO CHANGE BALANCE --- 

        ccb = sqlanb.cursor()

        # NEW BALANCE ENTRY CONVERTED TO FLOAT

        try:
            nbecf = Decimal(eanb.get())

        except:
            # DELETING ENTRY FOR NEW BALANCE --- 

            eanb.delete(0, "end")

            # CLOSING THE ERROR WINDOW FOR CANT CONVERT STRING TO FLOAT ERROR --- 

            def cwsf(clse):
                clse.destroy()


            # ERROR MESSAGE FOR CANT CONVERT STRING TO FLOAT ERROR --- 

            emsf = tk.Toplevel()

            # Gets the requested values of the height and widht.

            emsfwW = emsf.winfo_reqwidth()
            emsfwH = emsf.winfo_reqheight()
             
            # Gets both half the screen width/height and window width/height

            emsfpR = int(emsf.winfo_screenwidth()/2 - emsfwW/2)
            emsfpD = int(emsf.winfo_screenheight()/2 - emsfwH/2)
             
            # Positions the window in the center of the page.

            emsf.geometry("+{}+{}".format(emsfpR, emsfpD))
            emsf.title("Error")
            emsf.geometry("300x150")

            # FRAME FOR ERROR FOR CANT CONVERT STRING TO FLOAT ERROR --- 

            fesf = tk.Label(
                emsf, bg='#F7F6EE', 
                text='Incorrect input must be an integer', anchor='c')
            fesf.place(relx=.1, rely=.1, relwidth=.8, relheight=.3)

            # "OK" BUTTON --- 

            okbtt = ttk.Button(emsf, text='OK', command=lambda:cwsf(emsf))
            okbtt.place(relx=.17, rely=.55, relwidth=.31, relheight=.2)

            # "CANCEL" BUTTON --- 

            cnclbtt = ttk.Button(emsf, text='Cancel', command=lambda:cwsf(emsf))
            cnclbtt.place(relx=.52, rely=.55, relwidth=.31, relheight=.2)

            emsf.mainloop()

            return 

        # CREATING "BALANCE" TABLE IN BNK DATABASE --- 

        cbt = """CREATE TABLE BALANCE(

            "BALANCE" INTEGER

            )"""

        try:
            ccb.execute(cbt)

        except:
            pass

        # ACTIVATING "BALANCE" TABLE IN BNK DATABASE --- 

        ccbx = ccb.execute("SELECT rowid, * FROM BALANCE").fetchall()

        # GRABBING ROWID FROM "BALANCE" TABLE IN BNK DATABASE --- 

        for grb in ccbx:
            grb1 = grb[0]

        # DELETING BALANCE IN "BALANCE" TABLE IN BNK DATABASE --- 

        try:
            ccb.execute("DELETE FROM BALANCE WHERE rowid="+str(grb1))

        except:
            pass

        # INSERTING NEW BALANCE IN "BALANCE" TABLE IN BNK DATABASE --- 

        inbd = {

        "balance": [float(nbecf)]

        }

        inbpd = pd.DataFrame(inbd)

        for insnb in range(len(inbpd)):
            insnb1 = inbpd.iloc[insnb]
            ccb.execute("INSERT INTO BALANCE VALUES(?)", insnb1)

        # DELETING ENTRY FOR NEW BALANCE --- 

        eanb.delete(0, "end")

        sqlanb.commit()


    # PAGE TO "ADD NEW BALANCE" --- 

    panb = tk.Toplevel()

    # Gets the requested values of the height and widht.

    panbwW = panb.winfo_reqwidth()
    panbwH = panb.winfo_reqheight()
     
    # Gets both half the screen width/height and window width/height

    panbpR = int(panb.winfo_screenwidth()/2 - panbwW/2)
    panbpD = int(panb.winfo_screenheight()/2 - panbwH/2)
     
    # Positions the window in the center of the page.

    panb.geometry("+{}+{}".format(panbpR, panbpD))
    panb.title("Balance")
    panb.geometry("300x150")

    panb.geometry("300x300")
    panb.title("Add New Balance")

    # BACKGROUND PICTURE FOR "ADD NEW BALANCE" --- 

    bpanb1 = tk.PhotoImage(file="bnk_bc2.png")
    bpanb2 = tk.Label(panb, image=bpanb1)
    bpanb2.place(relwidth=1, relheight=1)

    # SUNKEN LABEL FOR "ADD NEW BALNCE" --- 

    slanb = tk.Label(panb, bg="#507062", bd=3, relief="sunken")
    slanb.place(relx=.1, rely=.25, relwidth=.8, relheight=.4)

    # RIDGE LABEL FOR "ADD NEW BALANCE" --- 

    rlanb = tk.Label(slanb, bg="#507062", relief="ridge")
    rlanb.place(relx=.1, rely=.2, relwidth=.8, relheight=.4)

    # ENTRY FOR "ADD NEW BALANCE" --- 

    eanb = tk.Entry(rlanb, relief="flat")
    eanb.config(font=("Calibri", 13))
    eanb.place(relx=.02, rely=.1, relwidth=.96, relheight=.8)

    # SUBMIT BUTTON TO "ADD NEW BALANCE" --- 

    sbanb = ttk.Button(panb, text="Add Balance", command=lambda: anbq())
    sbanb.place(relx=.29, rely=.57, relwidth=.4, relheight=.12)

    panb.mainloop()


# STARTING BNK DATABASE CONNECTION --- 

bnkDc = sqlite3.connect("BNK.db")

# ROOT MAIN MENU --- 

root = tk.Tk()
root.geometry("600x600")
root.title("BNK")

def login():
    # ROOT BACKGROUND IMAGE ---

    lrbi = tk.PhotoImage(file="bnk_bc1.png")
    lrbi2 = tk.Label(root, image=lrbi)
    lrbi2.place(relwidth=1, relheight=1)

    # ROOT LOGIN TITLE IMAGE --- 

    lrmtifrm = tk.Frame(root, bg="black")
    lrmtifrm.place(relx=.13, rely=.05, relwidth=.73, relheight=.22)
    lrmti = tk.PhotoImage(file="bnk_.png")
    lrmti2 = tk.Label(lrmtifrm, image=lrmti)
    lrmti2.place(relwidth=1, relheight=1)

    # ROOT LOGIN USER LABEL ---

    rlul = tk.Label(root, bg="#292929", text="User:", fg="white")
    rlul.config(font=("Calibri", 13))
    rlul.place(relx=.21, rely=.6)

    # ROOT USER ENTRY LOGIN ---

    ruel = tk.Entry(root, bd=3, relief="sunken")
    ruel.config(font=("Calibri", 12))
    ruel.place(relx=.3, rely=.6, relwidth=.4, relheight=.05)

    # ROOT LOGIN PASSWORD LABEL ---

    rlpl = tk.Label(root, bg="#292929", text="Password:", fg="white")
    rlpl.config(font=("Calibri", 13))
    rlpl.place(relx=.16, rely=.66)

    # ROOT PASSWORD ENTRY LOGIN ---

    rpel = tk.Entry(root, bd=3, relief="sunken", show="*")
    rpel.config(font=("Calibri", 12))
    rpel.place(relx=.3, rely=.66, relwidth=.4, relheight=.05)

    # ROOT LOGIN BUTTON ---

    rlb = ttk.Button(root, text="Login", command=lambda: main(bnkDc, ruel.get(), rpel.get()))
    rlb.place(relx=.47, rely=.73, relwidth=.2, relheight=.05)

    root.mainloop()


login()