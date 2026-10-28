@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================================
echo    ZIRO-HISTORY-STUDIO-V3 - KIEM TRA CAU HINH MAY LAN DAU (ONBOARDING)
echo    Danh cho Nguoi Nhan Ban Giao Skill tren may tinh moi
echo ============================================================================
echo.

if not exist "node_modules\playwright" (
    echo [1/3] Dang cai dat thu vien Node.js va trinh duyet Playwright cuc bo...
    call npm install
    call npx playwright install chromium
) else (
    echo [1/3] Da san sang thu vien Playwright cuc bo trong node_modules\.
)

echo.
echo [2/3] Dang kiem tra thu vien Python (numpy, Pillow, faster-whisper)...
python -c "import numpy, PIL; print('[PASS] Da co san numpy va Pillow.')" 2>nul
if errorlevel 1 (
    echo [CAI DAT] Dang cai numpy va Pillow...
    pip install numpy Pillow
)
python -c "import faster_whisper; print('[PASS] Da co san faster-whisper (Cat am thanh chinh xac tung chu).')" 2>nul
if errorlevel 1 (
    echo [TUY CHON] Chua co faster-whisper. Dang cai dat de ho tro cat am thanh chinh xac cao nhat...
    pip install faster-whisper
)

echo.
echo [3/3] Dang chay Kiem dinh Suc khoe Phao dai (Preflight Check)...
python engine\preflight.py

echo.
echo ============================================================================
echo Neu tat ca bao [PASS], may tinh cua ban da san sang 100%%!
echo Hay mo file HUONG_DAN_VAN_HANH_30_PHUT.md de bat dau lam tap phim dau tien.
echo ============================================================================
pause
