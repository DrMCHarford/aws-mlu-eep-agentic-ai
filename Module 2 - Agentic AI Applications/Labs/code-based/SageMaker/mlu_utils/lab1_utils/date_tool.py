
from datetime import date


def get_tool_spec():
    """
    Returns the JSON Schema specification for the date tool. The tool specification
    defines the input schema and describes the tool's functionality.
    For more information, see https://json-schema.org/understanding-json-schema/reference.

    :return: The tool specification for the Date tool.
    """
    return {
        "toolSpec": {
            "name": "Date_Tool",
            "description": "Get the current date.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "input_data": {
                            "type": "string",
                            "description": "input_data for date tool.",
                        },
                    },
                }
            },
        }
    }


def fetch_data(input_data):
    """
    Fetches current date for today

    :param input_data: The input data for date tool
    :return: Fetches current date for today
    """
    response = str(date.today())
    date_today = {"date_today": response}
    return date_today