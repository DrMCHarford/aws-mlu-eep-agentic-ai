lab1a_question1 = {
        "question": "Which type of schema is used for tool definition?",
        "options": [
                "XML",
                "JSON",
                "Python",
                "Typescript",
        ],
        "correctIndex": 1,
    }

lab1a_question2 = {
        "question": "Does the tool description enable the LLM to map the user request to the correct tool?",
        "options": [
            "True",
            "False",
        ],
        "correctIndex": 0,
    }

lab1b_question1 = {
        "question": "How does the agent plan and act?",
        "options": [
            "agents do not plan and act",
            "agents plan but do not act",
            "agents act but do not plan",
            "using techniques like ReAct",
        ],
        "correctIndex": 3,
    }

lab1b_question2 = {
        "question": "how do langchain agents know that a function is a tool definition ?",
        "options": [
            "Using @tooluse annotation",
            "Using @tool annotation",
            "Using tool registry",
            "Functions are not required for tools",
        ],
        "correctIndex": 1,
    }

lab2_question1 = {
        "question": "Which tool would be most suitable for giving the model information about a new AWS service which was just launched today?", "options" : [
            "Wikipedia tool",
            "Web search tool",
            "PythonREPL tool",
            "File manager tool",
        ],
        "correctIndex": 1,
    }

lab2_question2 = {
        "question": "For which of the following use cases would you prefer using a long-term memory?", "options":[
            "Generating a summary of the conversation you just had",
            "Rewrite the previous response in French.",
            "Store user profile as information is collected",
            "Classify user reviews as positive or negative.",
        ],
        "correctIndex": 2,
    }

lab3_question1 = {
        "question": "Which type of vulnerabilities are agents susceptible to?",
        "options": [
            "Tool poisoning",
                "Resource exhaustion",
                "Prompt attacks",
                "All of the above",
        ],
        "correctIndex": 3,
    }

lab3_question2 = {
        "question": "Which of these is NOT a best security practice for agents and tools?",
        "options": [
            "Principle of least privilege",
            "Documenting expected behavior and inputs",
            "Denying profanity",
            "Audit logging",
        ],
        "correctIndex": 2,
    }