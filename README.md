# VMS + QuickTalk Monorepo

Merged Visitor Management System (VMS) with:
- **QuickTalk PTT-IP** (push-to-talk over IP, GPS, photo/video upload stubs)
- **LoRa Mesh** voice-message store‑and‑forward (20s cap) with priority queue stubs

## Quick start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

Services:
- FastAPI backend: http://localhost:8000/docs
- Postgres: localhost:5432
- Redis: localhost:6379
- MinIO (S3-compatible): http://localhost:9001 (console), http://localhost:9000 (API)
  - Access key/secret from `.env`

## Repo layout

```
apps/
  backend/            # FastAPI + SQLAlchemy + Alembic-ready
  worker/             # Background jobs (RQ) for media/process queues
services/
  ptt_ip/             # PTT over IP server-side stubs
  lora_mesh/          # LoRa mesh queueing/priority logic (store & forward)
packages/
  shared/python/      # Reusable Python utilities (config, logging, schemas)
infra/
  docker-compose.yml
  alembic/            # Placeholder for migrations
data/
  uploads/            # Local dev storage for media (or MinIO bucket)
```

---

### Notes

- Guards can **capture photos** and **GPS**; backend exposes `/media/upload` and `/ptt/message` endpoints.
- LoRa path uses **20s max voice clips** and **priority queue** (`HIGH`, `NORMAL`, `LOW`). Worker simulates store‑and‑forward.
- Admin controls to suspend/resume a society and billing scaffolds included.
- Keep Flutter/React clients as separate repos for now; API is stable.
