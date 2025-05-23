ENTRY(_start)
SECTIONS {
    . = 0x40000000; /* Memory start address of the virt machine */
    .text : { *(.text) }
    .data : { *(.data) }
    .bss : { *(.bss) }
    . = ALIGN(4);
}
