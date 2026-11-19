# Verification status — 26 October 2026

## Executed successfully

- Installed the dependencies pinned in requirements.txt in the execution environment.
- Python syntax compilation; portable C++ CAALC and C Ascon compiled with GCC/G++.
- **101 pytest tests passed** in the final suite (see pytest.txt for exact run duration).
- Feistel inversion: 100 seeded random states and deterministic edge patterns through other checks.
- Python/native forward and inverse permutation agreement: 100 seeded states.
- Python/native AEAD agreement and round trips across 13 message lengths (0 through 65,536 bytes) and four AD lengths, including empty and partial blocks.
- Wrong key, wrong nonce, ciphertext change, tag change and AD change rejected in Python CAALC, native CAALC and native Ascon.
- **All 1,089 upstream final-standard Ascon-AEAD128 known-answer vectors** matched; all corresponding decryption round trips passed.
- WAV exact reconstruction at all 12 rate/frame/cipher combinations (2 rates × 3 frame durations × 2 algorithms), empty audio, truncated/extra/malformed containers, and invalid WAV handling.
- Large audio: 1 MiB PCM Ascon file test in pytest; separate **1 MiB PCM CAALC** exact file reconstruction, with recorded elapsed times in large_caalc_audio.json.
- MSE/PSNR/SNR reference cases, silence, mismatched lengths and invalid sizes.
- Nonce sequence generation uniqueness within a session, replay rejection, accepted reordering within window, invalid packets rejected without consuming replay state.
- Real localhost UDP send/receive test: eight accepted packets, duplicate and modified packet rejected; authenticated PCM recording verified.
- Fixed-deadline jitter reorder/concealment checks and seeded network-loss simulation.
- ML-KEM-512 encapsulation/decapsulation secret agreement, HKDF agreement and CAALC round trip using derived keys; no private KEM material is included in the release.
- Statistical/structural screening, native timed comparison, waveform/spectrogram and benchmark plot generation.
- Streamlit AppTest executed all seven screens; a separate live Streamlit process returned health `ok` (streamlit_health.json).
- Manual visual review of the generated waveform/spectrogram and benchmark PNGs.

## Attempted but not verified

An Arduino CLI executable was obtained. Its ESP32 index/core setup failed because its network/DNS requests were unavailable in this environment. A subsequent compile invocation reported the missing `esp32:esp32` platform. Logs are `esp32_toolchain_install.txt` and `esp32_compile_attempt.txt`.

**Therefore neither ESP32 sketch has a verified target-toolchain build here.** The shared portable cryptographic core did compile and match Python, but that does not validate Arduino APIs, I2S timing or device integration. Exact local installation/compile/flash instructions are in docs/HARDWARE.md. The standalone hardware benchmark sketch is similarly uncompiled on target here.

## Requires physical hardware / local environment

- Actual flashing, boot, INMP441 wiring, microphone sample alignment/level and audio fidelity.
- Real USB framing at 921600 baud and ESP32-to-laptop serial acceptance test.
- Wi-Fi connectivity, LAN firewall, UDP delivery and actual device packet loss/jitter.
- Laptop speaker playback and host sounddevice/PortAudio device support (recording tests do not exercise speakers).
- ESP32 cycles/timings, real-time deadlines, RAM/flash usage, stack high-water marks, energy/power and side-channel behavior.
- Actual procurement total within ₹500, including wires/tax/shipping.
- Windows/macOS dependency installation, C compiler setup and device drivers; execution here was Linux x86-64.

Use the exact USB and MIC acceptance procedures in docs/HARDWARE.md. Populate a new hardware result sheet only after observing actual device output. Do not replace “unverified” with “passed” based on source availability or a successful host compile.

## Security status

No independent cryptanalysis, formal AEAD proof, certification, authenticated remote ML-KEM protocol, or proven post-quantum security for CAALC. Statistical tests, a 128-bit tag and 256-bit capacity do not justify such claims. No physical hardware deployment is claimed complete.
