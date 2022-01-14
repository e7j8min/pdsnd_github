import time
import pandas as pd
import numpy as np



CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():

    """
    Gains input for filtering requirements.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Would you like to see data for Chicago, New York City, or Washington: ").lower()
    month = ""
    day = ""

    while True:
        if city.lower() in CITY_DATA:
            time_filter = input("Would you like to filter the data by month, day, or not at all?  Type \"none\" for no time filter.").lower()
            if time_filter.lower() == "day":
                day = input("Which day?  Type a day Monday, Tuesday, Wednesday,Thursday, Friday, Saturday, Sunday. ").lower()
                month = 'all'
                while day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    print("please enter a valid day")
                    day = input("Which day?  Type a day Monday, Tuesday, Wednesday,Thursday, Friday, Saturday, Sunday. ").lower()
                else:
                    break
            elif time_filter.lower() == "month":
                month = input("Which month? January, February, March, April, May or June?").lower()
                day = 'all'
                while month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):
                    print("Please enter a valid month")
                    month = input("Which month? January, February, March, April, May or June?").lower()
                else:
                    break
            elif time_filter.lower() == "none":
                day = 'all'
                month = 'all'
                break
            else:
                print("Please enter valid answer")
        else:
            print("Please enter valid city")
            city = input("Would you like to see bikeshare data for Chicago, New York City, or Washington: ").lower()

    print('-' * 40)
    print(city.title(), month.title(), day.title())
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
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print("The most common month: {}".format(popular_month))
    print("The most common day of week: {}".format(popular_day))
    print("The most common start hour: {}".format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].value_counts()[df['Start Station'].value_counts() == df['Start Station'].value_counts().max()]

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].value_counts()[df['End Station'].value_counts() == df['End Station'].value_counts().max()]

    # TO DO: display most frequent combination of start station and end station trip
    common_station_combo = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)

    print("Most common start station is {}".format(common_start_station.index[0]))
    print("Most common end station is {}".format(common_end_station.index[0]))
    print("Most common station combination is {}".format(common_station_combo.index[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['diff'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    total_time = df['diff'].sum()
    avg_time = df['diff'].mean()

    # TO DO: display mean travel time

    print('Total Duration: {}'.format(total_time))
    print('Average Duration: {}'.format(avg_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()

    # TO DO: Display counts of gender
    while "Gender" in df:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
        break

    # TO DO: Display earliest, most recent, and most common year of birth
    while "Birth Year" in df:
        common_birthyear = df['Birth Year'].mode()[0]
        print("Earliest birth year is {}".format(int(df['Birth Year'].min())))
        print("Most recent birth year is {}".format(int(df['Birth Year'].max())))
        print("Most common birth year is {}".format(int(common_birthyear)))
        break

    print(user_types)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        if city is not None and month != "" and day != "":
            df = load_data(city, month, day)
            #pd.set_option(df.max_columns, 200)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
            i = 0
            while raw_data.lower() == 'yes':
                print(df.iloc[i: (i + 5)])
                #print(tabulate(df.iloc[np.arange(0 + i, 5 + i)], headers="keys"))
                i += 5
                raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
            else:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    break
        else:
            break


if __name__ == "__main__":
    main()
