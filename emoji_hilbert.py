# Function for clockwise rotation
def rotate_pattern_clockwise(pattern):
    rotation_mapping = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U', 'X': 'X'}
    rows = pattern.split("\n")
    rows = list(reversed(rows))
    rotated_pattern = []
    for i in range(len(rows[0])):
        new_row = []
        for row in rows:
            new_row.append(rotation_mapping[row[i]])
        rotated_pattern.append(''.join(new_row))
    return "\n".join(rotated_pattern)

# Function for counter-clockwise rotation
def rotate_pattern_counter_clockwise(pattern):
    rotation_mapping = {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U', 'X': 'X'}
    rows = pattern.split("\n")
    rows = [row[::-1] for row in rows]
    rotated_pattern = []
    for i in range(len(rows[0])):
        new_row = []
        for row in rows:
            new_row.append(rotation_mapping[row[i]])
        rotated_pattern.append(''.join(new_row))
    return "\n".join(rotated_pattern)

def make_rectangular(pattern):
    # Split the pattern into rows
    rows = pattern.split("\n")

    # Compute the maximum length of rows
    max_length = max(len(row) for row in rows)

    # Pad the shorter rows with Xs
    padded_rows = [row + 'X' * (max_length - len(row)) for row in rows]

    return "\n".join(padded_rows)

def append_horizontal(pattern1, pattern2, to_left=True, pad_up=True):
    # Make both patterns rectangular
    pattern1 = make_rectangular(pattern1)
    pattern2 = make_rectangular(pattern2)
    
    # Split both patterns into rows
    rows1 = pattern1.split("\n")
    rows2 = pattern2.split("\n")

    # Compute the height difference
    height_diff = len(rows1) - len(rows2)

    # Pad the shorter pattern with Xs
    if height_diff > 0:  # Pattern2 is shorter
        padding = ['X'*len(rows2[0])] * abs(height_diff)
        rows2 = padding + rows2 if pad_up else rows2 + padding
    elif height_diff < 0:  # Pattern1 is shorter
        padding = ['X'*len(rows1[0])] * abs(height_diff)
        rows1 = padding + rows1 if pad_up else rows1 + padding

    # Join the patterns
    if to_left:
        joined_pattern = "\n".join([r1 + r2 for r1, r2 in zip(rows1, rows2)])
    else:
        joined_pattern = "\n".join([r2 + r1 for r1, r2 in zip(rows1, rows2)])

    return joined_pattern

def append_vertical(pattern1, pattern2, above=True, pad_left=True):
    # Make both patterns rectangular
    pattern1 = make_rectangular(pattern1)
    pattern2 = make_rectangular(pattern2)
    
    # Split both patterns into rows
    rows1 = pattern1.split("\n")
    rows2 = pattern2.split("\n")

    # Compute the width difference
    width_diff = len(rows1[0]) - len(rows2[0])

    # Pad the narrower pattern with Xs
    if width_diff > 0:  # Pattern2 is narrower
        padding = 'X' * abs(width_diff)
        rows2 = [padding + row if pad_left else row + padding for row in rows2]
    elif width_diff < 0:  # Pattern1 is narrower
        padding = 'X' * abs(width_diff)
        rows1 = [padding + row if pad_left else row + padding for row in rows1]

    # Join the patterns
    if above:
        joined_pattern = "\n".join(rows1 + rows2)
    else:
        joined_pattern = "\n".join(rows2 + rows1)

    return joined_pattern

def append_to_direction(pattern1, pattern2, append_direction, padding_direction):
    # Ensure that append_direction and padding_direction are orthogonal
    if append_direction in ["Up", "Down"] and padding_direction in ["Up", "Down"]:
        raise ValueError("Incompatible directions: cannot append and pad in the same (vertical) direction.")
    if append_direction in ["Left", "Right"] and padding_direction in ["Left", "Right"]:
        raise ValueError("Incompatible directions: cannot append and pad in the same (horizontal) direction.")

    # Map directions to parameters for append_horizontal and append_vertical
    append_to_left = append_direction == "Left"
    pad_up = padding_direction == "Up"
    append_above = append_direction == "Up"
    pad_left = padding_direction == "Left"

    # Decide which function to call based on append_direction
    if append_direction in ["Left", "Right"]:
        return append_horizontal(pattern1, pattern2, to_left=append_to_left, pad_up=pad_up)
    else:  # Up or Down
        return append_vertical(pattern1, pattern2, above=append_above, pad_left=pad_left)

def append_to_left(pattern1, pattern2, pad_up=True):
    return append_to_direction(pattern1, pattern2, "Left", "Up" if pad_up else "Down")

def append_to_right(pattern1, pattern2, pad_up=True):
    return append_to_direction(pattern1, pattern2, "Right", "Up" if pad_up else "Down")

def append_above(pattern1, pattern2, pad_left=True):
    return append_to_direction(pattern1, pattern2, "Up", "Left" if pad_left else "Right")

def append_below(pattern1, pattern2, pad_left=True):
    return append_to_direction(pattern1, pattern2, "Down", "Left" if pad_left else "Right")

# Creating aliases for append_above and append_below
append_to_up = append_above
append_to_down = append_below

# Defining aliases
rotate_upside_down = lambda p: rotate_pattern_clockwise(rotate_pattern_clockwise(p))
rotate_right = rotate_pattern_clockwise
rotate_left = rotate_pattern_counter_clockwise
rotate_down = rotate_upside_down
rotate_up = lambda p: p

# Defining rotate_direction function
def rotate_direction(direction, pattern):
    # Define a dict to map each direction to a rotation function
    rotation_funcs = {"U": rotate_up,
                      "R": rotate_right,
                      "D": rotate_down,
                      "L": rotate_left}

    # Use the dict to call the appropriate function for the given direction
    return rotation_funcs[direction](pattern)

def rotations_row(rotations_pattern, rotated_pattern):
    # Initialize the current_pattern to the rotated_pattern in the direction specified by the first character of the rotations_pattern
    current_pattern = rotate_direction(rotations_pattern[0], rotated_pattern)

    # Initialize the output_pattern with the current_pattern
    output_pattern = current_pattern

    # Loop over the directions in the rotations_pattern (skipping the first one)
    for direction in rotations_pattern[1:]:
        # Set current_pattern to the rotated_pattern in the specified direction
        current_pattern = rotate_direction(direction, rotated_pattern)

        # Append the current_pattern to the right of the output_pattern
        output_pattern = append_to_right(current_pattern, output_pattern, pad_up=True)

    return output_pattern

def rotations_board(multiline_rotations_pattern, rotated_pattern):
    # Rectangularize the multiline_rotations_pattern
    rectangular_rotations_pattern = make_rectangular(multiline_rotations_pattern)
    
    # Split the rectangular_rotations_pattern into lines
    rotations_patterns = rectangular_rotations_pattern.split("\n")

    # Initialize output_board with the rotations_row for the first rotations_pattern
    output_board = rotations_row(rotations_patterns[0], rotated_pattern)

    # Loop over the remaining rotations_patterns
    for rotations_pattern in rotations_patterns[1:]:
        # Get the rotations_row for the current rotations_pattern
        rotations_row_current = rotations_row(rotations_pattern, rotated_pattern)

        # Append the current rotations_row below the output_board
        output_board = append_below(rotations_row_current, output_board, pad_left=True)

    return output_board

def beautify_pattern(pattern):
    # Define the mapping from characters to emojis
    mapping = {
        'U': '⬆️',
        'D': '⬇️',
        'L': '⬅️',
        'R': '➡️',
        'X': '❌',
        '\n': '\n'
    }
    
    # Convert the pattern into a list of characters
    chars = list(pattern)
    
    # Replace each character with its corresponding emoji
    beautified_chars = [mapping[char] for char in chars]
    
    # Join the beautified characters back into a string
    beautified_pattern = ''.join(beautified_chars)
    
    return beautified_pattern

# pattern = "UU\nRL"
# beautified_pattern = beautify_pattern(pattern)
# print(beautified_pattern)

# Recursive version (deprecated)
# def fractal_generator(iterations, initial_pattern):
#     # Base case: if there are no iterations left, return the initial pattern
#     if iterations == 0:
#         return initial_pattern
# 
#     # Recursive case: apply rotations_board to the result of fractal_generator with one less iteration
#     return rotations_board(fractal_generator(iterations - 1, initial_pattern), initial_pattern)

def fractal_generator(iterations, initial_pattern):
    fractal_pattern = initial_pattern
    for _ in range(iterations):
        fractal_pattern = rotations_board(fractal_pattern, initial_pattern)
    return fractal_pattern

def beautiful_fractal_generator(iterations):
    initial_pattern = "UU\nRL"
    fractal = fractal_generator(iterations, initial_pattern)
    beautiful_fractal = beautify_pattern(fractal)
    print(beautiful_fractal)

beautiful_fractal_generator(3)