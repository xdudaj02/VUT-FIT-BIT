# ###  file:       inerpret.py  ### #
# ###  name: ipp project no. 2  ### #
# ###  author:        xdudaj02  ### #
# ###  date:          8.4.2021  ### #
# ###  version:            1.0  ### #

import xml.etree.ElementTree as Et
import sys
import re

# NOT SUPPORTED:
# unordered instruction arguments
# filenames containing whitespace

# ### GLOBAL VARIABLES ### #
# dict with valid opcodes and strings containing mandatory arguments
# argument representation: V: variable, S: symbol (constant or variable), L: label, T: type
opcodes = {'MOVE': 'VS',
           'CREATEFRAME': '',
           'PUSHFRAME': '',
           'POPFRAME': '',
           'DEFVAR': 'V',
           'CALL': 'L',
           'RETURN': '',
           'PUSHS': 'S',
           'POPS': 'V',
           'ADD': 'VSS',
           'SUB': 'VSS',
           'MUL': 'VSS',
           'IDIV': 'VSS',
           'LT': 'VSS',
           'GT': 'VSS',
           'EQ': 'VSS',
           'AND': 'VSS',
           'OR': 'VSS',
           'NOT': 'VS',
           'INT2CHAR': 'VS',
           'STRI2INT': 'VSS',
           'READ': 'VT',
           'WRITE': 'S',
           'CONCAT': 'VSS',
           'STRLEN': 'VS',
           'GETCHAR': 'VSS',
           'SETCHAR': 'VSS',
           'TYPE': 'VS',
           'LABEL': 'L',
           'JUMP': 'L',
           'JUMPIFEQ': 'LSS',
           'JUMPIFNEQ': 'LSS',
           'EXIT': 'S',
           'DPRINT': 'S',
           'BREAK': '',
           }

types = ['int', 'bool', 'string', 'nil', 'label', 'type', 'var']  # list of valid types

# dict containing valid types for each argument type
type_validity = {'V': ['var'], 'S': ['var', 'int', 'bool', 'string', 'nil'], 'L': ['label'], 'T': ['type']}

# dict used for converting ipp representation of bool values to python representation, repeated application is kosher
bool_map = {'true': True, 'false': False, True: True, False: False}

# regex used for finding escaped characters (with decimal codes)
regex_dec_escapes = re.compile(r"\\(\d{3})")


# CLASS DEFINITIONS
# class containing all frames used by ipp programs
class FrameStack:
    def __init__(self):
        self.lf_frame_arr = []  # local frames stack
        self.lf_frame_arr.append(None)  # first element is None by default
        self.lf_frames_in = 0  # local frames stack size
        self.lf = None  # local frame (uninitialized by default)
        self.tf = None  # temporary frame (uninitialized by default)
        self.gf = Frame()  # global frame

    def __repr__(self):
        return 'GF:' + str(self.gf) + ', LF:' + str(self.lf) + ', TF:' + str(self.tf) + '\n' + str(self.lf_frame_arr)

    # pushes tf into lf stack
    def lf_push(self):
        if self.tf is None:
            sys.exit(55)
        self.lf_frame_arr.append(self.tf)
        self.lf_frames_in += 1
        self.lf = self.tf
        self.tf = None

    # pops top frame from lf stack into tf
    def lf_pop(self):
        if self.lf_frames_in < 1:
            sys.exit(55)
        self.lf_frames_in -= 1
        self.tf = self.lf_frame_arr.pop()
        self.lf = self.lf_frame_arr[-1]

    # defines variable with given name in given frame
    def ipp_defvar(self, var_string):
        var_frame, var_name = var_string.split('@')
        if var_frame == 'GF':
            var_def_check(self.gf, var_name)
            self.gf.vars[var_name] = Variable()
        elif var_frame == 'TF':
            frame_check(self.tf)
            var_def_check(self.tf, var_name)
            self.tf.vars[var_name] = Variable()
        elif var_frame == 'LF':
            frame_check(self.lf)
            var_def_check(self.lf, var_name)
            self.lf.vars[var_name] = Variable()

    # assigns value and type to variable with given name in given frame
    def ipp_move(self, var_string, value, value_type):
        var_frame, var_name = var_string.split('@')
        if value_type == 'int':
            value = int(value)
        if value_type == 'bool':
            value = bool_map[value]
        if var_frame == 'GF':
            var_assign_check(self.gf, var_name)
            self.gf.vars[var_name].set(value, value_type)
        elif var_frame == 'TF':
            frame_check(self.tf)
            var_assign_check(self.tf, var_name)
            self.tf.vars[var_name].set(value, value_type)
        elif var_frame == 'LF':
            frame_check(self.lf)
            var_assign_check(self.lf, var_name)
            self.lf.vars[var_name].set(value, value_type)

    # returns type of given variable in given frame
    def get_var_type(self, var_string):
        var_frame, var_name = var_string.split('@')
        if var_frame == 'GF':
            var_assign_check(self.gf, var_name)
            return self.gf.vars[var_name].type
        if var_frame == 'TF':
            frame_check(self.tf)
            var_assign_check(self.tf, var_name)
            return self.tf.vars[var_name].type
        if var_frame == 'LF':
            frame_check(self.lf)
            var_assign_check(self.lf, var_name)
            return self.lf.vars[var_name].type

    # returns Variable object of given variable in given frame
    def get_var(self, var_string):
        var_frame, var_name = var_string.split('@')
        if var_frame == 'GF':
            var_assign_check(self.gf, var_name)
            return self.gf.vars[var_name]
        if var_frame == 'TF':
            frame_check(self.tf)
            var_assign_check(self.tf, var_name)
            return self.tf.vars[var_name]
        if var_frame == 'LF':
            frame_check(self.lf)
            var_assign_check(self.lf, var_name)
            return self.lf.vars[var_name]


# class represents frame
class Frame:
    def __init__(self):
        self.vars = {}

    def __repr__(self):
        return str(self.vars)

    def __contains__(self, frame_item):
        return frame_item in self.vars


# class represents variable
class Variable:
    def __init__(self, var_value=None, var_type=''):
        self.value = var_value
        self.type = var_type

    def __repr__(self):
        return str(self.value) + ' - ' + self.type

    # sets the value and type of a variable to given values
    def set(self, var_value, var_type):
        self.value = var_value
        self.type = var_type


# class represents ipp stack
class Stack:
    def __init__(self):
        self.arr = []

    def __repr__(self):
        return 'stack: ' + str(self.arr)

    # pushes a new Variable object onto the ipp stack with given value and type
    def ipp_pushs(self, var_value, var_type):
        self.arr.append(Variable(var_value, var_type))

    # pops value and type from ipp stack into given variable
    def ipp_pops(self, var_string):
        if len(self.arr) == 0:
            sys.exit(56)
        var = self.arr.pop()
        frames.ipp_move(var_string, var.value, var.type)


# class represents instruction register
class InstructionRegister:
    def __init__(self):
        self.label_dict = {}  # dict of labels in the code
        self.return_address_arr = []  # stack for return addresses (when using jump instruction)
        self.curr_i = 1  # stores number of current instruction

    def __repr__(self):
        return 'labels: ' + str(self.label_dict) + '\nret_addresses:' + str(self.return_address_arr)

    # adds a new label
    def ipp_label(self, label_name):
        self.label_def_check(label_name)
        self.label_dict[label_name] = self.curr_i

    # performs jump
    def ipp_jump(self, label):
        self.label_use_check(label)
        self.curr_i = self.label_dict[label]

    # performs jump and saves return address
    def ipp_call(self, label):
        self.label_use_check(label)
        self.return_address_arr.append(self.curr_i)
        self.curr_i = self.label_dict[label]

    # performs return
    def ipp_return(self):
        if len(self.return_address_arr) == 0:
            sys.exit(56)
        self.curr_i = self.return_address_arr.pop()

    # detects repeated label definition
    def label_def_check(self, label_name):
        if label_name in self.label_dict:
            sys.exit(52)

    # detects usage of a non existent label
    def label_use_check(self, label_name):
        if label_name not in self.label_dict:
            sys.exit(52)


# classes used for xml document representation
# class represents one instruction argument
class Argument:
    def __init__(self, arg_type, arg_val):
        # empty strings conversion (they are returned as none from xml document)
        if arg_type == 'string' and arg_val is None:
            arg_val = ''
        self.type = arg_type  # argument type
        self.val = arg_val  # argument value

    def __repr__(self):
        return self.type + ' ' + str(self.val)


# class represents one instruction
class Instruction:
    def __init__(self, name):
        self.opcode = name  # instruction name
        self.arg_num = 1  # no of argument (default is 1)
        self.args = {}  # dict of arguments of instruction

    # adds new instruciton argument
    def add_arg(self, arg_type, arg_val):
        self.args[self.arg_num] = Argument(arg_type, arg_val)
        self.arg_num += 1

    # returns argument with given number
    def arg(self, arg_num):
        return self.args[arg_num]

    def __add__(self, other):
        return self.opcode + other

    def __eq__(self, other):
        return self.opcode == other

    def __repr__(self):
        return self.opcode


# class represents the whole xml program
class InstructionArray:
    def __init__(self, xml_tree):
        self.root = {}  # root = program element
        self.inst_num = 1  # order of the instruction
        for xml_inst in xml_tree:  # loop over every instruction
            # add new Instruction object to the root dict of instructions
            self.root[self.inst_num] = Instruction(xml_inst.attrib['opcode'])
            for xml_arg in xml_inst:  # loop over every argument
                # add new argument to the argument dict of a instruction
                self.root[self.inst_num].add_arg(xml_arg.attrib['type'], xml_arg.text)
            self.inst_num += 1

    def __repr__(self):
        output = ''
        for key, value in self.root.items():
            output += str(key) + '. ' + str(value) + '\n'
            for a_key, a_value in value.args.items():
                output += '  - arg' + str(a_key) + ' ' + str(a_value.val) + ' (' + a_value.type + ')\n'
        return output

    def __getitem__(self, ia_item):
        return self.root[ia_item]


# ### end of class definitions ### #


# ### FUNCTIONS ### #
# displays program usage help
def display_help():
    print('''interpret.py  |  version 1.0  |  xdudaj02
interpreter for IPPcode21

USAGE:
  python3.8 interpret.py --source=source_file --input=input_file >output      classic IPPcode21 interpretation
  python3.8 interpret.py --source=source_file <input_file >output             classic IPPcode21 interpretation
  python3.8 interpret.py --input=input_file <source_file >output              classic IPPcode21 interpretation
  python3.8 interpret.py --help                                               display help

ARGUMENTS:  
  source_file         file containing source code written in IPPcode21
  input_file          file containing input for IPPcode21 interpreter
    -at least one of source_file and input_file must be provided through command line argument,
    -other one is expected on stdin
          ''')


# checks argument type validity
def check_argument_type(actual, expected):
    return actual in type_validity[expected]


# checks whether given value is of the given type
def check_type_validity(actual_type, actual_value):
    if actual_type == 'nil':
        return actual_value == 'nil'
    if actual_type == 'bool':
        return re.fullmatch(r'^(?:true|false)$', actual_value)
    if actual_type == 'int':
        return re.fullmatch(r'^(?:[+\-]?[1-9]\d*|0)$', actual_value)
    if actual_type == 'string':
        return re.fullmatch(r'^(?:[^\s#\\]|\\\d{3})*$', empty_string_map(actual_value))
    if actual_type == 'type':
        return re.fullmatch(r'^(?:int|bool|string|nil)$', actual_value)
    if actual_type == 'label':
        return re.fullmatch(r'^[a-zA-Z_\-$&%*!?][0-9a-zA-Z_\-$&%*!?]*$', actual_value)
    if actual_type == 'var':
        return re.fullmatch(r'^[GLT]F@[a-zA-Z_\-$&%*!?][0-9a-zA-Z_\-$&%*!?]*$', actual_value)
    return True


# corrects empty string wrongly represented as None
def empty_string_map(string):
    if string is None:
        return ''
    else:
        return string


# calculates and returns a character from its decimal escaped representation
def replace_dec_escapes(match):
    return chr(int(match.group(1)))


# checks whether frame is defined
def frame_check(frame):
    if frame is None:
        sys.exit(55)


# detects repeated definition of a variable
def var_def_check(frame, var_name):
    if var_name in frame:
        sys.exit(52)


# detects usage of an undefined variable
def var_assign_check(frame, var_name):
    if var_name not in frame:
        sys.exit(54)


# retrieves value and type if given symbol is a variable else returns value and type of given symbol
def safe_get_symb(symb_arg):
    if symb_arg.type == 'var':
        symb_var = frames.get_var(symb_arg.val)
        symb_result = symb_var.value, symb_var.type
    else:
        if symb_arg.type == 'int':
            return int(symb_arg.val), symb_arg.type
        if symb_arg.type == 'bool':
            return bool_map[symb_arg.val], symb_arg.type
        symb_result = symb_arg.val, symb_arg.type
    if symb_result[0] is None:
        sys.exit(56)
    return symb_result


# ### end of function definitions ### #


# ### PROGRAM ARGUMENT PARSING ### #
if 2 > len(sys.argv) > 3:
    sys.exit(10)  # wrong number of arguments supplied
if len(sys.argv) == 2 and sys.argv[1] == '--help':
    display_help()  # display help
    sys.exit(0)

source_from_stdin = False  # true if source file not supplied
input_from_stdin = False  # true if input file not supplied
if len(sys.argv) == 2:  # only one file supplied
    argument = re.fullmatch(r'^--(source|input)=([^\s]*)$', sys.argv[1])
    if argument is None:  # wrong argument
        sys.exit(10)
    if argument.group(1) == 'source':  # source from file
        pr_source = argument.group(2)
        pr_input = sys.stdin.read()
        input_from_stdin = True  # input from stdin
    else:
        pr_input = argument.group(2)  # input from file
        pr_source = sys.stdin.read()
        source_from_stdin = True  # source from stdin
else:  # both files supplied
    argument = re.fullmatch(r'^--(source|input)=([^\s]*)$', sys.argv[1])
    if argument is None:  # wrong argument
        sys.exit(10)
    if argument.group(1) == 'source':  # first file is source
        pr_source = argument.group(2)
        pr_input_gr = re.fullmatch(r'^--input=([^\s]*)$', sys.argv[2])
        if pr_input_gr is None:  # wrong second argument
            sys.exit(10)
        pr_input = pr_input_gr.group(1)
    else:  # first file is input
        pr_input = argument.group(2)
        pr_source_gr = re.fullmatch(r'^--source=([^\s]*)$', sys.argv[2])
        if pr_source_gr is None:
            sys.exit(10)  # wrong second argument
        pr_source = pr_source_gr.group(1)

# opening files
if not input_from_stdin:
    try:
        input_text = open(pr_input, 'r').read().splitlines()  # save input from a file into a list
    except FileNotFoundError:  # file doesnt exist
        sys.exit(11)
else:
    input_text = pr_input.splitlines()  # save input from stdin into a list
if len(input_text) > 0 and input_text[-1] == '':  # trim extra item in input list
    input_text.pop()

if not source_from_stdin:
    try:
        pr_source = open(pr_source, 'r').read()  # open and read source code into a variable
    except FileNotFoundError:  # file doesnt exist
        sys.exit(11)

input_text = [regex_dec_escapes.sub(replace_dec_escapes, i) for i in input_text]

# PARSING XML SOURCE DOCUMENT
# checking validity of xml source document
try:
    root = Et.fromstring(pr_source)  # open source from string
except Et.ParseError:
    sys.exit(31)  # xml document not well-formed (syntax errors)

# checking validity of structure of xml source document (ipp validity)
# checking validity of root element
if root.tag != 'program':  # root element name = program
    sys.exit(32)
if len(root.attrib) > 3:  # max 3 attributes in program element
    sys.exit(32)
for item in root.attrib:  # allowed attribute names
    if item not in ['language', 'name', 'description']:
        sys.exit(32)
if 'language' not in root.attrib.keys():  # mandatory attribute
    sys.exit(32)
if root.attrib['language'] != 'IPPcode21':  # mandatory language attribute value
    sys.exit(32)

# checking validity of instruction elements
order_arr = []  # array of order numbers that already occurred
for i, instr in zip(range(len(root)), root):  # loop over all instructions
    if instr.tag != 'instruction':  # mandatory instruction element name
        sys.exit(32)
    if len(instr.attrib) != 2:  # two mandatory attributes
        sys.exit(32)
    if 'order' not in instr.attrib.keys() or 'opcode' not in instr.attrib.keys():  # names of mandatory attributes
        sys.exit(32)
    try:
        order = int(instr.attrib['order'])  # order must be integer
    except ValueError:
        sys.exit(32)
    if order <= 0:
        sys.exit(32)  # order value restrictions
    if order in order_arr:  # orders must not repeat
        sys.exit(32)
    order_arr.append(order)
    if instr.attrib['opcode'] not in opcodes:  # opcode must be valid
        sys.exit(32)
    arg_types = opcodes[instr.attrib['opcode']]  # expected types of arguments
    if len(instr) != len(arg_types):  # expected number of arguments for an instruction
        sys.exit(32)

    # checking validity of argument elements
    for j, arg in zip(range(len(instr)), instr):
        arg_gr = re.fullmatch(r'^arg(\d+)$', arg.tag)  # mandatory argument name format
        if arg_gr is None:
            sys.exit(32)
        arg_no = int(arg_gr.group(1))
        if arg_no != (j + 1):  # argument number validity, must be in correct order, no missing numbers
            sys.exit(32)
        if len(arg.attrib) != 1:  # mandatory number of attributes (1)
            sys.exit(32)
        if 'type' not in arg.attrib.keys():  # mandatory attribute type
            sys.exit(32)
        if arg.attrib['type'] not in types:  # type must be valid
            sys.exit(32)
        # checking if supplied argument is expected for given instruction
        if not check_argument_type(arg.attrib['type'], arg_types[arg_no - 1]):
            sys.exit(53)
        if not check_type_validity(arg.attrib['type'], arg.text):  # checking if value is of given type
            sys.exit(32)

# ### end of xml document validity checks ### #

# ### INTERPRETATION OF SOURCE CODE ### #
pr_source = regex_dec_escapes.sub(replace_dec_escapes, pr_source)  # sub decimal escapes for actual characters
root = Et.fromstring(pr_source)  # open source from string again (is definitely correct)
root = sorted(root, key=lambda x: int(x.attrib['order']))  # sort instructions
ia = InstructionArray(root)  # creating program representation for easier usage
frames = FrameStack()  # new FrameStack object (all frames)
ir = InstructionRegister()  # new InstructionRegister object (instruction counter, labels, return addresses)
stack = Stack()  # new Stack object (program stack - pushs or pops instructions)

# prerun, saves all label names with their addresses (instruction numbers)
while True:
    if ir.curr_i > len(root):
        break
    curr_opcode = ia[ir.curr_i]  # current instruction

    # LABEL label
    if curr_opcode == 'LABEL':
        ir.ipp_label(curr_opcode.arg(1).val)

    ir.curr_i += 1  # increment instruction counter

ir.curr_i = 1  # reset instruction counter
exit_code = 0  # set default exit code

# main run, interprets the source code
while True:
    if ir.curr_i > len(root):
        break
    curr_opcode = ia[ir.curr_i]  # current instruction

    # CREATEFRAME
    if curr_opcode == 'CREATEFRAME':
        frames.tf = Frame()

    # PUSHFRAME
    elif curr_opcode == 'PUSHFRAME':
        frames.lf_push()

    # POPFRAME
    elif curr_opcode == 'POPFRAME':
        frames.lf_pop()

    # DEFVAR var
    elif curr_opcode == 'DEFVAR':
        frames.ipp_defvar(curr_opcode.arg(1).val)

    # MOVE var symb
    elif curr_opcode == 'MOVE':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        frames.ipp_move(curr_opcode.arg(1).val, var1_value, var1_type)

    # PUSHS symb
    elif curr_opcode == 'PUSHS':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(1))
        stack.ipp_pushs(var1_value, var1_type)

    # POPS var
    elif curr_opcode == 'POPS':
        stack.ipp_pops(curr_opcode.arg(1).val)

    # ADD var symb symb
    elif curr_opcode == 'ADD':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'int' or var2_type != 'int':  # operands must be int
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value + var2_value, 'int')

    # SUB var symb symb
    elif curr_opcode == 'SUB':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'int' or var2_type != 'int':  # operands must be int
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value - var2_value, 'int')

    # MUL var symb symb
    elif curr_opcode == 'MUL':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'int' or var2_type != 'int':  # operands must be int
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value * var2_value, 'int')

    # IDIV var symb symb
    elif curr_opcode == 'IDIV':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'int' or var2_type != 'int':  # operands must be int
            sys.exit(53)
        if var2_value == 0:  # division by zero not allowed
            sys.exit(57)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value // var2_value, 'int')

    # LT var symb symb
    elif curr_opcode == 'LT':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != var2_type:  # operand types must be the same
            sys.exit(53)
        if var1_type == 'nil' or var2_type == 'nil':
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value < var2_value, 'bool')

    # GT var symb symb
    elif curr_opcode == 'GT':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != var2_type:  # operand types must be the same
            sys.exit(53)
        if var1_type == 'nil' or var2_type == 'nil':
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value > var2_value, 'bool')

    # EQ var symb symb
    elif curr_opcode == 'EQ':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != var2_type:  # operand types must be the same
            if var1_type != 'nil' and var2_type != 'nil':
                sys.exit(53)
            else:  # operands types may be different if one is nil
                result = False  # always not equal
        else:
            result = (var1_value == var2_value)
        frames.ipp_move(curr_opcode.arg(1).val, result, 'bool')

    # AND var symb symb
    elif curr_opcode == 'AND':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'bool' or var2_type != 'bool':  # operands must be bool
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value and var2_value, 'bool')

    # OR var symb symb
    elif curr_opcode == 'OR':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'bool' or var2_type != 'bool':  # operands must be bool
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value or var2_value, 'bool')

    # NOT var symb
    elif curr_opcode == 'NOT':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        if var1_type != 'bool':  # operand must be bool
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, not var1_value, 'bool')

    # INT2CHAR var symb
    elif curr_opcode == 'INT2CHAR':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        if var1_type != 'int':  # operand must be int
            sys.exit(53)
        try:
            result = chr(var1_value)
        except ValueError:  # negative int is invalid
            sys.exit(58)
        frames.ipp_move(curr_opcode.arg(1).val, result, 'string')

    # STR2INT var symb symb
    elif curr_opcode == 'STRI2INT':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'string' or var2_type != 'int':  # operands must be string and int
            sys.exit(53)
        if var2_value < 0 or var2_value >= len(var1_value):  # index must not be out of bounds
            sys.exit(58)
        frames.ipp_move(curr_opcode.arg(1).val, ord(var1_value[var2_value]), 'int')

    # CONCAT var symb symb
    elif curr_opcode == 'CONCAT':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'string' or var2_type != 'string':  # operands must be string
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value + var2_value, 'string')

    # STRLEN var symb
    elif curr_opcode == 'STRLEN':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        if var1_type != 'string':  # operand must be string
            sys.exit(53)
        frames.ipp_move(curr_opcode.arg(1).val, len(var1_value), 'int')

    # GETCHAR var symb symb
    elif curr_opcode == 'GETCHAR':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != 'string' or var2_type != 'int':  # operands must be string and int
            sys.exit(53)
        if var2_value < 0 or var2_value >= len(var1_value):  # index must not be out of bounds
            sys.exit(58)
        frames.ipp_move(curr_opcode.arg(1).val, var1_value[var2_value], 'string')

    # SETCHAR var symb symb
    elif curr_opcode == 'SETCHAR':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        dest_value, dest_type = safe_get_symb(curr_opcode.arg(1))
        # operands must be string, int and string
        if var1_type != 'int' or var2_type != 'string' or dest_type != 'string':
            sys.exit(53)
        # index must not be out of bounds, source must not be empty
        if var1_value < 0 or var1_value >= len(dest_value) or len(var2_value) == 0:
            sys.exit(58)
        # set value of char in dest at given index to first char in source
        result = dest_value[:var1_value] + var2_value[0] + dest_value[(var1_value + 1):]
        frames.ipp_move(curr_opcode.arg(1).val, result, 'string')

    # READ var type
    elif curr_opcode == 'READ':
        read_type = curr_opcode.arg(2).val
        try:
            read_value = input_text.pop(0)
        except IndexError:  # no input, reads nil
            read_value = read_type = 'nil'
        else:
            if curr_opcode.arg(2).val == 'int':
                try:
                    read_value = int(read_value)  # read int value
                except ValueError:  # invalid int value, reads nil
                    read_value = read_type = 'nil'
            elif curr_opcode.arg(2).val == 'bool':
                read_value = (read_value.lower() == 'true')  # bool is True if value is 'true' else False
        frames.ipp_move(curr_opcode.arg(1).val, read_value, read_type)

    # WRITE symb
    elif curr_opcode == 'WRITE':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(1))
        if var1_type == 'int':  # convert int to str
            result = str(var1_value)
        elif var1_type == 'bool':  # correctly convert bool value to ipp representation of bool
            if var1_value:
                result = 'true'
            else:
                result = 'false'
        elif var1_type == 'nil':  # convert nil to its ipp representation
            result = ''
        else:
            result = var1_value
        print(result, end='')  # print without default newlines

    # TYPE var symb
    elif curr_opcode == 'TYPE':
        if curr_opcode.arg(2).type == 'var':
            dyn_type = frames.get_var_type(curr_opcode.arg(2).val)
        else:
            dyn_type = curr_opcode.arg(2).type
        frames.ipp_move(curr_opcode.arg(1).val, dyn_type, 'string')

    # JUMP label
    elif curr_opcode == 'JUMP':
        ir.ipp_jump(curr_opcode.arg(1).val)

    # JUMPIFEQ label symb symb
    elif curr_opcode == 'JUMPIFEQ':
        ir.label_use_check(curr_opcode.arg(1).val)  # check label existence
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != var2_type:  # operands types must be the same
            if var1_type != 'nil' and var2_type != 'nil':  # except when one is nil
                sys.exit(53)
        elif var1_value == var2_value:  # jump if values are equal
            ir.ipp_jump(curr_opcode.arg(1).val)

    # JUMPIFNEQ label symb symb
    elif curr_opcode == 'JUMPIFNEQ':
        ir.label_use_check(curr_opcode.arg(1).val)  # check label existence
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(2))
        var2_value, var2_type = safe_get_symb(curr_opcode.arg(3))
        if var1_type != var2_type:  # operands types must be the same
            if var1_type != 'nil' and var2_type != 'nil':  # except when one is nil
                sys.exit(53)
            else:
                ir.ipp_jump(curr_opcode.arg(1).val)  # not equal operand types -> jump
        else:
            if var1_value != var2_value:  # jump if values are not equal
                ir.ipp_jump(curr_opcode.arg(1).val)

    # CALL label
    elif curr_opcode == 'CALL':
        ir.ipp_call(curr_opcode.arg(1).val)

    # RETURN
    elif curr_opcode == 'RETURN':
        ir.ipp_return()

    # EXIT symb
    elif curr_opcode == 'EXIT':
        var1_value, var1_type = safe_get_symb(curr_opcode.arg(1))
        if var1_type != 'int':
            sys.exit(53)
        if var1_value < 0 or var1_value > 49:  # exit code must be in this range
            sys.exit(57)
        exit_code = var1_value
        break

    ir.curr_i += 1  # increment instruction no

sys.exit(exit_code)  # exit with exit code

# ### end of file ### #
