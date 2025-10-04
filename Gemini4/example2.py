# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def draw_rectangle_paint(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint_maximized first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active and focused
        paint_window.set_focus()
        time.sleep(1)
        
        # Select Rectangle tool from toolbar
        paint_window.click_input(coords=(180, 80))  # Rectangle tool position
        time.sleep(1)
        
        # Draw rectangle using drag operation
        paint_window.press_mouse_input(coords=(x1, y1))
        time.sleep(0.5)
        paint_window.move_mouse_input(coords=(x2, y2))
        time.sleep(0.5)
        paint_window.release_mouse_input(coords=(x2, y2))
        time.sleep(1)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def draw_rectangle_with_turtle(width: int = 300, height: int = 150, text: str = "TSAI") -> dict:
    """Draw a rectangle with text using Turtle graphics with maximized window"""
    try:
        import turtle
        
        def draw_rectangle_with_text():
            # Setup screen
            screen = turtle.Screen()
            screen.title("Rectangle with TSAI")
            screen.setup(width=1.0, height=1.0)  # Maximize window

            # Create the turtle
            pen = turtle.Turtle()
            pen.pensize(3)
            pen.color("blue", "lightyellow")  # (outline color, fill color)

            # Rectangle dimensions
            rect_width = width
            rect_height = height

            # Move turtle to starting position (centered)
            pen.penup()
            pen.goto(-rect_width / 2, -rect_height / 2)
            pen.pendown()

            # Draw and fill rectangle
            pen.begin_fill()
            for _ in range(2):
                pen.forward(rect_width)
                pen.left(90)
                pen.forward(rect_height)
                pen.left(90)
            pen.end_fill()

            # Write text centered
            pen.penup()
            pen.goto(0, -15)  # adjust Y to center visually
            pen.color("darkblue")
            pen.write(text, align="center", font=("Arial", 36, "bold"))

            # Hide turtle
            pen.hideturtle()
            
            # Close window after 12 seconds
            screen.ontimer(lambda: screen.bye(), 12000)
            
            # Start the turtle main loop
            turtle.mainloop()
        
        # Run the function
        draw_rectangle_with_text()
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle with text '{text}' drawn using Turtle graphics with maximized window"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing with Turtle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text_in_paint(text: str) -> dict:
    """Add text in Paint with improved reliability"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active and focused
        paint_window.set_focus()
        time.sleep(1)
        
        # Click on the Text tool in the toolbar (more precise coordinates)
        paint_window.click_input(coords=(120, 70))  # Text tool position
        time.sleep(1.5)
        
        # Click where to place the text (center of the rectangle)
        paint_window.click_input(coords=(200, 150))
        time.sleep(2)
        
        # Clear any existing text and type the new text
        paint_window.type_keys('^a')  # Select all
        time.sleep(0.5)
        paint_window.type_keys(text)  # Type the text
        time.sleep(1)
        
        # Click outside to finish text editing
        paint_window.click_input(coords=(400, 300))
        time.sleep(1)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_paint_maximized() -> dict:
    """Open Microsoft Paint maximized with enhanced window management"""
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(2)  # Wait longer for Paint to fully load
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get screen dimensions
        primary_width = GetSystemMetrics(0)
        screen_width = GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
        screen_height = GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
        
        # Move to secondary monitor and maximize
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            primary_width + 1, 0,  # Position on secondary monitor
            screen_width, screen_height,  # Full screen size
            win32con.SWP_SHOWWINDOW
        )
        
        # Force maximize
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(3)  # Wait for full maximization
        
        # Bring to front and focus
        win32gui.SetForegroundWindow(paint_window.handle)
        win32gui.BringWindowToTop(paint_window.handle)
        paint_window.set_focus()
        time.sleep(1)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paint opened and maximized successfully on secondary monitor"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING THE SERVER AT AMAZING LOCATION")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
