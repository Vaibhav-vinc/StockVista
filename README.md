# StockVista - Minor Project

This repository contains a Django project that includes installation of the TA-Lib (Technical Analysis Library) Python library using GitHub Actions. TA-Lib is used for performing technical analysis of financial markets.

## Requirements

-   Python 3.1x
-   Django
-   TA-Lib (v4.28) - Technical Analysis Library

## Installation

Follow these steps to set up the Django project and install TA-Lib using GitHub Actions:

### 1. Clone the Repository

```bash
git clone https://github.com/your_username/your_django_project.git
cd your_django_project
```

### 2. Install Dependencies Locally

Make sure you have Python and pip installed. Create and activate a virtual environment (optional but recommended) and install the required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Django

Apply migrations and create a superuser (if needed):

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Install TA-Lib using `ta-lib-bin` Package

TA-Lib can be installed easily using the `ta-lib-bin` package, which provides pre-built binaries for various operating systems:


```bash
pip install ta-lib-bin
```

Alternatively, you can follow the detailed installation instructions provided on the [TA-Lib Bin PyPI page](https://pypi.org/project/ta-lib-bin/) to install the TA-Lib library based on your specific operating system.

### 5. Start the Django Development Server

Run the Django development server:

```bash
python manage.py runserver
```

Access the Django admin interface and other pages in your browser at `http://127.0.0.1:8000/`.
## Project Structure

-   `stockvista/` - Main Django project directory.
-   `analyze/` - Django app directory.
-   `requirements.txt` - Python dependencies file.
-   `manage.py` - Django project management script.
-   `README.md` - This README file.

## Further Information

For more details about TA-Lib, visit the [TA-Lib Bin PyPI page](https://pypi.org/project/ta-lib-bin/) which provides installation instructions for different platforms.
