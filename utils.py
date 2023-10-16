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

def update_javascript():
    """
    Update any changed JS file(s).

    This code was gracefully borrowed from the ComfyUI-OpenPose-Editor extension. Thank you! ❤️
    """
    extensions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                    "web" + os.sep + "extensions" + os.sep + "cute-comfy")
    javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

    if not os.path.exists(extensions_folder):
        cuteprint("(One-time) Initializing extension folder in web directory.")
        os.mkdir(extensions_folder)

    result = filecmp.dircmp(javascript_folder, extensions_folder)

    if result.left_only or result.diff_files:
        cuteprint('JS files have changed, updating web directory...')
        file_list = list(result.left_only)
        file_list.extend(x for x in result.diff_files if x not in file_list)

        for file in file_list:
            cuteprint(f'Updating {file}...')
            src_file = os.path.join(javascript_folder, file)
            dst_file = os.path.join(extensions_folder, file)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_file)
        cuteprint('Done! :)')
