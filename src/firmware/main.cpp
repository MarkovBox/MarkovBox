#include "Synthesis/oscillator.h"
#include "daisy_seed.h"

using namespace daisy;
using namespace daisysp;

DaisySeed hw;
Oscillator osc;

void AudioCallback(AudioHandle::InputBuffer in, AudioHandle::OutputBuffer out, size_t size)
{
  float sig;
	for (size_t i = 0; i < size; i++)
	{
    sig = osc.Process();

    out[0][i] = sig;
    out[1][i] = sig;
	}
}

int main(void)
{
  float sample_rate;
	hw.Init();
	hw.SetAudioBlockSize(4);
	sample_rate = hw.AudioSampleRate();
  osc.Init(sample_rate);

  // Set basic parameters for Oscillator
  osc.SetWaveform(osc.WAVE_SIN);
  osc.SetFreq(440);
  osc.SetAmp(0.5);

	hw.StartAudio(AudioCallback);
	while(1) {}
}
