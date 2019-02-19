import time
import pandas as pd
import numpy as np
from datetime import datetime as dt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hi There!\nThis script will analyse data provided by Motivate to compare the Bikeshare system usage over the first 6 months of 2017 across the three following cities: \n -Chicago \n -New York City \n -Washington, DC \n')

    # Valid input lists

    city_list = ['chicago', 'new york', 'washington']

    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday', 'all']


    # TO DO:get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Would you like to see data for Chicago, New York, or Washington?:\n").lower()


    # while loop to handle invalid user input for city name

    while city not in city_list:
        city = input("Enter a valid city name to analyse (Chicago, New York City, Washington):\n").lower()


    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('For which month would you like to filter the data by - January, February, March, April, May or June?\nPlease enter "all" if you would like to apply no month filter:\n').lower()


    # while loop to handle invalid user input for month name

    while month not in month_list:
        month = input(" Please enter a valid month name - January, February, March, April, May, June or all:\n").lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('For which day of the week would you like to filter the data by -Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \nPlease enter "all" if you would like to apply no day filter: \n').lower()

    # while loop to handle invalid user input for day name

    while day not in day_list:
        day = input("Please enter a valid day name -Monday, Tuesday, Wednesday, Thursday, Friday, Saturday,Sunday or all:\n").lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

   # load data file into a dataframe

    df = pd.read_csv(CITY_DATA[city])

  # ask user if they would like to see 5 line of raw data

    print('\nWould you like to see randomly selected five lines of raw data? Please enter Yes or No')

    while True:
        answer_raw = input()
        if answer_raw.lower() == 'yes':
            print(df.sample(n=5))
            print('\nWould you like to see 5 more randomly selected raw data? Enter yes or no.')

        if answer_raw.lower() != 'yes':
            print(df)
            break

    # convert the Start Time and End time columns to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # TO DO: display the most common month

    print('Most Common Month: ', df['month'].mode()[0])

    # TO DO: display the most common day of week

    print('Most Common Day: ', df['day_of_week'].mode()[0])


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most Common Hour: ',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    print('Most Popular Start Station: ', df['Start Station'].mode()[0])
    print()

    # TO DO: display most commonly used end station

    print('Most Popular End Station: ', df['End Station'].mode()[0])
    print()

    # TO DO: display most frequent combination of start station and end station trip


    df['Start and End'] = '(Start) ' + df['Start Station'] + ' (End) ' + df['End Station'] # create a new column to display the combination of  start  and end stations

    combi = df['Start and End'].value_counts().index[0] # returns sorted Series (descending)
    occurances = df['Start and End'].value_counts().iloc[0] # returns sorted Series (descending)
    print('Trip: {} occurances of {}'.format(occurances, combi))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    df['TTT'] = df['End Time'] - df['Start Time']
    total_travel_time = df['TTT'].sum() # datetime.timedelta object, displays as 'X days XX:XX:XX.XXXXXX'

    print('Total Travel Time = ', total_travel_time)

    print()

    # TO DO: display mean travel time

    print('Mean Travel Time = ', df['TTT'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    print('User Types:\n',df['User Type'].value_counts())

    print()


    # TO DO: Display counts of gender

    # Since the gender data is only available for NYC and Chicago, we need to specify an exception to handle
    # KeyError that may occur when user want to see Washington results

    try:
        df['Gender'].value_counts()
        print('Gender:\n',df['Gender'].value_counts())

    except KeyError:
        if CITY_DATA == 'Washington'.lower():
            pass
        print("The gender data are unfortunatelynot available for Washington.")

    print()


    # TO DO: Display earliest, most recent, and most common year of birth

    # Since the birth data is only available for NYC and Chicago, we need to specify an exception to handle
    # KeyError for  Washington

    try:
        current_year = dt.now().year
        age = current_year - df['Birth Year'].mode()[0]
        print('Most Common Year of Birth: ', int(age))
        print()
        age = current_year - df['Birth Year'].min()
        print('Earliest Year of Birth: ' + str(int(age)))
        print()
        age = current_year - df['Birth Year'].max()
        print('Most Recent Year of Birth: ' + str(int(age)))
        print()

    except KeyError:
        if CITY_DATA == 'Washington'.lower():
            pass
        print("The birth data are unfortunatelynot available for Washington.")

    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
