import tkinter as tk
import math
import urllib.request as req
import json
import urllib.request as urllib2
import urllib
import requests
from urllib.request import quote
import jsonpath






window = tk.Tk()
window.title('Patient查詢')
window.geometry('600x800')
window.configure(background='white')





    
    
def pdata():
    pi=''
    noresult=''
    pid=''
    pn=''
    pf=''
    passport=''
    ir=''
    pe=''
    active=''
    gender=''
    birth=''
    address=''
    cname=''
    crelate=''
    cphone=''
    cemail=''
    caddress=''
    og=''
    listr=[]
    lista=[]
    listb=[]
    listc=[]
    listd=[]
    pid = id_entry.get()

        
    url='http://192.168.50.3:10678/hapi-fhir-jpaserver/fhir/Patient?name='
    
    url1=quote(str(pid))  
    url2="http://192.168.50.3:10678/hapi-fhir-jpaserver/fhir/Patient?name={}".format(url1)
    #url="http://startfhir.dicom.org.tw/fhir/Patient"
    token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw'
    
    print(url2)
    request=urllib2.Request(url2,headers={'Authorization':token})
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
        fhir_str=json.loads(data)
        print(fhir_str)
        for i in fhir_str["entry"]:
            print(i["resource"]["managingOrganization"]["reference"])
            try:
                if i["resource"]["managingOrganization"]["reference"]=="Organization/MITW.ForContact":
                
                    pi='病人ID：'+i["resource"]["id"]
                    pn='病人姓名：'+i["resource"]["name"][0]["text"]
                    try:
                        pf="病人姓氏："+i["resource"]["name"][0]["family"]
                    except:
                        pass
                    try:
                        for j in i["resource"]["identifier"]:
                            if j["system"]=="https://www.dicom.org.tw/cs/passportNumber":
                                passport="護照號碼："+j["value"]
                            elif j["system"]=="https://www.dicom.org.tw/cs/identityCardNumber_tw":
                                ir="身分證字號："+j["value"]
                            elif j["system"]=="https://www.dicom.org.tw/cs/ResidentNumber_tw":
                                ir="居留證號碼："+j["value"]
                    except:
                        pass
                    try:
                        for telecom in i["resource"]["telecom"]:
                            if telecom["system"]=="phone":
                                phone="手機號碼：",telecom["value"]
                            elif telecom["system"]=="email":
                                email="電子郵件地址"+telecom["value"]
                    except:
                        pass
                    try:
                        gender="性別："+i["resource"]["gender"]
                    except:
                        pass
                    try:
                        birth="生日："+i["resource"]["birthDate"]
                    except:
                        pass
                    try:
                        address="地址："+i["resource"]["address"][0]["text"]
                    except:
                        pass
                    try:
                        for relate in i["resource"]["contact"]:
                            try:
                                cname="聯絡人姓名："+relate["name"]["text"]
                                cnvget=relate["name"]
                                cnv=jsonpath.jsonpath(cnvget,"$..text")
                                for cnv2 in cnv:
                                    listr.append(cnv2)
                            except:
                                pass
                            try:
                                crelate=relate["relationship"][0]
                                
                                cre=jsonpath.jsonpath(crelate,"$..text")
                                for cre2 in cre:
                                    lista.append(cre2)
                            except:
                                pass
                            try:
                                cphone=relate["telecom"][0]
                                cph=jsonpath.jsonpath(cphone,"$..value")
                                for cph2 in cph:
                                    listb.append(cph2)
                            except:
                                pass
                            try:
                                cemail=relate["telecom"][1]
                                cem=jsonpath.jsonpath(cemail,"$..value")
                                for cem2 in cem:
                                    listc.append(cem2)
                            except:
                                pass
                            try:
                                caddress=relate["address"]
                                cad=jsonpath.jsonpath(caddress,"$..text")
                                for cad2 in cad:
                                    listd.append(cad2)
                            except:
                                pass
                    except:
                        pass
                    og="管理機構："+i["resource"]["managingOrganization"]["reference"]
                
                    result = 'Patient 姓名{}'.format(pid),'資料為：{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(noresult,pi,pn,pf,passport,ir,pe,gender,active,birth,address,listr,lista,listb,listc,listd,og)
                    result_label.configure(text=result)
                else:
                    result="data not found"
                    result_label.configure(text=result)
            except:
                result="data not found"
                result_label.configure(text=result)
                
           
   
    
header_label = tk.Label(window, text='Patient資料')
header_label.pack()

id_frame = tk.Frame(window)
id_frame.pack(side=tk.TOP)
id_label = tk.Label(id_frame, text='請輸入姓名')
id_label.pack(side=tk.LEFT)
id_entry = tk.Entry(id_frame)
id_entry.pack(side=tk.LEFT)

result_label = tk.Label(window)
result_label.pack()
id_btn2 = tk.Button(window, text='查詢', command=pdata)
id_btn2.pack()


window.mainloop()
