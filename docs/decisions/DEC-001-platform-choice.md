# Decision DEC-001: Selection of Embedded Microcontroller Platform
 
**Date:** 25-10-2026 <br>
**Area:** Hardware <br>
 
## Context
 
We need an embedded microcontroller platform capable of running real-time audio synthesis.
 
Key technical constraints:
 
- **Memory:** Sufficient RAM to hold large multi-order Markov transition tables in memory.
- **DSP Performance:** FPU support and enough clock speed for real-time audio synthesis.
- **Development environment:** Limited development time, requiring existing audio libraries rather than building from scratch.
 
## Options considered
 
|   Option   |                                                                      Pros                                                                      |                                                     Cons                                                      |
| :--------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
| Daisy Seed | - Mature libDaisy and DaisySP libraries <br> - 64 MB SDRAM <br> - High-performance ARM Cortex-M7 with hardware FPU <br> - Built-in audio codec | - Higher cost compared to basic microcontrollers <br> - Currently out of stock (restock in November/December) |
|   RP2040   |                                                    - Very low cost <br> - Widely available                                                     |                       - No FPU <br> - Only 264 KB SRAM <br> - Requires external I2S DAC                       |
 
## Decision
 
We choose **Daisy Seed**.
 
## Reasoning
 
Daisy Seed provides us with the libDaisy and DaisySP libraries, which will drastically speed up our development process. It also offers significantly more RAM to store Markov transition tables, solving two of our biggest bottlenecks. The potential cost savings of choosing the RP2040 are not worth the heavy compromises its limited memory and lack of FPU would force on the way.
