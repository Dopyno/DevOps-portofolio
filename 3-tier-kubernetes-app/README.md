# Proiect: Deploy aplicație 3-tier pe Kubernetes (Proxmox + Ubuntu + kubeadm)

## 1. Scop
Acest proiect demonstrează deploy-ul unei aplicații clasice 3-tier pe Kubernetes:
- **Frontend**: NGINX servește conținut static și proxy pentru `/api` către backend
- **Backend**: REST API (PostgREST) conectat la baza de date
- **Database**: PostgreSQL cu persistență prin PVC

Cerințe acoperite:
- Secret pentru parole DB
- PersistentVolumeClaim pentru persistența bazei de date
- ConfigMap pentru configurații non-sensibile (backend)
- Backend folosește Secret (parola DB) injectat ca env var
- Backend are Liveness + Readiness probes
- Frontend are ConfigMap cu `nginx.conf` custom (proxy `/api` -> backend) montat în container
- Frontend expus extern prin Service de tip NodePort

---

## 2. Arhitectură Kubernetes

### Noduri
Cluster Kubernetes instalat cu `kubeadm` pe VM-uri Ubuntu în Proxmox:
- 1 x control-plane (master): rulează componentele de control (API Server, Scheduler, Controller Manager, etcd)
- 3 x worker nodes: rulează pod-urile aplicației (frontend/backend/postgres)

### Networking
- CNI: Calico
- Acces extern la aplicație: NodePort `30080`

---

## 3. Componente (resurse Kubernetes)

### Namespace
- `three-tier`

### Database (PostgreSQL)
- **Secret**: `postgres-secret` (cheie: `POSTGRES_PASSWORD`)
- **PVC**: `postgres-pvc` (5Gi, RWO)
- **Deployment**: `postgres`
- **Service**: `postgres` (ClusterIP:5432)

### Backend (PostgREST)
- **ConfigMap**: `backend-config` (DB_HOST, DB_PORT, DB_NAME, DB_USER)
- **Deployment**: `backend`
  - injectează parola din `postgres-secret`
  - LivenessProbe + ReadinessProbe pe `/` port 3000
- **Service**: `backend` (ClusterIP:3000)

### Frontend (NGINX)
- **ConfigMap**: `frontend-nginx-conf` (nginx.conf cu proxy `/api/` -> backend)
- **ConfigMap**: `frontend-html` (index.html)
- **Deployment**: `frontend` (montează `nginx.conf` peste config default)
- **Service**: `frontend` (NodePort: `30080`)

---

## 4. Fișiere YAML incluse

- `00-namespace.yaml`
- `10-db-secret.yaml`
- `11-db-pvc.yaml`
- `12-db-deployment.yaml`
- `13-db-service.yaml`
- `20-backend-configmap.yaml`
- `21-backend-deployment.yaml`
- `22-backend-service.yaml`
- `30-frontend-configmap-nginx.yaml`
- `31-frontend-configmap-html.yaml`
- `32-frontend-deployment.yaml`
- `33-frontend-service-nodeport.yaml`
- `40-db-seed-job.yaml` (opțional: creează tabelă de test și date)

---

## 5. Instalare StorageClass (pentru PVC) – local-path-provisioner
Pentru laborator, s-a instalat Rancher Local Path Provisioner, iar `local-path` este StorageClass default.

Verificare:
kubectl get storageclass
kubectl -n local-path-storage get pods
kubectl -n three-tier get pvc

6. Deploy aplicație
6.1 Aplicare manifests
Din directorul proiectului:
kubectl apply -f .

6.2 Verificare resurse
kubectl -n three-tier get pods -o wide
kubectl -n three-tier get svc
kubectl -n three-tier get pvc

7. Testare aplicație
7.1 Acces extern (NodePort)
Aplicația este disponibilă pe:

http://<IP-ORICARUI-NOD-WORKER>:30080/ (frontend)

http://<IP-ORICARUI-NOD-WORKER>:30080/api/ (backend via proxy)

Exemplu:
curl -i http://192.168.X.Y:30080/
curl -i http://192.168.X.Y:30080/api/

7.2 Seed DB (opțional, recomandat)
Rulează jobul de seed:
kubectl apply -f 40-db-seed-job.yaml
kubectl -n three-tier logs job/db-seed

Apoi testează:
curl -i http://<IP-NOD>:30080/api/cats

8. Debug rapid
Poduri:
kubectl -n three-tier get pods
kubectl -n three-tier describe pod <pod>
kubectl -n three-tier logs <pod>

Evenimente:
kubectl -n three-tier get events --sort-by=.lastTimestamp

9. Curățare (uninstall)
kubectl delete namespace three-tier

