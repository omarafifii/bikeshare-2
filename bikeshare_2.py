import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city_letter = input("Please choose a city, \n For Chicago type: a \n For New York City type: b \n For Washington type: c\n ")

    while city_letter not in {'a','b','c'}:
        print("That's an invalid input")
        city_letter = input("Please choose a city, \n For Chicago type: a \n For New York City type: b \n For Washington type: c\n ").lower()
    
    if city_letter == 'a':
        city = 'chicago'
    elif city_letter == 'b':
        city = 'new york city'
    elif city_letter == 'c':
        city = 'washington'
        
    
    # get user input if he wants to filter by month or date or both or not at all
    time_frame = input('\n\nWould you like to filter {}\'s data by month, day, both, or not at all? \nType month or day or both or none: \n '.format(city.title())).lower()
    
    while time_frame not in {'month','day','both','none'}:
        print("That's an invalid input")
        time_frame = input('\n\nWould you like to filter {}\'s data by month, day, both, or not at all? \nType month or day or both or none: \n '.format(city.title())).lower()

    if time_frame == 'none':
        month, day = 'all', 'all'
    elif time_frame == 'month':
        month = get_month()
        day = 'all'
    elif time_frame == 'day':
        day = get_day()
        month = 'all'
    elif time_frame == 'both':
        month = get_month()
        day = get_day()



    print('-'*40)
    return city, month, day
    

def get_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by
        
    """

    month = input("Please enter a value between 1 and 6 to specify the month, \n For example if you want January enter: 1 \n ")

    while month not in {'1','2','3','4','5','6'}:
        print("That's an invalid input")
        month = input("Please enter a value between 1 and 6 to specify the month, \n For example if you want January enter: 1 \n ")

    return month


def get_day():
    """
    Asks user to specify a day to analyze.

    Returns:
        (str) day - name of the day to filter by
        
    """

    day = input("Please enter a value between 1 and 7 to specify the day, \n For Sunday enter: 1 \n For Monday enter: 2 \n and so on.. \n ")

    while day not in {'1','2','3','4','5','6','7'}:
        print("That's an invalid input")
        day = input("Please enter a value between 1 and 6 to specify the month, \n For example if you want January enter: 1 \n ")

    return day        
    

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, hour and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    

    # filter by month if applicable
    if month != 'all':
        

        # filter by month to create the new dataframe
        df = df[df['month'] == int(month)]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
        day = days[int(day)-1]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nMost common month: ' + str(df['month'].mode()[0]))
    

    # display the most common day of week
    print('\nMost common day: ' + str(df['day_of_week'].mode()[0]))
    

    # display the most common start hour
    print('\nMost common Start hour: ' + str(df['hour'].mode()[0]))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost common Start Station: ' + str(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nMost common End Station: ' + str(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('\nMost common combination of Start and End Station: ' + str(df.groupby(['Start Station','End Station']).size().idxmax()))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time in seconds: ' + str(df['Trip Duration'].sum()))

    # display mean travel time
    print('\nMean travel time in seconds: ' + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of users: \n' + str(df['User Type'].value_counts()))

    # Display counts of gender
    # only if city not washington
    if city != 'washington':
        print('\nCounts of gender: \n' + str(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('\nEarliest year of birth: ' + str(int(df['Birth Year'].min())))
        print('\nEarliest year of birth: ' + str(int(df['Birth Year'].max())))
        print('\nMost common year of birth: ' + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_5_rows(city):
    """
    Asks the user if they want to see 5 rows of data 
    if yes then it prints 5 rows and then asks the user again
    """
    print_5 = input("Would you like to see 5 rows of raw data? \n Type: yes or no \n ").lower()

    while print_5 not in {'yes','no'}:
        print("That's an invalid input")
        print_5 = input("Would you like to see 5 rows of raw data? \n Type: yes or no \n ").lower()

    if print_5 == 'no':
        return

    for chunk in pd.read_csv((CITY_DATA[city]), chunksize=5):
        print(chunk)
        print_5 = input("Would you like to see 5 more rows of raw data? \n Type: yes or no \n ").lower()

        while print_5 not in {'yes','no'}:
            print("That's an invalid input")
            print_5 = input("Would you like to see 5 more rows of raw data? \n Type: yes or no \n ").lower()

        if print_5 == 'no':
            break    

    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        print_5_rows(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
