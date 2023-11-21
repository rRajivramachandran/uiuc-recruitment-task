### System requirements:
- Python 3.11 should be installed
- Libraries for json, datetime and sys are part of the standard python installation so no need to install them
### Steps to run
1. `git clone https://github.com/rRajivramachandran/uiuc-recruitment-task.git`
2. `cd uiuc-recruitment-task`
3. Copy any new "trainings.txt" file to this folder with the same name or use the default one
4. `python3 application.py`. This will generate the three output files 
5. If you want to verify changing the parameters, go to `application.py` file and within `__name__ == "__main__"` the following are configurable:
    - file_path: Input JSON path
    - trainings_list: list used for task 2 to generate "completed_fiscal_year.json"
    - fiscal_year: used for task 2
    - date_string: used for task 3 to generate "expired_trainings.json"
