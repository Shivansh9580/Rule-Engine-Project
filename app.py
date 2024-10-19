from flask import Flask, request, jsonify
from Rule_Engine import create_rule, combine_rules, evaluate_rule, print_ast

app = Flask(__name__)


# Route for the home page
@app.route("/")
def home():
    return "Welcome to the Rule Engine Application!"


# Route to create a rule and return its AST structure
@app.route("/create_rule", methods=["POST"])
def create_rule_route():
    data = request.json
    rule_string = data.get("rule")
    if not rule_string:
        return jsonify({"error": "No rule provided"}), 400

    ast = create_rule(rule_string)
    print_ast(ast)  # Optional: Print AST to console
    return jsonify({"message": "AST created successfully for rule", "rule": rule_string}), 200


# Route to combine multiple rules
@app.route("/combine_rules", methods=["POST"])
def combine_rules_route():
    data = request.json
    rules = data.get("rules")
    if not rules or not isinstance(rules, list):
        return jsonify({"error": "Please provide a list of rules"}), 400

    combined_ast = combine_rules(rules)
    print_ast(combined_ast)  # Optional: Print combined AST to console
    return jsonify({"message": "Rules combined successfully", "rules": rules}), 200


# Route to evaluate a rule against provided data
@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule_route():
    data = request.json
    rule_ast = data.get("rule_ast")
    user_data = data.get("user_data")

    if not rule_ast or not user_data:
        return jsonify({"error": "Both rule_ast and user_data must be provided"}), 400

    # Recreate AST from rule string (for simplicity, assuming the rule is passed as a string)
    combined_ast = create_rule(rule_ast)

    result = evaluate_rule(combined_ast, user_data)
    return jsonify({"result": result}), 200


if __name__ == "__main__":
    app.run(debug=True)
