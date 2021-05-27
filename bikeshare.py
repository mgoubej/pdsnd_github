import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all','january','february','march','april','may','june']
DAYS = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']


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
    
    city = ''
    while not(city in CITY_DATA):
        city = input('Select city (Chicago, New York City, Washington):').lower()
    

    # get user input for month (all, january, february, ... , june)
    month = ''
    while not(month in MONTHS):
        month = input('Select month to filtery by (all, January-June):').lower()
    


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while not(day in DAYS):
        day = input('Select day to filtery by (all, Sunday-Saturday):').lower()


    print('-'*60)
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
    
    # load csv file according to the selected city
    df = pd.read_csv(CITY_DATA[city]) 

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract hour from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    
    # extract day of week from the Start Time column to create a dow column
    df['dow'] = df['Start Time'].dt.dayofweek
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        m_ind = MONTHS.index(month)
                
        # filter by month to create the new dataframe
        df = df[df['month'] == m_ind]

    # filter by day of week if applicable
    if day != 'all':
        
       dow =  DAYS.index(day)-1
        # filter by day of week to create the new dataframe
       df = df[df['dow'] == dow]
    
    # extract starting hour from the filtered data to create a hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # extract start + end station combinations to create a new Route column
    df['Route'] = df['Start Station']+'-'+df['End Station']
    
    # extract time deltas to create a new deltat column
    df['deltat'] = df['End Time']-df['Start Time']
    
    # convert the time difference to minutes
    df['deltat'] = df['deltat'] / np.timedelta64(1,'m')
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month:', MONTHS[df['month'].mode()[0]])
    
    # display the most common day of week
    print('Most common day of week:', DAYS[df['dow'].mode()[0]+1])


    # display the most common start hour
    print('Most common start hour (0-23):', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most common route:', df['Route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time - sum of deltat column
    print('Total travel time in minutes:',  round(df['deltat'].sum()) ) 

    # display mean travel time
    print('Average travel time in minutes:',  round(df['deltat'].mean()) ) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""



    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:\n', df['User Type'].value_counts())
    print('');
        
        
    if ('Gender' in df) and ('Birth Year' in df): #Gender and Birth Year not available in some datasets, check this
        
        # Display counts of gender

        print('Counts of gender:\n', df['Gender'].dropna(axis = 0).value_counts()) 
        print('');
        # Display earliest, most recent, and most common year of birth, drop rows with missing year data
        print('Earliest year of birth:', int(df['Birth Year'].dropna(axis = 0).min()))
        print('Most recent year of birth:', int(df['Birth Year'].dropna(axis = 0).max()))
        print('Most common year of birth:', int(df['Birth Year'].dropna(axis = 0).mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print("Gender and birth year data not available in this dataset")


def main():
    while True:
        
        #get filter types from user
        city, month, day = get_filters()
        
        #apply filters and load data-frame
        df = load_data(city, month, day)
        
        #print data statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        #print raw data if requested
        rawdata = input('\nWould you like to see raw data? Enter yes or no:')
        if rawdata.lower() == 'yes':
            i_start = 0 #index of the starting row
            i_end = df.shape[0] #total number of rows
            cont='yes'
            while cont == 'yes':
                print(df.iloc[min(i_start,i_end):min(i_start+5,i_end),:])
                i_start+=5
                if i_start >= i_end:
                    break
                cont = input('\nWould you like to see next 5 rows of data? Enter yes or no:')
        
        #offer restarting
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
