"""

MIT License

Copyright (c) 2025 ignViral

This is a standalone wrapper for the Jailbreak Trading API.
This file can be copy and pasted directly into a new location and it will function fine.

** Values are based on the JBValues API **

"""

import requests
import json
import time

class JBValuesAPI:
    def __init__(self, cache_duration=3600):
        """
        Initialize the JB Values API wrapper
        
        Args:
            cache_duration (int): How long to cache the API data in seconds (default: 1 hour)
        """
        self.api_url = "https://jbvalues.com/api/itemdata/"
        self.data = {}
        self.last_fetch_time = 0
        self.cache_duration = cache_duration
    
    def fetch_api_data(self):
        """
        Fetch the latest data from the JB Values API
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            self.data = response.json()
            self.last_fetch_time = time.time()
            return True
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching API data: {e}")
            return False
    
    def ensure_fresh_data(self):
        """
        Ensure we have fresh data, fetching from API if needed
        
        Returns:
            bool: True if data is available, False otherwise
        """
        current_time = time.time()
        if current_time - self.last_fetch_time > self.cache_duration or not self.data:
            return self.fetch_api_data()
        return True

    def get_latest_value(self, name):
        """
        Get the latest value of a vehicle customization by its name
        
        Args:
            name (str): The name of the customization (case insensitive)
            
        Returns:
            int: The latest value in integer format, or 0 if not found
        """
        if not self.ensure_fresh_data():
            print("Warning: Using potentially outdated data")
            if not self.data:
                return 0
        
        if not name:
            return 0
        
        # Normalize the search name to lowercase for case-insensitive comparison
        search_name = name.lower()
        
        # First try exact match
        for item_key, item in self.data.items():
            if item.get('name') and item['name'].lower() == search_name:
                return item['value']
        
        # If no exact match, try contains match
        for item_key, item in self.data.items():
            if item.get('name') and search_name in item['name'].lower():
                return item['value']
        
        return 0
    
    def get_all_customization_names(self):
        """
        Get all available customization names
        
        Returns:
            list: Array of all customization names
        """
        if not self.ensure_fresh_data():
            print("Warning: Using potentially outdated data")
            if not self.data:
                return []
        
        return [item['name'] for item in self.data.values() if item.get('name')]
    
    def get_customization_details(self, name):
        """
        Get detailed information about a customization by name
        
        Args:
            name (str): The name of the customization (case insensitive)
            
        Returns:
            dict or None: Full customization data or None if not found
        """
        if not self.ensure_fresh_data():
            print("Warning: Using potentially outdated data")
            if not self.data:
                return None
        
        if not name:
            return None
        
        search_name = name.lower()
        
        # First try exact match
        for item_key, item in self.data.items():
            if item.get('name') and item['name'].lower() == search_name:
                return item
        
        # If no exact match, try contains match
        for item_key, item in self.data.items():
            if item.get('name') and search_name in item['name'].lower():
                return item
        
        return None
    
    def print_categories(self):
        """Print all available categories in the JB Values data"""
        if not self.ensure_fresh_data():
            print("Warning: Using potentially outdated data")
            if not self.data:
                return
        
        categories = set()
        for item in self.data.values():
            if item.get('badimoCategory'):
                categories.add(item['badimoCategory'])
        
        print("Available categories:")
        for category in sorted(categories):
            print(f"- {category}")


def get_vehicle_value(name):
    """
    Get the latest value for any vehicle customization by name
    
    Args:
        name (str): Name of the vehicle customization
        
    Returns:
        int: The latest value in integer format
    """
    api = JBValuesAPI()
    return api.get_latest_value(name)