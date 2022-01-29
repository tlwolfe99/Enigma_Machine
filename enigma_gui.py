# ===================================================================
# Create an enigma machine simple GUI
# ===================================================================

import PySimpleGUI as sg
import sys

def enigma_gui(config):

    #font2     = ('Aerial',12)
    #font4     = ('Aerial',14)
    font2      = ('Courier New',14)
    font4      = ('Courier New',16)

    rotors     = list(config.rotors.keys())
    abc        = config.abc
    abclen     = config.abclen
    tsize      = 64              # GUI text field size

    # ---- GUI rotors -----------------------------------------------

    names  = config.default_rotor_names
    starts = config.default_rotor_starts

    rotor1 = [ [sg.Combo(rotors,
                         default_value=names[2],
                         font=font4,key='-RROTOR-'),
                sg.Combo(abc,
                         default_value=abc[starts[2]],
                         font=font4,key='-RPOSITION-',size=(2,1))]]
    rotor2 = [ [sg.Combo(rotors,
                         default_value=names[1],
                         font=font4,key='-MROTOR-'),
                sg.Combo(abc,
                         default_value=abc[starts[1]],
                         font=font4,key='-MPOSITION-',size=(2,1))]]
    rotor3 = [ [sg.Combo(rotors,
                         default_value=names[0],
                         font=font4,key='-LROTOR-'),
                sg.Combo(abc,
                         default_value=abc[starts[0]],
                         font=font4,key='-LPOSITION-',size=(2,1))]]

    # ---- big alphabet (many characters) ---------------------------

    alphabet0 = [ 'A','B','C','D','E','F','G','H','I','J','K','L',
                  'M','N','O','P','Q','R','S','T','U','V','W','X',
                  'Y','Z','1','2','3','4','5','6','7','8','9','0',
                  '.','=','+','-','/','*','(',')' ]
    layout0   = [ [sg.Button('1',font=font4),
                   sg.Button('2',font=font4),
                   sg.Button('3',font=font4),
                   sg.Button('4',font=font4),
                   sg.Button('5',font=font4),
                   sg.Button('6',font=font4),
                   sg.Button('7',font=font4),
                   sg.Button('8',font=font4),
                   sg.Button('9',font=font4),
                   sg.Button('0',font=font4)],

                  [sg.Button('Q',font=font4),
                   sg.Button('W',font=font4),
                   sg.Button('E',font=font4),
                   sg.Button('R',font=font4),
                   sg.Button('T',font=font4),
                   sg.Button('Y',font=font4),
                   sg.Button('U',font=font4),
                   sg.Button('I',font=font4),
                   sg.Button('O',font=font4),
                   sg.Button('P',font=font4)],

                  [sg.Button('A',font=font4),
                   sg.Button('S',font=font4),
                   sg.Button('D',font=font4),
                   sg.Button('F',font=font4),
                   sg.Button('G',font=font4),
                   sg.Button('H',font=font4),
                   sg.Button('J',font=font4),
                   sg.Button('K',font=font4),
                   sg.Button('L',font=font4)],

                  [sg.Button('Z',font=font4),
                   sg.Button('X',font=font4),
                   sg.Button('C',font=font4),
                   sg.Button('V',font=font4),
                   sg.Button('B',font=font4),
                   sg.Button('N',font=font4),
                   sg.Button('M',font=font4),
                   sg.Button('.',font=font4),
                   sg.Button('M',font=font4)],

                  [sg.Button('=',font=font4),
                   sg.Button('+',font=font4),
                   sg.Button('-',font=font4),
                   sg.Button('*',font=font4),
                   sg.Button('(',font=font4),
                   sg.Button(')',font=font4)] ]

    # ---- enigma alphabet (26 characters) --------------------------
    # ---- special key layout for enigma alphabet

    alphabet1 = [ 'A','B','C','D','E','F','G','H','I','J','K','L','M',
                  'N','O','P','Q','R','S','T','U','V','W','X','Y','Z' ]
    layout1   = [ [sg.Button('Q',font=font4),
                   sg.Button('W',font=font4),
                   sg.Button('E',font=font4),
                   sg.Button('R',font=font4),
                   sg.Button('T',font=font4),
                   sg.Button('Y',font=font4),
                   sg.Button('U',font=font4),
                   sg.Button('I',font=font4),
                   sg.Button('O',font=font4),
                   sg.Button('P',font=font4)],

                  [sg.Button('A',font=font4),
                   sg.Button('S',font=font4),
                   sg.Button('D',font=font4),
                   sg.Button('F',font=font4),
                   sg.Button('G',font=font4),
                   sg.Button('H',font=font4),
                   sg.Button('J',font=font4),
                   sg.Button('K',font=font4),
                   sg.Button('L',font=font4)],

                  [sg.Button('Z',font=font4),
                   sg.Button('X',font=font4),
                   sg.Button('C',font=font4),
                   sg.Button('V',font=font4),
                   sg.Button('B',font=font4),
                   sg.Button('N',font=font4),
                   sg.Button('M',font=font4)] ]

    # ---- test alphabet --------------------------------------------

    alphabet2 = [ 'A','B','C','D','E','F' ]
    layout2   = [ [sg.Button('A',font=font4),
                   sg.Button('B',font=font4),
                   sg.Button('C',font=font4),
                   sg.Button('D',font=font4),
                   sg.Button('E',font=font4),
                   sg.Button('F',font=font4)] ]

    # ---- layout without alphabet ----------------------------------

    layoutx = [ [sg.Text(font=font4,text_color='black',key='-IN-',
                         background_color='white',size=(tsize,1))],
                [sg.Text(font=font4,text_color='black',key='-OUT-',
                         background_color='white',size=(tsize,1))],

                [sg.Button('Exit',font=font4),
                 sg.Button('Clear Buffer',font=font4),
                 sg.Button('Reset Rotors',font=font4),
                 sg.Button('Set Rotors',font=font4)],

                [sg.Frame('Left Rotor',rotor3,title_location='n',
                       border_width=2,key='-ROTOR3-'),
                 sg.Frame('Middle Rotor',rotor2,title_location='n',
                          border_width=2,key='-ROTOR2-'),
                  sg.Frame('Right Rotor',rotor1,title_location='n',
                           border_width=2,key='-ROTOR1-')],

                [sg.Button('Stats',font=font4),
                 sg.Button('Display',font=font4)],

                [sg.Button('Auto Advance On',font=font4),
                 sg.Button('Auto Advance Off',font=font4),
                 sg.Button('Sub Debug On',font=font4),
                 sg.Button('Sub Debug Off',font=font4)],

                [sg.Text(config.configfile,font=font2)] ]

    # ---- return a GUI window --------------------------------------

    if abclen == 44:                   # big alphabet
        layout = layout0 + layoutx
    elif abclen == 26:                 # enigma alphabet
        layout = layout1 + layoutx
    elif abclen == 6:                  # test apphabet
        layout = layout2 + layoutx
    else:
        print()
        print('internal error - ' +
              'alaphabet size and GUI layout mismatch - ' +
              'end program')
        print()
        sys.exit()

    win = sg.Window('Enigma Machine',layout,
                    element_justification='c')

    return (win,tsize)
