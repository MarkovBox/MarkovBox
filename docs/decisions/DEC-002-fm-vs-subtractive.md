# Decision DEC-002: Selecting Synthesis Type for Our Sound Engine
**Date:** 11-11-2026 <br>
**Area:** Sound Engine <br>
**Related issue:** #21 <br>
**Related research:** [/research/fm_vs_subtractive_synthesis.md](../../research/fm_vs_subtractive_synthesis.md) 
## Context
 
We need a synthesis engine for our synthesizer. The research compared the main synthesis types, focusing on FM vs subtractive.
 
Key constraints:
 
- **Sound variety:** The engine should offer a broad range of timbres and room for experimentation.
- **Complexity:** Implementation effort must stay realistic for the project's timeframe.
- **Hardware:** The engine must run in real time on the Daisy Seed.

## Options considered
 
|   Option    |                                                                                                           Pros                                                                                                            |                                                               Cons                                                               |
| :---------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------: |
| Subtractive |                                            - Most common and well-known method <br> - Simple signal chain <br> - Lowest implementation complexity                                            |          - Filter can only remove existing harmonics <br> - Limited options for complex modulation and experimentation           |
|   4-op FM   | - Many operator connections <br> - Wide variety of sounds, including inharmonic ones <br> - Detailed control over the spectrum <br>  | - Much higher implementation complexity <br> - Many parameters to expose and tune <br> - Less intuitive to program than a filter |
 
## Decision
 
We choose **4-operator FM synthesis**, implemented as phase modulation:
 
`y(t) = A * sin(2*pi*fc*t + I * sin(2*pi*fm*t))`
 
## Reasoning
 
Four operators connected in different algorithms give far more control over the spectrum and more room for experimentation than a basic subtractive synth. FM is clearly more complex to implement than subtractive synthesis, but we accept this on purpose. Digital FM is usually implemented as phase modulation, which is the approach we will follow.
