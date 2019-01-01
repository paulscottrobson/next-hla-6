@echo off
call build.bat
copy standard.lib boot.img
..\bin\CSpect.exe -zxnext -brk -exit -esc -w3 ..\files\bootloader.sna