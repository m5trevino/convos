import json
import os # Import the os module

# --- Script Starts Here ---

def format_conversation(json_string):
    """
    Parses a JSON string containing conversation chunks and formats it
    into a specific text layout.
    """
    try:
        data = json.loads(json_string)
        # Navigate safely to the chunks list, defaulting to empty list if keys are missing
        chunks = data.get('chunkedPrompt', {}).get('chunks', [])
    except json.JSONDecodeError as e:
        # Provide more context if possible
        print(f"Error decoding JSON: {e}")
        # You could add logic here to try and show the problematic area if needed
        # For now, just returning an error message
        return f"Error decoding JSON: {e}"
    except AttributeError:
         return "Error: Input JSON structure is not as expected (missing 'chunkedPrompt' or 'chunks')."


    output_parts = []

    for chunk in chunks:
        role = chunk.get('role')
        text = chunk.get('text', '') # Default to empty string if text is missing
        is_thought = chunk.get('isThought', False)

        # Skip chunks that are missing essential role or text
        if not role or text is None: # Check for None text too
            print(f"Skipping chunk due to missing role or text: {chunk}")
            continue

        formatted_block = ""
        if role == 'user':
            # *** Corrected formatting for user block ***
            formatted_block = f"""###user output starts###
{text}
above is from - user
###user output end###"""
        # *** Corrected indentation for elif/else block ***
        elif role == 'model':
            # *** Corrected indentation for inner if/else ***
            if is_thought:
                formatted_block = f"""###model thoughts starts###
{text}
above is the thoughts of the model
###model thoughts end###"""
            else:
                formatted_block = f"""###model output starts###
{text}
###model output end###"""
        # *** Corrected indentation for outer else ***
        else:
            print(f"Skipping chunk with unexpected role: {role}")
            continue # Skip appending if role is unexpected

        # *** Corrected indentation for append ***
        # This should only happen if a valid block was formatted
        if formatted_block: # Only append if we actually created a block
             output_parts.append(formatted_block)

    return "\n\n".join(output_parts)

# --- Execute the formatting ---

# Define the filename
json_filename = 'conversation.json'
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get script's directory
json_filepath = os.path.join(script_dir, json_filename)

formatted_output = f"Error: File '{json_filename}' not found in script directory." # Default error

if os.path.exists(json_filepath):
    try:
        # Read the JSON data from the file with explicit UTF-8 encoding
        with open(json_filepath, 'r', encoding='utf-8') as f:
            input_json_string_from_file = f.read()

        # Process the JSON string
        formatted_output = format_conversation(input_json_string_from_file)

    except IOError as e:
        formatted_output = f"Error reading file '{json_filename}': {e}"
    except Exception as e: # Catch other potential errors during processing
         formatted_output = f"An unexpected error occurred: {e}"
else:
     print(f"Error: Could not find the file '{json_filename}' at '{json_filepath}'")


# Print the final result (or error message)
print(formatted_output)

# Optional: Save the result to a file
# Check if the output actually contains the expected start markers, indicating success
if "###user output starts###" in formatted_output or \
   "###model thoughts starts###" in formatted_output or \
   "###model output starts###" in formatted_output:
    try:
        output_filename = 'formatted_conversation.txt'
        output_filepath = os.path.join(script_dir, output_filename)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        print(f"\nFormatted conversation saved to '{output_filename}'")
    except IOError as e:
        print(f"\nError writing to file '{output_filename}': {e}")