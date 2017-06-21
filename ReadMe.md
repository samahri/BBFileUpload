# How to Setup and Launch *Refrigerator Delivery Path Dimension Calculator* Web Application Prototype:
1. Download the source code from this repository;
2. Install all dependencies located in "Requirements.txt" (see below on how to properly install Django without using *virtualenv*);
3. Using a terminal emulator interface (e.g. Terminal app on MacOS), navigate to the project's root directory;
4. Type `$ python manage.py migrate` to set the database;
5. Type `$ python manage.py check` to ensure that the program compiles error free;
6. Type `$ python manage.py runserver` to launch the development server;
7. Using your favorite web browser, type `127.0.0.1:8000` in the address bar to navigate to the application's homepage.

# Note: to install Django without *virtualenv*:
```
$ conda install -c anaconda django=1.10.5
```

# IMPORTANT!
Do not install OpenCV using pip; instead, use conda
```
conda install -c https://conda.binstar.org/menpo opencv
```
