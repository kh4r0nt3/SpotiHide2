###############################################################################
## Steganographic tool developed as an end-of-master's thesis at the Carlos III 
## University of Madrid that hides information in public playlists of spotify.
###############################################################################
## Author: Jose Carlos Quiroga Alvarez
## Copyright: Copyright 2020, SpotiHide2
## Email: kh4r0nt3@protonmail.com
## Status: Development
###############################################################################

import colored
from os import system
from lib.spotihidegui import SpotiHideGui
from lib.spotihideapi import SpotiHideApi

class Main:
    """Main script class.

    This class is responsible for managing the main menu options helped by
    the rest of the classes and functions.

    :Attributes

        choices(dict): dictionary with the menu choices
    """

    def __init__(self):
        self.choices = {
			'1': self.gui,
            '2': self.api,
			'3': self.quit
		}

    def display_menu(self):
        """
        Displays a menu and responds to choices when run.
        """
        BANNER = colored.stylize("""
  ______                      __     __ __    __ __       __                          ▓▓▓▓▓▓▓▓▓▓▓▓             
 /      \                    |  \   |  \  \  |  \  \     |  \                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       
|  ▓▓▓▓▓▓\ ______   ______  _| ▓▓_   \▓▓ ▓▓  | ▓▓\▓▓ ____| ▓▓ ______          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    
| ▓▓___\▓▓/      \ /      \|   ▓▓ \ |  \ ▓▓__| ▓▓  \/      ▓▓/      \       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  
 \▓▓    \|  ▓▓▓▓▓▓\  ▓▓▓▓▓▓//▓▓▓▓▓▓ | ▓▓ ▓▓    ▓▓ ▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓\    ▓▓▓▓▓                        ▓▓▓▓▓▓▓ 
 _\▓▓▓▓▓▓\ ▓▓  | ▓▓ ▓▓  | ▓▓ | ▓▓ __| ▓▓ ▓▓▓▓▓▓▓▓ ▓▓ ▓▓  | ▓▓ ▓▓    ▓▓    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▓▓▓▓▓▓
|  \__| ▓▓ ▓▓__/ ▓▓ ▓▓__/ ▓▓ | ▓▓|  \ ▓▓ ▓▓  | ▓▓ ▓▓ ▓▓__| ▓▓ ▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓                    ▓▓▓▓▓▓▓▓▓▓▓
 \▓▓    ▓▓ ▓▓    ▓▓\▓▓    ▓▓  \▓▓  ▓▓ ▓▓ ▓▓  | ▓▓ ▓▓\▓▓    ▓▓\▓▓     \    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▓▓▓▓▓▓▓▓
  \▓▓▓▓▓▓| ▓▓▓▓▓▓▓  \▓▓▓▓▓▓    \▓▓▓▓ \▓▓\▓▓   \▓▓\▓▓ \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓    ▓▓▓▓▓▓▓                  ▓▓▓▓▓▓▓▓▓▓▓ 
         | ▓▓                                                              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓  
         | ▓▓                                                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    
          \▓▓                                                                   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       
                                                                                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 
                    
                            [ A Steganographic Tool For Data Exfiltration V.2 ]                                
""", colored.fg('light_green_3') + colored.attr('bold'))

        print(BANNER)
        print(colored.stylize("""\n\t{1}--GUI\n\t{2}--API\n\t{3}--Quit\n""", colored.fg("light_green_3")))
        

    def run(self):
        """
        Displays the main menu and waits until some option is entered. When the option is entered, calls choices 
        with the value of the option.
        """
        try:
            while True:
                self.display_menu() 
                choice = input(colored.stylize("""\nMain Menu > """, colored.fg("light_green_3")))
                print("")
                action = self.choices.get(choice)
                if action:
                    action()
                else:
                    system('cls')
                    print(colored.stylize("""\n[*] """, colored.fg("light_red")) + "Invalid option: %s\n"  % (choice))
        except KeyboardInterrupt:
            exit(0)

    def gui(self):
        """
        GUI function.
        """
        try:
            spoti_hide_gui = SpotiHideGui().spotify_console()
        except KeyboardInterrupt:
            return
        finally:
            system('cls')

    def api(self):
        """
        API function.
        """
        try:
            spoti_hide_api = SpotiHideApi().spotify_console()
        except KeyboardInterrupt:
            return
        finally:
            system('cls')

    def quit(self):
        """
        Exit function.
        """
        system('cls')
        exit(0)

if __name__ == '__main__':
    Main().run()
