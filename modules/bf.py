#!/usr/bin/python3
# coding:utf-8

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

class BrainSth(object):
    def __init__(self, tapelength):
        # body
        self.code = None
        self.tape = BFTape(tapelength)
        self.commands = BFCommands()
        self.printed_chars = ""
    
    def give_code(self, code):
        self.code = BFCode(code)
    
    def add_to_code(self, codetoadd):
        self.code.add_to_code(codetoadd)
    
    def clearcode(self):
        self.code = None
    
    def execute_command(self, command):
        
        if command == self.commands.right:
            self.tape.right()
        elif command == self.commands.left:
            self.tape.left()
        elif command == self.commands.incr:
            self.tape.incr()
        elif command == self.commands.decr:
            self.tape.decr()
        elif command == self.commands.output:
            self.printed_chars += chr(self.tape.read())
        elif command == self.commands.accept:
            self.tape.accept( input('\n') )
        elif command == self.commands.whileb:
            if self.tape.read() == 0:
                self.code.jump_to_match()
        elif command == self.commands.whilee:
            if self.tape.read() != 0:
                self.code.jump_to_match()
        else:
            pass
        
        self.code.proceed()
        
    def execute(self):
        while True:
            # try to read
            try:
                currentcommand = self.code.read()
            except:
                break
            # execute read command 
            self.execute_command(currentcommand)
        return self.printed_chars




class BFCode(object):
    def __init__(self, code):
        self.code = code
        self.reader = 0
        self.obracs = ()
        self.cbracs = ()
        self.match_brackets()
    
    def read(self):
        return self.code[self.reader]
    
    def proceed(self):
        self.reader += 1
    
    def add_to_code(self, codetoadd):
        self.code += codetoadd
    
    def set_reader_at(self, loc):
        self.reader = loc
    
    def jump_to_match(self):
        try:
            self.set_reader_at(self.cbracs[self.obracs.index(self.reader)])
        except:
            try:
                self.set_reader_at(self.obracs[self.cbracs.index(self.reader)])
            except:
                return None
    
    def reset(self, code):
        if code != None:
            self.code = code
        else:
            pass
        self.match_brackets()
        self.reader = 0 
    
    def match_brackets(self):
        open_buffer = []
        matches = []
        open_brackets = []
        close_brackets = []
        for i in range(len(self.code)):
            if self.code[i] == '[':
                open_buffer.append(i)
            elif self.code[i] == ']':
                open_brackets.append(open_buffer.pop(-1)) 
                close_brackets.append(i)
        self.obracs = tuple(open_brackets)
        self.cbracs = tuple(close_brackets)
    

class BFTape(object):
    def __init__(self, tapelength):
        self.tapelength = tapelength
        self.tape = [0] * tapelength
        self.pointer = 0
    
    def refresh(self):
        self.tape = [0] * self.tapelength
        self.pointer = 0
    
    def right(self):
        # moves the pointer 1 cell to the right.
        # bf command : >
        self.pointer += 1
    
    def left(self):
        # moves the pointer 1 cell to the left.
        # bf command : <
        self. pointer -= 1
    
    def incr(self):
        # increment the byte at the pointer.
        self.tape[ self.pointer ] += 1
    
    def decr(self):
        # decrement the byte at the pointer.
        self.tape[ self.pointer ] -= 1
    
    def accept(self, value):
        # accepts input, storing its value at the pointer
        self.tape[ self.pointer ] = value
    
    def read(self):
        return self.tape[ self.pointer ] 
    



class BFCommands(object):
    def __init__(self):
        self.right = '>'
        self.left  = '<'
        self.incr  = '+'
        self.decr  = '-'
        self.output= '.'
        self.accept= ','
        self.whileb= '['
        self.whilee= ']'
    

