# PA2

## core fn
    - binary to instruction : convert 4bytes binary to instruction (in assembly)
    - execute instruction :  execute assembly instruction (imm/4를 통해 branch/jump는 index를 통해 access)

## help fn
    - read binary file : parse binary file by 4 bytes to get instruction
    - imm to int : convert imm(binary) to int
    - access memory : access memory by address(we'll use index of array)
    - access register : access register by index(we'll use index of array)

## note
    - memory access 할 때 address는 low order 2byte만 사용
    - memory & register access 할 때 global var 사용
    - instuction list는 function을 통해 얻기
    - data list는 먼저 initialize 필요


~swe3005/2023f/proj2/riscv-sim ~swe3005/2023f/proj2/proj2_8_inst.bin ~swe3005/2023f/proj2/proj2_8_data.bin 2001 > r.txt
python3 t.py ~swe3005/2023f/proj2/proj2_8_inst.bin ~swe3005/2023f/proj2/proj2_8_data.bin 2001 > m.txt
python3 t.py ~swe3005/2023f/proj2/proj2_8_inst.bin ~swe3005/2023f/proj2/proj2_8_data.bin 2001
~swe3005/2023f/proj2/riscv-sim ~swe3005/2023f/proj2/proj2_8_inst.bin ~swe3005/2023f/proj2/proj2_8_data.bin 2001
diff r.txt m.txt
```


./riscv-sim ~swe3005/2023f/proj2/proj2_8_inst.bin ~swe3005/2023f/proj2/proj2_8_data.bin 2001  > m.txt

~swe3005/2023f/proj2/riscv-sim ~swe3005/2023f/proj2/proj2_8_inst.bin ~swe3005/2023f/proj2/proj2_8_data.bin 2001 > r.txt

diff m.txt r.txt 