# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:01:15 2024

@author: Medonlakador Syiem
"""
import PySimpleGUI as psg
import scan

def initialize():
    layout = [        
                        [psg.Column([
                            [psg.Text("NetAnalyst",
                                  font=("Verdana", 40))]],
                                  justification='center',
                                  element_justification='center')],
                        
                        [psg.Column([
                            [psg.Text("Let's scan your network")],
                            [psg.Text("Enter the IP Address/Range"),psg.InputText(),psg.Button('Scan')]],
                                  element_justification='left')],
                        
                        # TABLE
                        [psg.Column(
                            [[psg.Table({},
                                  font=("Verdana", 14),
                                  headings=["IP Address","Mac Address", "Vendor Name"],
                                  key="VendorData",
                                  col_widths=[25, 25, 50],
                                  auto_size_columns=False,
                                  num_rows=40,
                                  justification='center',
                                  size=(1200, 500))]],
                          justification='center', 
                          element_justification='center')],
                      [psg.Text("Footer")],
                ]
    # psg.theme("Dark Grey 9")
    psg.theme("BrownBlue")

    window = psg.Window('NetAnalyst',
                        layout,
                        font=("Verdana", 20),
                        margins=(50,20),
                        location=(0,0),
                        size=(1920,1080),
                        finalize=True)

    window.maximize()
    
    while True:
        event, values = window.read()
        window["VendorData"].update(visible = not window["VendorData"].visible)
        
        if event == 'Scan':
            window["VendorData"].update(visible = True)
            # SCAN RESULT
            scan_result = scan.beginScan(values[0])
            new_table_data = [[row['ip'], row['mac'], row['vendorName']] for row in scan_result]
            window["VendorData"].update(values=new_table_data)
            
            print('You entered ', values[0])

        if event == psg.WIN_CLOSED:# if user closes window or clicks cancel
            break
    
    window.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    