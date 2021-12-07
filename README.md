# wdb

A little complement to Wayne Holder's fantastic work with the [debugWIRE protocol](https://sites.google.com/site/wayneholder/debugwir). Basically, Wayne found a way to make a debugWIRE probe out of an AVR-related product (bare AVR chip or an Arduino board). Sadly, the probe can't be used to debug C/C++ code, and it doesn't seem there is anything on the Internet to solve that issue.

This project proposes some kind of solution for basic C/C++ debugging, shamefully using Wayne's work and avr-gdb.

## Requirement

This project works with an AVR chip with the latest version of [Wayne's code](https://sites.google.com/site/wayneholder/debugwire3) uploaded on it (such a chip will be called a Wayne probe) and avr-gdb installed on your computer. You also need a .elf version of your code with debug symbols.
