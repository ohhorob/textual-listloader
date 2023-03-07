# textual-listloader
Textual ListView loader

Goals: 

 - ❓ Push the Main screen and show (indeterminate) progress while values are fetched. 
 - ❓ Display list of values after they are fetched
 - ✅ Update list of values as user adds/removes

Approach:

Use a Screen
 * compose a layout
 * implement mutation actions (load/add/remove)

Extend a ListView
 * reacts to changes in a value set

Looking for a solution–

_How to aynchronously trigger a load of the value set?_

