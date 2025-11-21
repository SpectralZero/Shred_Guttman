import secrets

# === YOUR PATTERN LIST EXTRACTED VERBATIM ===
PATTERNS = [
    *[lambda size: secrets.token_bytes(size) for _ in range(4)],   # Random passes 1-4
    lambda size: bytes([0x55] * size),                            # Pass 5
    lambda size: bytes([0xAA] * size),                            # Pass 6
    lambda size: bytes([0x92, 0x49, 0x24] * (size // 3 + 1))[:size], # Pass 7
    lambda size: bytes([0x49, 0x24, 0x92] * (size // 3 + 1))[:size], # Pass 8
    lambda size: bytes([0x24, 0x92, 0x49] * (size // 3 + 1))[:size], # Pass 9
    lambda size: bytes([0x00] * size),                            # Pass 10
    lambda size: bytes([0x11] * size),                            # Pass 11
    lambda size: bytes([0x22] * size),                            # Pass 12
    lambda size: bytes([0x33] * size),                            # Pass 13
    lambda size: bytes([0x44] * size),                            # Pass 14
    lambda size: bytes([0x55] * size),                            # Pass 15
    lambda size: bytes([0x66] * size),                            # Pass 16
    lambda size: bytes([0x77] * size),                            # Pass 17
    lambda size: bytes([0x88] * size),                            # Pass 18
    lambda size: bytes([0x99] * size),                            # Pass 19
    lambda size: bytes([0xAA] * size),                            # Pass 20
    lambda size: bytes([0xBB] * size),                            # Pass 21
    lambda size: bytes([0xCC] * size),                            # Pass 22
    lambda size: bytes([0xDD] * size),                            # Pass 23
    lambda size: bytes([0xEE] * size),                            # Pass 24
    lambda size: bytes([0xFF] * size),                            # Pass 25
    lambda size: bytes([0x92, 0x49, 0x24] * (size // 3 + 1))[:size], # Pass 26
    lambda size: bytes([0x49, 0x24, 0x92] * (size // 3 + 1))[:size], # Pass 27
    lambda size: bytes([0x24, 0x92, 0x49] * (size // 3 + 1))[:size], # Pass 28
    lambda size: bytes([0x6D, 0xB6, 0xDB] * (size // 3 + 1))[:size], # Pass 29
    lambda size: bytes([0xB6, 0xDB, 0x6D] * (size // 3 + 1))[:size], # Pass 30
    lambda size: bytes([0xDB, 0x6D, 0xB6] * (size // 3 + 1))[:size], # Pass 31
    *[lambda size: secrets.token_bytes(size) for _ in range(4)]    # Random passes 32-35
]


# === VISUALIZER ===
def inspect_gutmann(size=64):
    print(f"\n=== GUTMANN 35-PASS VISUALIZER (size={size} bytes) ===\n")
    for i, pattern_fn in enumerate(PATTERNS, start=1):
        data = pattern_fn(size)

        print(f"\n--- PASS {i} ---")

        # Detect pattern type
        is_random = False
        if i <= 4 or i >= 32:
            is_random = True
        
        if is_random:
            print("TYPE: RANDOM (cryptographically secure)")
        else:
            print("TYPE:", "CONSTANT PATTERN" if len(set(data)) == 1 else "REPEATING MULTI-BYTE PATTERN")

        # Print byte statistics
        print(f"Length: {len(data)} bytes")

        # Show first 64 bytes in hex
        print("Hex preview:", data[:64].hex(" ").upper())

        # If constant, also print repeated value
        if len(set(data)) == 1:
            print(f"Constant byte: {hex(data[0])}")

    print("\n=== END ===\n")


# RUN DEMO
if __name__ == "__main__":
    inspect_gutmann(1024)  # Example with 1024 bytes per pass

