@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================================
echo    ZIRO-HISTORY-STUDIO-V3 - CONG CU DONG GOI VA DON RAC CHO NGUOI DUNG
echo    (Chay truc tiep tren may - KHONG TON TOKEN AI!)
echo ============================================================================
echo.
echo Danh sach cac Tap phim hien co trong thu muc episodes\:
echo ----------------------------------------------------------------------------
for /d %%D in ("episodes\*") do (
    echo   - %%~nxD
)
echo ----------------------------------------------------------------------------
echo.
set /p EP="Nhap chinh xac Ma Tap phim (vi du: EP01_TrieuTien): "
if "%EP%"=="" goto :EOF

if not exist "episodes\%EP%" (
    echo [LOI] Khong tim thay thu muc episodes\%EP%!
    pause
    goto :EOF
)

echo.
echo Chon thao tac cho tap [%EP%]:
echo   [1] Gop tat ca cac cum .mp4 thanh 1 file Video Master dai 30 phut (mat ~3 giay)
echo   [2] Xoa sach bo nho tam .cache\%EP% (giai phong o cung truoc khi Cut sang Kho)
echo   [3] LAM CA HAI (Gop Master + Xoa sach .cache\%EP% de san sang mang di cat kho!)
echo.
set /p CHOICE="Nhap lua chon cua ban (1, 2 hoac 3): "

if "%CHOICE%"=="1" (
    python engine\concat_master.py --episode %EP%
)
if "%CHOICE%"=="2" (
    if exist ".cache\%EP%" (
        rmdir /s /q ".cache\%EP%"
        echo [HOAN TAT] Da don sach 100%% file tam trong .cache\%EP%!
    ) else (
        echo [THONG BAO] Khong co file tam nao trong .cache\%EP%.
    )
)
if "%CHOICE%"=="3" (
    python engine\concat_master.py --episode %EP%
    if exist ".cache\%EP%" (
        rmdir /s /q ".cache\%EP%"
        echo [HOAN TAT] Da gop Master MP4 va don sach 100%% .cache\%EP%!
    )
    echo.
    echo ==^> BAY GIO BAN CO THE MO THU MUC: episodes\%EP%
    echo ==^> KIEM TRA FILE: episodes\%EP%\4_output\master\%EP%_Master.mp4
    echo ==^> VA TU TAY CUT / PASTE CA THU MUC [episodes\%EP%] SANG KHO LUU TRU CUA BAN!
)

echo.
pause
