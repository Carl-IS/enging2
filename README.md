# Challenger Selection Engine

Engine 2 is a separated FastAPI backend and Vite React frontend. No Engine 1 or Engine 3 is included.

## Backend

```powershell
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Route: `POST http://localhost:8000/recommend`

Allowed challenger regions for 3ISA: `Hoenn`, `Sinnoh`, `Galar`.

The Challenger Selection Engine provides two selection modes. Balanced Counter Mode recommends a safer lineup by considering type advantage, resistance, bulk, and team diversity. Fast-Win Race Mode is designed for race-style battles where quick victories are prioritized, so it gives higher weight to speed, offensive stats, STAB, and super-effective coverage.

Both modes still filter by native region and battle restrictions before scoring.

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

The temporary React interface only collects inputs, sends `selection_mode` as `balanced` or `fast_win`, calls the backend, and displays the returned recommended team table.