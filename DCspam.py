import tkinter as tk
from tkinter import messagebox, Toplevel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import time
import threading

def send_messages(driver, message, num_messages):
    # Wait for Discord to load
    time.sleep(5)  # Ensure Discord is fully loaded

    # Find the message input box
    message_box = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")

    messages_sent = 0

    for _ in range(num_messages):
        message_box.send_keys(message)  # Type the message
        message_box.send_keys(Keys.RETURN)  # Press Enter to send
        messages_sent += 1

        # Check if we've reached the limit for the break
        if messages_sent % 5 == 0:  # After every 5 messages
            print("Taking a short break to avoid rate limits...")
            time.sleep(5)  # Take a 5-second break
        else:
            time.sleep(0.1)  # Quick interval for other messages

    print("Finished sending messages!")
    driver.quit()

def start_spamming():
    message = message_entry.get()
    num_messages = int(num_messages_entry.get())
    num_accounts = int(num_accounts_entry.get())  # Get the number of accounts

    # Show loading screen
    show_loading_screen()

    # Create threads for each account
    for i in range(num_accounts):
        threading.Thread(target=run_spammer, args=(message, num_messages, i)).start()

    messagebox.showinfo("Info", "Spamming started!")

def run_spammer(message, num_messages, account_number):
    # Set up Edge options
    edge_options = Options()
    edge_options.use_chromium = True

    # Open Edge and navigate to Discord
    driver = webdriver.Edge(options=edge_options)
    driver.get("https://discord.com/login")  # Open Discord login

    # Wait for user to log in and select the channel
    input(f"Press Enter in tab {account_number + 1} after logging in and selecting the channel...")

    # Start sending messages after login
    send_messages(driver, message, num_messages)

def show_loading_screen():
    # Create a new window for the loading screen
    loading_window = Toplevel()
    loading_window.title("Loading...")
    loading_window.geometry("600x400")
    loading_window.configure(bg='black')

    # ASCII Art Skull Animation
    skull_art = r"""

  _                 _ _                   
 | |               | (_)                  
 | | ___   __ _  __| |_ _ __   __ _       
 | |/ _ \ / _ |/ _ | | '_ \ / _ |      
 | | (_) | (_| | (_| | | | | | (_| |  _ _ _ 
 |_|\___/ \__,_|\__,_|_|_| |_|\__, | (_|_|_)
                               __/ |      
                              |___/       

    """

    label = tk.Label(loading_window, text="Loading...", font=("Courier", 14), fg='green', bg='black')
    label.pack(pady=20)

    skull_label = tk.Label(loading_window, text='', font=("Courier", 10), fg='red', bg='black')
    skull_label.pack(pady=10)

    def animate_skull():
        skull_label.config(text=skull_art)
        loading_window.update()
        time.sleep(3)  # Display the skull for 3 seconds
        loading_window.destroy()

    # Start the skull animation in a separate thread
    threading.Thread(target=animate_skull).start()

# GUI Setup
root = tk.Tk()
root.title("DCspam - Made by fear.io")
root.geometry("600x400")
root.configure(bg='black')

# Title ASCII Art
title_art = r"""
DDDDDDDDDDDDD                CCCCCCCCCCCCC                                                                                    
D::::::::::::DDD          CCC::::::::::::C                                                                                    
D:::::::::::::::DD      CC:::::::::::::::C                                                                                    
DDD:::::DDDDD:::::D    C:::::CCCCCCCC::::C                                                                                    
  D:::::D    D:::::D  C:::::C       CCCCCC         ssssssssss   ppppp   ppppppppp     aaaaaaaaaaaaa      mmmmmmm    mmmmmmm   
  D:::::D     D:::::DC:::::C                     ss::::::::::s  p::::ppp:::::::::p    a::::::::::::a   mm:::::::m  m:::::::mm 
  D:::::D     D:::::DC:::::C                   ss:::::::::::::s p:::::::::::::::::p   aaaaaaaaa:::::a m::::::::::mm::::::::::m
  D:::::D     D:::::DC:::::C                   s::::::ssss:::::spp::::::ppppp::::::p           a::::a m::::::::::::::::::::::m
  D:::::D     D:::::DC:::::C                    s:::::s  ssssss  p:::::p     p:::::p    aaaaaaa:::::a m:::::mmm::::::mmm:::::m
  D:::::D     D:::::DC:::::C                      s::::::s       p:::::p     p:::::p  aa::::::::::::a m::::m   m::::m   m::::m
  D:::::D     D:::::DC:::::C                         s::::::s    p:::::p     p:::::p a::::aaaa::::::a m::::m   m::::m   m::::m
  D:::::D    D:::::D  C:::::C       CCCCCC     ssssss   s:::::s  p:::::p    p::::::pa::::a    a:::::a m::::m   m::::m   m::::m
DDD:::::DDDDD:::::D    C:::::CCCCCCCC::::C     s:::::ssss::::::s p:::::ppppp:::::::pa::::a    a:::::a m::::m   m::::m   m::::m
D:::::::::::::::DD      CC:::::::::::::::C     s::::::::::::::s  p::::::::::::::::p a:::::aaaa::::::a m::::m   m::::m   m::::m
D::::::::::::DDD          CCC::::::::::::C      s:::::::::::ss   p::::::::::::::pp   a::::::::::aa:::am::::m   m::::m   m::::m
DDDDDDDDDDDDD                CCCCCCCCCCCCC       sssssssssss     p::::::pppppppp      aaaaaaaaaa  aaaammmmmm   mmmmmm   mmmmmm
                                                                 p:::::p                                                      
                                                                 p:::::p                                                      
                                                                p:::::::p                                                     
                                                                p:::::::p                                                     
                                                                p:::::::p                                                     
                                                                ppppppppp                                                     


"""
title_label = tk.Label(root, text=title_art, font=("Courier", 8), fg='green', bg='black')
title_label.pack(pady=10)

# Number of Accounts Entry
tk.Label(root, text="Number of accounts to open:", fg='green', bg='black').pack()
num_accounts_entry = tk.Entry(root, width=50)
num_accounts_entry.pack()

# Message Entry
tk.Label(root, text="Message to send:", fg='green', bg='black').pack()
message_entry = tk.Entry(root, width=50)
message_entry.pack()

# Number of Messages Entry
tk.Label(root, text="Number of messages to send:", fg='green', bg='black').pack()
num_messages_entry = tk.Entry(root, width=50)
num_messages_entry.pack()

# Start Button
start_button = tk.Button(root, text="Start Spamming", command=start_spamming)
start_button.pack(pady=20)

# Run the GUI
root.mainloop()
