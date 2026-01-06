@echo off
echo --- Building CortexAI (Cortex.exe) ---

rmdir /s /q dist
rmdir /s /q build
del /q *.spec

echo [0/3] locating dependencies...
for /f "delims=" %%i in ('python find_llama_dll.py') do set LLAMA_LIB=%%i
echo Found llama_cpp lib at: %LLAMA_LIB%

echo [1/3] Running PyInstaller...
pyinstaller --noconfirm --onedir --console --name "Cortex" ^
    --add-data "src;src" ^
    --add-data "%LLAMA_LIB%;llama_cpp/lib" ^
    --exclude-module torch ^
    --exclude-module pandas ^
    --exclude-module sklearn ^
    --exclude-module scipy ^
    --exclude-module matplotlib ^
    --exclude-module cv2 ^
    --exclude-module skimage ^
    --exclude-module PIL ^
    --hidden-import="uvicorn.logging" ^
    --hidden-import="uvicorn.loops" ^
    --hidden-import="uvicorn.loops.auto" ^
    --hidden-import="uvicorn.protocols" ^
    --hidden-import="uvicorn.protocols.http" ^
    --hidden-import="uvicorn.protocols.http.auto" ^
    --hidden-import="uvicorn.protocols.websockets" ^
    --hidden-import="uvicorn.protocols.websockets.auto" ^
    --hidden-import="uvicorn.lifespan.on" ^
    src/server.py

echo [2/3] Organizing Folders...
REM Rename default output 'Cortex' to 'CortexAI' to match desired root
if exist dist\CortexAI rmdir /s /q dist\CortexAI
move dist\Cortex dist\CortexAI

mkdir dist\CortexAI\models
mkdir dist\CortexAI\memories
mkdir dist\CortexAI\examples

echo [3/3] Copying Resources...
if exist qwen2.5-1.5b-instruct-q4_k_m.gguf (
    copy qwen2.5-1.5b-instruct-q4_k_m.gguf dist\CortexAI\models\qwen-1.5b.gguf
) else (
    echo WARNING: Model file not found, please copy manually to models/
)

echo.
echo --- Build Complete! ---
echo Output: dist\CortexAI\
pause
