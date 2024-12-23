# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:01:15 2024

@author: Medonlakador Syiem
"""
import PySimpleGUI as psg
import scan

def initialize():
    layout = [      [psg.Text("Let's scan your network")],
                    [psg.Text("Enter the IP Address/Range"),psg.InputText()],
                    [psg.Button('Scan')],
                    [psg.Table({},
                           headings=["IP Address","Mac Address", "Vendor Name"],
                           key="VendorData",
                           visible=False)]
                ]

    window = psg.Window('NetAnalyst',
                        layout,
                        background_color="White",
                        size=(1920,1080),
                        finalize=True)
    window.maximize()
    
    while True:
        event, values = window.read()
        
        if event == 'Scan':
            # window["Table123"].update(visible=not window["Table123"].visible)
            window["VendorData"].update(visible = not window["VendorData"].visible)
            scan_result = scan.beginScan(values[0])
            new_table_data = [[row['ip'], row['mac'], row['vendorName']] for row in scan_result]
            window["VendorData"].update(values=new_table_data)
            
            print('You entered ', values[0])

        if event == psg.WIN_CLOSED:# if user closes window or clicks cancel
            break
    
    window.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    