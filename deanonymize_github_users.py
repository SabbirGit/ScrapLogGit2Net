#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module  deanonymizes GitHub noreply emails in gramphML files created with ScrapLogGit2Net
"""



import sys
import argparse
import networkx as nx

from typing import Tuple 

import time
from time import sleep 


# Combining loguru with rich provides a powerful logging setup that enhances readability and adds visual appeal to your logs. This integration makes it easier to debug and monitor applications by presenting log messages in a clear, color-coded, and structured format while using loguru's other features, such as log rotation and filtering,
from loguru import logger

# You can then print strings or objects to the terminal in the usual way. Rich will do some basic syntax highlighting and format data structures to make them easier to read.
from rich import print as rprint


# For complete control over terminal formatting, Rich offers a Console class.
# Most applications will require a single Console instance, so you may want to create one at the module level or as an attribute of your top-level object. 
from rich.console import Console

# Initialize the console
console = Console()

# JSON gets easier to understand 
from rich import print_json
from rich.json import JSON


# Strings may contain Console Markup which can be used to insert color and styles in to the output.
from rich.markdown import Markdown

# Python data structures can be automatically pretty printed with syntax highlighting.
from rich import pretty
from rich.pretty import pprint
pretty.install()

# Rich has an inspect() function which can generate a report on any Python object. It is a fantastic debug aid
from rich import inspect
from rich.color import Color

#Rich supplies a logging handler which will format and colorize text written by Python’s logging module.
from rich.logging import RichHandler

# Add RichHandler to the loguru logger
logger.remove()  # Remove the default logger
logger.add(
    RichHandler(console=console, show_time=True, show_path=True, rich_tracebacks=True),
    format="{message}",  # You can customize this format as needed
    #level="DEBUG",  # Set the desired logging level
    level="INFO",  # Set the desired logging level
)


# Rich’s Table class offers a variety of ways to render tabular data to the terminal.
from rich.table import Table


# Rich provides the Live  class to to animate parts of the terminal
# It's handy to annimate tables that grow row by row 
from rich.live import Live

# Rich can display continuously updated information regarding the progress of long running tasks / file copies etc. The information displayed is configurable, the default will display a description of the ‘task’, a progress bar, percentage complete, and estimated time remaining.
from rich.progress import Progress, TaskID

# Rich has a Text class you can use to mark up strings with color and style attributes.
from rich.text import Text


from rich.traceback import Traceback 

# For configuring 
from rich.traceback import install
# Install the Rich Traceback handler with custom options
install(
    show_locals=True,  # Show local variables in the traceback
    locals_max_length=10, locals_max_string=80, locals_hide_dunder=True, locals_hide_sunder=False,
    indent_guides=True,
    suppress=[__name__],
    # suppress=[your_module],  # Suppress tracebacks from specific modules
    #max_frames=3,  # Limit the number of frames shown
    max_frames=5,  # Limit the number of frames shown
    #width=50,  # Set the width of the traceback display
    width=100,  # Set the width of the traceback display
    extra_lines=3,  # Show extra lines of code around the error
    theme="solarized-dark",  # Use a different color theme
    word_wrap=True,  # Enable word wrapping for long lines
)





def log_messages() -> None: 
    rprint("\n\t [green] Testing logger messages:\n")
    
    # Log messages at different levels
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    rprint("\n")
    
def console_messages() -> None: 
    
    rprint("\n\t [green] Testing console messages:\n")

    markdown_text = Markdown("# This is a heading\n\n- This is a list item\n- Another item")
    console.print(markdown_text)

    
    # An example of a styled message
    console.print("[bold blue]Welcome to [blink]Rich[/blink]![/bold blue]")
    console.print("[bold green]Success:[/bold green] Your operation completed successfully.")
    console.print("[bold red]Error:[/bold red] Something went wrong. Please try again.")


    # Other examples

    console.print([1, 2, 3])
    console.print("[blue underline]Looks like a link")
    console.print(locals())
    console.print("FOO", style="white on blue")
    
    console.print(inspect("test-string", methods=True))

    # Logging with time console.log("Hello, World!")

    # json and low level examples 
    console.print_json('[false, true, null, "foo"]')
    console.log(JSON('["foo", "bar"]'))
    console.out("Locals", locals())

    # The rule
    console.rule("[bold red]Chapter 2")


def demonstrate_traceback_exceptions():

    # Define functions that raise specific exceptions
    def raise_index_error():
        my_list = [1, 2, 3]
        return my_list[5]  # Index out of range

    def raise_key_error():
        my_dict = {'a': 1, 'b': 2}
        return my_dict['c']  # Key not found

    def raise_value_error():
        return int("not_a_number")  # Value conversion error

    def raise_type_error():
        return 'string' + 5  # Type operation error

    def raise_file_not_found_error():
        with open('non_existing_file.txt') as f:
            return f.read()  # File not found

    # List of exception functions
    exception_functions = [
        ("IndexError", raise_index_error),
        ("KeyError", raise_key_error),
        ("ValueError", raise_value_error),
        ("TypeError", raise_type_error),
        ("FileNotFoundError", raise_file_not_found_error)
    ]

    for exc_name, func in exception_functions:
        try:
            func()  # Call the function that raises an exception
        except Exception as e:
            # Print the exception traceback using Rich
            console.print(f"[bold yellow]{exc_name} occurred:[/bold yellow]", style="bold red")
            # Print formatted traceback using Rich
            console.print(Traceback(), style="bold red")
            console.print("-" * 40)  # Separator for clarity

def status_messages():

    
    console.print("[blue] Counting started")
    # Create the status spinner and progress bar
    with console.status("[bold green]Processing... Counting to 100", spinner="dots") as status:
        # Loop from 1 to 100
        for i in range(1, 101):
            sleep(0.03)  # Simulate work being done

    console.print("[green]Counting completed!")

def display_advanced_text():
    # Initialize the console
    console = Console()

    # Create various styles and formats
    text1 = Text("Bold and Italic", style="bold italic cyan")
    text2 = Text(" Underlined with Green", style="underline green")
    text3 = Text(" Strike-through and Red", style="strike red")
    text4 = Text(" Background Color", style="on yellow")
    text5 = Text(" Custom Font Style", style="bold magenta on black")

    # Combine different styles into one Text object
    combined_text = Text()
    combined_text.append("Rich Text Features:\n", style="bold underline")
    combined_text.append(text1)
    combined_text.append(text2)
    combined_text.append("\n")
    combined_text.append(text3)
    combined_text.append(text4)
    combined_text.append("\n")
    combined_text.append(text5)
    
    # Print the advanced text
    console.print(combined_text)


def display_emojis():
    # Initialize the console
    console = Console()

    # List of 30 emojis with descriptions
    emojis = [
        ("Smiley Face", "😀"),
        ("Thumbs Up", "👍"),
        ("Rocket", "🚀"),
        ("Heart", "❤️"),
        ("Sun", "☀️"),
        ("Star", "⭐"),
        ("Face with Sunglasses", "😎"),
        ("Party Popper", "🎉"),
        ("Clap", "👏"),
        ("Fire", "🔥"),
        ("100", "💯"),
        ("Thumbs Down", "👎"),
        ("Check Mark", "✔️"),
        ("Cross Mark", "❌"),
        ("Lightning Bolt", "⚡"),
        ("Flower", "🌸"),
        ("Tree", "🌳"),
        ("Pizza", "🍕"),
        ("Ice Cream", "🍦"),
        ("Coffee", "☕"),
        ("Wine Glass", "🍷"),
        ("Beer Mug", "🍺"),
        ("Camera", "📷"),
        ("Laptop", "💻"),
        ("Books", "📚"),
        ("Globe", "🌍"),
        ("Envelope", "✉️"),
        ("Gift", "🎁"),
        ("Calendar", "📅"),
        ("Alarm Clock", "⏰"),
        ("Basketball", "🏀")
    ]

    # Print each emoji with its description
    for description, emoji in emojis:
        # Create a rich text object with some styling
        text = Text(f"{description}: {emoji}", style="bold magenta")
        console.print(text)


    
def progress_bars_demo():
    # Create the progress bar
    with Progress() as progress:
        # Add two tasks for the progress bars
        task1 = progress.add_task("[green]Counting to 100...", total=100)
        task2 = progress.add_task("[blue]Counting to 200...", total=200)
        
        # Loop until both tasks are complete
        while not progress.finished:
            sleep(0.05)  # Simulate work being done
            progress.update(task1, advance=1)  # Update the first progress bar
            #progress.console.print(f"Working on")
            progress.update(task2, advance=0.5)  # Update the second progress bar more slowly
            
    print("Counting to 100 and 200 completed!")
    

    
# For the GitHub REST APY
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Use GITHUB_TOKEN in your requests
# Replace with your personal access token if needed

GITHUB_TOKEN = config.get('github', 'token', fallback=None)

rprint("\t Accessing GitHub Rest API with GITHUB_TOKEN=[",GITHUB_TOKEN,"]")

if not GITHUB_TOKEN:
    raise ValueError("Please set the GITHUB_TOKEN in the config.ini file")



import requests
import json


import os
import xml.etree.ElementTree as ET

def check_file_exists(file_path):
    return os.path.isfile(file_path)

def is_valid_graphml(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        logger.debug(f"checking graphml file root tag {root.tag=}")

        # Check if the root tag is 'graphml'
        if  'graphml' in root.tag:
            return True
        return False
    except ET.ParseError:
        return False

def deanonymize_github_user(email):
    logger.info(f"deanonymizing github user for {email=}")

    if '@users.noreply.github.com' not in email:
        raise ValueError("The provided email address is not a valid GitHub noreply email.")

    # Extract the username part from the email
    #try:
    #    username = email.split('+')[1].split('@')[0]
    #except IndexError:
    #    raise ValueError("Unable to extract GitHub username from the email address.")

    # GitHub API URL for the user's profile
    url = f"https://api.github.com/users/jaateixeira"

    # Perform the API request
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        
        # Extracting affiliation/organization information
        affiliation = user_data.get('company', 'No affiliation/organization available')
        
        return {
            "username": username,
            "affiliation": affiliation,
            "profile_url": user_data.get("html_url"),
            "name": user_data.get("name", "Name not available"),
            "location": user_data.get("location", "Location not available"),
            "bio": user_data.get("bio", "Bio not available"),
        }
    else:
        raise ValueError(f"Failed to retrieve information for GitHub user: {username}")

# Example Usage
#email = "userID+username@users.noreply.github.com"
#try:
#    result = deanonymize_github_user(email)
#    print(json.dumps(result, indent=4))
#except ValueError as e:
#    print(e)


def print_all_nodes(network: nx.Graph):
    """
    Print all nodes in a NetworkX graph along with their attributes using rich for pretty formatting.

    Parameters:
    network (nx.Graph): The NetworkX graph.
    """

    logger.info(f"Printing all nodes in network {network=}:")
    
    if not isinstance(network, nx.Graph):
        raise TypeError("The input must be a NetworkX graph.")

    console = Console()
    table = Table(title="Nodes and Attributes")

    # Add columns to the table
    table.add_column("Node ID", style="bold cyan")
    table.add_column("Attributes", style="bold magenta")

    # Iterate over the nodes and their attributes
    for node, attributes in network.nodes(data=True):
        attr_str = ", ".join(f"{key}: {value}" for key, value in attributes.items())
        table.add_row(str(node), attr_str if attr_str else "None")

    # Print the table
    console.print(table)


    
def read_graphml_with_progress(file_path: str) -> nx.Graph:
    """
    Read a GraphML file and display a progress bar using rich.

    Parameters:
    file_path (str): The path to the GraphML file.

    Returns:
    nx.Graph: The NetworkX graph.
    """

    # Get the total size of the file
    total_size = os.path.getsize(file_path)
    
    # Initialize the progress bar
    with Progress() as progress:
        task = progress.add_task("[cyan]Reading file...", total=total_size)
        
        # Open the file for reading
        with open(file_path, "rb") as file:
            content = b""
            while not progress.finished:
                # Read a chunk of the file
                chunk = file.read(1024)  # 1 KB chunks
                if not chunk:
                    break
                # Update the progress bar
                progress.update(task, advance=len(chunk))
                # Append chunk to content
                content += chunk

    # Load the graph from the content
    # Convert bytes content to string
    content_str = content.decode('utf-8')
    # Use networkx to read the GraphML data from the string
    graph = nx.parse_graphml(content_str)

    # Print basic info about the graph
    console.print(f"Graph loaded: {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges", style="bold green")

    return graph


def read_graphml_fast(file_path: str) -> nx.Graph:
    return nx.read_graphml(file_path)

    

def copy_graph_with_attributes(source_graph: nx.Graph) -> nx.Graph:
    """
    Copy nodes, edges, and their attributes from the source graph to a new target graph.
    Both node attributes and edge attributes 

    Parameters:
    source_graph (nx.Graph): The source graph.

    Returns:
    nx.Graph: The new target graph with copied nodes, edges, and attributes.
    """
    target_graph = nx.Graph()

    # Copy nodes with attributes
    for node, attributes in source_graph.nodes(data=True):
        target_graph.add_node(node, **attributes)

    # Copy edges with attributes
    for u, v, attributes in source_graph.edges(data=True):
        target_graph.add_edge(u, v, **attributes)

    return target_graph

    
def iterate_graph(input_file, output_file):
    logger.info(f"Iterating network in file graph({input_file=} to copy to {output_file=} with  deanonymized github user emails")
    

    if not check_file_exists(input_file):
        logger.error(f"The file '{input_file}' does not exist.")
        sys.exit()
    else:
        logger.info (f"The file '{input_file}' to be copied and deanonymize  exist.")
    

    #if is_valid_graphml(input_file):
    #    logger.info(f"The file '{input_file}' is a valid GraphML file.")
    #else:
    #    logger.error(f"The file '{input_file}' is an invalid GraphML file.")
    #    sys.exit()



    # Read the input GraphML file
    logger.info(f"Reading input GraphML file: {input_file}")


    
    try:
        # Option 1) With the facing progress 
        # G = read_graphml_with_progress(input_file)

        # Option 2) Without the facing progress 
        G = read_graphml_fast(input_file)
        
        console.print("[green]Graph read successfully![/green]")
        # You can now work with the graph
        print(f"Number of nodes: {graph.number_of_nodes()}")
        print(f"Number of edges: {graph.number_of_edges()}")
    except Exception as e:
        console.print(f"[red]Failed to read the graph: {e}[/red]")
        


    # Create a new directed graph for the output
    G_copy = nx.Graph()


    #print_all_nodes(G)
    

  # Retrieve nodes and attributes
    nodes_data = G.nodes(data=True)

    table = Table(title="Nodes and Attributes")

    # Add columns to the table
    table.add_column("Node ID", style="bold cyan")
    table.add_column("Attributes", style="bold magenta")
    
    # Create a Live display
    with Live(table, console=console, refresh_per_second=3) as live:
        # Iterate over the nodes and their attributes
        for node, attributes in nodes_data:
            attr_str = ", ".join(f"{key}: {value}" for key, value in attributes.items())
            table.add_row(str(node), attr_str if attr_str else "None")
            live.update(table)



    logger.info(f"Coping node {G=} to {G_copy=}")
    G_copy=copy_graph_with_attributes(G)

    console.rule("Replacing emails and affiliations for each node using GitHub REST API")

    logger.info("Looking for @users.noreply.github.com emails to call the API")
    
    for node, data in G_copy.nodes(data=True):
        logger.debug("iterating over {node=}")
        
        console.print(f"Checking {node=} with {data['e-mail']=} and {data['affiliation']=}")

        old_email = data['e-mail']

        if '@users.noreply.github.com' in old_email:
            deanonymize_github_user(old_email)

    

            
    sys.exit()
    
        # Write the copied graph to the output GraphML file
    logger.info(f"Writing output GraphML file: {output_file}")
    nx.write_graphml(G_copy, output_file)

    console.print(f"[bold green]Successfully copied the graph to {output_file}[/bold green]")



def validate_input_file(input_file):
    # Check if the file has a .graphML extension
    if not input_file.lower().endswith('.graphml'):
        logger.error(f"Error: The input file '{input_file}' does not have a .graphML extension.")
        sys.exit(1)  # Exit the program with an error code
    
def main():

    #log_messages()
    #console_messages()
    #display_advanced_text()
    #display_emojis()
    #demonstrate_traceback_exceptions()
    #status_messages()
    #progress_bars_demo()
    
    parser = argparse.ArgumentParser(description="Creates a more correct GraphML file by  correcting e-mails and affiliations via the GitHub REST API.")




    # Add input file argument - a must one 
    parser.add_argument(
        'input', 
        type=str, 
        help='Path to the input GraphML file.'
    )
    
    # Add output file argument with default value 
    parser.add_argument(
        'output', 
        type=str, 
        nargs='?',  # This makes the argument optional
        default=None,  # Default is None, will be set based on input_file
        help='Path to the output file (default: input_file.out).'
    )
    
    args = parser.parse_args()

        # Validate input file
    validate_input_file(args.input)
    
    # Set default for output_file if not provided
    if args.output is None:
        # Generate default output file name
        base, ext = os.path.splitext(args.input)
        args.output_file = f"{base}.out.graphML"

    # Call the function to copy and modify the graph
    iterate_graph(args.input, args.output)

if __name__ == "__main__":
    main()


