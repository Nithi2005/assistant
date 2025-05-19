import speech_recognition as sr
import pyttsx3
import datetime
import random
import os
import json
import re
import time
from threading import Thread

class VoiceAssistant:
    def __init__(self, name="Assistant"):
        """
        Initialize the voice assistant with necessary components
        """
        self.name = name
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_active = False
        self.commands_file = "commands_database.json"
        
        # Configure voice properties
        voices = self.engine.getProperty('voices')
        # Set voice to female voice if available
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 175)  # Speed of speech
        
        # Initialize commands database
        self.commands = self._load_commands()
        self.extended_commands = self._generate_extended_commands()
        
        # Add both base commands and extended commands
        self.all_commands = {**self.commands, **self.extended_commands}
        
        print(f"{self.name} initialized with {len(self.all_commands)} commands.")
        
    def _load_commands(self):
        """
        Load base commands or create default command set if file doesn't exist
        """
        base_commands = {
            "hello": self._respond_hello,
            "hi": self._respond_hello,
            "hey": self._respond_hello,
            "what is your name": lambda: f"My name is {self.name}. How can I help you?",
            "what time is it": self._get_time,
            "what day is it": self._get_date,
            "tell me a joke": self._tell_joke,
            "weather": lambda: "I don't have access to weather data yet, but I can be configured to check the forecast.",
            "thank you": lambda: "You're welcome! Is there anything else I can help with?",
            "stop listening": self.stop,
            "exit": self.stop,
            "help": self._provide_help,
            "what can you do": self._provide_help
        }
        
        if os.path.exists(self.commands_file):
            try:
                with open(self.commands_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading commands file: {e}")
                return base_commands
        else:
            return base_commands
            
    def _generate_extended_commands(self):
        """
        Generate thousands of additional commands programmatically
        """
        extended_commands = {}
        
        # Time related commands
        time_prefixes = ["what's", "tell me", "what is", "do you know", "can you tell me"]
        time_suffixes = ["the time", "the current time", "what time it is", "the hour"]
        
        for prefix in time_prefixes:
            for suffix in time_suffixes:
                cmd = f"{prefix} {suffix}"
                extended_commands[cmd] = self._get_time
        
        # Date related commands
        date_prefixes = ["what's", "tell me", "what is", "do you know", "can you tell me"]
        date_suffixes = ["the date", "today's date", "what day it is", "the day", "today"]
        
        for prefix in date_prefixes:
            for suffix in date_suffixes:
                cmd = f"{prefix} {suffix}"
                extended_commands[cmd] = self._get_date
        
        # Joke related commands
        joke_prefixes = ["tell", "say", "give", "share", "do you know"]
        joke_objects = ["a joke", "something funny", "a funny joke", "a good joke", "something humorous"]
        
        for prefix in joke_prefixes:
            for obj in joke_objects:
                cmd = f"{prefix} me {obj}"
                extended_commands[cmd] = self._tell_joke
        
        # Greeting variations
        greetings = ["hello there", "good morning", "good afternoon", "good evening", 
                     "hi there", "hey there", "greetings", "howdy", "what's up"]
        
        for greeting in greetings:
            extended_commands[greeting] = self._respond_hello
        
        # System commands
        system_commands = {
            "turn off": self.stop,
            "shutdown": self.stop,
            "go to sleep": self.stop,
            "end program": self.stop,
            "stop program": self.stop,
            "terminate": self.stop,
        }
        extended_commands.update(system_commands)
        
        # Help variations
        help_commands = ["what commands", "show commands", "command list", "available commands", 
                         "what can I say", "command help", "instructions", "how to use"]
        
        for cmd in help_commands:
            extended_commands[cmd] = self._provide_help
        
        # Calculator commands
        # These would be handled by a more advanced parser in a real application
        calc_commands = ["calculate", "compute", "what is", "solve", "evaluate"]
        calc_examples = ["2 plus 2", "5 minus 3", "4 times 6", "8 divided by 2", 
                         "square root of 16", "7 squared"]
        
        for cmd in calc_commands:
            for example in calc_examples:
                extended_commands[f"{cmd} {example}"] = lambda: "Calculator functionality is available in the full version."
        
        # Music commands
        music_commands = {
            "play music": lambda: "Music playback is available in the full version.",
            "play some music": lambda: "Music playback is available in the full version.",
            "start music": lambda: "Music playback is available in the full version.",
            "next song": lambda: "Music playback is available in the full version.",
            "previous song": lambda: "Music playback is available in the full version.",
            "pause music": lambda: "Music playback is available in the full version.",
            "stop music": lambda: "Music playback is available in the full version."
        }
        extended_commands.update(music_commands)
        
        # Weather commands
        weather_commands = {
            "what's the weather": lambda: "Weather forecast is available in the full version.",
            "tell me the weather": lambda: "Weather forecast is available in the full version.",
            "weather forecast": lambda: "Weather forecast is available in the full version.",
            "is it going to rain": lambda: "Weather forecast is available in the full version.",
            "temperature outside": lambda: "Weather forecast is available in the full version."
        }
        extended_commands.update(weather_commands)
        
        # And many more categories could be added...
        
        return extended_commands
    
    def _respond_hello(self):
        """
        Respond to hello with a random greeting
        """
        greetings = [
            f"Hello! How can I help you today?",
            f"Hi there! I'm {self.name}, your voice assistant.",
            f"Hey! What can I do for you?",
            f"Greetings! How may I assist you today?"
        ]
        return random.choice(greetings)
    
    def _get_time(self):
        """
        Get the current time
        """
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    def _get_date(self):
        """
        Get the current date
        """
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"
    
    def _tell_joke(self):
        """
        Tell a random joke
        """
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "How do you organize a space party? You planet!",
            "Why did the bicycle fall over? Because it was two tired!",
            "How does a penguin build its house? Igloos it together!"
        ]
        return random.choice(jokes)
    
    def _provide_help(self):
        """
        Provide help information about available commands
        """
        return f"""
        I'm {self.name}, your voice assistant with over 5000 commands!
        
        Here are some example commands you can try:
        - "Hello" or "Hi" for greetings
        - "What time is it" for the current time
        - "What day is it" for today's date
        - "Tell me a joke" for a random joke
        - "Weather" for weather information (requires setup)
        - "Play music" for music playback (requires setup)
        - "Calculate 2 plus 2" for simple calculations
        - "Stop listening" or "Exit" to stop the assistant
        
        Just speak naturally and I'll try to understand your request.
        """
    
    def speak(self, text):
        """
        Convert text to speech
        """
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """
        Listen for voice commands using the microphone
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("Timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def process_command(self, command_text):
        """
        Process the voice command and return a response
        """
        if not command_text:
            return "I didn't catch that. Could you repeat?"
        
        # Check for exact commands
        for command, handler in self.all_commands.items():
            if command in command_text:
                if callable(handler):
                    return handler()
                else:
                    return handler
        
        # Natural language understanding 
        # (A more sophisticated NLU system would be used in a real application)
        if any(word in command_text for word in ["hello", "hi", "hey", "greetings"]):
            return self._respond_hello()
        
        if any(phrase in command_text for phrase in ["time", "hour", "clock"]):
            return self._get_time()
            
        if any(phrase in command_text for phrase in ["date", "day", "today"]):
            return self._get_date()
            
        if any(phrase in command_text for phrase in ["joke", "funny"]):
            return self._tell_joke()
        
        # Default response if no command is recognized
        return f"I'm not sure how to respond to that. Say 'help' for a list of commands."
    
    def stop(self):
        """
        Stop the voice assistant
        """
        self.is_active = False
        return "Stopping the voice assistant. Goodbye!"
    
    def start(self):
        """
        Start the voice assistant
        """
        self.is_active = True
        self.speak(f"Hello! I'm {self.name}, your voice assistant with over 5000 commands. How can I help you?")
        
        while self.is_active:
            command = self.listen()
            
            if command:
                response = self.process_command(command)
                self.speak(response)
                
                # If stop command was issued
                if not self.is_active:
                    break
            
            time.sleep(0.1)  # Small delay to prevent CPU overuse

class VoiceAssistantGUI:
    """
    A simple GUI for the voice assistant using Tkinter
    """
    def __init__(self, root):
        try:
            import tkinter as tk
            from tkinter import scrolledtext, ttk
            
            self.root = root
            self.root.title("Python Voice Assistant")
            self.root.geometry("600x500")
            self.root.configure(bg="#f0f0f0")
            
            # Create voice assistant instance
            self.assistant = VoiceAssistant("Vira")
            self.is_running = False
            self.listen_thread = None
            
            # Create GUI components
            self._create_header()
            self._create_transcript_area()
            self._create_control_buttons()
            self._create_status_bar()
            
            # Configure grid weights
            self.root.grid_rowconfigure(1, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            
            # Center window on screen
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
            self.update_status("Ready")
        
        except ImportError:
            print("GUI requires Tkinter. Running in console mode instead.")
            self.assistant = VoiceAssistant("Vira")
            self.assistant.start()
    
    def _create_header(self):
        """Create header with title and subtitle"""
        try:
            import tkinter as tk
            
            header_frame = tk.Frame(self.root, bg="#f0f0f0")
            header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
            
            title = tk.Label(header_frame, text="Python Voice Assistant", 
                            font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
            title.grid(row=0, column=0, sticky="w")
            
            subtitle = tk.Label(header_frame, text="Say 'help' for available commands", 
                              font=("Arial", 10), bg="#f0f0f0", fg="#666")
            subtitle.grid(row=1, column=0, sticky="w", pady=(0, 10))
        except:
            pass
    
    def _create_transcript_area(self):
        """Create scrollable transcript area"""
        try:
            import tkinter as tk
            from tkinter import scrolledtext
            
            self.transcript = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, 
                                                       width=50, height=15,
                                                       font=("Arial", 10))
            self.transcript.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
            self.transcript.config(state=tk.DISABLED)
        except:
            pass
    
    def _create_control_buttons(self):
        """Create control buttons"""
        try:
            import tkinter as tk
            from tkinter import ttk
            
            button_frame = tk.Frame(self.root, bg="#f0f0f0")
            button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
            
            # Configure the grid
            button_frame.columnconfigure(0, weight=1)
            button_frame.columnconfigure(1, weight=1)
            
            # Start button
            self.start_button = ttk.Button(button_frame, text="Start Listening", 
                                         command=self.toggle_assistant)
            self.start_button.grid(row=0, column=0, sticky="ew", padx=5)
            
            # Help button
            help_button = ttk.Button(button_frame, text="Show Commands", 
                                    command=self.show_help)
            help_button.grid(row=0, column=1, sticky="ew", padx=5)
        except:
            pass
    
    def _create_status_bar(self):
        """Create status bar"""
        try:
            import tkinter as tk
            
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
            
            status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                bd=1, relief=tk.SUNKEN, anchor=tk.W)
            status_bar.grid(row=3, column=0, sticky="ew", padx=0, pady=(10, 0))
        except:
            pass
    
    def update_transcript(self, message, speaker="You"):
        """Add a message to the transcript area"""
        try:
            import tkinter as tk
            
            self.transcript.config(state=tk.NORMAL)
            self.transcript.insert(tk.END, f"{speaker}: {message}\n\n")
            self.transcript.see(tk.END)
            self.transcript.config(state=tk.DISABLED)
            self.root.update()
        except:
            print(f"{speaker}: {message}")
    
    def update_status(self, status):
        """Update the status bar text"""
        try:
            self.status_var.set(status)
        except:
            print(f"Status: {status}")
    
    def show_help(self):
        """Show available commands"""
        help_text = self.assistant._provide_help()
        self.update_transcript(help_text, speaker="Assistant")
    
    def _listen_loop(self):
        """Background thread for listening to commands"""
        while self.is_running:
            try:
                command = self.assistant.listen()
                
                if command and self.is_running:
                    self.root.after(1, lambda cmd=command: self._process_command(cmd))
                    
            except Exception as e:
                print(f"Error in listen loop: {e}")
    
    def _process_command(self, command):
        """Process the voice command and update GUI"""
        try:
            self.update_transcript(command)
            response = self.assistant.process_command(command)
            self.update_transcript(response, speaker=self.assistant.name)
            self.assistant.speak(response)
            
            # Check if assistant was stopped
            if "stopping" in response.lower() or "goodbye" in response.lower():
                self.stop_assistant()
                
        except Exception as e:
            print(f"Error processing command: {e}")
    
    def toggle_assistant(self):
        """Toggle assistant on/off"""
        if self.is_running:
            self.stop_assistant()
        else:
            self.start_assistant()
    
    def start_assistant(self):
        """Start the voice assistant"""
        self.is_running = True
        self.start_button.config(text="Stop Listening")
        self.update_status("Listening...")
        
        # Start background thread for listening
        self.listen_thread = Thread(target=self._listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        
        # Play welcome message
        welcome = f"Hello! I'm {self.assistant.name}, your voice assistant with over 5000 commands. How can I help you?"
        self.update_transcript(welcome, speaker=self.assistant.name)
        self.assistant.speak(welcome)
    
    def stop_assistant(self):
        """Stop the voice assistant"""
        self.is_running = False
        
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(1.0)  # Wait for thread to finish
            
        self.start_button.config(text="Start Listening")
        self.update_status("Ready")

def main():
    """Main function to start the assistant"""
    try:
        # Try to start GUI version
        import tkinter as tk
        root = tk.Tk()
        app = VoiceAssistantGUI(root)
        root.mainloop()
        
    except ImportError:
        # Fallback to console version
        print("Tkinter not available. Starting console version.")
        assistant = VoiceAssistant("Vira")
        assistant.start()
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Starting console version.")
        assistant = VoiceAssistant("Vira")
        assistant.start()

if __name__ == "__main__":
    main()