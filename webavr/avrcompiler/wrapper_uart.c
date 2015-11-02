/**CFile***********************************************************************

  FileName    [wrapper_uart.c]

  Synopsis [Provides a main in which the UART is initialized and used as the
  output of printf functions]

  Description [The program is meant to be used as a wrapper for other programs
  that invoke assembly code and return data that needs to be printed through
  the Serial channel. The wrapper provides the mapping between the printf
  function and the serial port.]

  SeeAlso [Most of the source code is taken from
  http://hekilledmywire.wordpress.com/2011/01/05/using-the-usartserial-tutorial-part-2/]

  Author      [Abelardo Pardo <abelardo.pardo@sydney.edu.au>]

  Copyright   [Copyright (c) 2014 The University of Sydney
  All rights reserved.

  Permission is hereby granted, without written agreement and without license
  or royalty fees, to use, copy, modify, and distribute this software and its
  documentation for any purpose, provided that the above copyright notice and
  the following two paragraphs appear in all copies of this software.

  IN NO EVENT SHALL THE UNIVERSITY OF SYDNEY BE LIABLE TO ANY PARTY FOR DIRECT,
  INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
  USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERISY OF SYDNEY
  HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

  THE UNIVERISY OF SYDNEY SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT
  NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
  PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
  AND THE UNIVERSITY OF SYDNEY HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
  SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.]

******************************************************************************/
#include <avr/io.h>
#include <stdio.h>
#include <stdbool.h>
#include <util/delay.h>

/*---------------------------------------------------------------------------*/
/* Constant declarations                                                     */
/*---------------------------------------------------------------------------*/
#define BAUDRATE 9600
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)
 
/*---------------------------------------------------------------------------*/
/* External function prototypes                                              */
/*---------------------------------------------------------------------------*/
unsigned int asm_function();
void print_integer(unsigned int v);

/*---------------------------------------------------------------------------*/
/* Static function prototypes                                                */
/*---------------------------------------------------------------------------*/
static void usart_init(uint16_t ubrr);
static char usart_getchar(void) __attribute__ ((unused));
static void usart_putchar(char data) __attribute__ ((unused));
static void usart_pstr(char *s) __attribute__ ((unused));
static unsigned char usart_kbhit(void) __attribute__ ((unused));
static int usart_putchar_printf(char var, FILE *stream);

/*---------------------------------------------------------------------------*/
/* Variable declarations                                                     */
/*---------------------------------------------------------------------------*/
static FILE mystdout = FDEV_SETUP_STREAM(usart_putchar_printf, NULL, 
                                         _FDEV_SETUP_WRITE);

/*---------------------------------------------------------------------------*/
/* Definition of functions                                                   */
/*---------------------------------------------------------------------------*/
/**Function********************************************************************

  Synopsis           [Initializes the UART and invokes assembly functions]

  Description [This program is intended to initialize the UART, call an
  assembly function and print the result in the screen.]

  SideEffects        [Programs the UART in the board]

******************************************************************************/
int main() {
    // To catch the result
    unsigned int myvalue = -1;

    // set up stdio stream
    stdout = &mystdout;
    
    // Initialize the usart
    usart_init (BAUD_PRESCALLER);
    
    // Capture the result of the execution
    myvalue = (unsigned int)asm_function();

    // Print the result of the function
    printf("Result (unsigned integer): %d\n", myvalue);
    
    // main loop
    while(true) {
        // do nothing
    }
}

/**Function********************************************************************

  Synopsis           [Function that prints a given unsigned int]

  Description [The function simply prints the value give as parameter with a 
  preceding text.]

  SideEffects        [Prints the message in STDOUT]

******************************************************************************/
void print_integer(unsigned int v)
{
    printf("The given parameter is %d\n", v);
    return;
}

/*---------------------------------------------------------------------------*/
/* Definition of static functions                                            */
/*---------------------------------------------------------------------------*/

/**Function********************************************************************

  Synopsis           [Initializes the UART in the board]

  Parameters         [UBRR: The 16 value used to set the bit rate]  

  SideEffects [Sets the baud rate and enables the transmission and reception of
  data through the UART in the board.]

******************************************************************************/
static void usart_init(uint16_t ubrr) {
    // Set baud rate
    UBRR0H = (uint8_t)(ubrr >> 8);
    UBRR0L = (uint8_t)(ubrr);
    
    // Enable receiver and transmitter
    UCSR0B = (1 << RXEN0)|(1 << TXEN0);

    // Set frame format: 8data, 1stop bit
    UCSR0C = (3 << UCSZ00);
}
 
/**Function********************************************************************

  Synopsis           [Sends the char received as parameter through the UART]

  Parameters         [Char to be sent]  

  SideEffects [Char is sent through the UART, thus modifying the status
  registers accordingly.]

******************************************************************************/
static void usart_putchar(char data) {
    // Wait for empty transmit buffer
    while (!(UCSR0A & (_BV(UDRE0))));

    // Start transmission
    UDR0 = data;
}

/**Function********************************************************************

  Synopsis           [Read a character from the USART]

  SideEffects        [None]

******************************************************************************/
static char usart_getchar(void) {
	// Wait for incoming data
	while (!(UCSR0A & (_BV(RXC0))));

	// Return the data
	return UDR0;
}

/**Function********************************************************************

  Synopsis           [Detect if a nonzero character is waiting]

  SideEffects        [None]

******************************************************************************/
static unsigned char usart_kbhit(void) {
    //return nonzero if char waiting polled version
    unsigned char b;
    b = 0;

    if(UCSR0A & (1 << RXC0)) {
        b = 1;
    }

    return b;
}

/**Function********************************************************************

  Synopsis           [Send a zero-terminated string through the UART]

  Description [Receives a zero-terminated string and iterates over all its
  characters invoking usart_putchar to send it through the USART.]

  Parameters         [Zero-terminated string.]  

  SideEffects        [None]

******************************************************************************/
static void usart_pstr(char *s) {
    // loop through entire string
    while (*s) {
        usart_putchar(*s);
        s++;
    }
}

/**Function********************************************************************

  Synopsis           [Handler invoked by printf to handle the stream.]

  Description [The function receives a character and a file stream, but it
  simply sends that character through the UART. It also takes care of the
  special case of the new line character (\n) which translates to new-line and
  line feed (\n\r)]

  Parameters         [Character to send and stream from which it comes.]  

  SideEffects        [None]

******************************************************************************/
// this function is called by printf as a stream handler
static int usart_putchar_printf(char var, FILE *stream) {

    // translate \n to \r for br@y++ terminal
    if (var == '\n') {
        usart_putchar('\r');
    }
    usart_putchar(var);
    return 0;
}
