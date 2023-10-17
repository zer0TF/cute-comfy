import os
import filecmp
import shutil
import __main__

from colorama import Style, Fore

def cuteprint(text):
    """
    Prints, except it's CUTE! 💜
    """
    print(f'{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}Cute Comfy: {Fore.RESET}{Style.RESET_ALL}{text}')
