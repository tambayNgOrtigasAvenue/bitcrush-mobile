import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn Python - BITCRUSH")

# Fonts and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)

# Load custom font or fallback to a default font
try:
    FONT = pygame.font.Font("python/images/minecraft.ttf", 24)  # Main font
    TITLE_FONT = pygame.font.Font("python/images/minecraft.ttf", 36)  # Title font
    BUTTON_FONT = pygame.font.Font("python/images/minecraft.ttf", 28)  # Button font
except FileNotFoundError:
    FONT = pygame.font.SysFont("arial", 24)
    TITLE_FONT = pygame.font.SysFont("arial", 36, bold=True)
    BUTTON_FONT = pygame.font.SysFont("arial", 28)

# Button setup
next_button = pygame.Rect(WIDTH - 160, HEIGHT - 70, 120, 50)
back_button = pygame.Rect(40, HEIGHT - 70, 120, 50)
quick_nav_button = pygame.Rect(180, HEIGHT - 70, 200, 50)  # Positioned next to the Back button

# Load a sound effect (optional)
try:
    click_sound = pygame.mixer.Sound("python/sounds/click.wav")
except FileNotFoundError:
    click_sound = None

# Pages content
pages = [
    {
        "title": "Python - Quick Navigation",
        "quick_navigation": [
            "1 - Introduction",
            "2 - Syntax & Hello World",
            "3 - Variables",
            "4 - Data Types",
            "5 - Operators",
            "6 - Control Flow",
            "7 - Functions",
            "8 - Lists",
            "9 - Dictionaries",
            "10 - File I/O",
            "11 - Modules",
            "12 - Classes and Objects",
            "13 - Inheritance",
            "14 - Exception Handling",
            "15 - Iterators and Generators",
            "16 - Decorators",
            "17 - Lambda Functions",
            "18 - Python Libraries",
            "19 - Debugging",
            "20 - Best Practices"
        ]
    },
    {
        "title": "Select a Topic",
        "buttons": [str(i) for i in range(1, 21)]  # Buttons for topics 1-20
    },
    {
        "title": "1 - Introduction",
        "content": [
            "Python is a high-level, interpreted programming language.",
            "It was created by Guido van Rossum and released in 1991.",
            "Python emphasizes code readability and simplicity.",
            "It is widely used for web development, data analysis, AI, and more."
        ]
    },
    {
        "title": "2 - Syntax & Hello World",
        "content": [
            "Python syntax is simple and easy to learn.",
            "Every Python program starts with a script or a .py file.",
            "Example of a Hello World program:",
            "",
            "print('Hello, World!')"
        ]
    },
    {
        "title": "3 - Variables",
        "content": [
            "Variables are used to store data values.",
            "In Python, you don't need to declare the type of a variable.",
            "Example:",
            "",
            "x = 10  # Integer variable",
            "name = 'Python'  # String variable",
            "is_fun = True  # Boolean variable"
        ]
    },
    {
        "title": "4 - Data Types",
        "content": [
            "Python supports various data types, including:",
            "- int, float, str, bool, list, tuple, dict, set",
            "Example:",
            "",
            "age = 25  # int",
            "pi = 3.14  # float",
            "greeting = 'Hello!'  # str",
            "is_python_fun = True  # bool"
        ]
    },
    {
        "title": "5 - Operators",
        "content": [
            "Operators are used to perform operations on variables and values.",
            "Types of operators in Python:",
            "- Arithmetic Operators: +, -, *, /, %",
            "- Comparison Operators: ==, !=, >, <, >=, <=",
            "- Logical Operators: and, or, not",
            "Example:",
            "",
            "a = 10",
            "b = 20",
            "print(a + b)  # Output: 30"
        ]
    },
    {
        "title": "6 - Control Flow",
        "content": [
            "Control flow statements control the order of execution of statements.",
            "Types of control flow statements:",
            "- Conditional: if, elif, else",
            "- Loops: for, while",
            "- Branching: break, continue, pass",
            "Example:",
            "",
            "if age > 18:",
            "    print('Adult')",
            "else:",
            "    print('Minor')"
        ]
    },
    {
        "title": "7 - Functions",
        "content": [
            "Functions are blocks of code designed to perform a specific task.",
            "They can be defined using the def keyword.",
            "Example:",
            "",
            "def add(a, b):",
            "    return a + b",
            "",
            "result = add(5, 10)",
            "print(result)  # Output: 15"
        ]
    },
    {
        "title": "8 - Lists",
        "content": [
            "A list is a collection of elements of any type.",
            "Lists in Python are mutable and ordered.",
            "Example:",
            "",
            "numbers = [1, 2, 3, 4, 5]",
            "print(numbers[0])  # Output: 1",
            "",
            "numbers.append(6)  # Add an element",
            "print(numbers)  # Output: [1, 2, 3, 4, 5, 6]"
        ]
    },
    {
        "title": "9 - Dictionaries",
        "content": [
            "Dictionaries are collections of key-value pairs.",
            "They are used to store structured data.",
            "Example:",
            "",
            "person = {",
            "    'name': 'John',",
            "    'age': 30,",
            "    'city': 'New York'",
            "}",
            "print(person['name'])  # Output: John"
        ]
    },
    {
        "title": "10 - File I/O",
        "content": [
            "Python provides built-in functions for file input and output.",
            "Example:",
            "",
            "with open('example.txt', 'w') as file:",
            "    file.write('Hello, File!')",
            "",
            "with open('example.txt', 'r') as file:",
            "    content = file.read()",
            "    print(content)  # Output: Hello, File!"
        ]
    },
    {
        "title": "11 - Modules",
        "content": [
            "Modules are files containing Python code that can be imported into other scripts.",
            "They help organize code into reusable components.",
            "Example: Create a module named 'mymodule.py':",
            "",
            "# mymodule.py",
            "def greet(name):",
            "    return f'Hello, {name}!'",
            "",
            "Import and use the module:",
            "",
            "import mymodule",
            "print(mymodule.greet('Alice'))  # Output: Hello, Alice!"
        ]
    },
    {
        "title": "12 - Classes and Objects",
        "content": [
            "Classes are blueprints for creating objects.",
            "Objects are instances of classes.",
            "Example:",
            "",
            "class Person:",
            "    def __init__(self, name, age):",
            "        self.name = name",
            "        self.age = age",
            "",
            "    def greet(self):",
            "        return f'Hi, I am {self.name} and I am {self.age} years old.'",
            "",
            "person = Person('John', 30)",
            "print(person.greet())  # Output: Hi, I am John and I am 30 years old."
        ]
    },
    {
        "title": "13 - Inheritance",
        "content": [
            "Inheritance allows a class to inherit attributes and methods from another class.",
            "Example:",
            "",
            "class Animal:",
            "    def __init__(self, name):",
            "        self.name = name",
            "",
            "    def speak(self):",
            "        return 'I make a sound.'",
            "",
            "class Dog(Animal):",
            "    def speak(self):",
            "        return 'Woof!'",
            "",
            "dog = Dog('Buddy')",
            "print(dog.name)  # Output: Buddy",
            "print(dog.speak())  # Output: Woof!"
        ]
    },
    {
        "title": "14 - Exception Handling",
        "content": [
            "Exception handling is used to manage errors gracefully.",
            "Use try-except blocks to handle exceptions.",
            "Example:",
            "",
            "try:",
            "    result = 10 / 0",
            "except ZeroDivisionError:",
            "    print('Cannot divide by zero!')",
            "finally:",
            "    print('Execution complete.')"
        ]
    },
    {
        "title": "15 - Iterators and Generators",
        "content": [
            "Iterators are objects that can be iterated upon.",
            "Generators are functions that yield values one at a time using the yield keyword.",
            "Example of a generator:",
            "",
            "def count_up_to(n):",
            "    count = 1",
            "    while count <= n:",
            "        yield count",
            "        count += 1",
            "",
            "for number in count_up_to(5):",
            "    print(number)  # Output: 1, 2, 3, 4, 5"
        ]
    },
    {
        "title": "16 - Decorators",
        "content": [
            "Decorators are functions that modify the behavior of other functions.",
            "They are often used for logging, access control, etc.",
            "Example:",
            "",
            "def decorator(func):",
            "    def wrapper():",
            "        print('Before the function call.')",
            "        func()",
            "        print('After the function call.')",
            "    return wrapper",
            "",
            "@decorator",
            "def say_hello():",
            "    print('Hello!')",
            "",
            "say_hello()",
            "# Output:",
            "# Before the function call.",
            "# Hello!",
            "# After the function call."
        ]
    },
    {
        "title": "17 - Lambda Functions",
        "content": [
            "Lambda functions are anonymous functions defined using the lambda keyword.",
            "They are often used for short, simple operations.",
            "Example:",
            "",
            "add = lambda x, y: x + y",
            "print(add(5, 3))  # Output: 8",
            "",
            "numbers = [1, 2, 3, 4, 5]",
            "squared = list(map(lambda x: x ** 2, numbers))",
            "print(squared)  # Output: [1, 4, 9, 16, 25]"
        ]
    },
    {
        "title": "18 - Python Libraries",
        "content": [
            "Python has a rich ecosystem of libraries for various tasks.",
            "Popular libraries include:",
            "- NumPy: Numerical computing",
            "- Pandas: Data manipulation",
            "- Matplotlib: Data visualization",
            "- Requests: HTTP requests",
            "- Flask/Django: Web development",
            "",
            "Example with NumPy:",
            "",
            "import numpy as np",
            "array = np.array([1, 2, 3])",
            "print(array * 2)  # Output: [2 4 6]"
        ]
    },
    {
        "title": "19 - Debugging",
        "content": [
            "Debugging is the process of identifying and fixing errors in code.",
            "Common debugging tools include:",
            "- print statements",
            "- Python's built-in debugger (pdb)",
            "- IDE debuggers",
            "",
            "Example with pdb:",
            "",
            "import pdb",
            "def divide(a, b):",
            "    pdb.set_trace()  # Set a breakpoint",
            "    return a / b",
            "",
            "divide(10, 2)"
        ]
    },
    {
        "title": "20 - Best Practices",
        "content": [
            "Follow these best practices for writing clean and maintainable Python code:",
            "- Use meaningful variable and function names.",
            "- Write comments and docstrings.",
            "- Follow PEP 8 style guidelines.",
            "- Write modular and reusable code.",
            "- Use version control (e.g., Git).",
            "- Write tests for your code.",
            "",
            "Example of a docstring:",
            "",
            "def add(a, b):",
            "    \"\"\"Add two numbers and return the result.\"\"\"",
            "    return a + b",
            "",
            "print(add(3, 4))  # Output: 7"
        ]
    }
    
]

# Configuration for button layout
button_width = 80
button_height = 50
start_x = 20
start_y = 100
button_spacing = 20
max_buttons_per_column = (HEIGHT - start_y) // (button_height + button_spacing)

page_index = 0  # Starting at the first page

# Reuse the same functions from javalearning.py for drawing pages, handling navigation, etc.
# Ensure to replace references to "Java" with "Python" where applicable.

def draw_page():
    global page_index
    screen.fill(WHITE)  # Set the background color to white

    # Title
    title_surf = TITLE_FONT.render(pages[page_index]["title"], True, BLACK)  # Set font color to black
    screen.blit(title_surf, (40, 40))

    # Content for the current page
    if "content" in pages[page_index]:
        y_offset = 100
        for line in pages[page_index]["content"]:
            text_surf = FONT.render(line, True, BLACK)  # Set font color to black
            screen.blit(text_surf, (60, y_offset))
            y_offset += 32  # line spacing

    # Quick Navigation
    if "quick_navigation" in pages[page_index]:
        y_offset = 100
        x_offset = 60
        max_items_per_column = 10  # Limit items per column
        margin_per_column = 400  # Adjusted margin between columns
        for idx, item in enumerate(pages[page_index]["quick_navigation"]):
            if idx > 0 and idx % max_items_per_column == 0:  # Move to the next column
                x_offset += margin_per_column  # Use margin for column spacing
                y_offset = 100
            text_surf = FONT.render(item, True, BLACK)  # Set font color to black
            screen.blit(text_surf, (x_offset, y_offset))
            y_offset += 32  # line spacing

    # Buttons for the "Select a Topic" page
    if "buttons" in pages[page_index]:
        mouse_pos = pygame.mouse.get_pos()
        buttons_per_row = 10  # Limit buttons to 10 per row
        button_horizontal_margin = 36  # Horizontal margin between buttons
        button_vertical_margin = 26  # Vertical margin between rows
        for idx, button_text in enumerate(pages[page_index]["buttons"]):
            row = idx // buttons_per_row
            col = idx % buttons_per_row
            x = start_x + col * (button_width + button_horizontal_margin)
            y = start_y + row * (button_height + button_vertical_margin)
            button_rect = pygame.Rect(x, y, button_width, button_height)

            # Change color based on hover
            color = (180, 180, 180) if button_rect.collidepoint(mouse_pos) else (220, 220, 220)
            pygame.draw.rect(screen, color, button_rect, border_radius=8)

            # Render button text
            button_text_surf = BUTTON_FONT.render(button_text, True, BLACK)  # Set font color to black
            screen.blit(button_text_surf, (x + (button_width - button_text_surf.get_width()) // 2,
                                           y + (button_height - button_text_surf.get_height()) // 2))

    # Draw navigation buttons
    draw_navigation_buttons()

# Reuse navigation and event handling functions from javalearning.py
def draw_navigation_buttons():
    """Draw the Back, Quick Navigation, and Next buttons with hover effects."""
    mouse_pos = pygame.mouse.get_pos()

    # Draw the Next button
    if page_index < len(pages) - 1:  # Only draw if not on the last page
        color = (180, 180, 180) if next_button.collidepoint(mouse_pos) else (220, 220, 220)
        pygame.draw.rect(screen, color, next_button, border_radius=8)
        screen.blit(BUTTON_FONT.render("Next", True, BLACK), (next_button.x + 25, next_button.y + 10))
    # Draw the Back button
    if page_index > 0:  # Only draw if not on the first page
        color = (180, 180, 180) if back_button.collidepoint(mouse_pos) else (220, 220, 220)
        pygame.draw.rect(screen, color, back_button, border_radius=8)
        screen.blit(BUTTON_FONT.render("Back", True, BLACK), (back_button.x + 30, back_button.y + 10))

    # Draw the Quick Navigation button (hide if on the Quick Navigation page)
    if page_index != 0:  # Only draw if not on the Quick Navigation page
        color = (180, 180, 180) if quick_nav_button.collidepoint(mouse_pos) else (220, 220, 220)
        pygame.draw.rect(screen, color, quick_nav_button, border_radius=8)
        screen.blit(BUTTON_FONT.render("Quick Nav", True, BLACK), (quick_nav_button.x + 20, quick_nav_button.y + 10))

def handle_navigation_buttons(event):
    """Handle clicks on the Back, Quick Navigation, and Next buttons."""
    global page_index

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Handle Next button click
        if next_button.collidepoint(event.pos) and page_index < len(pages) - 1:
            if click_sound:
                click_sound.play()
            page_index += 1  # Go to the next page
            print(f"Navigated to page {page_index + 1}: {pages[page_index]['title']}")

        # Handle Back button click
        if back_button.collidepoint(event.pos) and page_index > 0:
            if click_sound:
                click_sound.play()
            page_index -= 1  # Go to the previous page
            print(f"Navigated to page {page_index + 1}: {pages[page_index]['title']}")

        # Handle Quick Navigation button click
        if quick_nav_button.collidepoint(event.pos):
            if click_sound:
                click_sound.play()
            page_index = 0  # Navigate to the Quick Navigation page
            print(f"Navigated to Quick Navigation: {pages[page_index]['title']}")

def handle_topic_selection(event):
    """Handle clicks on topic buttons in the 'Select a Topic' page."""
    global page_index

    if page_index == 1 and "buttons" in pages[page_index]:  # Check if on the "Select a Topic" page
        buttons_per_row = 10  # Match the layout with 10 buttons per row
        button_horizontal_margin = 36  # Horizontal margin between buttons
        button_vertical_margin = 26  # Vertical margin between rows
        for idx, button_text in enumerate(pages[page_index]["buttons"]):
            row = idx // buttons_per_row
            col = idx % buttons_per_row
            x = start_x + col * (button_width + button_horizontal_margin)
            y = start_y + row * (button_height + button_vertical_margin)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(event.pos):  # Check if the mouse click is inside the button
                print(f"Button {button_text} clicked!")
                # Navigate to the first page of the selected topic
                topic_start_page = pages.index(next(page for page in pages if page["title"].startswith(f"{button_text} -")))
                if topic_start_page < len(pages):
                    page_index = topic_start_page
                    print(f"Navigated to page {page_index}: {pages[page_index]['title']}")
                else:
                    print(f"Page {topic_start_page} does not exist.")

def py_learning_loop():
    global page_index
    running = True

    while running:
        draw_page()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_navigation_buttons(event)  # Handle Back, Next, and Quick Nav button clicks
                handle_topic_selection(event)  # Handle topic button clicks

        pygame.display.flip()
 
if __name__ == "__main__":
    py_learning_loop()