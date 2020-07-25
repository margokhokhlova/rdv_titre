import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#sendgrid data



driver = webdriver.Chrome('D:/chromedriver.exe')
driver.get('https://rdv-etrangers-94.interieur.gouv.fr/eAppointmentpref94/element/jsp/specific/pref94.jsp')

code = driver.find_element_by_id('CPId')
code.send_keys("94300")

nextButton1 = driver.find_element_by_css_selector(".btn.btn-primary[value='Continuer']").click()

checkboxes = driver.find_elements_by_css_selector("[name='selectedMotiveKeyList']")
select_motive = checkboxes[1].click()

sleep(5)


while True:
    alert = False
    nextButton2 = driver.find_element_by_id("nextButtonId").click()
    sleep(10)
    try:
        #Switch the control to the Alert window
        alert = driver.switch_to.alert
        print(f'Alert {alert}')
        if alert:
            #Retrieve the message on the Alert window
            msg = alert.text
            print(f"Alert shows following message: {msg}")
            if msg == "Aucun rendez-vous n'est possible pour les motifs selectionnnés ou le créneau horaire séléctionné.":
                #use the accept() method to accept the alert
                alert.accept()
                print(" Clicked on the OK Button in the Alert Window")
                # 15 min
                sleep(18000)
    except:
        print('no alert, send notification')
        message = Mail(
        from_email='', 
        to_emails='',  # add your email
        subject='There is a rendez-vous to take in the prefecture!',
        html_content='<strong>Go and book your rendez-vous</strong>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
        # select RDV
        # some code
        # click on save rdv button
        saveRdvId = driver.find_element_by_id("saveRdvId").click()
        driver.close()


