#!/bin/python3

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

username = "username"       # Username za POPR npr. "ab1234@student.uni-lj.si"
password = "password"

finished = False


try:
    dogodek = input("Termin: ")   # Vnesi številko termina. Zadnji termin ima številko 1, predzadnji 2... Če je samo en termin vnesi število 1
    button_number = int(dogodek)

except ValueError:
    print("Neveljaven vnos. Vnesi celo stevilo od 1 do 10")
    exit()


if not (1 <= button_number <= 10):
    print("Neveljaven vnos. Vnesi celo stevilo od 1 do 10")
    exit()


koda = input("Koda dogodka: ")      # Vsak dogodek ma svojo kodo, to so zadnje štiri številke v URL-ju, npr https://popr.uni-lj.si/.../event/7897     --> 7897

hour = time.localtime(time.time()).tm_hour
minute = time.localtime(time.time()).tm_min
sec = time.localtime(time.time()).tm_sec

formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, sec)

print("---------------------------------------------------")
print("Trenuten čas: " + formatted_time)
print("Čakanje na začetek prijavljanja...")
print("Lahko noč:)")

while not finished:
    hour = time.localtime(time.time()).tm_hour
    minute = time.localtime(time.time()).tm_min
    sec = time.localtime(time.time()).tm_sec

    if hour == 5 and minute == 58: # V sistem POPR se bo prijavil dve minuti prej. Na dogodek se bo prijavil ob 6:00:00
        options = FirefoxOptions()
        #options.add_argument("--headless") # Program ne bo odprl firefox-a ampak bo firefox tekel v ozadju
        driver = webdriver.Firefox(options=options)
        driver.get('https://popr.uni-lj.si//student/home.html')

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0116')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        uporabnik = driver.find_element("id", 'i0116')
        uporabnik.send_keys(username)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        button = driver.find_element('id', 'idSIButton9')
        button.click()
        time.sleep(2)      # Pocakaj da se nalozi spletna stran, ker drugace javi napako

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0118')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        uporabnik = driver.find_element("id", 'i0118')
        uporabnik.send_keys(username)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        button = driver.find_element('id', 'idSIButton9')
        button.click()
        time.sleep(3)

# Preveri ali je bilo geslo pravilno
        try:
            element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'passwordError')))
            print("Napaka pri prijavi!")
            print("Neuspešno prijavljen!")
            exit()
        except TimeoutException:

            hour = time.localtime(time.time()).tm_hour
            minute = time.localtime(time.time()).tm_min
            sec = time.localtime(time.time()).tm_sec

            formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, sec)

            print("Uspešno prijavljen v POPR ob " + formatted_time + "!")
            print("Čakanje na 6:00:00 za prijavo na dogodek...")

        while not (hour == 6 and minute == 0):              # Počakaj da bo ura 6:00:00

            hour = time.localtime(time.time()).tm_hour
            minute = time.localtime(time.time()).tm_min
            sec = time.localtime(time.time()).tm_sec
            formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, sec)

            time.sleep(0.02)   # Počakaj 0,02 sekunde vsak krog, da se ne vrti na polno

        print("Čas: " + formatted_time)
        print("Začetek prijavljanja v aktivnost...")

        driver.get('https://popr.uni-lj.si/student/svc/events.html#/user/event/' + str(koda))

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        button= driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm')

        time.sleep(0.3)
        joinButton = button[len(button) - button_number]

        if str(joinButton.text) == "Book":
            joinButton.click()
        else:
            print("Gumb ni bil najden: ", joinButton.text)
            exit()

        button= driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-primary')

        if str(button[len(button)-1].text) == "Yes":
            button[len(button)-1].click()

        else:
            print("Gumb ni bil najden: ", button[len(button)-1].text)

        hour = time.localtime(time.time()).tm_hour
        minute = time.localtime(time.time()).tm_min
        sec = time.localtime(time.time()).tm_sec
        formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, sec)

        print("Uspešno prijavljen na dogodek :)")
        print("Prijavljen si bil ob: " + formatted_time)

        finished = True
    time.sleep(10)  # Počaka 10 sekund, da se while zanka ne porabi preveč računske moči
