import sys

'''
def parse(line):
    code = line.strip()
    if code:
        if code[0] == '@':
            print 'A instruction',code
        elif code[0] == '(':
            print 'L instruction', code
        elif code[0] =='D' or code[0] =='M' or code[0] =='A':
            print 'C instruction', code
        elif code[:2] == '//':
            print 'Comentario',code
        else:
            print 'invalid line'

'''

d_symbols = {

    'SP':'0',
    'LCL':'1',
    'ARG':'2',
    'THIS':'3',
    'THAT':'4',
    'R0':'0',
    'R1':'1',
    'R2' :'2',
    'R3' :'3',
    'R4' :'4',
    'R5' :'5',
    'R6' :'6',
    'R7' :'7',
    'R8' :'8',
    'R9' :'9',
    'R10':'10',
    'R11':'11',
    'R12':'12',
    'R13':'13',
    'R14':'14',
    'R15':'15',
    'SCREEN':'16384',
    'KBD':'24576'
}


d_dest = {
    "":'000',
    'M':'001',
    'D':'010',
    'MD':'011',
    'A':'100',
    'AM':'101',
    'AD':'110',
    'AMD':'111'
    }

d_jump = {
    "":'000',
    'JGT':'001',
    'JEQ':'010',
    'JGE':'011',
    'JLT':'100',
    'JNE':'101',
    'JLE':'110',
    'JMP':'111'
          }

d_comp = {
    '0'  :'0101010',
    '1'  :'0111111',
    '-1' :'0111010',
    'D'  :'0001100',
    'A'  :'0110000',
    '!D' :'0001101',
    '!A' :'0110001',
    '-D' :'0001111',
    '-A' :'0110011',
    'D+1':'0011111',
    'A+1':'0110111',
    'D-1':'0001110',
    'A-1':'0110010',
    'D+A':'0000010',
    'D-A':'0010011',
    'A-D':'0000111',
    'D&A':'0000000',
    'D|A':'0010101',
    'M'  :'1110000',
    '!M' :'1110001',
    '-M' :'1110011',
    'M+1':'1110111',
    'M-1':'1110010',
    'D+M':'1000010',
    'D-M':'1010011',
    'M-D':'1000111',
    'D&M':'1000000',
    'D|M':'1010101'
          }




def parse(line):
    bin_code = ""
    code = line.strip().upper()
    if code:
        #A instruction
        if code[0] == '@':
            try:
                bin_code = bin(int(code[1:]))[2:].zfill(16)
            except ValueError:
                pass

        elif code[:2] == '//':
            pass

        #C Instruction
        else:
            dest = ""
            jump = ""
            comp = ""
            head = '111'

            piece = code.split(";")
            if len(piece) > 1:
                jump = piece[1]

            piece = piece[0].split("=")
            if len(piece) > 1:
                dest = piece[0]
                comp = piece[1]
            else:
                comp = piece[0]


            bin_code = head + d_comp[comp] + d_dest[dest] + d_jump[jump]

    return bin_code



#f = open(sys.argv[1])
#f_out = sys.argv[1].split(".")[0]+".hack"

f_name = sys.argv[1]



# Verifying LABELS

f = open(f_name)

code_line = 0


while True:
    s = f.readline()

    if len(s) == 0:
        break

    code = s.strip().upper()
    if code:
        if code[:2] == '//':
            pass
        elif code[0] == '(':
            code = code.split('//')[0].strip()
            label = code.strip('()')
            if not d_symbols.has_key(label):
                d_symbols[label] = str(code_line)
        else:
            code_line += 1
f.close()


#Verifying VARIABLES

variable_pos = 16


f = open(f_name)

while True:
    s = f.readline()

    if len(s) == 0:
        break

    code = s.strip().upper()
    if code:
        if code[:2] == '//':
            pass
        elif code[0] == '(':
            pass
        elif code[0] == '@':
            code = code.split('//')[0].strip()
            value = code[1::]
            try:
                int(value)
            except ValueError:
                if not d_symbols.has_key(value):
                    d_symbols[value] = str(variable_pos)
                    variable_pos = variable_pos + 1
        else:
            pass



f.close()


#PARSING CODE

f = open(f_name)
f_out = open(f_name.split(".")[0]+".hack",'w')
f_hex = open(f_name.split(".")[0]+".hex",'w')

f_hex.write('v2.0 raw'+'\n');

while True:
    s = f.readline()

    if len(s) == 0:
        break

    bin_code = ""
    hex_code = ""
    code = s.strip().upper()
    if code:
        if code[:2] == '//':
            pass
        elif code[0] == '(':
            pass

        # A instruction
        elif code[0] == '@':
            code = code.split('//')[0].strip()
            try:
                bin_code = bin(int(code[1:]))[2:].zfill(16)
            except ValueError:
                bin_code = bin(int(d_symbols[code[1:]]))[2:].zfill(16)
	    hex_code = hex(int(bin_code,2))[2:].zfill(4)

        # C Instruction
        else:
            dest = ""
            jump = ""
            comp = ""
            head = '111'

            code = code.split('//')[0].strip()

            piece = code.split(";")
            if len(piece) > 1:
                jump = piece[1]

            piece = piece[0].split("=")
            if len(piece) > 1:
                dest = piece[0]
                comp = piece[1]
            else:
                comp = piece[0]

            bin_code = head + d_comp[comp] + d_dest[dest] + d_jump[jump]
	    hex_code = hex(int(bin_code,2))[2:].zfill(4)
		
	

    if len(bin_code) >0:
        print hex_code,
        f_out.write(bin_code+'\n')
	f_hex.write(hex_code + ' ')


f.close()
f_out.close()
f_hex.close()
#h.close()


