# Multiservice Load Balancer – DevOps Demo

## Overview

Acest proiect demonstrează o arhitectură **multi-service** bazată pe Docker Compose, în care un **Nginx reverse proxy** funcționează ca **load balancer** pentru două backend-uri identice Flask și, în același timp, servește un **frontend static**.

Scopul proiectului este de a simula distribuirea traficului între mai multe instanțe backend și de a evidenția principiile de bază DevOps:

* containerizare
* networking între servicii
* load balancing
* separarea responsabilităților

---

## Architecture

```
Client (Browser)
        |
        v
+-------------------+
|   Nginx (Edge)    |  ← Reverse Proxy + Load Balancer
|  Port 8080 -> 80  |
+-------------------+
        |
        +----------------------+
        |                      |
        v                      v
+---------------+      +---------------+
| Backend API 1 |      | Backend API 2 |
| Flask (5000)  |      | Flask (5000)  |
+---------------+      +---------------+
```

* **Nginx**

  * entry point al aplicației
  * load balancing (round-robin) către backend-uri
  * servește frontend static (HTML/CSS/JS)
* **Backend API (x2)**

  * aplicație Flask identică
  * diferențiere prin variabila de mediu `INSTANCE`
* **Frontend**

  * pagină HTML statică
  * JavaScript face requesturi către `/api/*` prin Nginx

---

## Project Structure

```
Multiservice-load-balancer/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── assets/
│       └── bg.jpg
│
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
└── README.md
```

---

## Technologies Used

* **Docker & Docker Compose**
* **Nginx** – reverse proxy & load balancer
* **Python Flask** – backend API
* **HTML / CSS / JavaScript** – frontend
* **Linux (Ubuntu Server)** – deployment environment

---

## How It Works

1. Clientul accesează aplicația prin `http://SERVER_IP:8080`
2. Nginx:

   * servește frontend-ul static
   * redirecționează requesturile `/api/*` către backend-uri
3. Backend-urile Flask răspund alternativ (round-robin)
4. Fiecare răspuns API conține numele instanței (`backend-api-1` / `backend-api-2`) pentru a demonstra load balancing-ul

---

## Running the Application

### Prerequisites

* Docker
* Docker Compose

### Start services

```bash
docker compose up --build -d
```

### Check running containers

```bash
docker ps
```

---

## Testing

### From server (local test)

```bash
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/api/health
```

### From browser (remote)

```
http://SERVER_IP:8080/
http://SERVER_IP:8080/api/health
```

Refresh de mai multe ori endpoint-ul `/api/health` pentru a observa schimbarea valorii `instance`.

---

## Features

* Reverse proxy cu Nginx
* Load balancing între două backend-uri
* Frontend static servit de Nginx
* Upload imagini (postere filme)
* Background image pentru UI
* Docker network dedicat pentru comunicarea serviciilor
* Healthcheck pentru backend-uri

---

## DevOps Concepts Demonstrated

* Containerization
* Service discovery prin Docker networking
* Load balancing (round-robin)
* Separation of concerns
* Infrastructure reproducibility

---

## Notes

* Datele sunt stocate local doar pentru scop de test (demo).
* Proiectul este destinat scopurilor educaționale și de portofoliu DevOps.

---

## Author

Marius Iordan
2026

