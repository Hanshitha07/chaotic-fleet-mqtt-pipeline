# 🚗 Chaotic Fleet
### Edge-Assisted IoT Data Ingestion & Cloud Persistence Pipeline

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT-purple)](https://mqtt.org/)
[![Redis](https://img.shields.io/badge/Redis-Deduplication-red?logo=redis)](https://redis.io/)
[![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-blue?logo=microsoftazure)](https://azure.microsoft.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Project-Academic%20Prototype-orange)]()

**Chaotic Fleet** is an IoT data ingestion and cloud persistence pipeline designed to simulate real-world vehicle telemetry streams and handle unreliable data before it reaches cloud storage.

The system simulates multiple vehicle sensor nodes that continuously generate telemetry messages, including valid messages, duplicate transmissions, and corrupted payloads. Using MQTT for communication, Redis for duplicate detection, and Azure cloud services for persistence, the pipeline demonstrates a structured approach to handling unreliable IoT data streams.

---

## 📌 1. Problem Statement

Modern IoT systems generate large volumes of telemetry data from connected devices such as vehicles, industrial sensors, and monitoring equipment.

However, real-world IoT communication can introduce several challenges:

- Duplicate messages caused by repeated transmissions.
- Corrupted or malformed payloads.
- Missing or invalid sensor fields.
- Unnecessary cloud database writes.
- Unreliable communication between devices and cloud services.

Sending every incoming message directly to cloud storage can result in redundant records, poor data quality, and unnecessary processing overhead.

**Chaotic Fleet addresses these challenges by introducing an edge-assisted ingestion pipeline that validates incoming telemetry, filters duplicate messages, isolates invalid data, and persists accepted messages to cloud storage.**

---

## 🎯 2. Project Objectives

- Simulate multiple IoT vehicle sensor nodes.
- Generate realistic and intentionally faulty telemetry streams.
- Establish MQTT-based communication between publishers and consumers.
- Detect and filter duplicate messages using Redis.
- Validate incoming telemetry against a predefined data schema.
- Route malformed and invalid messages to a Dead Letter Queue (DLQ).
- Persist accepted telemetry records in Azure Cosmos DB.
- Store telemetry data in Azure Blob Storage for archival and retrieval.
- Demonstrate reliable data handling across an IoT–Edge–Cloud pipeline.

---

## 🏗️ 3. System Architecture

The project follows an IoT–Edge–Cloud architecture.

```text
       IoT VEHICLE SENSOR SIMULATORS
       ┌───────────────────────────┐
       │ Vehicle Node 01           │
       │ Vehicle Node 02           │
       │ Vehicle Node 03           │
       │ ...                       │
       │ Vehicle Node N            │
       └─────────────┬─────────────┘
                     │
                     ▼
             MQTT PUBLISHER
                     │
                     ▼
             MQTT BROKER
                Mosquitto
                     │
                     ▼
             CLOUD CONSUMER
                     │
                     ▼
              JSON PARSING
                     │
                     ▼
          REDIS DUPLICATE FILTER
                     │
                     ▼
             SCHEMA VALIDATION
                     │
              ┌──────┴──────┐
              │             │
           Invalid        Valid
              │             │
              ▼             ▼
          DEAD LETTER    CLOUD STORAGE
            QUEUE             │
              │          ┌────┴─────┐
              │          │          │
              ▼          ▼          ▼
         Invalid Data  Cosmos DB  Blob Storage
                        Database    Archive
```

### Data Processing Flow

1. **Telemetry Generation:** Python-based virtual vehicle nodes generate sensor readings and simulated fault conditions.
2. **Message Publishing:** Generated telemetry is published through MQTT.
3. **Message Consumption:** The consumer subscribes to the MQTT topic and receives incoming messages.
4. **JSON Parsing:** Incoming messages are parsed to identify malformed JSON payloads.
5. **Duplicate Detection:** Redis checks message IDs and prevents repeated messages from being processed again.
6. **Schema Validation:** The consumer checks required fields and expected data types.
7. **Dead Letter Queue:** Invalid messages are isolated for further inspection instead of being persisted as valid telemetry.
8. **Cloud Persistence:** Accepted telemetry is stored in Azure Cosmos DB and Azure Blob Storage.

---

## ⚙️ 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Core application development |
| MQTT | Lightweight IoT messaging protocol |
| Eclipse Mosquitto | MQTT message broker |
| Redis | Message deduplication |
| Azure Cosmos DB | Structured telemetry persistence |
| Azure Blob Storage | Telemetry archival |
| Docker | Local infrastructure and service deployment |
| Paho MQTT | Python MQTT communication |
| Azure Python SDKs | Cloud service integration |

---

## ✨ 5. Key Features

### 5.1 Virtual IoT Vehicle Simulation

The project simulates multiple vehicle sensor nodes without requiring physical IoT hardware.

Each simulated vehicle can generate telemetry containing:

- Device ID
- Message ID
- Timestamp
- Sequence number
- Temperature readings
- Vibration readings
- Fault-related metadata

### 5.2 Chaos and Fault Injection

The telemetry generator introduces different message conditions to simulate unreliable IoT communication.

| Message Type | Description |
|---|---|
| Valid | Correctly structured telemetry |
| Duplicate | Previously transmitted message ID |
| Corrupted | Invalid sensor values or malformed data |
| Incomplete | Missing required fields |

### 5.3 Redis-Based Deduplication

Redis is used to identify previously processed message IDs.

The deduplication mechanism helps prevent repeated telemetry messages from being unnecessarily processed and stored.

### 5.4 Schema Validation

Incoming messages are checked against the expected telemetry structure.

Messages that fail validation are separated from valid telemetry.

### 5.5 Dead Letter Queue

Invalid or corrupted messages are routed to a Dead Letter Queue for isolation and later inspection.

This prevents invalid data from being treated as successfully processed telemetry.

### 5.6 Azure Cloud Persistence

Accepted telemetry is intended to be stored in two cloud services:

- **Azure Cosmos DB:** Stores structured telemetry records for querying and analysis.
- **Azure Blob Storage:** Stores telemetry data as objects for archival and retrieval.

---

## 📂 6. Project Structure

```text
chaotic-fleet/
│
├── chaos_generator/
│   ├── __init__.py
│   └── generator.py
│
├── cloud_consumer/
│   ├── __init__.py
│   ├── consumer.py
│   ├── deduplicator.py
│   └── ...
│
├── cloud_infrastructure/
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*Note: The structure above is representative. Adjust the file list to match the actual contents of your repository.*

---

## 🚀 7. Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.12
- Docker Desktop
- Git
- Microsoft Azure account
- Azure Cosmos DB account
- Azure Storage account

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd chaotic-fleet
```

### Step 2: Create a Virtual Environment

```bash
py -3.12 -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
python -m pip install -r requirements.txt
```

### Step 4: Start Local Infrastructure

Start the MQTT broker and Redis using Docker Compose:

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root using the configuration required by your application.

Example configuration template:

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# Azure Cosmos DB
COSMOS_DB_CONNECTION_STRING=your_cosmos_connection_string
COSMOS_DB_NAME=your_database_name
COSMOS_CONTAINER_NAME=your_container_name

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
AZURE_STORAGE_CONTAINER_NAME=your_container_name
```

Use the exact variable names expected by your Python source files.

**Security:** Never commit `.env` files, Azure connection strings, access keys, or other credentials to GitHub.

### Step 6: Start the Cloud Consumer

From the project root:

```bash
python -m cloud_consumer.consumer
```

The consumer listens for incoming MQTT telemetry and processes messages through the ingestion pipeline.

### Step 7: Start the Chaos Generator

Open another terminal, activate the same virtual environment, and run:

```bash
python -m chaos_generator.generator
```

The generator publishes simulated vehicle telemetry messages through the MQTT broker.

### Step 8: Monitor the Pipeline

Check running Docker containers:

```bash
docker ps
```

Check Redis:

```bash
docker exec local_redis redis-cli ping
```

Expected response:

```text
PONG
```

Monitor the MQTT broker and consumer terminal outputs to observe incoming messages, duplicate detection, validation results, and cloud persistence activity.

---

## 🧪 8. Expected Processing Behaviour

| Scenario | Expected Processing |
|---|---|
| Valid telemetry | Accepted and sent for cloud persistence |
| Duplicate message ID | Detected and filtered |
| Malformed JSON | Rejected and routed to DLQ |
| Missing required field | Rejected and routed to DLQ |
| Invalid sensor data type | Rejected and routed to DLQ |
| Cloud persistence failure | Reported as a failed write, not successful persistence |

The expected behaviour depends on the configuration and successful availability of the corresponding services.

---

## 🔐 9. Security Considerations

- Keep cloud credentials in environment variables.
- Exclude `.env` files from version control.
- Avoid hardcoding connection strings in source code.
- Use appropriate Azure access permissions.
- Validate incoming messages before cloud persistence.
- Avoid exposing sensitive telemetry or credentials in logs.

---

## 🔮 10. Future Enhancements

Potential improvements include:

- Real-time fleet monitoring dashboard.
- Integration with physical ESP32 or Arduino sensor nodes.
- Advanced telemetry analytics and anomaly detection.
- Automated retry mechanisms for temporary cloud failures.
- Persistent DLQ monitoring and message replay.
- Performance benchmarking under different message loads.
- Configurable fault-injection rates.
- Containerized deployment of the complete ingestion pipeline.

---

## 📚 11. Learning Outcomes

This project demonstrates practical implementation concepts in:

- Internet of Things (IoT).
- MQTT-based communication.
- Edge-assisted data processing.
- Distributed message handling.
- Redis-based deduplication.
- Data validation and fault injection.
- Dead Letter Queue design.
- Docker-based infrastructure.
- Microsoft Azure cloud integration.
- Cloud data persistence.

---


## ⭐ 12. Conclusion

Chaotic Fleet demonstrates how an IoT data ingestion pipeline can handle unreliable telemetry before persisting it to cloud services.

By combining MQTT communication, Redis-based duplicate detection, schema validation, Dead Letter Queue handling, and Azure cloud storage, the project provides a practical demonstration of an IoT–Edge–Cloud data processing architecture.

The project highlights the importance of data quality, fault handling, and reliable message processing in connected vehicle and large-scale IoT environments.

---

**Built with Python, MQTT, Redis, Docker, and Microsoft Azure.** 🚀
