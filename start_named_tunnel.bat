@echo off
TITLE SchemeSaathi Cloudflare Named Tunnel Auto-Service
echo ========================================================
echo SchemeSaathi Cloudflare Production Named Tunnel
echo ========================================================
cd /d "%~dp0"

IF "%1"=="" (
    echo Starting tunnel using config.yml or token...
    IF EXIST "%USERPROFILE%\.cloudflared\config.yml" (
        cloudflared.exe tunnel run
    ) ELSE (
        echo [INFO] To run with a tunnel token:
        echo   start_named_tunnel.bat <YOUR_CLOUDFLARE_TUNNEL_TOKEN>
        echo.
        echo [INFO] Or create a named tunnel:
        echo   cloudflared.exe tunnel login
        echo   cloudflared.exe tunnel create schemesaathi
        echo   cloudflared.exe tunnel route dns schemesaathi app.schemesaathi.in
        echo   cloudflared.exe tunnel run schemesaathi
    )
) ELSE (
    echo Running tunnel with provided token...
    cloudflared.exe tunnel run --token %1
)
pause
