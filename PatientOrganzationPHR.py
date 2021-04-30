from bs4 import BeautifulSoup
import requests
import json
import math
import tkinter as tk
from  tkinter import ttk 
import tkinter.messagebox
import urllib.request as req
import urllib.request as req
import urllib.request as urllib2
k = 0
k1 = 0
total = 0
ALL = []






window = tk.Tk()
window.title('PatientPHR查詢')
window.geometry('1000x800')
window.configure(background='white')

    
    
def pdata():
        global ALL_url,k1
        tree.delete(*tree.get_children())
        total=''
        pid=''
        og1=''
        rio=[]
        rio2=''
        
        
        print(len(ALL_url),len([k1]))
        url=ALL_url[k1]["self"]
        token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw'
        request=urllib2.Request(url,headers={'Authorization':token})

        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")
            fhir_str=json.loads(data)
        
            total=fhir_str["total"]

            for i in range(total):              
                pid="Patient ID ："+fhir_str["entry"][i]["resource"]["id"]
                og = id_entry.get()
                og1=str(og)
                rio.append(pid)
                rio.append(og1)
            for i in range(0,total*2,2):
                tree.insert("",i,text=rio[i],values=(rio[i+1]))

            tree.pack()
def bt():
    global relation,k1,total,ALL_url
    og = id_entry.get()
    url='http://192.168.50.3:10610/gateway/fhir/Patient?organization=Organization/'+str(og)
    #url = "https://oauth.dicom.org.tw/fhir/Patient?organization=Organization/"+str(og)
    Token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw"
    r = requests.get(url, headers={'Authorization': Token})
    soup = BeautifulSoup(r.text,'html.parser')

    dicts = json.loads(str(soup).replace("(\"","").replace("\")",""))
    for i in dicts:
            line = i
            if i == "total":
                total = dicts[i]
            if i == "link":
                print(123)
                ALL_url.append({"self":"","next":"","previous":""})
                relation = ""
                link(dicts,i)
                k1 += 1
                
    while int(total) - k1*20 > 0:
        r = requests.get(ALL_url[k1-1]["next"], headers={'Authorization': Token})
        soup = BeautifulSoup(r.text,'html.parser')
        dicts = json.loads(json.dumps(str(soup)))
        for i in dicts:
            line = i
            if i == "link":
                ALL_url.append({"self":"","next":"","previous":""})
                relation = ""
                link(dicts,i)
                k1 += 1
    k1 = 0
    pdata()
            
                

header_label = tk.Label(window, text='Patient資料')
header_label.pack()

id_frame = tk.Frame(window)
id_frame.pack(side=tk.TOP)
id_label = tk.Label(id_frame, text='請輸入Patien Organization')
id_label.pack(side=tk.LEFT)
id_entry = tk.Entry(id_frame)
id_entry.pack(side=tk.LEFT)

result_label = tk.Label(window)
result_label.pack()
id_btn2 = tk.Button(window, text='查詢', command=bt)
id_btn2.pack()

tree=ttk.Treeview(window)
s = ttk.Style().configure("Treeview",rowheight=50)

word=tree["columns"]=("Organization")

tree.heading("#0",text="Id")
tree.heading("Organization",text="Organizaion")

tree.column("#0",width=200)
tree.column("Organization",width=200)










def link(m,n):
    global k1,relation
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

ALL_url = []
relation = ""


    
        

def nextpage():
    global k1
    if total - k1*20 >= 20:
        k1 += 1
        pdata()
def prepage():
    global k1
    if k1 > 0:
        k1 -= 1
        pdata()


button1 = tk.Button(window, text = "上一頁",command=prepage)
button1.pack()

button2 = tk.Button(window, text = "下一頁",command=nextpage)
button2.pack()

window.mainloop()
