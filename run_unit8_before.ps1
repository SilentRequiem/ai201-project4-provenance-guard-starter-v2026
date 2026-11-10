# Run from this repo in PowerShell: .\run_unit8_before.ps1
# This runs the actual Unit 8 BEFORE measurements and saves the evidence.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Missing .venv. Create it and install requirements.txt first."
}
New-Item -ItemType Directory -Path "results" -Force | Out-Null
& $python -m py_compile app.py audit.py config.py detector.py scoring.py stylometry.py scenarios.py run_eval.py run_attacks.py
if ($LASTEXITCODE -ne 0) { throw "Python syntax check failed." }

$attackFile = Get-ChildItem -Path $PSScriptRoot -Filter "attacks.csv" -File -Recurse | Select-Object -First 1
if (-not $attackFile) {
    $zip = Join-Path $PSScriptRoot "attack_set.zip"
    if (-not (Test-Path $zip)) {
        Write-Host "Downloading the staff attack set..."
        $url = "https://courses.codepath.org/course_files/ai201/fa26-29627bd0/attack_set.zip"
        try {
            Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
        } catch {
            throw "Download failed. Download attack_set.zip from Unit 8 in the course portal and put it in this repo."
        }
    }
    Expand-Archive -Path $zip -DestinationPath (Join-Path $PSScriptRoot "attack_set") -Force
    $attackFile = Get-ChildItem -Path (Join-Path $PSScriptRoot "attack_set") -Filter "attacks.csv" -File -Recurse | Select-Object -First 1
}
if (-not $attackFile) { throw "No attacks.csv found in the staff attack set." }
$folder = $attackFile.DirectoryName
Write-Host "Located staff attack set. Running it in full without previewing it."

$base = "http://127.0.0.1:5000"
$server = $null
$env:AI201_DEBUG = "0"
$health = $null
try {
    try {
        $health = Invoke-RestMethod -Uri "$base/health" -TimeoutSec 3
    } catch {
        Write-Host "Starting local service..."
        $server = Start-Process -FilePath $python -ArgumentList "app.py" -WorkingDirectory $PSScriptRoot -PassThru -RedirectStandardOutput "results\unit8_server_out.txt" -RedirectStandardError "results\unit8_server_err.txt"
        for ($attempt = 1; $attempt -le 20; $attempt++) {
            Start-Sleep -Seconds 1
            try {
                $health = Invoke-RestMethod -Uri "$base/health" -TimeoutSec 2
                break
            } catch {}
        }
    }
    if (-not $health) { throw "Service did not start. See results\unit8_server_err.txt." }
    if (-not $health.rate_limiting) {
        throw "Rate limiting is OFF in your running server. Stop any old app.py process, pull changes, then rerun."
    }

    Write-Host "Flood test..."
    & $python run_attacks.py --flood 15
    if ($LASTEXITCODE -ne 0) { throw "Flood test failed." }

    Write-Host "Full staff attack set (BEFORE)..."
    & $python run_attacks.py --set $folder --label before
    if ($LASTEXITCODE -ne 0) { throw "Attack run failed." }

    Write-Host "Five criteria, three trials each (BEFORE)..."
    & $python run_eval.py --label before
    if ($LASTEXITCODE -ne 0) { throw "Evaluation failed." }

    $log = Invoke-RestMethod -Uri "$base/log" -TimeoutSec 10
    $log | ConvertTo-Json -Depth 10 | Set-Content -Path "results\audit_before.json" -Encoding UTF8

    Write-Host "BEFORE run complete. Review results/ and logs/audit.jsonl before changing any scores or thresholds." -ForegroundColor Green
} finally {
    if ($server) { Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue }
}
