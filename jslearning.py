import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn JavaScript - BITCRUSH")

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
        "title": "JavaScript - Quick Navigation",
        "quick_navigation": [
            "1 - Introduction",
            "2 - Syntax & Hello World",
            "3 - Variables",
            "4 - Data Types",
            "5 - Operators",
            "6 - Control Flow",
            "7 - Functions",
            "8 - Arrays",
            "9 - Objects",
            "10 - DOM Manipulation",
            "11 - Events",
            "12 - ES6 Features",
            "13 - Promises & Async/Await",
            "14 - Error Handling",
            "15 - JSON",
            "16 - Fetch API",
            "17 - Local Storage",
            "18 - Modules",
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
            "JavaScript is a versatile, high-level programming language.",
            "It is primarily used for creating interactive web pages.",
            "JavaScript was developed by Netscape in 1995.",
            "It is now one of the core technologies of the web, alongside HTML and CSS."
        ]
    },
    {
        "title": "2 - Syntax & Hello World",
        "content": [
            "JavaScript syntax is simple and easy to learn.",
            "Every JavaScript program starts with a script tag in HTML or a .js file.",
            "Example of a Hello World program:",
            "",
            "<script>",
            "    console.log('Hello, World!');",
            "</script>"
        ]
    },
    {
        "title": "3 - Variables",
        "content": [
            "Variables are used to store data values.",
            "In JavaScript, you can declare variables using var, let, or const.",
            "Example:",
            "",
            "let number = 10;  // Integer variable",
            "const name = 'JavaScript';  // String variable",
            "var isFun = true;  // Boolean variable"
        ]
    },
    {
        "title": "4 - Data Types",
        "content": [
            "JavaScript has dynamic typing, meaning variables can hold any type of data.",
            "Primitive types include string, number, boolean, null, undefined, and symbol.",
            "Non-primitive types include objects and arrays.",
            "Example:",
            "",
            "let age = 25;",
            "let isJavaScriptFun = true;",
            "let greeting = 'Hello!';"
        ]
    },
    {
        "title": "5 - Operators",
        "content": [
            "Operators are used to perform operations on variables and values.",
            "Types of operators in JavaScript:",
            "- Arithmetic Operators: +, -, *, /, %",
            "- Comparison Operators: ==, ===, !=, !==, >, <, >=, <=",
            "- Logical Operators: &&, ||, !",
            "Example:",
            "",
            "let a = 10, b = 20;",
            "console.log(a + b);  // Output: 30"
        ]
    },
    {
        "title": "6 - Control Flow",
        "content": [
            "Control flow statements control the order of execution of statements.",
            "Types of control flow statements:",
            "- Conditional: if, if-else, switch",
            "- Loops: for, while, do-while",
            "- Branching: break, continue, return",
            "Example:",
            "",
            "if (age > 18) {",
            "    console.log('Adult');",
            "} else {",
            "    console.log('Minor');",
            "}"
        ]
    },
    {
        "title": "7 - Functions",
        "content": [
            "Functions are blocks of code designed to perform a specific task.",
            "They can be declared using the function keyword or as arrow functions.",
            "Example:",
            "",
            "function add(a, b) {",
            "    return a + b;",
            "}",
            "",
            "const multiply = (a, b) => a * b;"
        ]
    },
    {
        "title": "8 - Arrays",
        "content": [
            "An array is a collection of elements of any type.",
            "Arrays in JavaScript are zero-indexed.",
            "Example:",
            "",
            "let numbers = [1, 2, 3, 4, 5];",
            "console.log(numbers[0]);  // Output: 1",
            "",
            "You can also use array methods like push, pop, and map."
        ]
    },
    {
        "title": "9 - Objects",
        "content": [
            "Objects are collections of key-value pairs.",
            "They are used to store structured data.",
            "Example:",
            "",
            "let person = {",
            "    name: 'John',",
            "    age: 30,",
            "    greet: function() {",
            "        console.log('Hello, ' + this.name);",
            "    }",
            "};",
            "person.greet();"
        ]
    },
    {
        "title": "10 - DOM Manipulation",
        "content": [
            "The Document Object Model (DOM) represents the structure of a web page.",
            "JavaScript can be used to manipulate the DOM to create dynamic content.",
            "Example:",
            "",
            "document.getElementById('myElement').innerText = 'Hello, DOM!';"
        ]
    },
    {
        "title": "11 - Events",
        "content": [
            "Events are actions or occurrences that happen in the browser.",
            "JavaScript can listen for and respond to events using event listeners.",
            "Example:",
            "",
            "document.getElementById('myButton').addEventListener('click', function() {",
            "    console.log('Button clicked!');",
            "});"
        ]
    },
    {
        "title": "12 - ES6 Features",
        "content": [
            "ES6 introduced many new features to JavaScript.",
            "Some key features include:",
            "- let and const for variable declarations",
            "- Arrow functions",
            "- Template literals",
            "- Destructuring assignment",
            "- Modules",
            "- Promises",
            "Example:",
            "",
            "const greet = (name) => `Hello, ${name}!`;",
            "console.log(greet('World'));"
        ]
    },
    {
        "title": "13 - Promises & Async/Await",
        "content": [
            "Promises are used to handle asynchronous operations in JavaScript.",
            "Async/Await provides a cleaner way to work with Promises.",
            "Example:",
            "",
            "const fetchData = async () => {",
            "    try {",
            "        let response = await fetch('https://api.example.com/data');",
            "        let data = await response.json();",
            "        console.log(data);",
            "    } catch (error) {",
            "        console.error('Error:', error);",
            "    }",
            "};",
            "fetchData();"
        ]
    },
    {
        "title": "14 - Error Handling",
        "content": [
            "Error handling in JavaScript is done using try-catch blocks.",
            "You can also throw custom errors using the throw statement.",
            "Example:",
            "",
            "try {",
            "    let result = riskyOperation();",
            "    console.log(result);",
            "} catch (error) {",
            "    console.error('An error occurred:', error);",
            "}"
        ]
    },
    {
        "title": "15 - JSON",
        "content": [
            "JSON (JavaScript Object Notation) is a lightweight data format.",
            "It is commonly used for data exchange between a server and a client.",
            "Example:",
            "",
            "let jsonData = '{\"name\": \"John\", \"age\": 30}';",
            "let obj = JSON.parse(jsonData);",
            "console.log(obj.name);  // Output: John"
        ]
    },
    {
        "title": "16 - Fetch API",
        "content": [
            "The Fetch API is used to make HTTP requests in JavaScript.",
            "It returns a Promise that resolves to the Response object.",
            "Example:",
            "",
            "fetch('https://api.example.com/data')",
            "    .then(response => response.json())",
            "    .then(data => console.log(data))",
            "    .catch(error => console.error('Error:', error));"
        ]
    },
    {
        "title": "17 - Local Storage",
        "content": [
            "Local Storage allows you to store data in the browser persistently.",
            "Data stored in Local Storage does not expire.",
            "Example:",
            "",
            "localStorage.setItem('key', 'value');",
            "let value = localStorage.getItem('key');",
            "console.log(value);  // Output: value"
        ]
    },
    {
        "title": "18 - Modules",
        "content": [
            "Modules allow you to organize JavaScript code into reusable files.",
            "You can export and import functions, objects, or variables.",
            "Example:",
            "",
            "// In math.js",
            "export const add = (a, b) => a + b;",
            "",
            "// In main.js",
            "import { add } from './math.js';",
            "console.log(add(2, 3));  // Output: 5"
        ]
    },
    {
        "title": "19 - Debugging",
        "content": [
            "Debugging is the process of identifying and fixing errors in code.",
            "Use console.log() to print values to the console.",
            "Use browser developer tools to set breakpoints and inspect variables.",
            "Example:",
            "",
            "console.log('Debugging message');",
            "debugger;  // Pause execution here"
        ]
    },
    {
        "title": "20 - Best Practices",
        "content": [
            "Follow these best practices for writing clean and maintainable JavaScript code:",
            "- Use meaningful variable and function names.",
            "- Write comments to explain complex logic.",
            "- Avoid global variables.",
            "- Use strict mode ('use strict').",
            "- Test your code thoroughly.",
            "Example:",
            "",
            "'use strict';",
            "function calculateArea(radius) {",
            "    if (radius <= 0) throw new Error('Radius must be positive');",
            "    return Math.PI * radius * radius;",
            "}"
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

# Add a global variable for scroll offset
scroll_offset = 0  # Initial scroll position
scroll_speed = 20  # Speed of scrolling

# Reuse the same functions from javalearning.py for drawing pages, handling navigation, etc.
# Ensure to replace references to "Java" with "JavaScript" where applicable.

def draw_page():
    global page_index, scroll_offset
    screen.fill(WHITE)  # Set the background color to white

    # Title
    title_surf = TITLE_FONT.render(pages[page_index]["title"], True, BLACK)  # Set font color to black
    screen.blit(title_surf, (40, 40))

    # Content for the current page
    if "content" in pages[page_index]:
        y_offset = 100 + scroll_offset  # Apply scroll offset
        for line in pages[page_index]["content"]:
            text_surf = FONT.render(line, True, BLACK)  # Set font color to black
            screen.blit(text_surf, (60, y_offset))
            y_offset += 32  # Line spacing

    # Quick Navigation
    if "quick_navigation" in pages[page_index]:
        y_offset = 100 + scroll_offset  # Apply scroll offset
        x_offset = 60
        max_items_per_column = 10  # Limit items per column
        margin_per_column = 400  # Adjusted margin between columns
        for idx, item in enumerate(pages[page_index]["quick_navigation"]):
            if idx > 0 and idx % max_items_per_column == 0:  # Move to the next column
                x_offset += margin_per_column  # Use margin for column spacing
                y_offset = 100 + scroll_offset  # Reset y_offset for the new column
            text_surf = FONT.render(item, True, BLACK)  # Set font color to black
            screen.blit(text_surf, (x_offset, y_offset))
            y_offset += 32  # Line spacing

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
            y = start_y + row * (button_height + button_vertical_margin) + scroll_offset  # Apply scroll offset
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
                topic_start_page = int(button_text) + 1  # Add 1 to match the correct page index
                if topic_start_page < len(pages):
                    page_index = topic_start_page
                    print(f"Navigated to page {page_index}: {pages[page_index]['title']}")
                else:
                    print(f"Page {topic_start_page} does not exist.")

def js_learning_loop():
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
    js_learning_loop()