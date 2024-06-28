import sys


#### bin file to 4 bytes binary string list
def read_binary_file_4byte(file_path):
    binary_data_list = []
    with open(file_path, "rb") as binary_file:
        while True:
            chunk = binary_file.read(4)  # Read 4 bytes (32 bits) at a time
            if not chunk:
                break
            # Convert the 32 bits into a binary string (little endian to big endian)
            value = int.from_bytes(
                chunk, byteorder="little", signed=False
            )  # machine code to int
            binary_value = format(value, "032b")  # int to binary string
            binary_data_list.append(binary_value)

    return binary_data_list


def read_binary_file_1byte(file_path):
    binary_data_list = []
    with open(file_path, "rb") as binary_file:
        while True:
            chunk = binary_file.read(1)  # Read 1 byte at a time
            if not chunk:
                break
            # Convert the byte into a binary string
            value = ord(chunk)  # machine code to ascii
            binary_value = format(value, "08b")  # ascii to binary string
            binary_data_list.append(binary_value)

    return binary_data_list


#### converts an immediate (binary string) to a signed integer (2's complement)
def binary_to_int(binary_str):
    # Check if it's a negative number (2's complement)
    if binary_str[0] == "1":
        inverted_str = "".join(["1" if bit == "0" else "0" for bit in binary_str])
        absolute_value = int(inverted_str, 2) + 1
        return -absolute_value
    else:
        return int(binary_str, 2)


#### access register
def read_register(register_number):
    register_number = int(register_number, 2)
    if register_number == 0:  # (x0 = 0 always)
        return 0
    else:
        return register_list[register_number]


def write_register(register_number, value):
    register_number = int(register_number, 2)
    if register_number != 0:  # (x0 = 0 always)
        register_list[register_number] = int(value)


#### get address
def get_address(rs1, imm):
    rs1 = int(rs1, 2)
    return register_list[rs1] + imm


#### access memory
# read 4 byte integer from data memory
def read_memory(address):
    address -= 0x10000000  # data memory starts from 0x10000000 but the list index starts from 0
    binary_str = ""
    for i in range(4):
        binary_str += data_memory_list[address + (3 - i)]
        decimal_value = binary_to_int(binary_str)
    return decimal_value


# write 4 byte integer to data memory
def write_memory(address, decimal_value):
    address -= 0x10000000  # data memory starts from 0x10000000 but the list index starts from 0
    binary_str = format(decimal_value, "032b")
    for i in range(4):
        data_memory_list[address + (3 - i)] = binary_str[8 * i : 8 * (i + 1)]


#### execute binary instruction
def execute_binary_instruction(binary_str):
    # global variables
    global register_list
    global data_memory_list
    global program_counter

    # get opcode for determining instruction
    opcode = binary_str[25:32]

    # R-Type Instructions
    if opcode == "0110011":
        funct3 = binary_str[17:20]
        funct7 = binary_str[0:7]
        rd = binary_str[20:25]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]

        if funct3 == "000" and funct7 == "0000000":  # add
            write_register(rd, read_register(rs1) + read_register(rs2))
            program_counter += 1
        elif funct3 == "000" and funct7 == "0100000":  # sub
            write_register(rd, read_register(rs1) - read_register(rs2))
            program_counter += 1
        elif funct3 == "001" and funct7 == "0000000":  # sll
            write_register(
                rd,
                read_register(rs1) << (read_register(rs2) & 0b11111),
            )
            program_counter += 1
        elif funct3 == "010" and funct7 == "0000000":  # slt
            if read_register(rs1) < read_register(rs2):
                write_register(rd, 1)
            else:
                write_register(rd, 0)
            program_counter += 1
        elif funct3 == "100" and funct7 == "0000000":  # xor
            write_register(rd, read_register(rs1) ^ read_register(rs2))
            program_counter += 1
        elif funct3 == "101" and funct7 == "0000000":  # srl
            if (read_register(rs2) == 0):
                    write_register(rd, read_register(rs1))
            else:
                write_register(
                    rd,
                    (read_register(rs1) & 0xFFFFFFFF) >> (read_register(rs2) & 0b11111)
                )
            program_counter += 1
        elif funct3 == "101" and funct7 == "0100000":  # sra
            write_register(
                rd,
                read_register(rs1) >> (read_register(rs2) & 0b11111)
            )
            program_counter += 1
        elif funct3 == "110" and funct7 == "0000000":  # or
            write_register(rd, read_register(rs1) | read_register(rs2))
            program_counter += 1
        elif funct3 == "111" and funct7 == "0000000":  # and
            write_register(rd, read_register(rs1) & read_register(rs2))
            program_counter += 1

    # I-Type Instructions
    elif opcode in {"0010011", "0000011", "1100111"}:
        funct3 = binary_str[17:20]
        rd = binary_str[20:25]
        rs1 = binary_str[12:17]
        imm = binary_str[0:12]

        if opcode == "0010011":
            if funct3 == "000":  # addi
                write_register(rd, read_register(rs1) + binary_to_int(imm))
                program_counter += 1

            elif funct3 == "010":  # slti
                if read_register(rs1) < binary_to_int(imm):
                    write_register(rd, 1)
                else:
                    write_register(rd, 0)
                program_counter += 1
            elif funct3 == "100":  # xori
                write_register(rd, read_register(rs1) ^ binary_to_int(imm))
                program_counter += 1
            elif funct3 == "110":  # ori
                write_register(rd, read_register(rs1) | binary_to_int(imm))
                program_counter += 1
            elif funct3 == "111":  # andi
                write_register(rd, read_register(rs1) & binary_to_int(imm))
                program_counter += 1
            elif funct3 == "001" and imm[0:7] == "0000000":  # slli
                write_register(
                    rd,
                    read_register(rs1) << (binary_to_int(imm) & 0b11111)
                )
                program_counter += 1
            elif funct3 == "101" and imm[0:7] == "0000000":  # srli
                if (binary_to_int(imm) == 0):
                    write_register(rd, read_register(rs1))
                else:
                    write_register(
                        rd,
                        (read_register(rs1) & 0xFFFFFFFF) >> (binary_to_int(imm) & 0b11111),
                    )
                program_counter += 1
            elif funct3 == "101" and imm[0:7] == "0100000":  # srai
                write_register(
                    rd,
                    read_register(rs1) >> (binary_to_int(imm) & 0b11111),
                )
                program_counter += 1

        elif opcode == "0000011":  # lw
            if funct3 == "010":
                if get_address(rs1, binary_to_int(imm)) == 0x20000000:
                    # get user input and store it to rd register
                    user_input = int(input())
                    write_register(rd, user_input)
                else:
                    write_register(
                        rd,
                        read_memory(get_address(rs1, binary_to_int(imm))),
                    )
                program_counter += 1

        elif opcode == "1100111" and funct3 == "000":  # jalr
            write_register(
                rd, program_counter * 4 + 4
            )  # actual address of next instruction
            program_counter = int((read_register(rs1) + binary_to_int(imm)) / 4)

    # S-Type Instructions
    elif opcode == "0100011":
        funct3 = binary_str[17:20]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]
        imm = binary_str[0:7] + binary_str[20:25]

        if funct3 == "010":  # sw
            if get_address(rs1, binary_to_int(imm)) == 0x20000000:
                # print ascii code of rs2 register value
                print(chr(read_register(rs2)), end="")
            else:
                write_memory(
                    get_address(rs1, binary_to_int(imm)),
                    read_register(rs2),
                )
            program_counter += 1

    # SB-Type Instructions
    elif opcode == "1100011":
        funct3 = binary_str[17:20]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]
        imm = binary_str[0] + binary_str[24] + binary_str[1:7] + binary_str[20:24] + "0"

        if funct3 == "000":  # beq
            if read_register(rs1) == read_register(rs2):
                program_counter += int(binary_to_int(imm) / 4)
            else:
                program_counter += 1
        elif funct3 == "001":  # bne
            if read_register(rs1) != read_register(rs2):
                program_counter += int(binary_to_int(imm) / 4)
            else:
                program_counter += 1
        elif funct3 == "100":  # blt
            if read_register(rs1) < read_register(rs2):
                program_counter += int(binary_to_int(imm) / 4)
            else:
                program_counter += 1
        elif funct3 == "101":  # bge
            if read_register(rs1) >= read_register(rs2):
                program_counter += int(binary_to_int(imm) / 4)
            else:
                program_counter += 1

    # U-Type Instructions
    elif opcode in {"0110111", "0010111"}:
        rd = binary_str[20:25]
        imm = binary_str[0:20] + "000000000000"

        if opcode == "0110111":  # lui
            write_register(rd, binary_to_int(imm))
            program_counter += 1
        elif opcode == "0010111":  # auipc
            write_register(rd, (program_counter * 4) + (binary_to_int(imm)))
            program_counter += 1

    # UJ-type Instructions
    elif opcode == "1101111":
        rd = binary_str[20:25]
        imm = (
            binary_str[0] + binary_str[12:20] + binary_str[11] + binary_str[1:11] + "0"
        )
        write_register(
            rd, program_counter * 4 + 4
        )  # actual address of next instruction
        program_counter += int(binary_to_int(imm) / 4)


# convert integer to 32 bit 2's complement hexadecimal
def int_to_hex(integer):
    if integer < 0:
        return format((1 << 32) + integer, "08x")  # 2's complement property
    else:
        return format(integer, "08x")


#### main
register_list = [0 for i in range(32)]
data_memory_list = ["11111111" for i in range(64 * 1024)]  # 64KB = 64 * 1024 Byte
# only for data not instruction, initialize with "11111111"(0xff)
program_counter = 0

# load binary instrunction to instruction_list (1 element = 4 byte)
binary_instructions_path = sys.argv[1]
instruction_list = read_binary_file_4byte(binary_instructions_path)

if len(sys.argv) == 3:
    instruction_number = int(sys.argv[2])
elif len(sys.argv) == 4:
    binary_data_path = sys.argv[2]
    instruction_number = int(sys.argv[3])

    # load data to data_memory_list (1 element = 1 byte)
    binary_data_list = read_binary_file_1byte(binary_data_path)
    data_memory_list[0 : len(binary_data_list)] = binary_data_list

# execute instructions
for i in range(instruction_number):
    if program_counter >= len(instruction_list):
        break
    execute_binary_instruction(instruction_list[int(program_counter)])

# print register values in hexadecimal
for i in range(32):
    print("x" + str(i) + ": 0x" + format((register_list[i] & ((1 << 32)-1)), "08x"))
