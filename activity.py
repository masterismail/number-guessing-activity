import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton

import random

class HelloWorldActivity(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        super().__init__(handle)
        
        # Game properties
        self.range_max = 99  # The maximum range (up to 99)
        self.num_bits = 7  # Number of bits needed to represent numbers up to 99
        self.current_bit_index = 0  # The current bit being guessed
        self.guessed_bits = []  # List to store guessed bits
        
        # Initialize toolbar and UI layout
        self.setup_toolbar()
        self.setup_ui()
        
        # Initialize the game instructions and start button
        self.setup_instructions()

    def setup_toolbar(self):
        """Setup the toolbar for the activity."""
        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

    def setup_ui(self):
        """Set up the main user interface."""
        # Create the main vertical box for layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Create a label for displaying instructions and questions
        self.instruction_label = Gtk.Label()
        self.main_box.pack_start(self.instruction_label, False, False, 0)
        
        # Create a horizontal box to hold the start button and response buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Create the start button
        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.button_box.pack_start(self.start_button, True, True, 0)
        
        # Create two buttons for "Yes" and "No" responses
        self.yes_button = Gtk.Button(label="Yes")
        self.no_button = Gtk.Button(label="No")
        
        # Connect buttons to their respective event handlers
        self.yes_button.connect("clicked", self.on_yes_clicked)
        self.no_button.connect("clicked", self.on_no_clicked)
        
        # Add response buttons to the button box (initially hidden)
        self.button_box.pack_start(self.yes_button, True, True, 0)
        self.button_box.pack_start(self.no_button, True, True, 0)
        
        # Initially hide the response buttons
        self.yes_button.hide()
        self.no_button.hide()
        
        # Add the button box to the main box
        self.main_box.pack_start(self.button_box, False, False, 0)

        
        # Add the main box as the canvas
        self.set_canvas(self.main_box)
        
        # Display all widgets
        self.main_box.show_all()

    def setup_instructions(self):
        """Set up the game instructions and start button."""
        self.instruction_label.set_text(
            "Welcome to the guessing game!\n\n"
            "Please think of a number between 1 and 99 and keep it in mind.\n"
            "Press the 'Start' button to begin the game."
        )
        self.start_button.show()

    def on_start_clicked(self, widget):
        """Handle the 'Start' button click to start the game."""
        # Hide the start button and instructions
        self.start_button.hide()
        self.instruction_label.hide()
        
        # Show the response buttons
        self.yes_button.show()
        self.no_button.show()
        
        # Display the first question
        self.display_current_question()

    def display_current_question(self):
        """Display the current question to the player."""
        # Generate the sets of numbers based on the current bit index
        group_0, group_1 = self.generate_number_sets()
        
        # Randomly select one of the groups to display
        selected_group = random.choice([group_0, group_1])
        
        # Determine the correct response based on which group is selected
        self.correct_response = "Yes" if selected_group == group_0 else "No"
        
        # Format the selected group as a string and display it as a question
        group_text = ", ".join(map(str, selected_group))
        self.instruction_label.set_text(f"Is your number in this set?\n{group_text}")
        
        # Show the instruction label again to display the question
        self.instruction_label.show()

    def generate_number_sets(self):
        """Generate sets of numbers based on the current bit index."""
        group_0 = []
        group_1 = []
        for num in range(self.range_max + 1):
            # Check the current bit in the number
            if (num & (1 << self.current_bit_index)) == 0:
                group_0.append(num)
            else:
                group_1.append(num)
        
        # Return the groups as a tuple (group_0, group_1)
        return group_0, group_1

    def on_yes_clicked(self, widget):
        """Handle the 'Yes' button click."""
        self.handle_response("Yes")

    def on_no_clicked(self, widget):
        """Handle the 'No' button click."""
        self.handle_response("No")

    def handle_response(self, response):
        """Handle the player's response and update the game state."""
        # Check if the player's response matches the correct response
        if response == self.correct_response:
            # Add 0 to the guessed bits if response matches
            self.guessed_bits.append(0)
        else:
            # Add 1 to the guessed bits if response does not match
            self.guessed_bits.append(1)
        
        # Move to the next bit index
        self.current_bit_index += 1
        
        # Check if all bits have been guessed
        if self.current_bit_index >= self.num_bits:
            # Guess the chosen number
            guessed_number = sum((bit << i) for i, bit in enumerate(self.guessed_bits))
            
            # Display the guessed number on the canvas
            self.display_guessed_number(guessed_number)
            
            # Reset the game for a new round
            self.current_bit_index = 0
            self.guessed_bits = []
            # Optionally, you can restart the game or do something else here
            
        else:
            # Display the next question
            self.display_current_question()

    def display_guessed_number(self, guessed_number):
        """Display the guessed number on the canvas."""
        # Create a label to display the guessed number
        guessed_label = Gtk.Label(label=f"The chosen number is: {guessed_number}")
        
        # Add the guessed label to the main box
        self.main_box.pack_start(guessed_label, False, False, 0)
        
        # Show the guessed label
        guessed_label.show()

    def display_number_grid(self):
        """Display the number grid in a specific format."""
        # Create a grid with the specified rows and columns
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        # Iterate through the numbers 1 to 99 and organize them in the grid format
        current_number = 1
        for row in range(10):
            for col in range(10):
                if current_number > self.range_max:
                    break
                # Create a label for the current number
                label = Gtk.Label(label=str(current_number))
                
                # Attach the label to the grid at the current row and column
                grid.attach(label, col, row, 1, 1)
                
                # Increment the current number
                current_number += 1

            if current_number > self.range_max:
                break

        # Add the grid to the main box
        self.main_box.pack_start(grid, True, True, 0)
        
        # Show the grid
        grid.show_all()

        return grid
