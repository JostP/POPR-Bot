#!/bin/python3

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

username = "email"		# Username za POPR npr. jp1530@student.uni-lj.si
password = "geslo"

finished = False
dogodek = input("Dogodek: ")
if dogodek == "hiit" or dogodek == "Hiit":		# Če maš več gumbov bo pri "stevilka_gumba_od_spodaj == 1" pritisnl spodnji gumb, pri "2" predzadnjega itd.
    stevilka_gumba_od_spodaj = 2
elif dogodek == "fitnes" or dogodek == "Fitnes":
    stevilka_gumba_od_spodaj = 1
elif dogodek == "plavanje" or dogodek == "Plavanje":
    stevilka_gumba_od_spodaj = 1
else:
    print("Neveljaven dogodek")
    exit()


koda = input("Koda dogodka: ")		# Vsak dogodek ma svojo kodo, to so zadnje štiri številke v URL-ju, npr https://popr.uni-lj.si/.../event/7897     --> 7897

hour = time.localtime(time.time()).tm_hour
minute = time.localtime(time.time()).tm_min
sec = time.localtime(time.time()).tm_sec
print("Trenuten čas: " + str(hour) + ":" + str(minute))
print("Čakanje na uro začetka prijavljanja: 06:01")

while not finished:
    hour = time.localtime(time.time()).tm_hour
    minute = time.localtime(time.time()).tm_min
    sec = time.localtime(time.time()).tm_sec
    
    if hour == 6 and minute == 1: # Začel se bo prijavljat ob 06:01
        print("Začetek prijavljanja ob", str(hour) + ":" + str(minute))
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get('https://popr.uni-lj.si//student/home.html')
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        uporabnik = driver.find_element("id", 'username')
        uporabnik.send_keys(username)
        
        geslo = driver.find_element("id", 'user_pass')
        geslo.send_keys(password)
        
        poslji = driver.find_element('id', 'wp-submit')
        poslji.click()
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yesbutton')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()
         
        bt = driver.find_element('id', 'yesbutton')
        text = bt.text
        bt.click()
        print("Prijavljen v POPR")
        time.sleep(5)
        driver.get('https://popr.uni-lj.si/student/svc/events.html#/user/event/' + str(koda))
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm')))
        except TimeoutException:
            print("Loading took too much time!")
            exit()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        bt = driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sm')
        time.sleep(1)
        joinButton = bt[len(bt) - stevilka_gumba_od_spodaj]
        
        if str(joinButton.text) == "Book":
            joinButton.click()
        else:
            print("Gumb ni bil najden: ", joinButton.text)
            exit()
            
        time.sleep(1)
        bt = driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-primary')
        
        if str(bt[len(bt)-1].text) == "Yes":
            bt[len(bt)-1].click()

        else:
            print("Gumb ni bil najden: ", bt[len(bt)-1].text)

        try:
			# Pri enih dogodkih moraš napisat kje si izvedu za ta dogodek, ponavad na nekaterih slabo obiskanih delavnicah iz FDVja, no offence:),
			# pa pol rabs se obkljukat en checkbox, pri športnih aktivnostih tega ni, zato gre program sam naprej če ne najde checkboxa.
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
            bt = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            bt.click()
            
        except TimeoutException:
            print("Neuspešno obkljukan checkbox oziroma ga sploh ni")

        try:
            bt = driver.find_element(By.XPATH, "//button[@type='submit']")
            bt.click()
            
        except:
            print("Neuspešna prijava")
            exit()

        print("Uspešno prijavljen na dogodek:)!")
        finished = True
    time.sleep(60)


