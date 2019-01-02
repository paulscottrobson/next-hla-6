
python ../assembler/makekernel.py core console
zasm -buw library.asm -o standard.lib -l standard.lst
python ../assembler/makeimport.py standard

cp *.lib ../files
cp *.dict ../files


cp standard.lib ../assembler
cp standard.dict ../assembler

