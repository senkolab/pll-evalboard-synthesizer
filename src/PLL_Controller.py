#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This only works on a Windows machine with plink installed (i.e Putty)
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
                           '/src/Testing/test_PE4312.py %s \n')
    # Dictionaries conataining info on the pis and the laser pins + functions
    pi_database = {
        'pi3':{
            'ip': '192.168.168.103',
            'usr': 'pi',
            'pwd': 'raspberry',
            '493nm':{
                'pin':'12',
                'attn':'-1',
                'func':'Cool & Measure'
            },   
            '650nm':{
                'pin':'16',
                'attn':'-1',
                'func':'Repump'
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
        pin = self.pi_database[self.name][laser]['pin']
        command = self.change_attn_command % (pin + ' ' + level)
        # print(command)
        self.sp.stdin.write(command)
        time.sleep(0.75)
        self.pi_database[self.name][laser]['attn'] = level
        print('Attentuation changed to %s' % level)
        return level
    
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
    intro = ('Pll Controller: Type "help" or "? <command>" for help\n'
             'Open a connection to the relevant pi using "connect"\n'
             '(Currently only connects to pi3)')
    prompt = ('======================================\n'
              '>')
    file = None

    # User invisible functions:
    # Parse the input
    def parse(self, arg):
        'Split the input argument into a tuple.'
        return tuple(arg.split())
    
    def ping(self):
        'Pings pi3 currently, can be easily changed to ping whatever.'
        cmd = 'ping -n 1 192.168.168.103'
        result = subprocess.run(cmd)
        return result.returncode

    def change_attn(self, laser, cmd):
        'Changes the attenuation of the specified laser'
        # Should have 'attn' and desired value only
        if len(cmd) == 2:
            level = self.pi3.change_attn(laser,cmd[1])
            self.pi3.pi_database['pi3'][laser][cmd[0]] = level
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

    # User triggerable commands
    def do_ping(self, arg):
        'Pings pi3.'
        self.ping()

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
    
    def do_493nm(self, arg):
        # Both this and do_650nm are semi-redundant, could be compacted
        'Does things to the 493nm cooling laser. Syntax: "493nm" "attn" "25"'
        cmd = self.parse(arg)
        laser = '493nm'
        try:
            if cmd[0] == 'attn':
                self.change_attn(laser, cmd)
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
            else:
                pass
        except:
            print('Error: Command needs more arguments')
            print('or connection not established')

    def do_connect(self, arg):
        '''
        Connects to the raspberry pi of interest, currently only pi3,
        so no arguments needed.
        '''
        ping_result = self.ping()
        if ping_result == 0:
            self.pi3 = PllController('pi3')
            print('')
        else:
            print('Could not connect to pi3')

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
test_cmd = True

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
    else:
        print('Doing nothing:\n\n\n')
        pass