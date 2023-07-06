# Author: brad anderson jr
# Contact: brad@bradandersonjr.com
# Description: An add-in for Fusion 360 that allows you to search YouTube for Fusion 360 videos
# Version: 1.0

import adsk.core, adsk.fusion, traceback, webbrowser

handlers = []  # Create an empty list to hold the handlers

class ButtonCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    
    def notify(self, args):
        try:
            command = args.command
            onExecute = ButtonCommandExecuteHandler(self.ui)
            command.execute.add(onExecute)
            handlers.append(onExecute)  # Add the onExecute handler to the handlers list
        except:
            self.show_error_message(self.ui, traceback.format_exc())

    def show_error_message(self, ui, message):
        ui.messageBox(message)

class ButtonCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def notify(self, args):
        try:
            result = self.ui.inputBox("Fusion 360 Topic:", "Search Fusion 360 Videos on YouTube", "example: 'Extrude Feature'")

            # Retrieve the input value
            topic = result[0]  # Get the first element

            # Example: Perform a YouTube search based on the topic
            search_url = f"https://www.youtube.com/results?search_query=Fusion+360+{topic}"
            webbrowser.open(search_url)
            
        except:
            self.show_error_message(self.ui, traceback.format_exc())

    def show_error_message(self, ui, message):
        ui.messageBox(message)

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Delete existing command definition if it exists
        if ui.commandDefinitions.itemById('SearchYouTubeID'):
            ui.commandDefinitions.itemById('SearchYouTubeID').deleteMe()

        qatRToolbar = ui.toolbars.itemById('QATRight')
        buttonDefinition = ui.commandDefinitions.addButtonDefinition('SearchYouTubeID', 'Search Fusion 360 Videos on YouTube', '', './resources')

        onButtonCommandCreated = ButtonCommandCreatedHandler(ui)
        buttonDefinition.commandCreated.add(onButtonCommandCreated)
        handlers.append(onButtonCommandCreated)  # Add the onButtonCommandCreated handler to the handlers list

        status = qatRToolbar.controls.addCommand(buttonDefinition, 'HealthStatusCommand', False)

    except:
        ui.messageBox(traceback.format_exc())

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        qatRToolbar = ui.toolbars.itemById('QATRight')
        cmd = qatRToolbar.controls.itemById('SearchYouTubeID')
        if cmd:
            cmd.deleteMe()

    except:
        ui.messageBox(traceback.format_exc())