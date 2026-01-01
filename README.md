# Wordclock

Wordclock powered by Raspberry Pi Pico and Waveshare e-paper 3.7". Wordclock displays the actual time with **GERMAN** words onto a 3.7" Waveshare e-paper display (e.g. "ES IST FÜNF MINUTEN NACH VIER").

There is a light and dark mode, which can be set in wordclock.py:
´´´ python
# Night_Mode ist Weisse Schrift auf schwarzem Grund (z.B. für nachts)
Night_Mode_Hours = False
# Night_Mode_Hours = True
# Night_Mode_Hours = (18,19,20,21,22,23,0,1,2,3,4,5)
´´´
The clock will be synced 2 times a day: At 02:00 and 03:00 (for daylight saving)...

- [Required Hardware](#required-hardware)
- [Installation](#installation)
- [Links](#links)

## Required Hardware
* Raspberry Pi Pico (e.g. RP2040 or newer)
* Waveshare e-paper display 3.7", 480 x 280 pixel
* Power (battery or AC adapter)

## Installation
1. Get an api key from **Free Time Zone Database**
2. Connect the pico the the e-paper display
3. Upload all files to your Raspberry Pi Pico (e.g., with [Thonny](https://thonny.org/)).
4. Start wordclock.py (e.g., with Thonny)
5. wordclock needs a wifi connection and an api key for syncing time. This config is saved in wordclock.conf. If not set, wordclock starts a wifi access point *WORDCLOCK*, where you are able to enter the values.
6. To start wordclock automaticaly - rename wordclock.py to main.py

## Links
* [Raspberry Pi Pico-series](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
* [Waveshare 3.7" e-paper display](https://www.waveshare.com/pico-epaper-3.7.htm)
* [Free Time Zone Database & API](https://www.timezonedb.com/)
