@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "SKIP_INSTALL="
set "SKIP_TESTS="
set "SKIP_TRAINING="
set "SKIP_EVALUATION="
set "SKIP_EXPORT="
set "NO_SERVERS="
set "RUN_ID=%RANDOM%%RANDOM%%RANDOM%"
set "WORK_TMP=%CD%\.tmp"
set "PYTEST_TEMP=%WORK_TMP%\pytest-%RUN_ID%"
set "PYTEST_CACHE=%WORK_TMP%\.pytest_cache-%RUN_ID%"

:parse_args
if "%~1"=="" goto args_done
if /I "%~1"=="--skip-install" set "SKIP_INSTALL=1"
if /I "%~1"=="--skip-tests" set "SKIP_TESTS=1"
if /I "%~1"=="--skip-training" set "SKIP_TRAINING=1"
if /I "%~1"=="--skip-evaluation" set "SKIP_EVALUATION=1"
if /I "%~1"=="--skip-export" set "SKIP_EXPORT=1"
if /I "%~1"=="--no-servers" set "NO_SERVERS=1"
shift
goto parse_args

:args_done
echo.
echo DermaVision AI Full Pipeline
echo ============================
echo Root: %CD%
echo.

if not exist "%WORK_TMP%" mkdir "%WORK_TMP%"
set "TMP=%WORK_TMP%"
set "TEMP=%WORK_TMP%"
set "MLFLOW_ALLOW_FILE_STORE=true"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found on PATH.
  exit /b 1
)

if not exist ".env" (
  echo [INFO] Creating .env from .env.example
  copy /Y ".env.example" ".env" >nul
) else (
  echo [INFO] Using existing .env
)

if not defined SKIP_INSTALL (
  echo.
  echo [STEP] Installing Poetry if needed
  python -m pip install poetry
  if errorlevel 1 exit /b 1

  echo.
  echo [STEP] Installing backend and ML dependencies
  python -m poetry install --no-interaction
  if errorlevel 1 exit /b 1

  echo.
  echo [STEP] Installing frontend dependencies
  pushd frontend
  call npm.cmd install
  if errorlevel 1 (
    popd
    exit /b 1
  )
  popd
) else (
  echo [INFO] Skipping dependency installation
)

if not defined SKIP_TESTS (
  echo.
  echo [STEP] Running backend tests
  python -m poetry run pytest tests -q -p no:cacheprovider --basetemp="%PYTEST_TEMP%"
  if errorlevel 1 exit /b 1
) else (
  echo [INFO] Skipping tests
)

if not defined SKIP_TRAINING (
  echo.
  echo [STEP] Training the model
  python -m poetry run dermavision-train
  if errorlevel 1 exit /b 1
) else (
  echo [INFO] Skipping training
)

if not defined SKIP_EVALUATION (
  echo.
  echo [STEP] Evaluating the model
  python -m poetry run dermavision-evaluate
  if errorlevel 1 exit /b 1
) else (
  echo [INFO] Skipping evaluation
)

if not defined SKIP_EXPORT (
  echo.
  echo [STEP] Exporting TorchScript and ONNX models
  python -m poetry run dermavision-export
  if errorlevel 1 exit /b 1
) else (
  echo [INFO] Skipping model export
)

if not defined NO_SERVERS (
  echo.
  echo [STEP] Starting backend and frontend in new terminal windows
  start "DermaVision API" cmd /k "cd /d "%~dp0" && python -m poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000"
  start "DermaVision Frontend" cmd /k "cd /d "%~dp0frontend" && npm.cmd run dev"
  echo.
  echo [READY] Backend:  http://localhost:8000
  echo [READY] Swagger:  http://localhost:8000/docs
  echo [READY] Frontend: http://localhost:5173
) else (
  echo.
  echo [INFO] Pipeline finished without starting servers
)

echo.
echo Done.
exit /b 0
