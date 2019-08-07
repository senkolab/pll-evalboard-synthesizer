#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This only works on a Windows machine with plink installed (i.e Putty)
# Run this from a computer on the lab network, not on the raspberry pis themselves
import subprocess
import cmd
import time

class PllController:
    '''
    Opens a basic connection to the raspberry pi's and allows control of attenuation.
    Can be easlily updated to allow control of other things later.
    '''
    # Initial command to connect to pi through plink
    init_cmd = 'plink -ssh %s@%s -pw %s -batch'
    # Command to run Brendan's attenuation adjustment program once connected
    change_attn_command = ('python /home/pi/pll-evalboard-synthesizer'
                           '/src/Control-Programs/att1.py %s \n')
    change_freq_command =('python /home/pi/pll-evalboard-synthesizer'
                           '/src/Control-Programs/rf1.py %s \n')
    sweep_freq_command = ('python /home/pi/pll-evalboard-synthesizer'
                           '/src/Control-Programs/rf1_sweep.py %s \n')
    # Dictionaries conataining info on the pis and the laser pins + functions
    # Frequencies are in MHz
    pi_database = {
        'pi3':{
            'ip': '192.168.168.103',
            'usr': 'pi',
            'pwd': 'raspberry',
            'attn':{
                '493nm':{
                    'pin':'12',
                    'val':'-1'
                },
                '650nm':{
                    'pin':'16',
                    'val':'-1'
                }
            },   
            'freq':{
                '493nm':{
                    'pin':'4',
                    'val':'-1'
                },
                '650nm':{
                    'pin':'6',
                    'val':'-1'
                }
            }
        }
    }   

    def __init__(self, name):
        # Initiate everything and setup a connection to the named pi
        self.name = name
        # print(self.pi_database[self.name]['usr'])
        # print(self.pi_database[self.name]['ip'])
        # print(self.pi_database[self.name]['pwd'])
        self.connect_cmd = self.init_cmd % (self.pi_database[self.name]['usr'],
                                        self.pi_database[self.name]['ip'],
                                        self.pi_database[self.name]['pwd'])
        # print(self.connect_cmd)
        # Connect to the named pi through ssh
        # get rid of stdout and stderr to see output from pi
        self.sp = subprocess.Popen(self.connect_cmd,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                text=True, bufsize=0)
        time.sleep(1.5)
        print('\nConnection established')

    def change_attn(self, laser, level):
        # Changes the attentuation using Brendan's script on the pi
        function = 'attn'
        pin = self.pi_database[self.name][function][laser]['pin']
        command = self.change_attn_command % (pin + ' ' + level)
        # print(command)
        self.sp.stdin.write(command)
        time.sleep(0.75)
        self.pi_database[self.name][function][laser]['val'] = level
        print('Attentuation changed to %s' % level)
        return level
    
    def change_freq(self, laser, freq):
        'Changes the frequency of the aom corresponding to the laser.'
        function = 'freq'
        pin = self.pi_database[self.name][function][laser]['pin']
        command = self.change_freq_command % (pin + ' ' + freq)
        self.sp.stdin.write(command)
        time.sleep(0.75)
        self.pi_database[self.name][function][laser]['val'] = freq
        print('AOM frequency changed to %s' % freq)
        return freq
    
    def sweep_frequency(self, laser, start, end, step_size, time):
        '''
        Sweeps the frequency of the aome corresponding to the laser from
        start to end.
        '''
        freq_range = end - start
        if (freq_range) >= 0:
            function = 'freq'
            step_time = time / (freq_range / step_size)
            if step_time < 1:
                step_time = 1
            pin = self.pi_database[self.name][function][laser]['pin']
            args = (pin + ' '
                + start + ' '
                + end + ' '
                + step_size + ' '
                + step_time)
            command = self.sweep_freq_command % (args)
            self.sp.stdin.write(command)
            time.sleep(time + 0.75)
            self.pi_database[self.name][function][laser]['val'] = end
            return end
        else:
            pass

    def terminate(self):
        # Exits the session and kills the subprocess just in case
        self.sp.stdin.write('exit \n')
        time.sleep(0.1)
        self.sp.stdin.close()
        self.sp.kill()
        return True

class PllShell(cmd.Cmd):
    'CLI for the PLLController class.'
    # Startup paramaters and parateters to keep track of attentuation for the CLI
    l_493nm_attn = -1
    l_650nm_attn = -1
    l_493nm_freq = -1
    l_650nm_freq = -1
    intro = ('Pll Controller: Type "help" or "? <command>" for help\n'
             'Open a connection to the relevant pi using "connect piX"')
    prompt = ('======================================\n'
              '>')
    file = None

    # User invisible functions:
    # Parse the input
    def parse(self, arg):
        'Split the input argument into a tuple.'
        return tuple(arg.split())
    
    def ping(self, arg):
        'Pings pi of interest.'
        try:
            cmd = 'ping -n 1 %s' % (PllController.pi_database[arg]['ip']) 
            result = subprocess.run(cmd)
            return result.returncode
        except:
            return 1

    def change_attn(self, laser, cmd):
        'Changes the attenuation of the specified laser'
        # Should have 'attn' and desired value only
        if len(cmd) == 2:
            level = self.pi3.change_attn(laser, cmd[1])
            # self.pi3.pi_database['pi3']['attn'][laser][cmd[0]] = level
            if laser == '493nm':
                self.l_493nm_attn = level
            elif laser == '650nm':
                self.l_650nm_attn = level
            else:
                print('Laser not recognized...')
            # print('')
        else:
            print('Needs both setting and desired value, e.g: "attn" "25"')
            pass
    
    def change_freq(self, laser, cmd):
        "Changes the frequency assosiated with the specified laser's aom"
        if len(cmd) == 2:
            level = self.pi3.change_freq(laser, cmd[1])
            if laser == '493nm':
                self.l_493nm_freq = level
            elif laser == '650nm':
                self.l_650nm_freq = level
            else:
                print('Laser not recognized...')
            # print('')
        else:
            print('Needs both setting and desired value, e.g: "freq" "200"')
            pass

    # User triggerable commands
    def do_ping(self, arg):
        'Pings pi of interest.'
        name = self.parse(arg)[0]
        print(name)
        self.ping(name)

    def do_test(self, arg):
        'Prints Testing'
        print("Testing")
        return 0

    def do_close(self, arg):
        'Exits the program.'
        try:
            self.pi3.terminate()
        except:
            pass
        print("Exiting...")
        return True

    def do_exit(self, arg):
        'Exits the program.'
        try:
            self.pi3.terminate()
        except:
            pass
        print("Exiting...")
        return True
    
    def do_493nm(self, arg):
        # Both this and do_650nm are semi-redundant, could be compacted
        'Does things to the 493nm cooling laser. Syntax: "493nm" "attn" "25"'
        cmd = self.parse(arg)
        laser = '493nm'
        try:
            if cmd[0] == 'attn':
                self.change_attn(laser, cmd)
            elif cmd[0] == 'freq':
                self.change_freq(laser, cmd)
            else:
                pass
        except:
            print('Error: Command needs more arguments')
            print('or connection not established')

    def do_650nm(self, arg):
        'Does things to the 650nm repump laser. Syntax: "650nm" "attn" "25"'
        cmd = self.parse(arg)
        laser = '650nm'
        try:
            if cmd[0] == 'attn':
                self.change_attn(laser, cmd)
            elif cmd[0] == 'freq':
                self.change_freq(laser, cmd)
            else:
                pass
        except:
            print('Error: Command needs more arguments')
            print('or connection not established')

    def do_connect(self, arg):
        '''
        Connects to the raspberry pi of interest, "connect 'pi3'"
        '''
        try:
            name = self.parse(arg)[0]
            ping_result = self.ping(name)
            if ping_result == 0:
                self.pi3 = PllController(name)
                print('')
            else:
                print('Could not connect to %s' % name)
        except:
            print('Wrong number of arguments, needs only name of pi')

    def do_current(self, arg):
        'Prints the current attenuation settings for the 493nm and 650nm lasers.'
        c = self.l_493nm_attn
        r = self.l_650nm_attn
        print('The current attenuation settings are:')
        print('493nm Cooling: %s' % c)
        print('650nm Repump: %s' % r)

    def do_check_connection(self, arg):
        "Checks to see if there's a connection to pi3"
        try:
            temp = self.pi3
            print('Connection to pi3 found')
            del temp
        except:
            print('No connection to pi3 found')

# Control Tests:
test_attn = False
test_cmd = False
run = True

if __name__ == "__main__":
    print('Running')
    if test_attn == True:
        print('Testing Attenuation Control:\n')
        test = PllController('pi3')
        print(test.name)
        test.change_attn('493nm', '25')
        test.change_attn('493nm', '0')
        test_setting = test.change_attn('493nm', '25')
        test.terminate()
        print(test.pi_database[test.name]['493nm']['attn'])
        print(test_setting)
    elif test_cmd == True:
        print('Testing Command Interface:\n')
        PllShell().cmdloop()
    elif run == True:
        PllShell().cmdloop()
    else:
        print('Doing nothing:\n\n\n')
        pass