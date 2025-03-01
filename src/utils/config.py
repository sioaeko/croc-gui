import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = os.path.join(str(Path.home()), ".siro")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.history_file = os.path.join(self.config_dir, "history.json")
        
        # Default configuration
        self.default_config = {
            "theme": "dark",
            "last_directory": str(Path.home()),
            "save_directory": str(Path.home()),
            "relay_server": "https://croc.schollz.com:9009",
            "max_history": 100
        }
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize history if it doesn't exist
        if not os.path.exists(self.history_file):
            self.save_history([])
    
    def load_config(self):
        """Load configuration from file or create default if it doesn't exist"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.default_config
        else:
            # Create default config
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config
    
    def get_config(self):
        """Get the entire configuration"""
        return self.config
    
    def get_value(self, key, default=None):
        """Get a specific configuration value"""
        return self.config.get(key, default)
    
    def set_value(self, key, value):
        """Set a specific configuration value and save"""
        self.config[key] = value
        self.save_config(self.config)
    
    def get_theme(self):
        """Get the current theme"""
        return self.get_value("theme", "dark")
    
    def set_theme(self, theme):
        """Set the current theme"""
        self.set_value("theme", theme)
    
    def load_history(self):
        """Load transfer history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_history(self, history):
        """Save transfer history"""
        # Limit history size
        max_history = self.get_value("max_history", 100)
        if len(history) > max_history:
            history = history[-max_history:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=4)
    
    def add_history_entry(self, entry):
        """Add an entry to the transfer history"""
        history = self.load_history()
        history.append(entry)
        self.save_history(history) 