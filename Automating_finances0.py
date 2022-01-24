import pandas as pd
from tkinter import *
import datetime
from openpyxl import Workbook

def submit_fields():
    df = pd.read_excel(path)
    # rmove rows where TD is '0'
    df = df[df["Today's Date"] != 'Weekly Total']
    # print(df)
    SeriesA = df["Today's Date"]
    SeriesB = df['Food']
    SeriesC = df['Clothes']
    SeriesD = df['Bills']
    SeriesE = df['Social']
    SeriesF = df['Travel']
    SeriesG = df['Art']
    SeriesH = df['Other']
    A = pd.Series(today)
    B = pd.Series(entry1.get(), dtype='int64')
    C = pd.Series(entry2.get(), dtype='int64')
    D = pd.Series(entry3.get(), dtype='int64')
    E = pd.Series(entry4.get(), dtype='int64')
    F = pd.Series(entry5.get(), dtype='int64')
    G = pd.Series(entry6.get(), dtype='int64')
    H = pd.Series(entry7.get(), dtype='int64')
    # ===== If data already entered for today's date, sum series rather than append =====
    if date == today:
        # print('same day')
        valueB = (df['Food'].iloc[-1]) + B
        valueC = (df['Clothes'].iloc[-1]) + C
        valueD = (df['Bills'].iloc[-1]) + D
        valueE = (df['Social'].iloc[-1]) + E
        valueF = (df['Travel'].iloc[-1]) + F
        valueG = (df['Art'].iloc[-1]) + G
        valueH = (df['Other'].iloc[-1]) + H
        df2 = pd.DataFrame({"Today's Date":SeriesA, "Food":SeriesB, "Clothes":SeriesC,
         "Bills":SeriesD, "Social":SeriesE, "Travel":SeriesF, "Art":SeriesG, "Other":SeriesH})
        df3 = pd.DataFrame({"Today's Date":date, "Food":valueB, "Clothes":valueC,
         "Bills":valueD, "Social":valueE, "Travel":valueF, "Art":valueG, "Other":valueH})
        df2.set_index("Today's Date", inplace=True)
        df3.set_index("Today's Date", inplace=True)
        df2.update(df3)
        df2 = df2.reset_index()
    # ===== If new date =====
    else:
        SeriesA = SeriesA.append(A)
        SeriesB = SeriesB.append(B)
        SeriesC = SeriesC.append(C)
        SeriesD = SeriesD.append(D)
        SeriesE = SeriesE.append(E)
        SeriesF = SeriesF.append(F)
        SeriesG = SeriesG.append(G)
        SeriesH = SeriesH.append(H)
        # ===== New df =====
        df2 = pd.DataFrame({"Today's Date":SeriesA, "Food":SeriesB, "Clothes":SeriesC,
         "Bills":SeriesD, "Social":SeriesE, "Travel":SeriesF, "Art":SeriesG, "Other":SeriesH})
        # df2.set_index("Today's Date", inplace=True)
    # ===== Daily total =====
    df2['Daily/Weekly Total'] = df2.sum(axis=1)
    # print(df2)
    # ========= Create week end and today's date df's ==========
    df4 = df2[["Today's Date"]].copy()
    # print(df4)
    df4["Today's Date"] = pd.to_datetime(df4["Today's Date"])
    df4['Week End'] = df4.apply(lambda row: row["Today's Date"] + datetime.timedelta(days=(6 - row["Today's Date"].weekday())), axis=1)
    df4 = df4[['Week End',"Today's Date"]]
    # print(df4)
    # ========= Create new df with multi index ===========
    index = pd.MultiIndex.from_frame(df4)
    # print(index)
    df2 = df2.set_index(index)
    df2 = df2.drop(["Today's Date"], axis=1)
    # print(df2)
    # ========= Weekly Total ===========
    lst = df2.index.get_level_values(0).drop_duplicates().to_list() # take from level 0 of index
    # print(lst)
    # df2 = df2.drop(['Week End'], axis=1)
    # print(df)
    first = True

    # ======= Unless row is entered weekly =========
    # if row is weekly total....

    for w_e in lst:
        df6 = df2[df2.index.get_level_values('Week End').isin([w_e])]
        df6.index = df6.index.set_levels([df6.index.levels[0], pd.to_datetime(df6.index.levels[1])])
        # print(df6)
        df7 = df6.groupby([pd.Grouper(level=0, freq='W', label='left')]).sum()
        df7["Today's Date"] = 'Weekly Total'
        df7['Week End'] = w_e
        df7.set_index(['Week End', "Today's Date"], inplace=True)
        # print(df7)
    # make list of df's and append/concat afterwards?
        df6 = df6.append(df7)
        # print(df6)
        if first == True:
            dffinal = df6
            first = False
        else:
            dffinal = dffinal.append(df6)
        # print(dffinal)
        # print('==================================')
    # ========== Net spend on new sheet? ===========
    net = pd.DataFrame({'Net Spend': inc - dffinal['Daily/Weekly Total']})
    # net = net.drop_duplicates().dropna()
    # print(net)
    dffinal = pd.concat([dffinal, net], axis=1)
    # print(dffinal)
    dffinal.to_excel(path)
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)
    entry7.delete(0, END)
    print('entry made:',str(entry1))

# =============== Date function ================
today = datetime.date.today()
# print(today)
day = today.weekday()
count = 0
# work out how far from monday we are
if day == 0:
    wkbeg = today
else:
    while day > 0:
        day = day - 1
        count = count + 1
# Work out date of previous monday
    tdelta = datetime.timedelta(days = count)
    wkbeg = today - tdelta

# =============== Income =================
income = 85
inc = int(income)

# =============== Create workbook if doesn't exist and create headers ===============
# path = '/Users/James/Desktop/Budget_test.xlsx'
path = '/Users/James/Desktop/Budget0.xlsx'
try:
    df = pd.read_excel(path)
    # print(df)
except:
    wb = Workbook()
    wb.save(path)
    df = pd.DataFrame(columns = ["Today's Date", "Food", "Clothes", "Bills",
    "Social", "Travel", "Art", "Other"])
    print(df)
    df.to_excel(path)

# =============== Last entry in Date column, doesnt work if date is index =================
# =============== Does try block execute all code or pop out at first error? pops out =================
try:
    date = df["Today's Date"].iloc[-1]
    if isinstance(date, datetime.datetime) == False:
        date = df["Today's Date"].iloc[-2]
    date = date.date()
    # print(date)
    last_month = date.month
    last_month_name = date.strftime('%B')
    month_tday = today.month
    month_name_tday = today.strftime('%B')
    new_year = today.year
    # =============== New sheet if different month =================
    if last_month != month_tday and date.year == today.year:
        print('New month: ',month_name_tday)
    elif last_month != month_tday and date.year != today.year :
        print('New year: ',new_year)
        # def function create new workbook
    else:
        print('Still',last_month_name,'baby')
except:
    date = None
    # If wb exists...

# =============== Create UI ===============
master = Tk()

Label(master, text = "Today's Date: " + str(today)).grid(row=0)
Label(master, text = 'Week beginning: ' + str(wkbeg)).grid(row=0, column = 1)
Label(master, text = 'Food').grid(row=1)
Label(master, text = 'Clothes').grid(row=2)
Label(master, text = 'Bills').grid(row=3)
Label(master, text = 'Social').grid(row=4)
Label(master, text = 'Travel').grid(row=5)
Label(master, text = 'Art').grid(row=6)
Label(master, text = 'Other').grid(row=7)

entry1 = Entry(master)
entry2 = Entry(master)
entry3 = Entry(master)
entry4 = Entry(master)
entry5 = Entry(master)
entry6 = Entry(master)
entry7 = Entry(master)

entry1.grid(row=1, column=1)
entry2.grid(row=2, column=1)
entry3.grid(row=3, column=1)
entry4.grid(row=4, column=1)
entry5.grid(row=5, column=1)
entry6.grid(row=6, column=1)
entry7.grid(row=7, column=1)

Button(master, text = 'Done', command = master.quit).grid(row = 8, pady = 20)
Button(master, text = 'Submit', command = submit_fields).grid(row = 8, column = 1, pady = 20)
Button(master, text = 'Show weekly spending', command = master.quit).grid(row = 9, column = 1, pady = 20)

mainloop()
