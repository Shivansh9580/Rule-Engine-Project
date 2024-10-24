from flask import Flask, request, jsonify
from Rule_Engine import create_rule, combine_rules, evaluate_rule, print_ast
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util  # To handle MongoDB-specific serialization
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['Rule_Engine']
rules_collection = db['rules']

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Helper function to serialize AST (custom object to JSON)
def serialize_node(node):
    if node.type == "operator":
        return {
            "type": "operator",
            "value": node.value,
            "left": serialize_node(node.left),
            "right": serialize_node(node.right)
        }
    elif node.type == "operand":
        return {
            "type": "operand",
            "attribute": node.value["attribute"],
            "operator": node.value["operator"],
            "value": node.value["value"]
        }


# Helper function to deserialize AST (JSON back to custom object)
def deserialize_node(data):
    from Rule_Engine import Node  # Import the Node class
    if data['type'] == 'operator':
        left = deserialize_node(data['left'])
        right = deserialize_node(data['right'])
        return Node(type='operator', value=data['value'], left=left, right=right)
    elif data['type'] == 'operand':
        return Node(type='operand', value={
            'attribute': data['attribute'],
            'operator': data['operator'],
            'value': data['value']
        })


# Route for the home page
@app.route("/")
def home():
    return "Welcome to the Rule Engine Application!"


# Route to create a rule and store its serialized AST in MongoDB
@app.route("/create_rule", methods=["POST", "OPTIONS"])
def create_rule_route():
    if request.method == "OPTIONS":
        return '', 200  # Respond to preflight request

    data = request.json
    rule_string = data.get("rule")
    if not rule_string:
        return jsonify({"error": "No rule provided"}), 400

    ast = create_rule(rule_string)
    print_ast(ast)

    # Serialize the AST
    serialized_ast = serialize_node(ast)

    rule_data = {
        "rule_text": rule_string,
        "ast": serialized_ast
    }

    try:
        # Insert serialized rule into MongoDB
        rules_collection.insert_one(rule_data)
    except Exception as e:
        print("Error inserting rule:", str(e))  # Log the error message
        return jsonify({"error": "Failed to create rule", "details": str(e)}), 500

    return jsonify({"message": "AST created and stored successfully for rule", "rule": rule_string}), 200


@app.route("/get_rules", methods=["GET"])
def get_rules_route():
    try:
        # Retrieve all stored rules from the MongoDB collection
        stored_rules = list(rules_collection.find({}, {"_id": 0, "rule_text": 1}))
        # Convert MongoDB cursor to a list of rule strings
        rule_list = [rule['rule_text'] for rule in stored_rules]

        return jsonify({"rules": rule_list}), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve rules", "details": str(e)}), 500


# Route to combine multiple rules
@app.route("/combine_rules", methods=["POST", "OPTIONS"])
def combine_rules_route():
    if request.method == "OPTIONS":
        return '', 200  # Respond to preflight request

    data = request.json
    rules = data.get("rules")
    if not rules or not isinstance(rules, list):
        return jsonify({"error": "Please provide a list of rules"}), 400

    combined_ast = combine_rules(rules)
    print_ast(combined_ast)  # Optional: Print combined AST to console

    combined_rule = ""

    def collect_rule(node):
        nonlocal combined_rule
        if node.type == "operator":
            combined_rule += "("
            collect_rule(node.left)
            combined_rule += f" {node.value} "
            collect_rule(node.right)
            combined_rule += ")"
        elif node.type == "operand":
            combined_rule += f"{node.value['attribute']} {node.value['operator']} {node.value['value']}"

    collect_rule(combined_ast)

    return jsonify({"message": "Rules combined successfully", "combined_rule": combined_rule}), 200


# Route to evaluate a rule against provided data
@app.route("/evaluate_rule", methods=["POST", "OPTIONS"])
def evaluate_rule_route():
    if request.method == "OPTIONS":
        return '', 200  # Respond to preflight request

    data = request.json
    rule_ast = data.get("rule_ast")
    user_data = data.get("user_data")

    if not rule_ast or not user_data:
        return jsonify({"error": "Both rule_ast and user_data must be provided"}), 400

    # Deserialize AST from rule string
    deserialized_ast = create_rule(rule_ast)

    result = evaluate_rule(deserialized_ast, user_data)
    return jsonify({"result": result}), 200


if __name__ == "__main__":
    app.run(debug=True)
