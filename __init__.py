from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.entity import Entity
from datetime import datetime, timedelta
import aiohttp
import logging
import random

_LOGGER = logging.getLogger(__name__)

# Define the time ranges for random updates
time_ranges = [
    ["08:00", "09:30"],
    ["10:00", "11:30"],
    ["11:40", "14:00"],
    ["15:00", "16:30"],
    ["17:00", "18:30"],
    ["18:45", "20:00"],
]

async def async_setup_entry(hass: HomeAssistant, config_entry) -> bool:
    """Set up the Natis Checker component."""
    component = NatisChecker(hass, config_entry)
    hass.data["natis_checker"] = component  # Store the component instance
    component.schedule_random_updates()  # Schedule the initial updates
    return True

class NatisChecker(Entity):
    """A custom entity that checks Natis slots and sends notifications."""

    def __init__(self, hass: HomeAssistant, config):
        """Initialize the component."""
        self.hass = hass
        self.username = config.get("username")
        self.password = config.get("password")
        self.DTLCheck = config.get("DTLCheck")
        self.notification_title = "Slots have been found!"
        self.slots_data = []

    async def async_update(self):
        """Fetch data from the API and update the state."""
        login_url = "https://oauth.natis.gov.za/rtmc-jwt-auth/auth/login"
        slots_url = "https://online.natis.gov.za/vehicle-renewal-service/lookups/dltcs/4/05"

        try:
            async with aiohttp.ClientSession() as session:
                # Login request
                login_payload = {"username": self.username, "password": self.password}
                async with session.post(login_url, json=login_payload) as response:
                    response.raise_for_status()
                    token = response.headers.get("token")

                # Slots request
                headers = {"token": token}
                async with session.get(slots_url, headers=headers) as response:
                    response.raise_for_status()
                    self.slots_data = await response.json()

            await self.check_slots()

        except aiohttp.ClientError as e:
            _LOGGER.error(f"API request failed: {e}")

    async def check_slots(self):
        """Check slot availability and send a notification if slots are found."""
        if any(item["name"] == self.DTLCheck and item["count"] > 0 for item in self.slots_data):
            count = next(item["count"] for item in self.slots_data if item["name"] == self.DTLCheck)
            title = f"{self.notification_title} - {self.DTLCheck}"
            message = f"{title}: {count} slots available"

            await self.hass.services.async_call(
                "notify",
                "your_notification_service",  # Replace with the actual service name
                {
                    "title": title,
                    "message": message,
                },
            )

    def schedule_random_updates(self):
        """Schedule a single update at a random time within each time window."""
        now = datetime.now()
        for start, end in time_ranges:
            start_time = self._parse_datetime(start, now)
            end_time = self._parse_datetime(end, now)

            random_time = self._get_random_time_in_window(start_time, end_time)

            if random_time < now:
                random_time += timedelta(days=1)

            _LOGGER.info(f"Scheduling update at {random_time}")
            async_track_point_in_time(self.hass, self.async_update, random_time)

    def _parse_datetime(self, time_str, reference):
        """Convert 'HH:MM' time string to a datetime object."""
        hour, minute = map(int, time_str.split(":"))
        return reference.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def _get_random_time_in_window(self, start_time, end_time):
        """Generate a random time within the given window."""
        delta = end_time - start_time
        random_offset = random.randint(0, int(delta.total_seconds()))
        return start_time + timedelta(seconds=random_offset)

    @property
    def state(self):
        """Return the state of the entity."""
        return "ok"

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dtl_check_data = next((item for item in self.slots_data if item["name"] == self.DTLCheck), None)

        if dtl_check_data:
            return {
                "Last run time": last_run_time,
                "DTLCheck": self.DTLCheck,
                "Count": dtl_check_data["count"],
                "Infrastructure No": dtl_check_data["infrastructureNo"],
            }
        else:
            return {
                "Last run time": last_run_time,
                "DTLCheck": self.DTLCheck,
                "Status": "No data available",
            }
