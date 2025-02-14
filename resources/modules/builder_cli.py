import json
import os

print(os.getcwd())
class CLI_Builder:
    def __init__(self):
        print(
f'''
PySilon Malware Builder
Version: 4.0

Type "help" for list of commands.
''')
        self.get_command()

    def get_command(self):
        self.issued_command = input('.')
        match self.issued_command.split()[0]:
            case 'set':
                possible_settings = []
                for argument in self.issued_command.split()[1:]:
                    if argument.count('-') == 2 and argument.count('=') == 1 and argument.count('"') == 2:
                        possible_settings.append(argument)
                    else:
                        self.error('Syntax', 'set')
                        possible_settings = []
                        self.get_command()
                for setting in possible_settings:
                    setting = setting.split('=')
                    self.command_set(setting[0][2:], setting[1][1:-1])
            case 'config':
                match self.issued_command.split()[1]:
                    case '--view':
                        with open('resources/assets/configuration.tmp', 'r', encoding='utf-8') as read_configuration:
                            seek_configuration = json.loads(''.join(read_configuration.readlines()).replace('\n', ''))
                        self.command_config('view', seek_configuration)
                    case '--load':
                        with open(self.issued_command.split()[2], 'r', encoding='utf-8') as read_configuration:
                            draft_configuration = json.loads(''.join(read_configuration.readlines()).replace('\n', ''))
                        self.command_config('load', draft_configuration)
                    case _:
                        self.error('Syntax', 'config')
        self.get_command()

    def command_set(self, setting, value):
        print(setting, value)

    def command_config(self, subcommand, data=None):
        match subcommand:
            case 'view':
                print(
f'''
PySilon Malware Configuration
    Discord Token  . . . . . . : {self.malware_configuration['token']}
    Guild IDs  . . . . . . . . : {self.malware_configuration['guild_ids']}
    Registry Name  . . . . . . : {self.malware_configuration['registry_name']}
    Directory Name . . . . . . : {self.malware_configuration['directory_name']}
    Executable Name  . . . . . : {self.malware_configuration['executable_name']}
    Implode Password . . . . . : {self.malware_configuration['implode_secret']}
     f- Keylogger  . . . . . . : {self.malware_configuration['functionalities']['keylogr']}
     f- Screenshots  . . . . . : {self.malware_configuration['functionalities']['scrnsht']}
     f- File Management  . . . : {self.malware_configuration['functionalities']['f_manag']}
     f- Grabber  . . . . . . . : {self.malware_configuration['functionalities']['grabber']}
     f- Live Microphone  . . . : {self.malware_configuration['functionalities']['mc_live']}
     f- Microphone Recording . : {self.malware_configuration['functionalities']['mc_recc']}
     f- Processes  . . . . . . : {self.malware_configuration['functionalities']['process']}
     f- Reverse Shell  . . . . : {self.malware_configuration['functionalities']['rev_shl']}
     f- Webcam . . . . . . . . : {self.malware_configuration['functionalities']['webcam_']}
     f- Screen Recording . . . : {self.malware_configuration['functionalities']['scrnrec']}
     f- Input Blocking . . . . : {self.malware_configuration['functionalities']['inputbl']}
     f- Crypto-Clipper . . . . : {self.malware_configuration['functionalities']['crclipr']}
     f- Messager . . . . . . . : {self.malware_configuration['functionalities']['messger']}
     f- TextToSpeech . . . . . : {self.malware_configuration['functionalities']['txtspee']}
     f- Audio Controlling  . . : {self.malware_configuration['functionalities']['audctrl']}
     f- Monitors Controlling . : {self.malware_configuration['functionalities']['monctrl']}
     f- Website Blocking . . . : {self.malware_configuration['functionalities']['webbloc']}
     f- Jumpscare  . . . . . . : {self.malware_configuration['functionalities']['jmpscar']}
     f- Keystroke Type . . . . : {self.malware_configuration['functionalities']['keystrk']}
     f- Screen Manipulation  . : {self.malware_configuration['functionalities']['scrnman']}
     f- BlueScreenOfDeath  . . : {self.malware_configuration['functionalities']['bluesod']}
    Obfuscation  . . . . . . . : {self.malware_configuration['obfuscation']['enabled']}
    Anti-VM  . . . . . . . . . : {self.malware_configuration['anti_vm']['enabled']}
    Debug Mode . . . . . . . . : {self.malware_configuration['debug_mode']}
    Icon . . . . . . . . . . . : {self.malware_configuration['icon_path']}
'''
                )
            case 'load':
                self.malware_configuration = data
                print('Configuration successfully loaded. You can view it with "config --view" command.')

    def error(self, type, help):
        print('Error')
                
                


CLI_Builder()