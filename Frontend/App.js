function showSection(section) {
    console.log(`Showing section: ${section}`);
    // Hide all sections
    document.getElementById("createRuleSection").style.display = "none";
    document.getElementById("combineRuleSection").style.display = "none";
    document.getElementById("evaluateRuleSection").style.display = "none";

    // Show the selected section
    if (section === 'create') {
        document.getElementById("createRuleSection").style.display = "block";
    } else if (section === 'combine') {
        document.getElementById("combineRuleSection").style.display = "block";
    } else if (section === 'evaluate') {
        document.getElementById("evaluateRuleSection").style.display = "block";
    }
}

// Function to create rule
document.getElementById("createBtn").addEventListener("click", function () {
    console.log("Create rule button clicked");
    const ruleString = document.getElementById("createRule").value;

    fetch('http://127.0.0.1:5000/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule: ruleString })
    })
    .then(response => response.json()) // <-- Parse response as JSON
    .then(data => {
        // Check if the response contains the message
        if (data.message) {
            document.getElementById("createResult").innerText = "Rule created: " + data.message;
        } else if (data.error) {
            document.getElementById("createResult").innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to combine rules
document.getElementById("combineBtn").addEventListener("click", function () {
    const rule1 = document.getElementById("combineRule1").value;
    const rule2 = document.getElementById("combineRule2").value;

    const requestData = {
        rules: [rule1, rule2]
    };

    fetch('http://127.0.0.1:5000/combine_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("combineResult").innerText = "Combined Rule: " + data.combined_rule;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// Function to evaluate rule
document.getElementById("evaluateBtn").addEventListener("click", function () {
    console.log("evaluate rule button clicked");
    const rule = document.getElementById("evaluateRule").value;
    const age = document.getElementById("age").value;
    const department = document.getElementById("department").value;
    const salary = document.getElementById("salary").value;
    const experience = document.getElementById("experience").value;

    const requestData = {
        rule_ast: rule,
        user_data: {
            age: parseInt(age),
            department: department,
            salary: parseInt(salary),
            experience: parseInt(experience)  // <-- Added missing comma
        }
    };

    fetch('http://127.0.0.1:5000/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("evaluateResult").innerText = "Result: " + data.result;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// Function to retrieve and display stored rules
document.addEventListener("DOMContentLoaded", function () {
    // Function to retrieve and display stored rules on button click
    document.getElementById("fetchRulesBtn").addEventListener("click", function () {
        fetchStoredRules();
    });

    // Function to retrieve and display stored rules
    function fetchStoredRules() {
        fetch('http://127.0.0.1:5000/get_rules', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.rules) {
                const rulesContainer = document.getElementById("storedRules");
                rulesContainer.innerHTML = ''; // Clear existing rules
                data.rules.forEach(rule => {
                    const ruleElement = document.createElement("li");
                    ruleElement.textContent = rule;
                    rulesContainer.appendChild(ruleElement);
                });
            } else {
                console.error("Error fetching rules:", data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

// Call the function on page load to display stored rules
document.addEventListener("DOMContentLoaded", function () {
    fetchStoredRules();
});




