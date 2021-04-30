from bs4 import BeautifulSoup
import requests
import json

import tkinter as tk
from  tkinter import ttk 
import tkinter.messagebox

k = 0
k1 = 0
total = 0
ALL = []
def check(m,n,line):
    global k,k1
    if type(m[n]) == dict:
        for i in m[n]:
            line =  line + str(n)
            check(m[n],i,line)
    elif type(m[n]) == list:
        if n == "name":
            ALL[k]["name"] = m[n]
        elif n == "identifier":
            ALL[k]["identifier"] = m[n]
        elif n == "telecom":
            ALL[k]["telecom"] = m[n]
        elif n == "address":
            ALL[k]["address"] = m[n]
        elif n == "contact":
            ALL[k]["contact"] = m[n]
        else:
            for i in m[n]:
                line = line + n
                check(m[n],m[n].index(i),line)
    else:
        if n == "resourceType" and m[n] == "Patient":
            ALL.append({"id":"","identifier":"","active":"","name":"","telecom":"","address":"","contact":"","managingOrganization":""})
        if n == "id":
            ALL[k]["id"] = m[n]
        if n == "active":
            ALL[k]["active"] = m[n]
        if n == "reference":
            ALL[k]["managingOrganization"] = m[n]
        if n == "mode" and m[n] == "match":
            #print("=="*20,end="\n\n")
            k += 1
            
def link(m,n):
    global k1,relation,total
    if type(m[n]) == dict:
        for i in m[n]:
            line =  i + " : "
            link(m[n],i)
    elif type(m[n]) == list:
        for i in m[n]:
            link(m[n],m[n].index(i))
    else:
        if relation == "self":
            ALL_url[k1]["self"] = m[n].replace("amp;","")
            relation = ""
        if relation == "next":
            ALL_url[k1]["next"] = m[n].replace("amp;","")
            relation = ""
        if relation == "previous":
            ALL_url[k1]["previous"] = m[n].replace("amp;","")
            relation = ""
        if m[n] == "self":
            relation = "self"
        if m[n] == "next":
            relation = "next"
        if m[n] == "previous":
            relation = "previous"

window=tk.Tk()
window.title("Id Search")
window.geometry("1000x600+250+15")



label = tk.Label(window, text = 'Id')
label.pack()
var = tk.StringVar()
entry = tk.Entry(window, textvariable=var,width = 40 )

entry.pack()

tree=ttk.Treeview(window)
s = ttk.Style().configure("Treeview",rowheight=50)

word=tree["columns"]=("identifier","active","name","telecom","address","contact","managingOrganization")

tree.heading("#0",text="id")
tree.heading("identifier",text="identifier")
tree.heading("active",text="active")
tree.heading("name",text="name")
tree.heading("telecom",text="telecom")
tree.heading("address",text="address")
tree.heading("contact",text="contact")
tree.heading("managingOrganization",text="managingOrganization")  

    
ALL_url = []
relation = ""
Id = ""
def bt():
    global relation,k1,total,Id,ALL_url
    ForContact = var.get()
    #url = "https://oauth.dicom.org.tw/fhir/Patient?organization="+ForContact
    url = "http://192.168.50.3:10610/gateway/fhir/Patient?organization="+ForContact
    Token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw"
    r = requests.get(url, headers={'Authorization': Token})
    soup = BeautifulSoup(r.text,'html.parser')
    soup = str(soup)[:str(soup).find("]")]+"]}"
    dicts = json.loads(soup)

    for i in dicts:
            line = i
            if i == "total":
                total = dicts[i]
            if i == "link":
                ALL_url.append({"self":"","next":"","previous":""})
                relation = ""
                link(dicts,i)
            if i == "id":
                Id = dicts[i]
    ALL_url = []
    now = 0           
    while int(total) - k1 > 0:
        ALL_url.append("http://192.168.50.3:10610/gateway/fhir?_getpages="+Id+"&_getpagesoffset="+str(now)+"&_count=1&_pretty=true&_bundletype=searchset")
        now += 1
        k1 += 1
    k1 = 0
    label1 = tk.Label(window, text = 'total='+str(total))
    label1.pack()
    main()
    
def main():
    print(k1)
    tree.delete(*tree.get_children())
    global ALL,k,ALL_url
    ALL = []
    k = 0
    Token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw"
    r = requests.get(ALL_url[k1], headers={'Authorization': Token})
    soup = BeautifulSoup(r.text,'html.parser')
    dicts = json.loads(str(soup).replace("(\"","").replace("\")",""))
    for i in dicts:
            line = i
            if i == "entry":
                check(dicts,i,line)
            
    tree.column("#0",width=60)
    tree.column("identifier",width=200)
    tree.column("active",width=50)
    tree.column("name",width=100)
    tree.column("telecom",width=200)
    tree.column("address",width=200)
    tree.column("contact",width=200)
    tree.column("managingOrganization",width=200)   


    for i in range(len(ALL)):
        tree.insert("",i,text=ALL[i]["id"],values=(ALL[i]["identifier"],ALL[i]["active"],ALL[i]["name"],ALL[i]["telecom"],ALL[i]["address"],ALL[i]["contact"],ALL[i]["managingOrganization"]))

    tree.pack()
              

def nextpage():
    global k1
    if total - k1*1 > 1:
        k1 += 1
        main()
def prepage():
    global k1
    if k1 > 0:
        k1 -= 1
        main()

button = tk.Button(window, text = "搜尋",command=bt)
button.pack()


button1 = tk.Button(window, text = "上一頁",command=prepage)
button1.pack()

button2 = tk.Button(window, text = "下一頁",command=nextpage)
button2.pack()

window.mainloop()
