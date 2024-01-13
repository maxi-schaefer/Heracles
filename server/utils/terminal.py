import sys
import os
from datetime import datetime

def rgb(r, g, b, text):
        return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

def set_console_title(text:str):
    if os.name == "nt":
        sys.stdout.write(f"\x1b]2;{text}\x07")

def current_time_str() -> str:
     now = datetime.now()
     ct_string = now.strftime("%H:%M:%S")
     return f"[{ct_string}] "

def log(text:str):
    if text.startswith("[-]"):
        print(rgb(237, 59, 62, text=(current_time_str() + text)))
    elif text.startswith("[+]"):
        print(rgb(59, 237, 68, text=(current_time_str() + text)))

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print_banner()


def print_banner():
    banner = """
      ___           ___           ___           ___           ___                         ___           ___     
     /\  \         /\__\         /\  \         /\  \         /\__\                       /\__\         /\__\    
     \:\  \       /:/ _/_       /::\  \       /::\  \       /:/  /                      /:/ _/_       /:/ _/_   
      \:\  \     /:/ /\__\     /:/\:\__\     /:/\:\  \     /:/  /                      /:/ /\__\     /:/ /\  \  
  ___ /::\  \   /:/ /:/ _/_   /:/ /:/  /    /:/ /::\  \   /:/  /  ___   ___     ___   /:/ /:/ _/_   /:/ /::\  \ 
 /\  /:/\:\__\ /:/_/:/ /\__\ /:/_/:/__/___ /:/_/:/\:\__\ /:/__/  /\__\ /\  \   /\__\ /:/_/:/ /\__\ /:/_/:/\:\__\\
 \:\/:/  \/__/ \:\/:/ /:/  / \:\/:::::/  / \:\/:/  \/__/ \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  / \:\/:/ /:/  /
  \::/__/       \::/_/:/  /   \::/~~/~~~~   \::/__/       \:\  /:/  /   \:\  /:/  /   \::/_/:/  /   \::/ /:/  / 
   \:\  \        \:\/:/  /     \:\~~\        \:\  \        \:\/:/  /     \:\/:/  /     \:\/:/  /     \/_/:/  /  
    \:\__\        \::/  /       \:\__\        \:\__\        \::/  /       \::/  /       \::/  /        /:/  /   
     \/__/         \/__/         \/__/         \/__/         \/__/         \/__/         \/__/         \/__/    
                        
                        Use 'help' to see a list of commands!
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """
    print(rgb(65, 250, 188, banner))

         