# Your name: Debangi Mohanta
# Your student id: 65812361
# Your email: debangim@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute('SELECT name, rating, category_id, building_id FROM restaurants')
    bigtable = cur.fetchall()
    cur.execute('SELECT category, id FROM categories')
    categorytable= cur.fetchall()
    cur.execute('SELECT building, id FROM buildings')
    buildingstable = cur.fetchall()
    conn.commit()

    restaurant_dictionary = {}
    for the_tuple in bigtable:
        dict = {}
        for cat in categorytable:
            if cat[1] == the_tuple[2]:
                dict['category'] = cat[0]
                break
        for building in buildingstable:
            if building[1] == the_tuple[3]:
                dict['building'] = building[0]
                break
        dict['rating'] = the_tuple[1]
        restaurant_name = the_tuple[0]
        restaurant_dictionary[restaurant_name] = dict

    return restaurant_dictionary

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cur.execute('SELECT categories.category, categories.id FROM categories')
    categories = cur.fetchall()
    conn.commit()

    cur.execute('SELECT category_id, COUNT(*) as COUNT FROM restaurants GROUP BY CATEGORY_ID')
    number = cur.fetchall()
    conn.commit()

    restaurant_categories_dictionary = {}
    counter = 0
    for category in categories:
        restaurant_categories_dictionary[category[0]] = number[counter][1]
        counter += 1

    sorted_restaurant_categories_dictionary= dict(sorted(restaurant_categories_dictionary.items()))
    descending_restaurant_categories_dictionary = dict(sorted(restaurant_categories_dictionary.items(),key=lambda item: item[1],reverse=False))
    
    #bar chart
    restaurants = list(descending_restaurant_categories_dictionary.keys())
    count = list(descending_restaurant_categories_dictionary.values())

    plt.barh(restaurants, count, color=['darkblue'])
    plt.title('Types of Restaurant on South University Ave')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')
    plt.tight_layout()
    plt.show()

    return sorted_restaurant_categories_dictionary

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute('''SELECT r.name FROM restaurants r JOIN buildings b ON r.building_id = b.id WHERE b.building = ? ORDER BY r.rating DESC; ''', (building_num,))
    restaurant_names = [row[0] for row in cur.fetchall()]

    conn.close()

    return restaurant_names

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
