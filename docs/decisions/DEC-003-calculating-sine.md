# Decision DEC-003: Choosing a Method for Calculating Sine Values During Live Synthesis
**Date:** 18-11-2026 <br>
**Area:** Sound Engine <br>
**Related issue:** #34 <br>
## Context
 
We need a fast way to calculate sine values during audio synthesis.
 
Key constraints:
 
- **Required power:** We plan to implement 4-operator FM with four voices, which means 16 operators continuously evaluating the sine function.

## Options considered

| Option  |Pros|Cons|
|:-------:|:--:|:--:|
| `sinf()`| - Easy to use, no need to reinvent the wheel   |  - 16 operators calling `sinf()` 48000 times per second would be computationally expensive  |
| Lookup table  | - Drastically reduces the computation time of an approximated sine  | - Less accurate approximation <br> - Uses some memory, though not much   |
 
 
## Decision
 
We choose the **lookup table**

## Reasoning

A lookup table saves considerably more processing time than `sinf()`, and the memory it requires is minimal. The approximation is not as precise as sinf(), but a sufficiently large table combined with linear interpolation should be more than enough for our synthesis.
