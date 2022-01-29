#!/usr/bin/python3
# ===================================================================
# example from: stackoverflow.com/questions/75088895/
#               getting-the-value-or-index-of-combobox-itm
# ===================================================================

import PySimpleGUI as sg

#font2     = ('Aerial',12)
#font4     = ('Aerial',14)
font4      = ('Courier New',14)
font6      = ('Courier New',16)
font8      = ('Courier New',18)

clst = ['choice1','choice2','choice3']

layout = [ [sg.Combo(clst,
                    enable_events=True,
                    default_value=' do it ',
                    font=font8,
                    key='combo')],
           [sg.Button('Test',font=font8),
            sg.Exit(font=font8)] ]

win = sg.Window('combo test',layout)

while True:

    event,values = win.read()
    if event is None or event == 'Exit':
        break

    print()
    print(f'event = {event}')
    print(f'values= {values}')

    if event == 'Test':
        combo = values['combo']  # use the conbo key
        print()
        print(f'combo = {combo}')

win.Close()
print()
