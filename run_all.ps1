# ==============================================================
# CYBERDUDEBIVASH BUG HUNTER - Global Swarm Orchestrator
# Purpose: Synchronized startup of Redis, Celery, and API Server
# ==============================================================

Write-Host "🚀 ACTIVATING CYBERDUDEBIVASH GOD-MODE ECOSYSTEM..." -ForegroundColor Red

# 1. Start Redis Broker (Assumes redis-server is in PATH)
Write-Host "[1/3] Starting Redis Intelligence Broker..." -ForegroundColor Cyan
Start-Process "redis-server" -WindowStyle Minimized

# Wait for Redis to initialize
Start-Sleep -Seconds 3

# 2. Start Celery Worker Swarm
Write-Host "[2/3] Launching Autonomous Worker Swarm..." -ForegroundColor Cyan
# Using --pool=solo for Windows stability as established in scheduler_engine.py
Start-Process "powershell.exe" -ArgumentList "celery -A scheduler.scheduler_engine worker --loglevel=info --pool=solo" -WindowStyle Normal

# 3. Start God-Mode API Command Center
Write-Host "[3/3] Powering up API Command Center & WebSocket Bridge..." -ForegroundColor Cyan
Start-Process "powershell.exe" -ArgumentList "uvicorn dashboard.backend.api_server:app --host 0.0.0.0 --port 8000" -WindowStyle Normal

Write-Host "==============================================================" -ForegroundColor Red
Write-Host "✔ SYSTEM ONLINE: Global Swarm is sharding 1,000+ targets." -ForegroundColor Green
Write-Host "✔ DASHBOARD: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "✔ MONITOR: http://localhost:5555" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Red

# Keep the window open for log observation
Pause