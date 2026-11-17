#include "daisysp.h"
#include <cstdint>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace daisysp;

Oscillator osc;

static void WriteWav(const char* path, const std::vector<float>& samples, uint32_t sampleRate)
{
	uint32_t fileSize = 0; 
	uint32_t dataSize = static_cast<uint32_t>(samples.size() * sizeof(int16_t));

	uint32_t formatSize = 16;
	uint16_t pcm = 1; 
	uint16_t channels = 2; 
	uint32_t bitsPerSample = 16;
	uint32_t byteRate = (sampleRate * channels * bitsPerSample) / 8;
	uint32_t blockAlign = (channels * bitsPerSample) / 8;
	
	std::ofstream out(path, std::ios::binary);
	// RIFF Header
	out.write("RIFF", 4);
	out.write(reinterpret_cast<const char *>(&fileSize), 4);
	out.write("WAVE", 4);
	// Format chunk
	out.write("fmt ", 4);
    out.write(reinterpret_cast<const char*>(&formatSize), 4); 
    out.write(reinterpret_cast<const char*>(&pcm), 2); 
    out.write(reinterpret_cast<const char*>(&channels), 2); 
    out.write(reinterpret_cast<const char*>(&sampleRate), 4); 
    out.write(reinterpret_cast<const char*>(&byteRate), 4);
    out.write(reinterpret_cast<const char*>(&blockAlign), 2);
    out.write(reinterpret_cast<const char*>(&bitsPerSample), 2);
	out.write("data ", 4);
	// Data chunk
	out.write(reinterpret_cast<const char*>(&dataSize), 4);
	
	for(float sample : samples) {
		float clippedSample = std::min(1.0f, std::max(sample, -1.0f));
		int16_t pcmSample = static_cast<int16_t>(clippedSample * 32767.0f);
		out.write(reinterpret_cast<const char*>(&pcmSample), 2);
	}
}

int main()
{
    const uint32_t sampleRate = 48000;
	const uint32_t frames = sampleRate * 5;

    osc.Init(sampleRate);
    osc.SetFreq(440.0f);
    osc.SetWaveform(Oscillator::WAVE_SIN);
    osc.SetAmp(0.2f);

    std::vector<float> output;
    for(uint32_t i = 0; i < frames; i++)
    {
        float s = osc.Process();
        output.push_back(s);
        output.push_back(s);
    }

    WriteWav("output.wav", output, sampleRate);
}
