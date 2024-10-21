# **Natis Checker Home Assistant Component**  

This custom Home Assistant component automates the process of checking the availability of service slots on the Natis platform and sends notifications if slots are found. It can schedule these checks randomly within specified time windows, with dynamic controls to start or stop the cron jobs.

---

## **Features**  
- **API Integration**: Logs in to the Natis system and fetches available slots.  
- **Random Scheduling**: Runs **once at a random time** within each configured time window.  
- **Dynamic Control**: Start or stop the cron jobs using Home Assistant services.  
- **Notifications**: Sends alerts when slots matching your criteria are found.  

---

## **Installation**

1. **Download or Clone** this repository.
2. Create a folder named `natis_checker` in your Home Assistant `custom_components` directory:  
   ```
   config/custom_components/natis_checker/
   ```
3. Place the `__init__.py` file in the `natis_checker` folder.
4. Restart Home Assistant to load the component.

---

## **Configuration**  

Add the following entry to your `configuration.yaml`:

```yaml
natis_checker:
  username: "your_username"
  password: "your_password"
  DTLCheck: "DTL_you_wish_to_track"
```

### **Configuration Options**  
| Option      | Required | Description                            |
|-------------|----------|----------------------------------------|
| `username`  | Yes      | Your Natis account username.           |
| `password`  | Yes      | Your Natis account password.           |
| `DTLCheck`  | Yes      | Name of the service slot to check for. |

---

## **How to Use**

### **Available Services**  
This component exposes the following services:

1. **Start Cron**  
   Service: `natis_checker.start_cron`  
   - This starts the cron jobs to run at random times within each predefined time window.

2. **Stop Cron**  
   Service: `natis_checker.stop_cron`  
   - This stops the cron jobs and cancels all scheduled updates.

### **Start Cron Automatically at Home Assistant Start**  
You can create an automation to start the cron jobs when Home Assistant starts:

```yaml
automation:
  - alias: Start Natis Checker Cron
    trigger:
      platform: homeassistant
      event: start
    action:
      service: natis_checker.start_cron
```

---

## **Time Windows Configuration**

The component runs **once at a random time within each of the following time windows**:

```python
time_ranges = [
    ["08:00", "09:30"],
    ["10:00", "11:30"],
    ["11:40", "14:00"],
    ["15:00", "16:30"],
    ["17:00", "18:30"],
    ["18:45", "20:00"],
]
```

You can modify the `time_ranges` list in the code to suit your needs.

---

## **Notifications**  
The component sends notifications using Home Assistant’s notification service. Update the following part of the code to match your desired notification service:

```python
await self.hass.services.async_call(
    "notify",
    "your_notification_service",  # Replace with your service name
    {
        "title": title,
        "message": message,
    },
)
```

---

## **Logs and Troubleshooting**

Enable debug logging by adding the following to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.natis_checker: debug
```

Check logs in **Developer Tools > Logs** to verify if the component is running as expected.

---

## **Testing the Component**

1. Go to **Developer Tools > Services** in Home Assistant.
2. Select the `natis_checker.start_cron` or `natis_checker.stop_cron` service.
3. Verify the logs to see if the component runs at the scheduled random times.

---

## **License**  

This project is licensed under the **GNU General Public License v3.0**.  

### **GPL-3.0 License Summary**  
This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the **GNU General Public License** for more details.  

You should have received a copy of the GNU General Public License along with this program. If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).  

---

## **Contributing**  

Feel free to submit issues or feature requests via the repository, or fork the project and submit a pull request.

---

## **License File**  

Create a file named `LICENSE` in your project directory with the following content:

---

**LICENSE (GPL-3.0)**  

```
Copyright (C) [Year] [Your Name or Organization]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

---

## **FAQ**

### 1. How can I verify that cron jobs are scheduled?  
Check the logs for messages like:  
```
INFO: Scheduling update at 2024-10-21 15:45:30
```

### 2. Can I change the time windows?  
Yes, modify the `time_ranges` list in the code to fit your preferred schedule.

---