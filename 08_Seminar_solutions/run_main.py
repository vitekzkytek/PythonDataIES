
import json
import yaml

import logging

from src.processing import (
    request_meals_starting_w_letter,
    remove_prefix_until_capital_letter,
    clear_meal_attribute_names,
    get_meals,
    process_meals
)

if __name__ == "__main__":

    # set up logging
    logging.basicConfig(format = '%(asctime)s %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        filename = 'logs/run_main.log',
                        level=logging.INFO)
                        
    # load config - contains variables parametrizing runs 
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    logging.info(f'Loaded config with following contents: {config}')

    # load raw data from API
    meals_raw = get_meals(letters = config['letters'])
    logging.info(f'Loaded unprocessed (raw) meals information.')

 
    with open(config['raw_path'], 'w') as f:
        json.dump(meals_raw, f)
    logging.info(f"Saved unprocessed meals info to {config['raw_path']}")


    meals_processed = process_meals(meals_raw = meals_raw)
    logging.info(f'Processed meals.')

    with open(config['processed_path'], 'w') as f:
        json.dump(meals_processed, f)
    logging.info(f"Saved processed meals to {config['processed_path']}")






    
    


    