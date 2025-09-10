# 📊 Observability Playground (Traces + Metrics + Logs)

This project is an ***observability stack** designed to collect and visualize **metrics, logs, and distributed traces** from a sample FastAPI application.
It demonstrates how to instrument an application using **OpenTelemetry** and monitor it with **Prometheus, Loki, Tempo, and Grafana**. The project was made as an example project to learn how to connect and handle the observability of an application. 

*Serves purely educational purposes*

## 📖 Overview

The goal of this project is to provide a **hands-on playground** to explore observability concepts:

* **Metrics:** Powered by Prometheus.
* **Logs:** Collected and aggregated in Loki.
* **Traces:** Exported to Tempo and analyzed with Grafana’s TraceQL.

## ⚙️ Tech Stack

* **Sample Application:** FastAPI + OpenTelemetry (Traces + Prometheus metrics + JSON logs)
* **Prometheus:** Time-series database for metrics
* **Loki:** Log aggregation backend
* **Tempo:** Distributed tracing backend
* **Grafana:** Unified observability dashboard
* **Alloy:** Telemetry collector (OTLP → Loki + Tempo)
* **Containerization:** Docker + Docker Compose (single-network setup)

---

## 📁 Project Structure

```bash
.
├── app/                         # Sample FastAPI app with OTEL instrumentation
│   ├── main.py
│   └── requirements.txt
├── prometheus/
│   └── prometheus.yml           # Prometheus scrape config
├── loki/
│   └── loki-config.yaml         # Loki configuration
├── tempo/
│   └── tempo.yaml               # Tempo configuration
├── alloy/
│   └── config.alloy             # Alloy collector configuration
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── datasources.yaml # Preconfigured data sources for Grafana
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Start the Stack

Run the observability stack with:

```bash
docker compose up --build -d
```

This will spin up:

* **Sample App** → [http://localhost:8000](http://localhost:8000)
* **Prometheus** → [http://localhost:9090](http://localhost:9090)
* **Loki** → available at `localhost:3100`
* **Tempo** → available at `localhost:3200`
* **Grafana** → [http://localhost:3000](http://localhost:3000)

### 2. Generate Some Data

* Hit endpoints in the sample app:

  * `GET /` – logs a healthy status
  * `GET /work` – simulates work, logs a warning, and creates a trace
  * `GET /error` – logs an error and triggers an exception
* Check:

  * **Metrics:** `http://localhost:8000/metrics`
  * **Logs:** In Grafana → Explore → Loki
  * **Traces:** In Grafana → Tempo/Traces view

## 🔍 Experimentation Ideas

| Component  | Experiment                                                              |
| ---------- | ----------------------------------------------------------------------- |
| Logs       | Generate more `/error` calls and observe logs in Loki                   |
| Metrics    | Stress-test `/work` endpoint and watch latency histograms in Prometheus |
| Traces     | Correlate slow requests with their spans in Grafana Tempo               |
| Dashboards | Build custom Grafana panels combining logs + traces + metrics           |

## 📸 Demo

![Grafana picture](https://raw.githubusercontent.com/papdawin/Observability-playground/refs/heads/main/pictures/dashboard.png)
