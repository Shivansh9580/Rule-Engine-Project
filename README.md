# Rule Engine Project

## Objective
This project is a simple 3-tier rule engine application built to determine user eligibility based on attributes like age, department, income, spend, and experience. The system uses an Abstract Syntax Tree (AST) to represent conditional rules and enables the dynamic creation, combination, and modification of rules through a straightforward interface.

## Features
Conditional Rule Engine: Allows users to define rules using attributes like age, department, income, spend, and experience.<br>
Dynamic Rule Creation and Modification: Easily create, modify, or combine rules to adjust conditions without changing the code.<br>
Error Handling: Validates rule strings, catches format errors, and provides clear error messages if rule structure is incorrect.<br>
Attribute Validation: Ensures only valid attributes are used by maintaining a catalog of acceptable fields.<br>
Modification of Existing Rules: Offers a function to edit rules by changing operators, operand values, or adding/removing sub-expressions within the AST.<br>

## Project Structure
The project is divided into three main components:

Frontend (UI): HTML, CSS, and JavaScript to create rules, evaluate conditions, and view results.<br>
Backend (API): Flask server to handle rule creation, combination, and evaluation requests.<br>
Database (MongoDB): MongoDB is used to store rule definitions, allowing easy retrieval and management of previously defined rules.<br>

## Data Storage with MongoDB

MongoDB is implemented to store each created rule as a document within a collection. The schema for rules includes fields for:

Rule ID: A unique identifier for each rule.<br>
AST Structure: A JSON object that stores the AST representation of each rule.<br>
Metadata: Information about the rule such as creation date and any relevant description or tags for easy identification.<br>
Example document structure:

{
    "rule_id": "12345",
    "ast": {
        "type": "operator",
        "operator": "AND",
        "left": { "type": "operand", "attribute": "age", "operator": ">=", "value": 18 },
        "right": { "type": "operand", "attribute": "income", "operator": "<", "value": 50000 }
    },
    "metadata": {
        "created_at": "2023-10-25",
        "description": "Rule for eligibility based on age and income"
    }
}

## Prerequisites

Python 3.7+ - Required for running the Flask server and handling rule logic.<br>
MongoDB - Used for storing created rules and application metadata.<br>
Flask & Required Packages - Install using requirements.txt.


## Setup Instructions

Clone the Repository

```bash
git clone https://github.com/Shivansh9580/Rule-Engine-Project.git
cd Rule-Engine-Project
```

Install Dependencies Run the build.bat file to set up the environment. This will install the required dependencies, check MongoDB status, and open the frontend app in the default browser.

```bash
build.bat
```

Ensure MongoDB is Running If MongoDB does not start automatically, run it manually and update the build.bat script with the correct path to mongod.exe.

Run the Flask Server Manually (if needed)

```bash
python app.py
```

Launch the Web Application Double-click index.html or access http://127.0.0.1:5000 to use the rule engine application.

## Usage

### Creating a Rule<br>
Use the Create Rule button to define a new rule by inputting conditions and saving them to the database.

### Combining Rules<br>
The Combine Rule function allows combining two rules with logical operators (AND/OR), resulting in a new composite rule.

### Evaluating a Rule<br>
The Evaluate Rule button allows you to test defined rules with sample user data to check if they meet eligibility criteria.

## Additional Functionalities

1.Error Handling: Detects errors in rule strings (e.g., missing operators or invalid comparisons) and provides specific error messages.<br>
Attribute Validation: Checks if the specified attributes match the catalog to ensure only recognized fields are used.<br>
2.Rule Modification: Allows the modification of existing rules, including changing operators, operand values, or adding/removing sub-expressions within the AST.


## Troubleshooting
1.MongoDB Errors: Ensure MongoDB is running and accessible.
2.Requirements Error: Verify requirements.txt is in the project directory and all dependencies are listed.
3.Permission Issues: Run build.bat as Administrator if you encounter permission-related issues.
