@ECHO OFF

REM init env locally

CD %~dp0
SET WORK=%CD%

SET PYTHONPATH=%WORK%\mindformers

ECHO WORK=%WORK%
ECHO PYTHONPATH=%PYTHONPATH%

CMD /K conda activate llm
