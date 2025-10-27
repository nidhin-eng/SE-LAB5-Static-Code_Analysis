| **Issue** | **Type** | **Line(s)** | **Description** | **Fix Approach** |
| --- | --- | --- | --- | --- |
| **Use of `eval`** | Security / Bug | 59 | `eval()` is used (Bandit: B307, Pylint: W0123), which can execute arbitrary code and is a major security risk. | Remove the `eval()` call. If evaluating data from a trusted string is necessary, use the safer `ast.literal_eval`. |
| **Dangerous Default Value** | Bug | 8 | The `addItem` function uses a mutable default argument `logs=[]` (Pylint: W0102). This list will be shared across all calls to the function. | Change the default to `None` and initialize `logs = []` inside the function if `logs is None`. |
| **Bare Except / Pass** | Bug / Refactor | 19 | A bare `except:` (Flake8: E722, Pylint: W0702) is used, which catches all exceptions, including system-level ones, and silences them with `pass` (Bandit: B110). | Specify the exact exception(s) to catch (e.g., `except KeyError:`) and log the error or handle it appropriately instead of using `pass`. |
| **Unsafe File Handling** | Refactor / Bug | 26, 32 | `open()` is used without a `with` statement (Pylint: R1732), risking resource leaks. It also lacks an explicit `encoding` (Pylint: W1514), which can cause cross-platform bugs. | Refactor `loadData` and `saveData` to use a `with open(..., encoding="utf-8") as f:` block. |
| **Use of Global Statement** | Refactor | 27 | `loadData` modifies the global `stock_data` variable (Pylint: W0603). This makes the code hard to test and maintain. | Refactor `loadData` to return the data, and have the main script assign it to `stock_data`. (e.g., `stock_data = loadData()`). |
| **Unused Import** | Style / Cleanup | 2 | The `logging` module is imported (Flake8: F401, Pylint: W0611) but is never used in the file. | Remove the `import logging` line to clean up the code. |
| **Naming Convention** | Convention | 8, 14, 22, 25, 31, 36, 41 | Function names use `camelCase` (e.g., `addItem`, `loadData`) instead of the PEP 8 standard `snake_case` (Pylint: C0103). | Rename functions to use snake_case (e.g., `add_item`, `load_data`) and update all places where they are called. |
| **Missing Docstrings** | Convention | 1, 8, 14, 22, 25, 31, 36, 41, 48 | The module (C0114) and all functions (C0116) are missing docstrings, making the code difficult to understand for others. | Add descriptive docstrings to the module and each function explaining what they do, their arguments, and what they return. |
| **PEP 8 Whitespace** | Style | Various | There are multiple violations of PEP 8 whitespace rules, primarily "expected 2 blank lines" (Flake8: E302, E305). | Run an auto-formatter like `black` or `ruff format` over the file, or manually add the required blank lines between functions. |
1. Which issues were the easiest to fix, and which were the hardest? Why?
Easiest: The whitespace errors (C0303 trailing-whitespace and C0304 final-newline-missing) were by far the easiest. They were purely mechanical text edits (deleting a space or adding a newline) that didn't require any logical thinking or code restructuring.

Hardest: The slightly harder part was going through all the logging statements and making sure they were consistent everywhere. It wasn’t technically difficult, but it required paying close attention to detail across the entire script to avoid missing any instances.
 The W0603: Using the global statement was the most complex fix. It wasn't just a single-line change; it required refactoring the data flow of the entire program. I had to change load_data to return the data instead of modifying a global variable, and then update the main function (and potentially other functions) to pass the stock_data dictionary around as an argument. This is a much deeper change to the code's design.

2. Did the static analysis tools report any false positives? If so, describe one example.

No, there weren’t any false positives. All the issues reported by pylint and flake8 were valid. The “missing final newline” warning appeared at first, but that was just my mistake — I hadn’t actually pressed Enter at the very end of the file. Once I corrected that, the warning disappeared, confirming that the tools were accurate.

3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate tools like pylint and flake8 both locally and in the development pipeline.
On my local setup, I’d enable them to run automatically before each commit using pre-commit hooks, so basic style and logic issues get caught early.

For team projects, I’d include them in the CI/CD pipeline (for example, through GitHub Actions or Jenkins), so every pull request is automatically checked before merging. Having these tools also integrated in the IDE (like VS Code) helps get instant feedback while coding, which saves a lot of debugging time later.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

After applying the fixes, the code became cleaner, easier to read, and more consistent.
Using lazy logging made the code more efficient, and fixing minor style issues made it look more professional. The structure feels better organized, and it’s simpler to maintain or extend in the future.

Overall, the script now follows Python’s best practices, passes all static checks with a perfect pylint score (10/10), and gives more confidence that it’s reliable and ready for real use.