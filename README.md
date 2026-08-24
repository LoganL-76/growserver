# growserver

A full-stack IoT monitoring system for an indoor grow tent. Sensors collect environmental and soil data, publish it wirelessly to a local server, and a web dashboard displays live and historical graphs. Long-term goals include a mobile app and ML-based growth prediction and yield analysis.

---

## System Architecture

```
[ESP32 Sensor Node]
  BME280  (temp/humidity/pressure)
  BH1750  (light/lux)
  4x Soil Moisture Sensors
        |
        | WiFi / MQTT
        v
[Mosquitto MQTT Broker] -- desktop
        |
        | paho-mqtt subscriber
        v
[Django REST API] --> [PostgreSQL Database]
        |
        v
[React Web Dashboard]   [React Native Mobile App]
```

---

## Hardware

| Component | Purpose | Notes |
|---|---|---|
| ESP32 DevKit V1 (AITRIP, CP2102) | Sensor node | Publishes JSON to MQTT every 30s |
| ESP32-CAM MB + OV2640 | Camera / timelapse | Not yet implemented |
| BME280 | Temp, humidity, pressure | I²C address 0x76 |
| BH1750 | Light intensity (lux) | I²C address 0x23 |
| 4x Capacitive Soil Moisture Sensors | Soil moisture per plant | GPIO32, 33, 34, 35 (ADC1) |
| Mosquitto | MQTT broker | Running as Windows service |

### ESP32 Pin Mapping

| Pin | Purpose |
|---|---|
| GPIO21 | I²C SDA (BME280 + BH1750) |
| GPIO22 | I²C SCL (BME280 + BH1750) |
| GPIO32 | Soil sensor 1 |
| GPIO33 | Soil sensor 2 |
| GPIO34 | Soil sensor 3 |
| GPIO35 | Soil sensor 4 |

### MQTT

- Broker: `localhost`
- Topic: `grow/sensors`
- Payload format:

```json
{
  "temperature": 22.41,
  "humidity": 47.73,
  "pressure": 975.67,
  "light": 25.00,
  "soil1": 45,
  "soil2": 52,
  "soil3": 38,
  "soil4": 61
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Firmware | Arduino / C++ (ESP32) |
| MQTT Broker | Mosquitto |
| Backend | Django 6.1 + Django REST Framework |
| Database | PostgreSQL 17 |
| Frontend | React + Recharts (planned) |
| Mobile | React Native (planned) |
| ML | scikit-learn / PyTorch (planned) |

---

## Data Models

### grows app
- **Grow** — a single grow cycle with start/end date and status
- **Plant** — individual plant belonging to a grow, with strain
- **Harvest** — wet/dry weight per plant at harvest
- **Expense** — equipment, nutrients, electricity, seeds per grow
- **JournalEntry** — timestamped notes with optional photo per grow

### sensors app
- **Sensor** — registry of physical sensors, optionally linked to a plant
- **SensorReading** — timestamped float value from a sensor

---

## Project Status

### Complete ✅
- ESP32 firmware — all sensors reading and publishing JSON over MQTT
- Mosquitto broker installed and running
- Django project scaffolded with PostgreSQL
- All data models defined and migrated

### In Progress 🔨
- MQTT subscriber — ingests sensor data into Django via REST API
- REST API endpoints for sensor readings and grow management

### Planned 📋
- React web dashboard with live and historical graphs
- React Native mobile app for remote monitoring
- ESP32-CAM timelapse implementation
- Journal, expense, and harvest frontend
- ML growth prediction layer
- Permanent hardware installation (crimped wiring, junction box)
- Conformal coating on PCBs before tent installation

---

## Local Development Setup

### Prerequisites
- Python 3.14+
- PostgreSQL 17
- Git

### 1. Clone the repo

```bash
git clone https://github.com/LoganL-76/growserver.git
cd growserver
```

### 2. Install Python dependencies

```bash
pip install django djangorestframework psycopg2-binary paho-mqtt python-decouple
```

### 3. Create your .env file

Create a `.env` file in the project root — never commit this file:

```
SECRET_KEY=your_django_secret_key_here
DB_PASSWORD=your_postgres_password_here
```

### 4. Set up PostgreSQL

```sql
CREATE DATABASE growserver;
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. MQTT Broker

The Mosquitto broker runs on Logan's desktop at `localhost`. If developing locally without access to that network, install Mosquitto locally and update `mqtt_server` in the ESP32 firmware and the Django MQTT subscriber accordingly.

---

## Grow Tent

- **Size:** 2ft x 4ft x 5ft
- **Sensor wiring:** Routes outside tent through grommets, only sensor tips inside

---

## Future Additions

- MH-Z19C CO₂ sensor (deferred, modular add-on)
- Automated alerts for out-of-range sensor values
- Cost-per-gram yield analysis
- Canopy analysis from camera imagery; pest/disease detection


## Notes & Blockers

### Open Questions
- Soil sensor calibration concerns; averages or ranges may need to be decided
- Sensor protection and flexible mounting positions not determined
