# mainSplitGold

This python script take as parameter a Livesplit file (.lss) and extract your best times for each full segment (which can contains several subsplits).
Displays each main split PB, and the corresponding SOB.
Save the times in "MainSplitGold.txt"

Launch from your favorite python environment with the command:

python mainSplitGold.py "filePath"


Warning:
Will probably not work if several splits avec the same name.
If a main segment has never been finished and does not have a full time, the scripr will use 0 as best time. 