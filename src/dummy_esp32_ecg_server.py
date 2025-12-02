import asyncio
import websockets
import math
import random

# ---------------- CONFIG ----------------
HOST = "0.0.0.0"   # Use "localhost" if testing locally
PORT = 81
SAMPLE_RATE = 250   # samples per second
# ----------------------------------------

async def ecg_stream(websocket, *args):
    """Send fake ECG samples and print any message received from client (browser)."""
    print(f"Client connected: {websocket.remote_address}")

    async def sender():
        """Continuously send ECG-like waveform."""
        t = 0.0
        while True:
            base_wave = 0.5 * math.sin(2 * math.pi * 1.2 * t)  # ~1.2 Hz heart rhythm
            noise = random.uniform(-0.05, 0.05)
            qrs_spike = 1.5 if int(t * 1.2 * SAMPLE_RATE) % 200 == 0 else 0
            ecg_value = (base_wave + qrs_spike + noise) * 1000
            await websocket.send(f"{ecg_value:.2f}")
            await asyncio.sleep(1 / SAMPLE_RATE)
            t += 1 / SAMPLE_RATE

    async def receiver():
        """Listen for messages from client (browser)."""
        async for message in websocket:
            print(f"Received from browser: {message}")

    sender_task = asyncio.create_task(sender())
    receiver_task = asyncio.create_task(receiver())

    done, pending = await asyncio.wait(
        [sender_task, receiver_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()
    print("Client disconnected")

async def main():
    print(f"Starting dummy ECG WebSocket on ws://{HOST}:{PORT}")
    async with websockets.serve(ecg_stream, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
