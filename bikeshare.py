import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago','new york city','washington']
months = ['january','february','march','april','may','june']
dow = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print()
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    print('We have data for Chicago, New York City and Washington.')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("What city will you like to explore? ")).lower()
        if city not in cities:
            print("Entered city is invalid or not in the list. ")
            confirmation = input("Would you like to retry? Type yes or no to exit: ")
            if confirmation == 'yes':
                continue
            else:
                sys.exit()
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Enter a month between January through June or all to view all months: ")).lower()
        if (month not in months and month != 'all'):
            print("You've entered an invalid month or one which data is unavailable, Try again. ")
            confirmation = input("Would you like to retry? Type yes or no to exit: ")
            if confirmation == 'yes':
                continue
            else:
                sys.exit()
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("What day of the week do you require data? e.g. all, monday: ")).lower()
        if (day not in dow and day != 'all'):
            print("You've entered an invalid day, Try again. ")
            confirmation = input("Would you like to retry? Type yes or no to exit: ")
            if confirmation == 'yes':
                continue
            else:
                sys.exit()
        else:
            break

    print("\nYou have chosen to see details of {} for month: {} and day:{}".format(city.title(),month.title(),day.title()))


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    # at this point the df contains all the data without any filter

    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'] == day.title()]

    return df
#function to capitalize first letter of city

def time_stats(df):

    """\nDisplays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['Month'].mode()[0]
    print("The most common month for Bikeshare in this city is: {} \n".format(popular_month))
    
    # TO DO: display the most common day of week
    popular_day = df['Day_of_week'].mode()[0]
    print("The most common day of the week for Bikeshare in this city is: {} \n".format(popular_day))

    # TO DO: display the most common start hour
    df['Hours'] = df['Start Time'].dt.hour
    popular_start = df['Hours'].mode()[0]
    print("The most common start hour for Bikeshare in this city is: {} \n".format(popular_start))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """\nDisplays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print("The most popular start station for Bikeshare in this city is: {} \n".format(popular_station))

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most popular end station for Bikeshare in this city is: {} \n".format(popular_end))

    # TO DO: display most frequent combination of start station and end station trip
    # creat a df for each combination of start and end stations
    new_df = pd.DataFrame(df['Start Station'] + "," + df['End Station'] , columns = ['new'])
    start,end = new_df['new'].mode()[0].split(",")
    print("The most popular stations to start and end in this city are '{}' and '{}' respectively \n".format(start,end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):

    """\nDisplays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['End Time'] = pd.to_datetime(df['End Time'])
    # creates a new column that stores difference of each trip's start and end time
    df['diff'] = (df['End Time'] - df['Start Time'])#/np.timedelta64(1,'s')
    total_time = df['diff'].sum()
    print("The total trip duration is: {} ".format(total_time))

    # TO DO: display mean travel time
    average_time = df['diff'].mean()
    print("The average trip duration is: {} ".format(average_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """\nDisplays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Details of user types for in this city is:\n{}".format(user_types))

    # TO DO: Display counts of gender
    if city == 'Washington':
        print("\nThere are no gender details available for Washington\n")
    else:
        gender = df['Gender'].value_counts()
        print("\nCount of users in {} based on gender:\n {}".format(city,gender))
    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'Washington':
        print("There are no date of birth details for Washington\n")
    else:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("\nFind below details about the year of birth of users in {}:\n".format(city))
        print()
        print("The oldest user(s) was/were born in: {}\n".format(earliest_year))
        print()
        print("The youngest user(s) was/were born in: {}\n".format(recent_year))
        print()
        print("Most users were born in: {}\n".format(common_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function that loops through df returning 5 records
def five_rows(df):
    """ Function that recturns five records from the dataframe """
    # start of index
    i = 0
    # end of index
    n = 5
    while True:
        try:
            raw_data = int(input("\nWould you like to view 5 lines of raw data? Enter 1 to view data or 0 to exit.\n"))
            if raw_data != 1:
                break
            else:
                #prints all columns and rows from i to n
                print(df[:][i:n])
                i += 5
                n += 5
        except:
            print("Oops!, you entered an invalid value, Try again ")
            continue

def main():
     while True:
        global city
        city, month, day = get_filters()
        df = load_data(city, month, day)
        city = city.title()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        five_rows(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
