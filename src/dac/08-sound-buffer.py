def generate_note_buffer(frequency, duration_ms):
    total_samples = int(SAMPLE_RATE * duration_ms / 1000)
    note_buffer = bytearray(total_samples * 2)  # 16-bit mono

    if frequency == 0:
        # REST note, fill with zeros
        return note_buffer

    # Envelope parameters: fade in/out over first/last X% of samples
    attack_len = int(0.05 * total_samples)
    release_len = int(0.05 * total_samples)
    amplitude = 0.15

    samples_per_cycle = SAMPLE_RATE / frequency

    for i in range(total_samples):
        # Sine wave
        sample_pos = (i / samples_per_cycle) * 2 * math.pi
        raw_value = math.sin(sample_pos)

        # Apply a simple envelope
        if i < attack_len:
            env = i / attack_len       # fade in
        elif i > (total_samples - release_len):
            env = (total_samples - i) / release_len  # fade out
        else:
            env = 1.0                  # sustain

        value = int(32767 * amplitude * raw_value * env)
        struct.pack_into("<h", note_buffer, i*2, value)

    return note_buffer


# Then, in your melody loop
for note_name, duration in MELODY:
    frequency = NOTES[note_name]
    note_buf = generate_note_buffer(frequency, duration)
    audio_out.write(note_buf)
    sleep_ms(70)  # small gap after each note
