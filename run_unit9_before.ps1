# Unit 9 capstone BEFORE run.
# Run from this repository after committing your five Unit 9 criteria.
# Close any previously running python app.py process first.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Missing .venv. Install dependencies from requirements.txt first."
}
if (-not (Test-Path "criteria.md")) {
    throw "Missing criteria.md. Write and commit your own Unit 9 criteria before testing."
}
$expected = "## 1. Logging completeness"
if (-not (Select-String -LiteralPath "criteria.md" -Pattern $expected -SimpleMatch -Quiet)) {
    throw "The Unit 9 criteria are missing. Pull the newest repo and commit your criteria."
}
New-Item -ItemType Directory -Path "results" -Force | Out-Null

Write-Host "Checking Python source..." -ForegroundColor Cyan
& $python -m py_compile app.py audit.py config.py request_telemetry.py log_rotation.py capstone_eval.py test_capstone_rotation.py
if ($LASTEXITCODE -ne 0) { throw "Python syntax check failed." }

Write-Host "Checking 1 MiB rotation with isolated regression tests..." -ForegroundColor Cyan
& $python -m unittest -v test_capstone_rotation.py
if ($LASTEXITCODE -ne 0) { throw "Rotation tests failed. Do not record baseline evidence as successful." }

Write-Host "Running the five capstone criteria three times (BEFORE)..." -ForegroundColor Cyan
& $python capstone_eval.py --label before
if ($LASTEXITCODE -ne 0) {
    throw "Capstone evaluation did not finish. Check results\capstone_server_before.txt for the server error."
}

Write-Host "Recording the exact package versions in this environment..." -ForegroundColor Cyan
& $python -m pip freeze | Set-Content -Path "requirements-lock.txt" -Encoding UTF8
if ($LASTEXITCODE -ne 0) { throw "Could not record the installed package versions." }

Write-Host "Saving real BEFORE evidence to GitHub..." -ForegroundColor Cyan
& git add -- results/ logs/ requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw "Git staging failed. Evidence is still saved locally." }
& git diff --cached --quiet -- results/ logs/ requirements-lock.txt
if ($LASTEXITCODE -eq 1) {
    & git commit -m "Record Unit 9 before-run evidence" -- results/ logs/ requirements-lock.txt
    if ($LASTEXITCODE -ne 0) { throw "Git commit failed. Evidence is still saved locally." }
    & git push
    if ($LASTEXITCODE -ne 0) { throw "Git push failed. Commit exists locally. Run git push yourself." }
} elseif ($LASTEXITCODE -ne 0) {
    throw "Could not check staged evidence."
}

Write-Host "BEFORE complete. Stop here. Review the results before making exactly one improvement." -ForegroundColor Green
