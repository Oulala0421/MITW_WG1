import tkinter as tk
import math
import urllib.request as req
import json
import urllib.request as urllib2




window = tk.Tk()
window.title('PatientPHR查詢')
window.geometry('600x800')
window.configure(background='white')

    
    
def pdata():
   
        pid=''
        og=''
        pid = id_entry.get()
        
        url='http://192.168.50.3:10610/gateway/fhir/Patient/'+str(pid)
        #url="http://startfhir.dicom.org.tw/fhir/Patient/"+str(pid)
        token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw'
        request=urllib2.Request(url,headers={'Authorization':token})
        try:
                with req.urlopen(request) as response:
                        data=response.read().decode("utf-8")
                        fhir_str=json.loads(data)
                        
                        if pid==fhir_str["id"] and fhir_str["managingOrganization"]["reference"]=="Organization/MITW.PHR" :
                                pid="Patient ID ："+fhir_str["id"]
                                og="管理機構："+fhir_str["managingOrganization"]["reference"]
                                result = 'Patient ID{}'.format(pid),'資料為：\n{}\n{}'.format(pid,og)
                                result_label.configure(text=result)
                        else:
                                result='ID ERROR'
                                result_label.configure(text=result)
                
        except:
                result='ID ERROR'
                result_label.configure(text=result)
'''
    except :
        result='DATA Error'
        result_label.configure(text=result)
'''
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
