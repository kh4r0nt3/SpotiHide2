###############################################################################
## Steganographic tool developed as an end-of-master's thesis at the Carlos III 
## University of Madrid that hides information in public playlists of spotify.
###############################################################################
## Author: Jose Carlos Quiroga Alvarez
## Copyright: Copyright 2020, SpotiHide2
## Email: kh4r0nt3@protonmail.com
## Status: Development
###############################################################################

import os
import time
import colored
import warnings
import progressbar
from getpass import getuser
from pywinauto import Application
from pywinauto.mouse import right_click
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError
from pywinauto.findwindows import ElementNotFoundError
warnings.simplefilter('ignore', category=UserWarning)


class SpotiHideGui(object):

    def __init__(self):
        self.__cmd_path = 'C:\WINDOWS\system32\cmd.exe'
        self.__spotify_path = os.path.join('C:\\Users', getuser(), 'AppData\\Roaming\\Spotify\\Spotify.exe')
        self.__cmd = None
        self.__spotify = None
        self.__cmd_window = None
        self.__spotify_window = None


    def spotify_console(self):
        """
        """
        switch = {'add': self.add, 'show':self.show, 'help':self.help, 'exit': self.exit}
        while True:
            self.spotify_window = None
            self.show_spotify_window()
            self.cmd_set_focus()
            command = input(colored.stylize("""\nSpotify > """, colored.fg("light_green_3")))
            params = command.split()
            try:
                switch[params[0]](*params[1:])
            except KeyError:
                print(colored.stylize("""\n[*] """, colored.fg("light_red")) + 'Unknown command: %s\n' % (command))
            except IndexError:
                try:
                    switch[params[0]]()
                except KeyError:
                    print(colored.stylize("""\n[*] """, colored.fg("light_red")) + 'Unknown command: %s\n' % (command))
                except IndexError:
                    pass
            except SystemExit:
                return

    def add(self,
           *args):
        """
        """
        if args and len(args) == 1:
            try:
                self.spotify_set_focus()
                self.spotify_window.maximize()
                self.spotify_window_button(title='Local Files', control_type='Hyperlink')
                time.sleep(0.5)
                self.spotify_direct_button('Custom2')
                send_keys('^a')
                self.spotify_direct_button('Custom2', 'right')
                self.spotify_window_button(title='Add to Playlist', control_type='Text')
                self.spotify_window_button(title=args[0], control_type='Text')
                time.sleep(1)
                send_keys('{ENTER}')
            except Exception:
                print(colored.stylize("""\n[*] """, colored.fg("light_red")) + "Timeout error, element not found!\n")
                raise KeyError
        else:
            print("\nUsage:\tadd PLAYLIST")
            raise KeyError

    def show(self,
            *args):
        """
        """
        if args and len(args) == 1 and args[0] == 'local':
            self.show_spotify_window()
            while True:
                try:
                    #time.sleep(5)
                    send_keys('^p')
                    self.spotify_window_button(title="Settings", control_type="Document")
                    break
                except TimeoutError:
                    pass
            while True:
                try:
                    self.spotify_window_button(title="Show Local Files", control_type="CheckBox", timeout=1)
                    #if show_local_files_checkbox.get_toggle_state() == 0:
                    #    show_local_files_checkbox.click_input()
                    return
                except TimeoutError:
                    send_keys('{DOWN 6}')
            self.cmd_set_focus()
        else:
            print("\nUsage:\tshow local")
            raise KeyError

    def help(self, *args):
        if not args:
            print(colored.stylize("""\n[*] """, colored.fg("light_green_3")) + "Usage:\tshow local")
            print("\n\t\tadd PLAYLIST")
        else:
            raise KeyError

    def exit(self, *args):
        """Exit function.

            :param args:
            :type args: list
        """
        self.spotify_window.close()
        if not args:
            raise SystemExit
        else:
            raise KeyError

    def show_spotify_window(self):
        """
        """
        try:
            self.cmd = Application(backend="win32").connect(path=self.cmd_path)
            self.cmd_window = self.cmd.top_window()
            self.spotify = Application(backend="uia").connect(title_re=r'Spotify.*')
            self.spotify_window = self.spotify.window(title_re=r'Spotify.*')
            self.spotify_set_focus()
        except ElementNotFoundError:
            self.spotify = Application(backend="uia").start(self.spotify_path)
            self.spotify_window = self.spotify.window(title_re=r'Spotify.*')
        except Exception:
            print(colored.stylize("""\n[*] """, colored.fg("light_red")) + "Timeout error, restart Spotify!\n")
            raise KeyError
        finally:
            self.spotify_window.maximize()

    def spotify_set_focus(self):
        """
        """
        self.spotify_window.set_focus()

    def cmd_set_focus(self):
        """
        """
        self.cmd_window.set_focus()

    def spotify_window_button(self, title=None, auto_id=None, control_type=None, timeout=10, retry_interval=1):
        """
        """
        try:
            spotify_window_button = self.spotify_window.child_window(title=title,
                                                                     auto_id=auto_id,
                                                                     control_type=control_type).wait('visible', timeout=timeout, retry_interval=retry_interval).click_input()
        except Exception as e:
            spotify_window_button = self.spotify_window.child_window(title=title,
                                                                     auto_id=auto_id,
                                                                     found_index=1,
                                                                     control_type=control_type).wait('visible', timeout=timeout, retry_interval= retry_interval).click_input()
    
    def spotify_direct_button(self, label, button='left', timeout=10, retry_interval=1):
        self.spotify_window.label.wait('visible', timeout=timeout, retry_interval=retry_interval).click_input(button=button)

    @property
    def spotify_path(self):
        """
            :returns: spotify_path
            :rtype: str
        """
        return self.__spotify_path

    @spotify_path.setter
    def spotify_path(self, value):
        self.__spotify_path = value

    @property
    def spotify(self):
        """
            :returns: spotify
            :rtype: str
        """
        return self.__spotify

    @spotify.setter
    def spotify(self, value):
        self.__spotify = value

    @property
    def spotify_window(self):
        """
            :returns: spotify window
            :rtype: str
        """
        return self.__spotify_window

    @spotify_window.setter
    def spotify_window(self, value):
        self.__spotify_window = value

    @property
    def cmd_path(self):
        """
            :returns: cmd_path
            :rtype: str
        """
        return self.__cmd_path

    @cmd_path.setter
    def cmd_path(self, value):
        self.__cmd_path = value

    @property
    def cmd(self):
        """
            :returns: cmd
            :rtype: str
        """
        return self.__cmd

    @cmd.setter
    def cmd(self, value):
        self.__cmd = value

    @property
    def cmd_window(self):
        """
            :returns: cmd window
            :rtype: str
        """
        return self.__cmd_window

    @cmd_window.setter
    def cmd_window(self, value):
        self.__cmd_window = value
