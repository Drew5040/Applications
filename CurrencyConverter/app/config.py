from json import dump, load, JSONDecodeError
from os import getenv, makedirs
from os.path import join, exists
from logs import log_error


def save_api_key(api_key_var, remember_var):
    """
        Save the API key to a configuration file if the 'Remember API Key' checkbox is checked.

        Parameters:
        - api_key_var (tk.StringVar): The Tkinter variable holding the API key.
        - remember_var (tk.BooleanVar): The Tkinter variable representing the state of the 'Remember API Key' checkbox.

        Example:
        api_key_var = tk.StringVar()
        remember_var = tk.BooleanVar()
        api_key_var.set('your_api_key')
        remember_var.set(True)
        save_api_key(api_key_var, remember_var)

        """
    # Check for remember_var
    if remember_var.get():

        # Determine the path to the configuration file in the AppData folder
        appdata_folder = join(getenv('APPDATA'), "Anwoo's Currency Converter Tool")

        # Ensure the folder exists or create it
        if not exists(appdata_folder):
            makedirs(appdata_folder)

        config_file_path = join(appdata_folder, 'config.json')
        # Open JSON file as config_file
        print(config_file_path)
        with open(config_file_path, 'w') as config_file:
            # Retrieve the API-Key from Tkinter variable
            api_key = api_key_var.get()
            # Create a dict with api_key as value
            config = {'API-KEY': api_key}
            # Write the dict to file in JSON format
            dump(config, config_file)


def load_api_key():
    """
       Load the API key from the 'config.json' file.

       Returns:
       str or None: The loaded API key if the file exists and contains a valid API key, None otherwise.

       Example:
       api_key = load_api_key()
       if api_key:
            print(f"Loaded API key: {api_key}")
       else:
            print("No API key found in 'config.json'.")

       """
    try:
        # Determine the path to the configuration file in the AppData folder
        appdata_folder = join(getenv('APPDATA'), "Anwoo's Currency Converter Tool")
        config_file_path = join(appdata_folder, 'config.json')

        # Attempt to open the 'config.json' file
        with open(config_file_path) as config_file:
            # Load contents of the file as a JSON object
            config = load(config_file)
            # Retrieve API key
            api_key = config.get('API-KEY')
            # Return API key
            return api_key
        # Handle possible exceptions
    except (FileNotFoundError, JSONDecodeError) as e:
        # Log error
        log_error(type(e).__name__, str(e))

        return None
