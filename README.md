# Analyzer
Consists of:
main.py - code of the script
rules.json - rules for the script where to find the HTML elements

How to run the program:

parser.exe FIRST_ARGUMENT SECOND_ARGUMENT THIRD_ARGUMENT FOURTH_ARGUMENT

parser.exe - exe file of the script
FIRST_ARGUMENT - 1 or 0. 1 - writing to console; 0 - writing to file
SECOND_ARGUMENT - path to file "rules.json"
THIRD_ARGUMENT - path to html file from what the script should get info
FOURTH_ARGUMENT - path to result file where the script should write all the info in json format

Guide to rules.json:

"name_of_variable":{"id":[""],"class":[""],"variable":[""],"tag":[""],"recursive":[""]}
- All the lists should be equal length (if no info - write "")
- recursive: if "False" -> when the script doesn't find the element with id[n],class[n],variable[n],tag[n] it switches to n+1, when the script finds the element it stops searching. If "True" -> when the script finds id[n],class[n],variable[n],tag[n] it goes deeper into DOM three and searches for id[n+1],class[n+1],variable[n+1],tag[n+1]
