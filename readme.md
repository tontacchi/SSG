# Sitegeist

A static site generator for converting markdown files into HTML.

### Requirements

Python 3 >= 3.4

### Usage

1. `git clone https://github.com/tontacchi/SSG/` or use your favorite method for obtaining a copy of the codebase.
2. run the `main.sh` bash script.
  - This automatically converts the markdown files into HTML and starts a python `http.server` at `http://localhost:8888/`.
3. Navigate to the page & have fun! Contact me if there are any issues with running the script or viewing the site pages generated.

In the event you are unable to start the application:
1. navigate to `SSG/src/`
2. run `python3 main.py`
3. navigate to `SSG/public/`
4. run `python3 -m http.server 8888`
