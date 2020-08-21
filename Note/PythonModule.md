# Python Module

* [python - Relative imports - ModuleNotFoundError: No module named x - Stack Overflow](https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x)

> if you're sticking with Python 3 there is no more need in `__init__.py` files

* [Python Package Structure: Dead Simple Python: Project Structure and Imports - DEV](https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6#:~:text=Organize%20your%20modules%20into%20packages,root%20of%20your%20project's%20repository.)
  * [5. The import system — Python 3.8.5 documentation](https://docs.python.org/3/reference/import.html)

## Special Import

### Git Submodule

* [How to import python file from git submodule - Stack Overflow](https://stackoverflow.com/questions/29746958/how-to-import-python-file-from-git-submodule)
* [Using git submodule to import a python project - Stack Overflow](https://stackoverflow.com/questions/15668804/using-git-submodule-to-import-a-python-project/15676423)

### Soft Link

* [Python: import symbolic link of a folder - Stack Overflow](https://stackoverflow.com/questions/8749108/python-import-symbolic-link-of-a-folder)

## Making a Python Project

* [Structuring Your Project — The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
* [Using Git Submodule and Develop Mode to Manage Python Projects - Shun's Vineyard](https://shunsvineyard.info/2019/12/23/using-git-submodule-and-develop-mode-to-manage-python-projects/)

## Dealing with formatting problem

Sometimes the code like this, the formatter will force the `from mining.tfidf import TFIDF` to the top of the file, which will make our `sys.path.append` fail.

```py
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(curr_dir, '..'))

from mining.tfidf import TFIDF
```

Disable import sorting in VSCode

* [visual studio code - Disable python import sorting in VSCode - Stack Overflow](https://stackoverflow.com/questions/54015604/disable-python-import-sorting-in-vscode/54016555)
  * because I might need to import modules after append the path
  * **Add `"python.formatting.autopep8Args": ["--ignore", "E402"]` in `settings.json` of VSCode**
