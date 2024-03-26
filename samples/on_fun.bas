PRINT "Enter a number between 1 and 3:"
INPUT x

ON x GOTO 100, 200, 300
GOTO 400

100 REM Code block for x = 1
    PRINT "You entered 1"
    GOTO 400

200 REM Code block for x = 2
    PRINT "You entered 2"
    GOTO 400

300 REM Code block for x = 3
    PRINT "You entered 3"
    GOTO 400

400 REM Code after the branching logic
    PRINT "Program execution continues..."