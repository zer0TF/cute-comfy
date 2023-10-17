import __main__

from colorama import Style, Fore

from .watcher import init_watcher

# Placeholder node so that Comfy doesn't throw an error on load

class Cute_Placeholder:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return { }

    RETURN_TYPES = ()
    FUNCTION = "placeholder"

    CATEGORY = "Cute Comfy"

    def placeholder(self):
        return ()
    
NODE_CLASS_MAPPINGS = {
    "Cute.Placeholder": Cute_Placeholder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Cute.Placeholder": "Cute Comfy Placeholder",
}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

init_watcher()

print(f'{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX} °º¤ø,¸¸,ø¤º° Cute Comfy: {Fore.LIGHTGREEN_EX}Loaded! {Style.RESET_ALL}{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}°º¤ø,¸¸,ø¤º°{Style.RESET_ALL}{Fore.RESET}')
