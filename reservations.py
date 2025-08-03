from collections import defaultdict
from datetime import datetime

from pathlib import Path
import json

channel_reservations = defaultdict(list)

DATA_DIR = Path("data")
RESERVATIONS_FILE = DATA_DIR / "reservations.json"

def ensure_reservation_file_exists():
    DATA_DIR.mkdir(exist_ok=True)  # Create 'data/' folder if it doesn't exist
    if not RESERVATIONS_FILE.exists():
        with open(RESERVATIONS_FILE, "w") as f:
            json.dump({}, f)  # Start with an empty dict

# def save_reservations(filename="reservations.json"):
#     with open(filename, "w") as f:
#         json.dump({
#             str(cid): [
#                 (s.isoformat(), e.isoformat(), eid)
#                 for s, e, eid in reservations
#             ] for cid, reservations in channel_reservations.items()
#         }, f)

# def load_reservations(filename="reservations.json"):
#     try:
#         with open(filename) as f:
#             data = json.load(f)
#             for cid, reservations in data.items():
#                 channel_reservations[int(cid)] = [
#                     (datetime.fromisoformat(s), datetime.fromisoformat(e), eid)
#                     for s, e, eid in reservations
#                 ]
#     except FileNotFoundError:
#         pass  # No saved file yet

def save_reservations():
    with open(RESERVATIONS_FILE, "w") as f:
        json.dump({
            str(cid): [
                (s.isoformat(), e.isoformat(), eid)
                for s, e, eid in reservations
            ] for cid, reservations in channel_reservations.items()
        }, f)

def load_reservations():
    try:
        with open(RESERVATIONS_FILE) as f:
            data = json.load(f)
            for cid, reservations in data.items():
                channel_reservations[int(cid)] = [
                    (datetime.fromisoformat(s), datetime.fromisoformat(e), eid)
                    for s, e, eid in reservations
                ]
    except FileNotFoundError:
        pass

def is_channel_free(channel_id: int, start: datetime, end: datetime) -> bool:
    for reserved_start, reserved_end, _ in channel_reservations.get(channel_id, []):
        if start < reserved_end and end > reserved_start:
            return False
    return True

def reserve_channel(channel_id: int, start: datetime, end: datetime, event_id: int):
    channel_reservations[channel_id].append((start, end, event_id))
    save_reservations()

def cancel_reservation(event_id: int):
    for cid in channel_reservations:
        channel_reservations[cid] = [
            (s, e, eid) for s, e, eid in channel_reservations[cid]
            if eid != event_id
        ]
    save_reservations()

def cleanup_old_reservations():
    now = datetime.now(datetime.timezone.utc)
    for cid in channel_reservations:
        channel_reservations[cid] = [
            (s, e, eid) for s, e, eid in channel_reservations[cid]
            if e > now
        ]
    save_reservations()
