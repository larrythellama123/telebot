

import telebot
import constants
import random
import os
import time
import threading


quotes = ["Better to cum in the sink, than to sink in the cum", "struggle, grind, shine", "its all shits and giggles before someone giggles and shits", "you only got one shot, do not miss your chance"]

print("Bot started")



bot = telebot.TeleBot(constants.API)


last_check = 0
is_wishing = False

@bot.message_handler(commands=['meow'])
def meow(message):
    global is_wishing
    if not is_wishing:
        is_wishing = True
        threading.Thread(target=wish_thread, args=(message,)).start()
        bot.reply_to(message, "schmeow")
    else:
        bot.reply_to(message, "Aschemow")

def wish_thread(message):
    global last_check, is_wishing
    while is_wishing:
        current_time = time.time()
        if current_time - last_check >= 60:  # Check every minute
            if is_midnight():
                print("It's time! Sending birthday wish.")
                bot.send_message(message.chat.id, "Happy Birthday! 🎉🎂")
                is_wishing = False
                break
            last_check = current_time
        time.sleep(1)  # Sleep for 1 second to prevent high CPU usage

def is_midnight():
    current_time = time.localtime()
    print(f"Checking time: {current_time.tm_hour}:{current_time.tm_min}")
    return current_time.tm_hour == 0 and current_time.tm_min == 0

@bot.message_handler(commands=['stop_wish'])
def stop_wish(message):
    global is_wishing
    is_wishing = False
    bot.reply_to(message, "Stopped wishing process.")



    
# Schedule the birthday message


@bot.message_handler(commands=['input'])
def input(message):
  sent = bot.send_message(message.chat.id, 'Please enter your schedule for today.')
  bot.register_next_step_handler(sent, write)

def write(message):
    if not os.path.isfile(f'problem{message.chat.id}.txt') and not os.path.isfile(f'schedule{message.chat.id}.txt'):
        open(f'problem{message.chat.id}.txt', 'a').write(f'{message.text}\n')
        open(f'schedule{message.chat.id}.txt', 'a').write("")
    else:
        if os.path.getsize(f'problem{message.chat.id}.txt') != 0 and os.path.getsize(f'schedule{message.chat.id}.txt') == 0 or (os.path.getsize(f'schedule{message.chat.id}.txt') == 0 and os.path.getsize(f'problem{message.chat.id}.txt') == 0):
            open(f'problem{message.chat.id}.txt', 'a').write(f'{message.text}\n')
        elif os.path.getsize(f'problem{message.chat.id}.txt') == 0 and os.path.getsize(f'schedule{message.chat.id}.txt') != 0:
            open(f'schedule{message.chat.id}.txt', 'a').write(f'{message.text}\n')


    bot.send_message(message.chat.id, 'Thank you!')  


@bot.message_handler(commands=['sched'])
def sched(message):
    if os.path.getsize(f'problem{message.chat.id}.txt') != 0:   
        with open(f'problem{message.chat.id}.txt') as f:
            sched = f.readlines()
            bot.send_message(message.chat.id, f'{sched}\n')

    elif os.path.getsize(f'schedule{message.chat.id}.txt') != 0:
        with open(f'schedule{message.chat.id}.txt') as f:
            sched = f.readlines()
            bot.send_message(message.chat.id, f'{sched}\n')


@bot.message_handler(commands=['clear'])
def clear(message):
    if os.path.getsize(f'problem{message.chat.id}.txt') != 0:  
        open(f'problem{message.chat.id}.txt','w').close()
        bot.send_message(message.chat.id,"schedule has been cleared")
    elif os.path.getsize(f'schedule{message.chat.id}.txt') != 0:
        open(f'schedule{message.chat.id}.txt','w').close()
        bot.send_message(message.chat.id,"schedule has been cleared")

@bot.message_handler(commands=['delete'])
def delete(message):
        sent = bot.send_message(message.chat.id, 'what part of your schedule do you want to delete?')
        bot.register_next_step_handler(sent, removal)

def removal(message):
    if os.path.getsize(f'schedule{message.chat.id}.txt') == 0 and os.path.getsize(f'problem{message.chat.id}.txt') != 0 :
        with open(f"problem{message.chat.id}.txt",'r') as file:
            lines = file.readlines()
            for line in lines:
                new_lines = line.replace(message.text, "")
                open(f"schedule{message.chat.id}.txt",'a').write(new_lines)
        open(f'problem{message.chat.id}.txt', 'w').close()

    elif os.path.getsize(f'schedule{message.chat.id}.txt') != 0 and os.path.getsize(f'problem{message.chat.id}.txt') == 0 :
        with open(f"schedule{message.chat.id}.txt",'r') as file:
            lines = file.readlines()
            for line in lines:
                new_lines = line.replace(message.text, "")
                open(f"problem{message.chat.id}.txt",'a').write(new_lines)  
        open(f"schedule{message.chat.id}.txt",'w').close() 
     
   
    elif not os.path.isfile(f'problem{message.chat.id}.txt') and not os.path.isfile(f'schedule{message.chat.id}.txt'):
           bot.send_message(message.chat.id,"Nothing to delete!")

    elif os.path.getsize(f'schedule{message.chat.id}.txt') == 0 and os.path.getsize(f'problem{message.chat.id}.txt') == 0 :
        bot.send_message(message.chat.id,"Nothing to delete!")
            
    bot.send_message(message.chat.id,"Deleted!")




@bot.message_handler(command=['quote'])
def quote(message):
        bot.send_message(message.chat.id,f"{random.choice(quotes)}")
            






# Modified main execution
if __name__ == '__main__':
    
    
    
    while True:
        # Check for new messages
        try:
            bot.polling(none_stop=True, interval=0, timeout=0)
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(15)

        # Check if it's time to send birthday messages
        