@echo off

python ..\assembler\makekernel.py core console
..\bin\snasm -vice library.asm standard.lib
python ..\assembler\makeimport.py standard

copy *.lib ..\files
copy *.dict ..\files


copy standard.lib ..\assembler
copy standard.dict ..\assembler

