import bixel
import machine
import rtc
import sys
import time
import wlan
import wordclockconfig

print('Programm          : WordClock ePaper (3.7" Version)')
print(f'Machine-Id        : {machine.unique_id()}')
print(f'Machine-Freq      : {machine.freq() / 1_000_000} MHz')
print(f"sys.implementation: {sys.implementation}\n")


# Night_Mode ist Weisse Schrift auf schwarzem Grund (z.B. für nachts)
Night_Mode_Hours = False
# Night_Mode_Hours = True
# Night_Mode_Hours = (18,19,20,21,22,23,0,1,2,3,4,5)


# Merker für "letzte Worte", damit das Display nicht unnötig aktualisiert wird
Last_Words = None


# Bixel-Klasse und ePaper initialisieren
Bixel = bixel.Bixel(X_Size = 4, Y_Size = 4, X_Spacing = 1, Y_Spacing = 1, X_Offset = 3, Y_Offset = -2)


SSID, PASSWORD, API_KEY = wordclockconfig.load_config()


# WLAN aktivieren (notwendig für Ermittlung der aktuellen Uhrzeit)
WLAN = wlan.WLAN(verbose_mode = True)

while WLAN.connect(ssid=SSID, password = PASSWORD, timeout = 30) == False:
    WLAN.info()
    Bixel.ePaper.image4Gray.fill(Bixel.ePaper.white)
    Bixel.Draw_Word(5, Bixel.Y_Max, "WLAN ERROR", Bixel.ePaper.black, True, 270)
    Bixel.Draw_Word(5 + 7 + 7, Bixel.Y_Max, "STARTE NUN DEN", Bixel.ePaper.black, False, 270)
    Bixel.Draw_Word(5 + 7 + 7 + 7, Bixel.Y_Max, "WLAN HOTSPOT", Bixel.ePaper.black, False, 270)
    Bixel.Draw_Word(5 + 7 + 7 + 7 + 7 + 7, Bixel.Y_Max, "-= WORDCLOCK =-", Bixel.ePaper.black, True, 270)
    Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
    
    # Phew Accesspoint starten (wird beendet, sobald die Config geschrieben wird)
    wordclockconfig.ap_start()
    # Config erneut einlesen
    SSID, PASSWORD, API_KEY = wordclockconfig.load_config()


# Realtimeclock setzen anhand der Zeit eines Timeservers
while rtc.set(API_KEY) == False:
    print("RTC ERROR")
    Bixel.ePaper.image4Gray.fill(Bixel.ePaper.white)
    Bixel.Draw_Word(5, Bixel.Y_Max, "RTC ERROR", Bixel.ePaper.black, True, 270)
    Bixel.Draw_Word(5 + 7 + 7, Bixel.Y_Max, "STARTE NUN DEN", Bixel.ePaper.black, False, 270)
    Bixel.Draw_Word(5 + 7 + 7 + 7, Bixel.Y_Max, "WLAN HOTSPOT", Bixel.ePaper.black, False, 270)
    Bixel.Draw_Word(5 + 7 + 7 + 7 + 7 + 7, Bixel.Y_Max, "-= WORDCLOCK =-", Bixel.ePaper.black, True, 270)
    Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
    
    # Phew Accesspoint starten (wird beendet, sobald die Config geschrieben wird)
    wordclockconfig.ap_start()
    
    # Config erneut einlesen
    SSID, PASSWORD, API_KEY = wordclockconfig.load_config()


# WLAN de-aktivieren (zum Strom sparen)
WLAN.disconnect()


# Alle Buchstaben der Uhr (8 Zeilen mit je 16 Zeichen)
Clock_Letters = [
    'ESQLZISTHXGENAUM',
    'IFÜNFKZEHNGKURZR',
    'ZWANZIGDVIERTELA',
    'MINUTENYÖVORNACH',
    'HALBÜSECHSIEBENW',
    'MDREINSBZWEIJELF',
    'UVIERSZWÖLFÜNFEQ',
    'PACHTZEHNEUNÄUHR'
]


# Positionen der einzelnen Teil-Worte und Zahlen
Clock_Words = {}
Clock_Words["ES"]       = [[0,0],  [0,1]]
Clock_Words["IST"]      = [[0,5],  [0,6],  [0,7]]
Clock_Words["GENAU"]    = [[0,10], [0,11], [0,12], [0,13],[0,14]]
Clock_Words["FUENF"]    = [[1,1],  [1,2],  [1,3],  [1,4]]
Clock_Words["ZEHN"]     = [[1,6],  [1,7],  [1,8],  [1,9]]
Clock_Words["KURZ"]     = [[1,11], [1,12], [1,13], [1,14]]
Clock_Words["ZWANZIG"]  = [[2,0],  [2,1],  [2,2],  [2,3],[2,4],[2,5],[2,6]]
Clock_Words["VIERTEL"]  = [[2,8],  [2,9],  [2,10], [2,11],[2,12],[2,13],[2,14]]
Clock_Words["MINUTEN"]  = [[3,0],  [3,1],  [3,2],  [3,3],[3,4],[3,5],[3,6]]
Clock_Words["VOR"]      = [[3,9],  [3,10],  [3,11]]
Clock_Words["NACH"]     = [[3,12], [3,13], [3,14], [3,15]]
Clock_Words["HALB"]     = [[4,0],  [4,1],  [4,2],  [4,3]]
Clock_Words[6]          = [[4,5],  [4,6],  [4,7],  [4,8],[4,9]]
Clock_Words[7]          = [[4,9],  [4,10], [4,11], [4,12],[4,13],[4,14]]
Clock_Words[3]          = [[5,1],  [5,2],  [5,3],  [5,4]]
Clock_Words[-1]         = [[5,3],  [5,4],  [5,5]]
Clock_Words[1]          = [[5,3],  [5,4],  [5,5],  [5,6]]
Clock_Words[2]          = [[5,8],  [5,9],  [5,10], [5,11]]
Clock_Words[11]         = [[5,13], [5,14], [5,15]]
Clock_Words[4]          = [[6,1],  [6,2],  [6,3],  [6,4]]
Clock_Words[12]         = [[6,6],  [6,7],  [6,8],  [6,9],[6,10]]
Clock_Words[5]          = [[6,10], [6,11], [6,12], [6,13]]
Clock_Words[8]          = [[7,1],  [7,2],  [7,3],  [7,4]]
Clock_Words[10]         = [[7,5],  [7,6],  [7,7],  [7,8]]
Clock_Words[9]          = [[7,8],  [7,9],  [7,10], [7,11]]
Clock_Words["UHR"]      = [[7,13], [7,14], [7,15]]


# Nächsten Lauf für Ermittlung der Uhrzeit (wegen Sommer-/Winterzeitwechsel) festlegen
Local_Time   = time.localtime()
Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
if Local_Hour < 2: #                   Nächster Lauf um 02:00
    next_run = time.mktime((Local_Year, Local_Month, Local_Day, 2, 0, 0, 0, 0))
elif Local_Hour == 2: #                Nächster Lauf um 03:00
    next_run = time.mktime((Local_Year, Local_Month, Local_Day, 3, 0, 0, 0, 0))
else: #                                Nächster Lauf morgen um 02:00
    next_run = time.mktime((Local_Year, Local_Month, Local_Day + 1, 2, 0, 0, 0, 0))


def Get_Active_Words(Local_Time = None):
    if Local_Time == None:
        Local_Time = time.localtime()
    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
    
    Active_Words = []
    Active_Words.append("ES")
    Active_Words.append("IST")
    
    if Local_Minute % 5 == 0:
            Active_Words.append("GENAU")
    if Local_Minute == 0:
        Active_Words.append("UHR")
    elif Local_Minute in (1,2):
        for _ in ("KURZ", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (3,4,5,6,7):
        for _ in ("FUENF", "MINUTEN", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (8,9,10,11,12):
        for _ in ("ZEHN", "MINUTEN", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (13,14,15,16,17):
        for _ in ("VIERTEL","NACH"):
            Active_Words.append(_)
    elif Local_Minute in (18,19,20,21,22):
        for _ in ("ZWANZIG", "MINUTEN", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (23,24,25,26,27):
        for _ in ("FUENF", "MINUTEN", "VOR", "HALB"):
            Active_Words.append(_)
    elif Local_Minute in (28,29):
        for _ in ("KURZ", "VOR", "HALB"):
            Active_Words.append(_)
    elif Local_Minute == 30:
        Active_Words.append("HALB")
    elif Local_Minute in (31,32):
        for _ in ("KURZ", "NACH", "HALB"):
            Active_Words.append(_)
    elif Local_Minute in (33,34,35,36,37):
        for _ in ("FUENF", "MINUTEN", "NACH", "HALB"):
            Active_Words.append(_)
    elif Local_Minute in (38,39,40,41,42):
        for _ in ("ZWANZIG", "MINUTEN", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (43,44,45,46,47):
        for _ in ("VIERTEL", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (48,49,50,51,52):
        for _ in ("ZEHN", "MINUTEN", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (53,54,55,56,57):
        for _ in ("FUENF", "MINUTEN", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (58,59):
        for _ in ("KURZ", "VOR"):
            Active_Words.append(_)
    
    # Stunde noch berechnen
    Local_Hour_Logical = Local_Hour
    if Local_Minute == 0 and Local_Hour == 1:
        Local_Hour_Logical = -1
    elif Local_Minute >= 23:
        Local_Hour_Logical += 1
    
    if Local_Hour_Logical == 0:
        Local_Hour_Logical = 12
    elif Local_Hour_Logical > 12:
        Local_Hour_Logical -= 12
    
    Active_Words.append(Local_Hour_Logical)
    
    return Active_Words

    
while True:
    Local_Time  = time.localtime()
    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
    print(f"RTC Stunde {Local_Hour} - Minute {Local_Minute} - Sekunde {Local_Second}")
    
    print(f"RTC wird in {(next_run-time.time())} Sekunde(n) neugestellt...")
    
    if next_run <= time.time():
        print("RTC wird nun neugestellt...")
        if WLAN.connect(timeout = 5) == True:
            if rtc.set() == True:
                print("RTC erfolgreich neugestellt...")
                Local_Time  = time.localtime()
                Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
                if Local_Hour < 2: #       Nächster Lauf um 02:00
                    next_run = time.mktime((Local_Year, Local_Month, Local_Day, 2, 0, 0, 0, 0))
                elif Local_Hour == 2: #    Nächster Lauf um 03:00
                    next_run = time.mktime((Local_Year, Local_Month, Local_Day, 3, 0, 0, 0, 0))
                else: #                    Nächster Lauf morgen um 02:00
                    next_run = time.mktime((Local_Year, Local_Month, Local_Day  + 1, 2, 0, 0, 0, 0))
                WLAN.disconnect()
            else: #                        Nächster Lauf in 1 Minute
                print("RTC ERROR, neuer Versuch in 60 Sekunden...")
                next_run += 60
        else:
            print("RTC ERROR (WLAN ERROR), neuer Versuch in 60 Sekunden...")
            next_run += 60
    
    Local_Time  = time.localtime()
    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
    
    Active_Words = Get_Active_Words(Local_Time)
    print(Active_Words)
    
    if Active_Words != Last_Words:
        
        # Night_Mode prüfen
        if (type(Night_Mode_Hours) == bool) and  (Night_Mode_Hours == True):
            # print("Night_Mode on")
            Color_Background  = Bixel.ePaper.black
            Color_Letter_On   = Bixel.ePaper.white
            Filled_Letter_On  = True
            Color_Letter_Off  = Bixel.ePaper.darkgray
            Filled_Letter_Off = True
        elif (type(Night_Mode_Hours) == tuple) and (Local_Hour in Night_Mode_Hours):
            # print("Night_Mode on")
            Color_Background  = Bixel.ePaper.black
            Color_Letter_On   = Bixel.ePaper.white
            Filled_Letter_On  = True
            Color_Letter_Off  = Bixel.ePaper.darkgray
            Filled_Letter_Off = True
        else:
            # print("Night_Mode off")
            Color_Background  = Bixel.ePaper.white
            Color_Letter_On   = Bixel.ePaper.black
            Filled_Letter_On  = True
            Color_Letter_Off  = Bixel.ePaper.grayish
            Filled_Letter_Off = True
        
        # Komplette Anzeige leeren
        Bixel.ePaper.image4Gray.fill(Color_Background)
        
        # Gewünschte Buchstaben der Uhr "highlighten"
        Clock_Colors = [[(Color_Letter_Off, Filled_Letter_Off) for x in range(16)] for y in range(8)]
        
        for Active_Word in Active_Words:
            Clock_Word = Clock_Words[Active_Word]
            for _ in range(len(Clock_Word)):
                Clock_Colors[Clock_Word[_][0]][Clock_Word[_][1]] = (Color_Letter_On, Filled_Letter_On)
        
        # Aktuelle Uhrzeit anzeigen (Alle Buchstaben zeichnen)
        x = 5 #                            Untere Reihe der 1. Zeile
        for _ in range(0, len(Clock_Letters)):
            Clock_Letters_Line = Clock_Letters[_]
            y = Bixel.Y_Max #        1. Spalte der aktuellen Zeile
            for __ in range(0, len(Clock_Letters_Line)):
                color, filled = Clock_Colors[_][__]
                Bixel.Draw_Letter(x, y, Clock_Letters_Line[__], color, filled, 270)
                y -= 6
            x += 7
        
        # ePaper aktualisieren
        Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
        
        Last_Words = Active_Words
    
    Local_Time   = time.localtime()
    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
    
    print(f'Warte {60 - Local_Second} Sekunde(n) bis zur nächsten vollen Minute')
    
    # lightsleep wacht zu früh wieder auf... :-(
    time.sleep(60 - Local_Second)
    # time.sleep_ms(5)
    # machine.lightsleep((60 - Local_Second) * 1000)
    # time.sleep_ms(5)
    
    print("Bin wieder wach...")
