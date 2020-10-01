@set /p Start=<autonumberStart.txt
@set /p urls=<urls.txt
@set /p folder=<folder.txt
@rem echo %Start%
@rem echo %urls%
@youtube-dl -ciw -o "D:/Movies/Youtube Series/%folder%/S01E%%(autonumber)03d - %%(title)s [%%(id)s].%%(ext)s" -f "bestvideo[height<=1100]+bestaudio" --merge-output-format mkv --autonumber-start %Start% --batch-file urls.txt
rem @youtube-dl -ciw -o "Z:/Movies/Youtube Series/%folder%/S01E%%(autonumber)03d - %%(title)s [%%(id)s].%%(ext)s" -f "247+251" --merge-output-format mkv --autonumber-start %Start% --batch-file urls.txt