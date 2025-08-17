from collections import defaultdict
from datetime import datetime

from pathlib import Path
import json

import logging

logger = logging.getLogger("event_planner")
DATA_DIR = Path("data")
RESERVATIONS_FILE = DATA_DIR / "reservations.json"

class Reservation:
    channel_reservations = defaultdict(list)

    def __init__(self):
        pass

    def ensure_reservation_file_exists(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not RESERVATIONS_FILE.exists():
            logger.info(f"Created reservation file {RESERVATIONS_FILE}")
            with open(RESERVATIONS_FILE, "w") as f:
                json.dump({}, f)

    # def save_reservations(filename="reservations.json"):
    #     with open(filename, "w") as f:
    #         json.dump({
    #             str(cid): [
    #                 (s.isoformat(), e.isoformat(), eid)
    #                 for s, e, eid in reservations
    #             ] for cid, reservations in self.channel_reservations.items()
    #         }, f)

    # def load_reservations(filename="reservations.json"):
    #     try:
    #         with open(filename) as f:
    #             data = json.load(f)
    #             for cid, reservations in data.items():
    #                 self.channel_reservations[int(cid)] = [
    #                     (datetime.fromisoformat(s), datetime.fromisoformat(e), eid)
    #                     for s, e, eid in reservations
    #                 ]
    #     except FileNotFoundError:
    #         pass  # No saved file yet

    def save_reservations(self):
        with open(RESERVATIONS_FILE, "w") as f:
            json.dump({
                str(cid): [
                    (name, s.isoformat(), eid)
                    for name, s, eid in reservations
                ] for cid, reservations in self.channel_reservations.items()
            }, f)

    def load_reservations(self):
        try:
            with open(RESERVATIONS_FILE) as f:
                data = json.load(f)
                for cid, reservations in data.items():
                    self.channel_reservations[int(cid)] = [
                        (name, datetime.fromisoformat(s), eid)
                        for name, s, eid in reservations
                    ]
        except FileNotFoundError:
            logger.error("Reservation file not found. Creating reservation file.")
            self.ensure_reservation_file_exists()
            self.load_reservations()
            pass

    def is_channel_free(self, channel_id: int, start: datetime, end: datetime) -> bool:
        for reserved_start, reserved_end, _ in self.channel_reservations.get(channel_id, []):
            if start < reserved_end and end > reserved_start:
                return False
        return True
    
    def is_reservation_loaded(self, event_id: int) -> bool:
        return event_id in self.channel_reservations

    def reserve_channel(self, channel_id: int, name: str,start: datetime, event_id: int):
        self.channel_reservations[event_id].append((name, start, channel_id))
        self.save_reservations()

    def cancel_reservation(self, event_id: int):
        for cid in self.channel_reservations:
            self.channel_reservations[cid] = [
                (s, e, eid) for s, e, eid in self.channel_reservations[cid]
                if eid != event_id
            ]
        self.save_reservations()

    def cleanup_old_reservations(self):
        now = datetime.now(datetime.timezone.utc)
        for cid in self.channel_reservations:
            self.channel_reservations[cid] = [
                (s, e, eid) for s, e, eid in self.channel_reservations[cid]
                if e > now
            ]
        self.save_reservations()
