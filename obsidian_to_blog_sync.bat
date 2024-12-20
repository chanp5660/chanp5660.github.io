@echo off
call C:\Users\user\anaconda3\Scripts\activate.bat chanp5660
python obsidian_to_blog_sync.py

REM Git 명령어 실행
git add .
git commit -m "Add Blog Post"
git push origin

pause