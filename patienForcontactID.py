import tkinter as tk
import math
import urllib.request as req
import json
import urllib.request as urllib2




window = tk.Tk()
window.title('Patient查詢')
window.geometry('600x800')
window.configure(background='white')


    
    
def pdata():
    try:
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
        pid = id_entry.get()
        
        url='http://192.168.50.3:10610/gateway/fhir/Patient/'+str(pid)
        #url="https://oauth.dicom.org.tw/fhir/Patient/"+str(pid)
        token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw'
    
    
        request=urllib2.Request(url,headers={'Authorization':token})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")
            fhir_str=json.loads(data)

        
            if pid==fhir_str["id"] and fhir_str["managingOrganization"]["reference"]=='Organization/MITW.ForContact':
                pn='病人姓名：'+fhir_str["name"][0]["text"]
                pf="病人姓氏："+fhir_str["name"][0]["family"]
                for j in fhir_str["identifier"]:
                    if j["system"]=="https://www.dicom.org.tw/cs/passportNumber":
                        passport="護照號碼："+j["value"]
                    elif j["system"]=="https://www.dicom.org.tw/cs/identityCardNumber_tw":
                        ir="身分證字號："+j["value"]
                    elif j["system"]=="https://www.dicom.org.tw/cs/ResidentNumber_tw":
                        ir="居留證號碼："+j["value"]
                for telecom in fhir_str["telecom"]:
                    try:
                        if telecom["system"]=="phone":
                            pe="手機號碼："+telecom["value"]
                        elif telecom["system"]=="email":
                            pe="電子郵件地址"+telecom["value"]
                    except:
                        pass
                active="使用中？："+str(fhir_str["active"])
                gender="性別："+fhir_str["gender"]
                birth="生日："+fhir_str["birthDate"]
                address="地址："+fhir_str["address"][0]["text"]
                try:
                    for relate in fhir_str["contact"]:
                        cname="聯絡人姓名："+relate["name"]["text"]
                        crelate="聯絡人關係："+relate["relationship"][0]["text"]
                        cphone="聯絡人電話號碼："+relate["telecom"][0]["value"]
                        cemail="聯絡人email信箱："+relate["telecom"][1]["value"]
                        caddress="聯絡人住址："+relate["address"]["text"]
                except:
                    result="ID not found"
                    result_label.configure(text=result)
                og="管理機構："+fhir_str["managingOrganization"]["reference"]
            result = 'Patient ID{}'.format(pid),'資料為：{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(noresult,pn,pf,passport,ir,pe,gender,active,birth,address,cname,crelate,cphone,cemail,caddress,og)
            result_label.configure(text=result)
    except:
        result="id can not find"
        result_label.configure(text=result)

            
           
   
    
header_label = tk.Label(window, text='Patient資料')
header_label.pack()

id_frame = tk.Frame(window)
id_frame.pack(side=tk.TOP)
id_label = tk.Label(id_frame, text='請輸入Patien ID')
id_label.pack(side=tk.LEFT)
id_entry = tk.Entry(id_frame)
id_entry.pack(side=tk.LEFT)

result_label = tk.Label(window)
result_label.pack()
id_btn2 = tk.Button(window, text='查詢', command=pdata)
id_btn2.pack()


window.mainloop()
