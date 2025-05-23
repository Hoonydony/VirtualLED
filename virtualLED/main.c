#define SIGNAL_REG (*(volatile unsigned int*)(0x40010000))
#define DEBUG_REG (*(volatile unsigned int*)(0x40010004))
#define COUNTER_REG (*(volatile unsigned int*)(0x40010008))

void main(void) {
    unsigned int counter = 0;
    SIGNAL_REG = 0; // Initialize
    DEBUG_REG = 0xDEAD;
    COUNTER_REG = counter;
    while (1) {
        SIGNAL_REG = 1; // Turn signal ON
        DEBUG_REG = 0xAAAA;
        COUNTER_REG = counter + 1;
        counter++;
        SIGNAL_REG = 0; // Turn signal OFF
        DEBUG_REG = 0xBBBB;
        COUNTER_REG = counter + 1;
        counter++;
    }
}

void _start(void) {
    asm volatile (
        "mov sp, #0x8000000\n\t"
        "bl main\n\t"
        "b .\n\t"
    );
}
