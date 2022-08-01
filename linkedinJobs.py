#import packages
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests

jobTitleList = []
companyNameList = []
localList = []
postedTimeList = []
numApplicantsList = []
jobDetailsList = []

job_data = pd.DataFrame({
'jobTitle': jobTitleList,
'companyName': companyNameList,
'local': localList,
'postedTime': postedTimeList,
'jobDetails': jobDetailsList
})

buttonShowMoreExists = False
endPage = False

max_itens = 100

#add %20 to replace " " blank space
cargo = "Programador%20Python"
pais = "Brasil"
vagasLink = f"https://www.linkedin.com/jobs/search?keywords={cargo}&location={pais}"

def checkShowMoreButton(htmlPage):
    buttonShowMoreExists = htmlPage.find_all('button', {'class':'infinite-scroller__show-more-button infinite-scroller__show-more-button--visible'})
    return bool(buttonShowMoreExists)

def checkEndPage(htmlPage):
    checkEndPage = htmlPage.find_all('div', {'class':'inline-notification see-more-jobs__viewed-all'})
    return bool(checkEndPage)

driver = webdriver.Chrome()
driver.get(vagasLink)

while not buttonShowMoreExists: 
    time.sleep(1)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    pageSource = driver.page_source
    html = BeautifulSoup(pageSource, 'html.parser')
    buttonShowMoreExists = checkShowMoreButton(html)

links = html.find_all('a', {'class':'base-card__full-link'})
links_list = list()

i = 0
for l in links:
    i = i + 1
    links_list.append(l.get('href'))

def crawlerVags(url):
    print(str(url))
    print('\n')
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    try:
        jobTitle = html.find('h1', {'class':'top-card-layout__title topcard__title'}).text
        jobTitleList.append(jobTitle)
    except:
        jobTitle = ''
        jobTitleList.append(jobTitle)

    try:
        companyName = html.find('a', {'class':'topcard__org-name-link topcard__flavor--black-link'}).text
        companyNameList.append(companyName)
    except:
        companyName = ''
        companyNameList.append(companyName)

    try:
        local = html.find('span', {'class':'topcard__flavor topcard__flavor--bullet'}).text
        localList.append(local)
    except:
        local = ''
        localList.append(local)

    try:
        postedTime = html.find('span', {'class':'posted-time-ago__text topcard__flavor--metadata'}).text
        postedTimeList.append(postedTime)
    except:
        postedTime = ''
        postedTimeList.append(postedTime)

    try:
        numApplicants = html.find('span', {'class':'num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet'}).text
        numApplicantsList.append(numApplicants)
    except:
        numApplicants = ''
        numApplicantsList.append(numApplicants)

    try:
        jobDetails = html.find('div', {'class':'description__text description__text--rich'}).text
        jobDetailsList.append(jobDetails)
    except:
        jobDetails = ''
        jobDetailsList.append(jobDetails)


    df_bs = pd.DataFrame({
    'jobTitle': jobTitleList,
    'companyName': companyNameList,
    'local': localList,
    'postedTime': postedTimeList,
    'jobDetails': jobDetailsList
    })
    df_bs['jobTitle'] = df_bs['jobTitle'].str.replace('\n',' ')
    df_bs['companyName'] = df_bs['companyName'].str.replace('\n',' ')
    df_bs['local'] = df_bs['local'].str.replace('\n',' ')
    df_bs['postedTime'] = df_bs['postedTime'].str.replace('\n',' ')
    df_bs['jobDetails'] = df_bs['jobDetails'].str.replace('\n',' ')

    df_bs.to_csv('jobs.csv')

#Loop in vagas
for i in range(max_itens):
    crawlerVags(str(links_list[i]))    

driver.close()

#baixar driver chrome mais atualizado
def baixar_chrome(url, endereco):
    resposta = requests.get(url)
    with open(endereco,'wb') as novo_arquivo:
        novo_arquivo.write(resposta.content)

    
if __name__ == "__main__":
    baixar_chrome('https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_win32.zip', 'chromedriver.exe')

"""
Tentativa botão linkedin

python_button = driver.find_elements_by_xpath("/html/body/div[1]/div/main/section[2]/button")[0]
python_button.click()
"""
