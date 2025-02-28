import yaml

def load_config(filepath):
    """
    Reads a YAML configuration file and returns the data as a dictionary.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        dict: The configuration data as a dictionary, or None if an error occurs.
    """
    try:
        with open(filepath, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        print(f"Error: YAML file not found at {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {filepath}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    pass

print(load_config("C:\\Users\\mlohi\\Documents\\GitHub\\deployment-demo\\config\\dev.yml"))