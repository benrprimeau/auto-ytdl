@set /p Start=<autonumberStart.txt
@set /p urls=<urls.txt
@set /p folder=<folder.txt
@set /p after=<dateAfter.txt
@set /p url=<urls.txt
@set /p reverse=<reverse.txt

rem echo %Start%
youtube-dl -ciw -o "D:/Movies/Youtube Series/%folder%/S01E%%(autonumber)03d - %%(title)s [%%(id)s].%%(ext)s" -f "bestvideo[height<=1100]+bestaudio" --merge-output-format mkv --autonumber-start %Start% %reverse% --dateafter %after% %url%
rem @youtube-dl -ciw -o "Z:/Movies/Youtube Series/%folder%/S01E%%(autonumber)03d - %%(title)s [%%(id)s].%%(ext)s" -f "247+251" --merge-output-format mkv --autonumber-start %Start% %reverse% --dateafter %after% %url%