# Research: FM vs Subtractive Synthesis

**Related issue:** #21 <br>
**Time spent:** 9 h

## Question

What are different types of synthesis, and what are differences between FM and subtractive one?

## Findings

### 1. Sound basics

#### 1.1 Harmonics

Harmonics are higher-frequency sine waves that combine with a base pitch to create the rich, complex sound of musical instruments.

- **Fundamental frequency (f):** the lowest frequency and primary pitch you hear (also called the first harmonic).
- **Harmonics (2f, 3f, 4f...):** additional frequencies that are integer multiples of the fundamental. If the fundamental is 100 Hz, the 2nd harmonic is 200 Hz, the 3rd is 300 Hz, and so on.
- **Inharmonic spectrum:** partials that are not integer multiples of the fundamental. The ear does not group them into a clear pitch.

#### 1.2 Basic waveforms

Combining a fundamental sine wave with its harmonics creates different waveforms. With phase φ = (f·t) mod 1 and amplitude A:

| Waveform | Time domain | Harmonics | Sound |
|:---|:---|:---|:---|
| Sine | x(t) = A sin(2πft) | only f | pure, smooth, flute-like |
| Sawtooth | x(t) = 2A(φ − 1/2) | all n | bright, edgy, buzzy |
| Square | x(t) = A · sgn(sin(2πft)) | odd n | hollow, woody, clarinet-like |
| Triangle | x(t) = (2A/π) · arcsin(sin(2πft)) | odd n | soft, mellow |

#### 1.3 Amplifier and envelope

These two blocks exist in every synthesizer, regardless of the synthesis type.

- **Amplifier (VCA):** multiplies the signal by a gain value: y(t) = g(t) · x(t). It does not generate sound, it only scales it.
- **Envelope:** a control signal g(t) that changes over time after a key is pressed. Turning the volume simply on and off sounds unnatural (clicks, no decay), so g(t) follows a shape. The most common is **ADSR**:

| Stage | Meaning |
|:---|:---|
| Attack (time) | rise from 0 to the peak after key on |
| Decay (time) | fall from the peak to the sustain level |
| Sustain (level, not time) | level held as long as the key is pressed |
| Release (time) | fall to 0 after key off |

```
   Amplitude
   ^
   |      /\
   |     /  \
   |    /    \________
   |   /              \
   |  /                \
   +-------------------------> Time
     | A  | D |   S   | R |
   Key On             Key Off
```

An envelope is a general modulation source. The same shape can control the amplifier (loudness), the filter cutoff (subtractive) or the modulation index (FM).

### 2. Types of synthesis

Synthesis types can be grouped by how they produce sound. Layering and modulating basic waveforms is the common idea, and the sound is then shaped over time with envelopes.

| Type | How the sound is made |
|:---|:---|
| **Subtractive** | harmonically rich waveform, then a filter removes harmonics |
| **Additive** | sum of sine waves with individual amplitudes |
| **FM** | one oscillator modulates the frequency of another |
| **AM** | one oscillator modulates the amplitude of another |
| **Wavetable** | scanning through a table of stored waveforms |

### 3. Subtractive synthesis

The most common method, and the one that originated the concept of sound synthesis. It utilizes waveform choice, filtering and envelope adjustment.

**Idea:** start with a harmonically rich waveform (saw, square), then remove harmonics with a filter and shape the loudness with an envelope.

**Signal chain:** oscillator (VCO) -> mixer -> filter (VCF) -> amplifier with ADSR envelope (VCA)

#### 3.1 Oscillator
Generates the original waveform.

#### 3.2 Mixer
Combines the outputs of multiple oscillators, producing a much more complex signal: x(t) = x1(t) + x2(t) + x3(t)

#### 3.3 Filter
The key stage of subtractive synthesis. It changes the amplitude of different frequencies.

| Filter | Function |
|:---|:---|
| Low-pass | keeps low frequencies, reduces high frequencies |
| High-pass | keeps high frequencies, reduces low frequencies |
| Band-pass | keeps a selected frequency range |
| Notch | reduces a selected frequency range |

- **Cutoff frequency:** detemines where filtering begins.
- **Resonance:** boosts frequencies around the cutoff point.

In the frequency domain, filtering is a multiplication: Y(f) = X(f) · H(f), where X(f) is the original spectrum, H(f) the filter response and Y(f) the resulting spectrum. An envelope can also control the cutoff.

### 4. FM synthesis

FM synthesis works by using one oscillator to change the frequency of another oscillator.

In most project, FM synthesis is implemented using **Phase Modulation**. The output of a modulator is added to the phase of the carrier rather than directly changing its frequency.

y(t) = A · sin( 2π·fc·t + I · sin(2π·fm·t) )

- **Carrier (fc):** the oscillator producing the main audible sound.
- **Modulator (fm):** the oscillator that modulates the carrier.
- **Modulation index (I):** controls the amount of phase modulation.

**Signal chain:** modulator operators -> carrier operators -> amplifier (VCA)

**Idea:** The modulation creates sidebands above and below the carrier at multiples of the modulator frequency. With an index of zero there is no modulation at all. Digital FM is usually implemented as phase modulation.

#### 4.1 Frequency ratios

Each operator has a frequency ratio relative to the played note's fundamental frequency.
For a note with fundamental frequency f0, the frequency of operator i is:
fi = Ri · f0

When one operator modulates another, the effective modulation ratio is:
R = fm / fc

- **Integer ratios** give harmonic sounds and a clear pitch:
  - 1:1 -> all harmonics
  - 2:1 -> only odd harmonics
  - 3:1 -> every third harmonic is missing
- **Non-integer ratios** (like 1.41:1, 3.5:1, 2.5351:1) give inharmonic sounds: metallic, bell-like tones.

The algorithm determines which operators are connected, while their individual ratios determine the frequency relationships within that algorithm.

#### 4.2 Modulation index
The modulation index controls the amount of phase modulation applied to a carrier.

For sinus modulation:
I = Δf / fm

Δf -> peak frequency deviation <br>
fm -> modulator frequency


- Low index -> few sidebands (dark)
- High index -> many sidebands (bright)

The modulation index is the FM equivalent of filter in subtractive synthesis, but the underlying mechanism is different. A subtractive filter removes existing spectral components, while the FM modulation creates additional sidebands.
An envelope can control the modulation index over time.

#### 4.3 Sidebands 

y(t) = A Σ J_n(B) · sin(2π(fc + n·fm)t), n = −∞..∞

- Sidebands sit at fc ± n·fm, spaced by the modulator frequency.
- The amplitude of the n-th sideband is the Bessel function J_n(B).
- B = 0: J_0 = 1 and all others are 0, so only the carrier remains (pure sine).
- There are roughly B + 1 significant sidebands on each side.
- Sidebands below 0 Hz reflect back into the spectrum, which is an extra source of inharmonic content.

#### 4.5 Algorithms

An algorithm defines how the operators are connected. Each operator generates a sine wave that can either modulate another operator or contribute directly to the output.

- **Modulator:** an operator whose output is used to modulate the phase of another operator.
- **Carrier:** an operator whose output contributes directly to the audible signal.
- **Feedback:** an optional connection that feeds an operator's output back into its own phase input.


`A->B` = A modulates B, `*` = carrier.

| # | Connection | Carriers |
|:--|:---|:---|
| 1 | 4->3->2->1* | 1 |
| 2 | (4+3)->2->1* | 1 |
| 3 | (4->3) + 2 -> 1* | 1 |
| 4 | 4->(3, 2)->1* | 1 |


#### 4.6 Controls

A 4-op FM engine exposes many parameters. Each operator would have its frequency ratio, output level and envelope, while global settings would define configured algorithm.

**Proposed parameters**

| Patameter | Scope | Function |
|:---|:---|:---|
| Algorithm | Global | Define how operators are connected |
| Frequency ratio | Per operator | Sets the operator frequency relative to the played note |
| Fixed frequency (OPTIONAL) | Per operator | Set an absolute frequency |
| Frequency mode (OPTIONAL) | Per operator | Selects ratio or fixed-frequency mode |
| Operator output level | Per operator | Modulator: modulation index, Carrier: audible amplitude |
| Feedback (OPTIONAL) | Per operator | How much this operator modulates itself |
| ADSR envelope | Per operator | Shaped modulation index/output level over time|
| Master pitch/octave | Global | Transposes entire tone |
| Master volume | Global | Controls final output |

### 7. Conclusions

**Proposal:** 4-op FM as the synthesis engine

Why FM:
- Four operators can be connected in many different patterns, granting more control over how sounds are generated.
- FM is easily capable of producting a broad variety of sounds.
- Many operators allow us a detailed control over spectrum.
- Compared to basic subtractive synth, 4-op FM allows us more opportunities for complex modulation and experimentation.

Although FM engine introduces much more implementation complexity than subtractive synthesis, it is also what draws us to implementing it. Implementing it would make MarkovBox a much more complex and sophisticated project.

## Sources
- https://ristoid.net/modular/fm_variants.html
- https://beatkitchen.io/guides/synthesist/07-fm-synthesis/
- https://en.wikipedia.org/wiki/Sideband
- https://en.wikipedia.org/wiki/Frequency_modulation_synthesis
- https://www.perfectcircuit.com/signal/what-is-fm-synthesis 
- https://cs.wellesley.edu/~cs203/lecture_materials/freq_phase_modulation/freq_phase_modulation.pdf
- https://docs.google.com/document/d/1dLrLAFyj1qOBhgkgtjH0oDM67nwY9DkMXg1a5tIjvx4/edit?tab=t.0
- https://gamma.app/docs/SA1012-Modulation-Fundamentals-AM-FM-PM-zq5fs7t1ag08zky?mode=doc
