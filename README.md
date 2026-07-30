<img width="800" height="277" alt="Projekt bez nazwy(1)" src="https://github.com/user-attachments/assets/284b8289-fb7b-442d-85c5-fc59a3bbfd04" />

# Introduction
### Ledger is a modern personal finance application that helps you manage your money with ease. Track your income and expenses, create recurring transactions, set savings goals, and monitor your financial progress with interactive charts. The app also supports multiple currencies with real-time exchange rates through a currency API, making it easy to manage finances across different currencies.

## Features

- 💰 **Income & Expense Tracking** – Add, edit, and categorize your transactions
- 🔁 **Recurring Transactions** – Automate regular income and expenses (subscriptions, salary, rent, etc.)
- 🎯 **Savings Goals** – Set targets and track your progress toward them
- 📊 **Interactive Charts** – Visualize your spending and income trends over time
- 💱 **Multi-Currency Support** – Manage finances across different currencies with real-time exchange rates


## Tech Stack

**GUI Framework:**
- PyQt6 – desktop user interface

**Language:**
- Python

**Database:**
- SQLite – local data storage

**Charting:**
- Matplotlib – interactive financial charts

**API & Integrations:**
- [ExchangeRate-API](https://www.exchangerate-api.com/) – real-time currency exchange rates

**Other Libraries:**
- `requests` – for API calls
- `sqlite3` – built-in database handling

## Prerequisites

Before installing and running the application, ensure you have:

- Python 3.9+

- pip

- Internet connection

- Exchange rate API key

- Supported operating system: Windows, macOS, or Linux

## Installation

### 1. Clone the repository

```bash
git clone <[repository-url](https://github.com/johnnycodepoland/ledger)>
cd ledger
```

### 2. Create a virtual environment

Create a virtual environment to install dependencies separately from your system Python packages.

```bash
python -m venv .venv
```

### 3. Install dependencies

Install all required Python packages using the requirements file.

```bash
pip install -r requirements.txt
```

### 4. Configure API key

Create an account on [ExchangeRate-API](https://www.exchangerate-api.com/) and generate your API key.

Create a `.env` file in the project root directory and add your API key:

```env

API_KEY=your_api_key_here
```

### 5. Run the application

Start the application by running the main Python file.

```bash
python main.py
```

## Usage

After launching the application, you can manage your personal finances using four main sections:

- 📊 **Dashboard** – View your current month income, expenses, and balance. The dashboard also includes financial charts and a list of the 10 most recent transactions.

- 🧾 **Transaction History** – Browse all your transactions, filter them, and manage your financial records by adding, editing, and deleting transactions.

- 🔁 **Recurring Transactions** – Create, filter and manage regular payments or income sources. Recurring transactions can be added, edited, and deleted.

- 🎯 **Savings Goals** – Create savings goals and track your progress. Goals can be added, edited, and removed at any time.

## License

This project is licensed under the MIT License.
