#!/bin/bash
#
# Author: Abelardo Pardo <abelardo.pardo@sydney.edu.au>
#
# Script to compile a set of files with avr-gcc, create the corresponding hex
# program with abr-objcopy and send it to the board using avrdude.
#
# The following variables can be defined to adapt to different configurations:
#
# - exec_fname: Name of the executable to be created (default: exec)
#
# - chip_type: Chip type in the board (default: atmega328p)
#
# - usb_port: USB where the board is connected (default: /dev/ttyUSB0)
#
# You may set the values of these parameters by typing a command like the
# following one in the command interpreter (omit the dollar sign):
#
# $ export chip_type=atmega328p
# 
# Any compilation from then on will assume the atmega328. If now variable is
# defined, the script will take the default values.
#
# WARNING: The usb_port is the variable that most likely will need to be
# changed. Use the Arduino IDE to find out where is the board connected. Take
# that value and type the following command in the interpreter (omit the dollar
# sign):
#
export usb_port="/dev/ttyACM0"
# 

# Make sure at least a file has been given as parameter.
if [ "$1" == "" ]; then
    echo "#"
    echo "# The script name needs to be followed by parameters. Example:"
    echo "#"
    echo "# bash compile_upload.sh myprogram.s"
    echo "#"
    echo "# if you have more than one *.s file, separate them by spaces"
    echo "#"
    exit
fi

# Check that all given parameters are files that exist
for fname in $@; do
    if [ ! -e "$fname" ]; then
        echo "#"
        echo "# ERROR: File $fname not found in this folder."
        echo "#"
        exit
    fi
done

# If wrapper_uart.c is not present, nothing to do
if [ ! -e "avrcompiler/wrapper_uart.c" ]; then
    echo "#"
    echo "# ERROR: File wrapper_uart.c must be present in this folder."
    echo "#"
    echo "# Dowload the file from the course notes"
    echo "#"
    exit
fi

# Define some vars in case they haven't been defined before
if [ "$exec_fname" == "" ]; then
    exec_fname=exec
fi

if [ "$chip_type" == "" ]; then
    chip_type=atmega328p
fi

if [ "$usb_port" == "" ]; then
    # Do not change the value here. Type a command such as
    # export usb_port="COM4"
    # in your command interpreter window before compiling your program
    usb_port="/dev/ttyUSB0"
fi

# Set three vars depending on the platform we are working
if [ "$MACHTYPE" == "i686-pc-msys" ]; then
    # Windows values
    bin_prefix="/c/Program Files (x86)/Arduino/hardware/tools/avr/bin/"
    avr_conf_opt="-C"
    avr_conf="/c/Program Files (x86)/Arduino/hardware/tools/avr/etc/avrdude.conf"
    programmer=arduino
else
    # Linux values
    bin_prefix=
    avr_conf_opt=
    avr_conf=
    programmer=arduino
fi

# Step 1
echo
echo "Step 1: Compiling the files and obtain an executable using avr-gcc"
"$bin_prefix"avr-gcc -Wall -g -Os -DF_CPU=16000000UL -mmcu=$chip_type \
    -o $exec_fname $@ avrcompiler/wrapper_uart.c
if [ "$?" != 0 ]; then
    echo "#"
    echo "# ERROR: Compilation failed. Check error messges above this one."
    echo "# Stopping."
    exit
else
    echo "--Done!--"
fi
echo

# Step 2: Create the dump of the diassembled code
echo "Step 2: Create a file with the disassembled code"
"$bin_prefix"avr-objdump -h -s -S $exec_fname > $exec_fname.lst
if [ "$?" != 0 ]; then
    echo "#"
    echo "# ERROR: Disassembled file creation failed. Check error messages."
    echo "# Stopping."
    exit
else
    echo "--Done!-- (check the file $exec_fname.lst)"
fi
echo

# Step 3
echo "Step 3: Translate the executable to HEX format suitable for Atmel chips"
"$bin_prefix"avr-objcopy -O ihex -R .eeprom $exec_fname $exec_fname.hex
if [ "$?" != 0 ]; then
    echo "#"
    echo "# ERROR: Translation to HEX format failed. Check error messages"
    echo "# Stopping."
    exit
else
    echo "--Done!--"
fi
echo

# Step 4
echo "Step 4: Transmit the executable to the board."
"$bin_prefix"avrdude -F \
                     -V \
                     "$avr_conf_opt" "$avr_conf" \
                     -c "$programmer" \
                     -p $chip_type \
                     -P $usb_port \
                     -b 115200 \
                     -U flash:w:$exec_fname.hex
if [ "$?" != 0 ]; then
    echo "#"
    echo "# ERROR: Transmission didn't work."
    echo "# Verify that the board is connected to $usb_port."
    echo "# If not, you need to type the command:"
    echo '# export usb_port="YOURPORT"'
    echo "# where YOURPORT is something like COM3 or COM5."
    echo "#"
    exit
else
    echo "--Done!--"
fi
echo
echo "#"
echo "# Open the Serial Monitor in the IDE (Tools->Serial Monitor, "
echo "# or Crtl-Shift-M) to see the data produced by your program".
echo "#"