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
                           # visible=False,
                           col_widths=[40,40,70])]
                ]
    psg.theme("Dark Grey 9")
    window = psg.Window('NetAnalyst',
                        layout,
                        size=(1920,1080),
                        finalize=True)
    window.maximize()

    screen_width, screen_height = window.get_screen_dimensions()
    window.move(0,0)
    screen_width = screen_width/2
    window.size=(screen_width, screen_height)
    
    while True:
        event, values = window.read()
        window["VendorData"].update(visible = not window["VendorData"].visible)
        
        if event == 'Scan':
            window["VendorData"].update(visible = True)
            scan_result = scan.beginScan(values[0])
            new_table_data = [[row['ip'], row['mac'], row['vendorName']] for row in scan_result]
            window["VendorData"].update(values=new_table_data)
            
            print('You entered ', values[0])

        if event == psg.WIN_CLOSED:# if user closes window or clicks cancel
            break
    
    window.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    