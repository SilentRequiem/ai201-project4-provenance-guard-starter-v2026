# After-run script. Run only after the initial before results and the one validation change.
# Run from this repo in PowerShell: .\run_unit8_after.ps1
# This runs the actual Unit 8 AFTER measurements and saves the evidence.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Missing .venv. Create it and install requirements.txt first."
}
New-Item -ItemType Directory -Path "results" -Force | Out-Null
& $python -m py_compile app.py audit.py config.py detector.py scoring.py stylometry.py scenarios.py run_eval.py run_attacks.py
if ($LASTEXITCODE -ne 0) { throw "Python syntax check failed." }

# A course-site download can return an HTML page instead of a ZIP.
# Check the contents before trying to extract it.
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Test-AttackZip([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    $archive = $null
    try {
        $archive = [System.IO.Compression.ZipFile]::OpenRead($Path)
        $names = @($archive.Entries | ForEach-Object { $_.FullName.Replace('\', '/') })
        $hasText = @($names | Where-Object { $_ -match '(^|/)attacks\.csv$' }).Count -gt 0
        $hasMalformed = @($names | Where-Object { $_ -match '(^|/)attacks_malformed_requests\.csv$' }).Count -gt 0
        return ($hasText -and $hasMalformed)
    } catch {
        return $false
    } finally {
        if ($null -ne $archive) { $archive.Dispose() }
    }
}

$attackFile = Get-ChildItem -Path $PSScriptRoot -Filter "attacks.csv" -File -Recurse |
    Where-Object { $_.FullName -notmatch '[\\/]\.venv[\\/]' } | Select-Object -First 1

if (-not $attackFile) {
    $zip = Join-Path $PSScriptRoot "attack_set.zip"

    if ((Test-Path -LiteralPath $zip) -and -not (Test-AttackZip $zip)) {
        Write-Host "Removing the invalid attack_set.zip from the earlier download." -ForegroundColor Yellow
        Remove-Item -LiteralPath $zip -Force
    }

    # Copy an authenticated browser download automatically when available.
    if (-not (Test-AttackZip $zip)) {
        $downloads = Join-Path $HOME "Downloads"
        if (Test-Path $downloads) {
            $candidates = Get-ChildItem $downloads -Filter "*attack_set*.zip" -File |
                Sort-Object LastWriteTime -Descending
            foreach ($candidate in $candidates) {
                if (Test-AttackZip $candidate.FullName) {
                    Copy-Item -LiteralPath $candidate.FullName -Destination $zip -Force
                    Write-Host "Using valid staff ZIP from Downloads: $($candidate.Name)" -ForegroundColor Green
                    break
                }
            }
        }
    }

    if (-not (Test-AttackZip $zip)) {
        $url = "https://courses.codepath.org/course_files/ai201/fa26-29627bd0/attack_set.zip"
        $tempZip = Join-Path $PSScriptRoot "attack_set_download.tmp"
        Write-Host "Trying the course link once..." -ForegroundColor Cyan
        try {
            Invoke-WebRequest -Uri $url -OutFile $tempZip -UseBasicParsing -ErrorAction Stop
            if (Test-AttackZip $tempZip) {
                Move-Item -LiteralPath $tempZip -Destination $zip -Force
            }
        } catch {
            Write-Host "Direct course download was unavailable." -ForegroundColor Yellow
        } finally {
            if (Test-Path -LiteralPath $tempZip) {
                Remove-Item -LiteralPath $tempZip -Force
            }
        }
    }

    if (-not (Test-AttackZip $zip)) {
        throw "The course link did not provide a valid ZIP. Sign in to CodePath in your browser, download attack_set.zip from Unit 8, and leave it in Downloads (or this repo). Then rerun this script. Do not extract it yourself."
    }

    Expand-Archive -LiteralPath $zip -DestinationPath (Join-Path $PSScriptRoot "attack_set") -Force
    $attackFile = Get-ChildItem -Path (Join-Path $PSScriptRoot "attack_set") -Filter "attacks.csv" -File -Recurse |
        Select-Object -First 1
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

    Write-Host "Full staff attack set (AFTER)..."
    & $python run_attacks.py --set $folder --label after
    if ($LASTEXITCODE -ne 0) { throw "Attack run failed." }

    Write-Host "Five criteria, three trials each (AFTER)..."
    & $python run_eval.py --label after
    if ($LASTEXITCODE -ne 0) { throw "Evaluation failed." }

    $log = Invoke-RestMethod -Uri "$base/log" -TimeoutSec 10
    $log | ConvertTo-Json -Depth 10 | Set-Content -Path "results\audit_after.json" -Encoding UTF8

    Write-Host "AFTER run complete. Saving evidence to GitHub..." -ForegroundColor Green
    & git add -- results/ logs/audit.jsonl
    if ($LASTEXITCODE -ne 0) { throw "Git staging failed. Reports are saved locally." }
    & git diff --cached --quiet -- results/ logs/audit.jsonl
    if ($LASTEXITCODE -eq 1) {
        & git commit -m "Record Unit 8 after-run evidence" -- results/ logs/audit.jsonl
        if ($LASTEXITCODE -ne 0) { throw "Git commit failed. Reports are saved locally." }
        & git push
        if ($LASTEXITCODE -ne 0) { throw "Git push failed. Commit exists locally. Run git push manually." }
    }
    Write-Host "After-run evidence saved to GitHub. Do not change another system setting." -ForegroundColor Green
} finally {
    if ($server) { Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue }
}
