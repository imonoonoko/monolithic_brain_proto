@echo off
echo --- CortexAI Setup ---
echo.
echo [1/2] Creating directories...
if not exist "models" mkdir models

echo.
echo [2/2] Downloading Model (Qwen2.5-1.5B-Instruct)...
echo This may take a few minutes (approx. 1GB)...
echo.

powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf?download=true' -OutFile 'models\qwen-1.5b.gguf'"

if exist "models\qwen-1.5b.gguf" (
    echo.
    echo [SUCCESS] Model downloaded successfully!
    echo You can now run Cortex.exe
) else (
    echo.
    echo [ERROR] Download failed. Please download manually from:
    echo https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
    echo and save it to models\qwen-1.5b.gguf
)

echo.
pause
