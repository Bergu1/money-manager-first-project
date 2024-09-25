# Money Manager
Money Manager is a web application that helps users oversee their monthly budget and manage expenses and savings in different currencies.

## Features
* **Registration and Login:** Users can register, log in, and reset their password via email.
* **Expenses Managment:** In the "Expenses" section, users can add expenses (bills, daily purchases, random expenses) and import expenses from a CSV file.
* **Account Managment:** In the "Account" section, users can add income (e.g., salary), review income for a given month, and check the updated balance.
* **Monthly Financial Overview:** The "Manager" section allows users to review their monthly expenses and income, generate reports in PDF or CSV format, and assess whether they are "in the black" or "in the red".
* **Savings Goal:** The "Money Box" section enables users to set a savings goal, make deposits, and track the percentage progress toward reaching the goal.
* The application supports three currencies and dynamically updates the balance after each transaction using an API for currency conversion.

## Technologies
* **Backend:** Python, Django
* **Frontend:** HTML
* **Databases:** PostgreSQL
* **Testing:** pytest, unittest.mock
* **Containerization:** Docker
* **CI/CD:** Github Actions
* **Hosting:** AWS EC2
* **API:** ExchangeRate-API (currency conversion)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Bergu1/money-manager-first-project.git
   ```
2. Navigate to the project directiory:
   ```bash
   cd money-manager-first-project
   ```
3. Start the application:
   ```bash
   docker-compose up --build
   ```
4. The application will be available at: http://localhost:8000

## Usage
1. Register or log in to the application.
2. Navigate to the Expenses tab to add expenses or import them from a CSV file.
3. In the Account tab, you can add funds to your account and track your balance.
4. Use the Manager tab to monitor your financial situation and generate financial reports for a given month.
5. In the Money Box tab, set your savings goal and deposit funds to achieve it.

## Live Demo 
You can view the live application at this link:
[Money Manager - Live Demo](http://ec2-13-60-82-173.eu-north-1.compute.amazonaws.com/login/)

## Authors
* Konrad Landzberg 
