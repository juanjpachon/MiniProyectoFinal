import json
import os

def main():
    """
    Main function to process the input file, parse the letter soup and words,
    and generate a report in JSON format.

    Args:
        None

    Returns:
        None
    """
    carpeta_raiz = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(carpeta_raiz,"content_Letter_soup.txt")  # Replace with the actual file path
    output_path = os.path.join(carpeta_raiz,"result.json" )           # Path to save the report

    # Read the content of the file
    content = get_file_content(input_path)

    # Find the separator index
    separator_index = content.index('---\n')

    # Process the letter soup
    letter_soup = [list(line.replace(" ", "").strip()) for line in content[:separator_index]]

    # Process the words to search
    words = [line.strip() for line in content[separator_index + 1:]]

    # Generate the report
    generate_report(letter_soup, words, output_path)


def get_file_content(file_path):
    """
    Reads the content of a file and returns it as a list of lines.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of str: List containing lines of the file.
    """
    with open(file_path, 'r') as file:
        content = file.readlines()
    return content


def generate_report(letter_soup, words, output_path):
    """
    Generates a JSON report by finding words in the letter soup
    and saves it to the specified output file.

    Args:
        letter_soup (list of list of str): The letter soup as a 2D list.
        words (list of str): List of words to search in the letter soup.
        output_path (str): Path to save the generated report.

    Returns:
        None
    """
    # Check if the file already exists
    if os.path.exists(output_path):
        os.remove(output_path)  # Remove the existing file

    # Generate the report
    results = find_words(letter_soup, words)
    with open(output_path, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Report saved at: {output_path}")


def find_words(letter_soup, words):
    """
    Searches for a list of words in the letter soup and returns the results.

    Args:
        letter_soup (list of list of str): The letter soup as a 2D list.
        words (list of str): List of words to search.

    Returns:
        dict: Dictionary where keys are words and values are True (if found) or False.
    """
    results = {}
    # Convert the letter soup into a string representation for printing
    soup_str = '\n'.join([''.join(row) for row in letter_soup])  # Converts each row into a string and joins them with newlines
    for word in words:
        results[word] = find_word(letter_soup, word.upper())  # Converts the word to uppercase
    return results


def find_word(letter_soup, word):
    """
    Searches if a word is inside the letter soup.

    Args:
        letter_soup (list of list of str): The letter soup as a 2D list.
        word (str): The word to search for.

    Returns:
        bool: True if the word is in the soup, False otherwise.
    """
    rows, cols = len(letter_soup), len(letter_soup[0])

    # All possible directions
    directions = [
        (0, 1),   # Right
        (1, 0),   # Down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
        (-1, 0),  # Up
        (-1, 1),  # Diagonal up-right
        (-1, -1), # Diagonal up-left
        (0, -1)   # Left
    ]

    # Check if coordinates are within bounds
    def is_valid(x, y):
        """
        Checks if the given coordinates are within the bounds of the letter soup.

        Args:
            x (int): Row index.
            y (int): Column index.

        Returns:
            bool: True if the coordinates are valid, False otherwise.
        """
        return 0 <= x < rows and 0 <= y < cols

    # Search at every position in the soup
    for i in range(rows):
        for j in range(cols):
            if letter_soup[i][j] == word[0]:  # Initial match
                for dx, dy in directions:  # Test all directions
                    x, y = i, j
                    match = True
                    for k in range(len(word)):
                        if not is_valid(x, y) or letter_soup[x][y] != word[k]:
                            match = False
                            break
                        x += dx
                        y += dy
                    if match:  # If the word is found
                        return True
    return False


main()
