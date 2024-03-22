# TO READ

https://www.scitepress.org/PublishedPapers/2015/52297/52297.pdf

https://link.springer.com/article/10.1007/s10796-009-9210-z

# Card types definitions

## EM410x

The tag contains a contactless transponder carrying 64 bits of read only memory without use of encryption. The programming of the chip is performed by the manufacturer by laser fusing of poly silicon links. By this way, an unique code is assigned to each individual chip. The memory is organized into a 9 bit header, 40 bits of data (unique ID), 14 parity bits, and one stop bit. The output is modulated using the Manchester coding with a bit rate corresponding to 64 cpb (carrier cycles per bit). The tag uses 125 kHz carrier with ASK (amplitude-shift keying) modulation. An example of the modulation is depicted in Figure 1. The tag is transmitting data as long as it is in the range of the readers electromagnetic field (EM Microelectronic-Marin SA, 2004).

> 64 bits of data:
> 9 bit header
> 40 bits of ID = 5 byte ID
> 14 parity bits
> 1 stop bit

# Notes for LATEX

\documentclass zmenit oneside na twoside pri tisku, jinak nechat oneside

prepnout na kompilator xelatex

Pro cj:
\usepackage xevlna pevne mezery automaticky

# To ask:

- citation of a footnote