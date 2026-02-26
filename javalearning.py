import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn Java - BITCRUSH")

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
        "title": "Java - Quick Navigation",
        "quick_navigation": [
            "1 - Introduction",
            "2 - Syntax & Hello World",
            "3 - Variables",
            "4 - Data Types",
            "5 - Operators",
            "6 - Control Flow",
            "7 - Arrays",
            "8 - OOP Basics",
            "9 - Exception Handling",
            "10 - File I/O",
            "11 - Methods",
            "12 - Classes and Objects",
            "13 - Static and Final Keywords",
            "14 - Interfaces and Abstract Classes",
            "15 - Collections Framework",
            "16 - Generics",
            "17 - Threads and Concurrency",
            "18 - Java Streams",
            "19 - Lambda Expressions",
            "20 - JDBC (Database Connectivity)"
        ]
    },
    {
        "title": "Select a Topic",
        "buttons": [str(i) for i in range(1, 21)]  # Buttons for topics 1-20
    },
    {
        "title": "1 - Introduction",
        "content": [
            "Java is a high-level, class-based, object-oriented programming language.",
            "It is designed to have as few implementation dependencies as possible.",
            "Java was developed by Sun Microsystems in 1995 and is now owned by Oracle.",
            "It is widely used for building enterprise-scale applications."
        ]
    },
    {
        "title": "2 - Syntax & Hello World",
        "content": [
            "Java syntax is similar to C++ but simpler to learn and use.",
            "Every Java program starts with a class definition.",
            "Example of a Hello World program:",
            "",
            "public class HelloWorld {",
            "    public static void main(String[] args) {",
            "        System.out.println(\"Hello, World!\");",
            "    }",
            "}"
        ]
    },
    {
    "title": "3 - Variables (Page 1)",
    "content": [
        "Variables are containers for storing data values.",
        "In Java, you must declare a variable before using it.",
        "Example:",
        "",
        "int number = 10;  // Integer variable",
        "String name = \"Java\";  // String variable",
        "double pi = 3.14;  // Floating-point variable"
    ]
},
{
    "title": "3 - Variables (Page 2)",
    "content": [
        "Java supports different types of variables:",
        "- Local Variables",
        "- Instance Variables",
        "- Static Variables",
        "",
        "Example of static variables:",
        "",
        "class Example {",
        "    static int count = 0;",
        "    Example() { count++; }",
        "}"
    ]
},
    {
        "title": "4 - Data Types",
        "content": [
            "Java has two types of data types: Primitive and Non-Primitive.",
            "Primitive types include int, float, char, boolean, etc.",
            "Non-Primitive types include Strings, Arrays, Classes, etc.",
            "Example:",
            "",
            "int age = 25;",
            "boolean isJavaFun = true;",
            "String greeting = \"Hello!\";"
        ]
    },
    {
        "title": "5 - Operators",
        "content": [
            "Operators are used to perform operations on variables and values.",
            "Types of operators in Java:",
            "- Arithmetic Operators: +, -, *, /, %",
            "- Relational Operators: ==, !=, >, <, >=, <=",
            "- Logical Operators: &&, ||, !",
            "Example:",
            "",
            "int a = 10, b = 20;",
            "System.out.println(a + b);  // Output: 30"
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
            "    System.out.println(\"Adult\");",
            "} else {",
            "    System.out.println(\"Minor\");",
            "}"
        ]
    },
    {
        "title": "7 - Arrays",
        "content": [
            "An array is a collection of elements of the same type.",
            "Arrays in Java are zero-indexed.",
            "Example:",
            "",
            "int[] numbers = {1, 2, 3, 4, 5};",
            "System.out.println(numbers[0]);  // Output: 1",
            "",
            "You can also declare and initialize arrays separately."
        ]
    },
    {
        "title": "8 - OOP Basics",
        "content": [
            "Java is an object-oriented programming language.",
            "Key OOP concepts include:",
            "- Encapsulation: Wrapping data and methods into a single unit.",
            "- Inheritance: Acquiring properties of a parent class.",
            "- Polymorphism: Using a single interface for different types.",
            "- Abstraction: Hiding implementation details.",
            "Example:",
            "",
            "class Animal {",
            "    void sound() {",
            "        System.out.println(\"Animal makes a sound\");",
            "    }",
            "}"
        ]
    },
    {
        "title": "9 - Exception Handling",
        "content": [
            "Exceptions are problems that occur during program execution.",
            "Java provides a robust mechanism to handle exceptions.",
            "Key keywords: try, catch, finally, throw, throws",
            "Example:",
            "",
            "try {",
            "    int result = 10 / 0;",
            "} catch (ArithmeticException e) {",
            "    System.out.println(\"Cannot divide by zero\");",
            "}"
        ]
    },
    {
        "title": "10 - File I/O",
        "content": [
            "Java provides classes for file input and output.",
            "Key classes: File, FileReader, FileWriter, BufferedReader, etc.",
            "Example:",
            "",
            "import java.io.*;",
            "public class FileExample {",
            "    public static void main(String[] args) throws IOException {",
            "        FileWriter writer = new FileWriter(\"output.txt\");",
            "        writer.write(\"Hello, File!\");",
            "        writer.close();",
            "    }",
            "}"
        ]
    },
    {
        "title": "11 - Methods",
        "content": [
            "Methods are blocks of code that perform a specific task.",
            "They help in code reuse and modularity.",
            "Example:",
            "",
            "public int add(int a, int b) {",
            "    return a + b;",
            "}",
            "",
            "You can call this method using:",
            "int result = add(5, 10);"
        ]
    },
    {
        "title": "12 - Classes and Objects",
        "content": [
            "Classes are blueprints for creating objects.",
            "Objects are instances of classes.",
            "Example:",
            "",
            "class Car {",
            "    String brand;",
            "    int speed;",
            "",
            "    void drive() {",
            "        System.out.println(\"Driving \" + brand);",
            "    }",
            "}",
            "",
            "Car myCar = new Car();",
            "myCar.brand = \"Toyota\";",
            "myCar.drive();"
        ]
    },
    {
        "title": "13 - Static and Final Keywords",
        "content": [
            "The `static` keyword is used for memory management.",
            "The `final` keyword is used to declare constants or prevent inheritance.",
            "Example:",
            "",
            "static int count = 0;",
            "final int MAX = 100;"
        ]
    },
    {
        "title": "14 - Interfaces and Abstract Classes",
        "content": [
            "Interfaces define a contract that classes must follow.",
            "Abstract classes provide partial implementation.",
            "Example:",
            "",
            "interface Animal {",
            "    void sound();",
            "}",
            "",
            "class Dog implements Animal {",
            "    public void sound() {",
            "        System.out.println(\"Woof\");",
            "    }",
            "}"
        ]
    },
    {
        "title": "15 - Collections Framework",
        "content": [
            "The Collections Framework provides data structures like lists, sets, and maps.",
            "Example:",
            "",
            "ArrayList<String> list = new ArrayList<>();",
            "list.add(\"Java\");",
            "list.add(\"Python\");",
            "System.out.println(list);"
        ]
    },
    {
        "title": "16 - Generics",
        "content": [
            "Generics provide type safety for collections.",
            "Example:",
            "",
            "ArrayList<Integer> numbers = new ArrayList<>();",
            "numbers.add(10);",
            "numbers.add(20);",
            "System.out.println(numbers);"
        ]
    },
    {
        "title": "17 - Threads and Concurrency",
        "content": [
            "Threads allow concurrent execution of code.",
            "Example:",
            "",
            "class MyThread extends Thread {",
            "    public void run() {",
            "        System.out.println(\"Thread is running\");",
            "    }",
            "}",
            "",
            "MyThread t = new MyThread();",
            "t.start();"
        ]
    },
    {
        "title": "18 - Java Streams",
        "content": [
            "Streams provide a functional approach to processing collections.",
            "Example:",
            "",
            "List<Integer> numbers = Arrays.asList(1, 2, 3, 4);",
            "numbers.stream().filter(n -> n % 2 == 0).forEach(System.out::println);"
        ]
    },
    {
        "title": "19 - Lambda Expressions",
        "content": [
            "Lambda expressions simplify functional programming.",
            "Example:",
            "",
            "(a, b) -> a + b;"
        ]
    },
    {
        "title": "20 - JDBC (Database Connectivity)",
        "content": [
            "JDBC allows Java applications to interact with databases.",
            "Example:",
            "",
            "Connection conn = DriverManager.getConnection(url, user, password);",
            "Statement stmt = conn.createStatement();",
            "ResultSet rs = stmt.executeQuery(\"SELECT * FROM table\");"
        ]
    }
]

#java game questions (this is only for secmain)
java_questions = [
    {"prompt": "System.out.____(\"Hello\");", "answer": "println"},
    {"prompt": "int x = 10; ____ x++;", "answer": "System.out.println"},
    {"prompt": "public static ____ main(String[] args)", "answer": "void"},
    {"prompt": "Java was developed by ____ Microsystems.", "answer": "Sun"},
    {"prompt": "Every Java program starts with a ____ definition.", "answer": "class"},
    {"prompt": "int[] numbers = {1, 2, 3}; What is numbers[0]?", "answer": "1"},
    {"prompt": "Which keyword is used to define a constant in Java? ____", "answer": "final"},
    {"prompt": "Which keyword is used for inheritance in Java? ____", "answer": "extends"},
    {"prompt": "What is the output of 10 % 3? ____", "answer": "1"},
    {"prompt": "Which loop guarantees at least one execution? ____", "answer": "do-while"},
    {"prompt": "Which class is used for file writing in Java? ____", "answer": "FileWriter"},
    {"prompt": "What is the default value of a boolean in Java? ____", "answer": "false"},
    {"prompt": "Which method is used to start a thread? ____", "answer": "start"},
    {"prompt": "Lambda expressions are introduced in Java version ____.", "answer": "8"},
    {"prompt": "Which interface is used for database connectivity in Java? ____", "answer": "JDBC"},
    {"prompt": "What is the size of an int in Java? ____ bytes", "answer": "4"},
    {"prompt": "Which keyword is used to handle exceptions? ____", "answer": "try"},
    {"prompt": "What is the parent class of all classes in Java? ____", "answer": "Object"},
    {"prompt": "Which operator is used to compare two values? ____", "answer": "=="},
    {"prompt": "What is the access modifier for the most restricted access? ____", "answer": "private"}
]

# Configuration for button layout
button_width = 80
button_height = 50
start_x = 20
start_y = 100
button_spacing = 20
max_buttons_per_column = (HEIGHT - start_y) // (button_height + button_spacing)

page_index = 0  # Starting at the first page

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
                # Dynamically find the first page for the selected topic
                try:
                    topic_start_page = next(
                        idx for idx, page in enumerate(pages)
                        if page["title"].startswith(f"{button_text} -")
                    )
                    page_index = topic_start_page
                    print(f"Navigated to page {page_index}: {pages[page_index]['title']}")
                except StopIteration:
                    print(f"Error: No page found for topic {button_text}.")

def java_learning_loop():
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
    java_learning_loop()
