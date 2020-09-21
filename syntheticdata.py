import csv
from random import randint, choice, randrange
import datetime
import urllib.request
import json


def load_type_generator():
    random_value = randint(0, 1)
    loads = ('Cement', 'Asphalt')
    return loads[random_value]


delivery_ids = []


def delivery_id_generator():
    abcd = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_value = randint(10000, 99999)
    first_letter = choice(abcd)
    second_letter = choice(abcd)
    delivery_id = first_letter + second_letter + str(random_value)
    return delivery_id


def unique_delivery_id():
    delivery_id = delivery_id_generator()
    if delivery_id in delivery_ids:
        unique_delivery_id()
    else:
        delivery_ids.append(delivery_id)
        return delivery_id


def scheduled_arrival_generator():
    random_value = randint(1, 30)
    date = datetime.datetime(2020, 9, random_value).date()
    time = datetime.timedelta(minutes=randrange(1439))
    return date, time

def postcode_generator():
    postcodes = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16',
                 'E17', 'E18', 'E19', 'E20', 'SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8', 'SE9', 'SE10',
                 'SE11',
                 'SE12', 'SE13', 'SE14', 'SE15', 'SE16', 'SE17', 'SE18', 'SE19', 'SE20', 'SE21', 'SE22', 'SE23', 'SE24',
                 'SE25', 'SE26', 'SE27', 'SE28', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11',
                 'N12',
                 'N13', 'N14', 'N15', 'N16', 'N17', 'N18', 'N19', 'N20', 'N21', 'N22', 'WC1', 'WC2', 'EC1', 'EC2',
                 'EC3',
                 'EC4', 'SW1', 'SW2', 'SW3', 'SW4', 'SW5', 'SW6', 'SW7', 'SW8', 'SW9', 'SW10', 'SW11', 'SW12', 'SW13',
                 'SW14', 'SW15', 'SW16', 'SW17', 'SW18', 'SW19', 'SW20', 'NW1', 'NW2', 'NW3', 'NW4', 'NW5', 'NW6',
                 'NW7',
                 'NW8', 'NW9', 'NW10', 'NW11', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11',
                 'W12',
                 'W13', 'W14']
    abcd = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    postcode = choice(postcodes) + str(randint(0, 9)) + choice(abcd) + choice(abcd)

    if postcode_validator(postcode) is True:
        return postcode
    else:
        postcode = postcode_generator()
        return postcode


def postcode_validator(postcode):
    postcode_url_validator = "http://api.postcodes.io/postcodes/" + str(postcode) + "/validate"

    with urllib.request.urlopen(postcode_url_validator) as response:
        postcode_js = json.load(response)
        if postcode_js['result'] is True:
            return True
        else:
            return False


def starting_location_generator():
    random_value = randint(0, 1)
    postcodes = ('SW83HE', 'WC1E7JE')
    return postcodes[random_value]


def predicted_load_status():
    random_value = randint(0, 5)
    statues = ('Danger', 'Warning', 'Warning', 'Safe', 'Safe', 'Safe')
    return statues[random_value]


with open('deliveries.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['id', 'Delivery id', 'LoadType', 'Date', 'Time', "StartingLocation", "Destination", "Effectiveness"])
    for delivery in range(1, 20000):
        filewriter.writerow([delivery, delivery_id_generator(), load_type_generator(), scheduled_arrival_generator()[0],scheduled_arrival_generator()[1],
                             starting_location_generator(), postcode_generator(), predicted_load_status()])



