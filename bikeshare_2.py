import time
import pandas as pd
import numpy as np
import datetime
import json

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
#     keep asking the user to enter a city and beign case insensitive
    while True:
        city=input('Please enter the city (Chicago, New York City, Washington): ')
        city=city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            print("Okay then you chose "+city.title())
            break
        else:
            print("Please enter a valid city")
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    #     the same as the city but asking the user if he is sure about his choice or if he wants to change it
    # he might type yes instead of y but that can be handled easily
    while True:
        month=input("Please enter a month (All, January, February, ... , June)")
        if month in ["all",'january', 'february', 'march', 'april', 'may', 'june']:
            choice=input("You chose "+month.title()+"\nDo you want to continue? [y/n]")
            if choice.lower() in ['y','yes']:
                  
                break
            else:
                continue
        else:
            print("Please enter a valid month")
            continue     
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("Please enter a day (All, Monday, Tuesday, ... Sunday)")
        day=day.lower()
        if day in ["all", "monday", "tuesday", "wednesday" ,"thursday" ,"friday", "saturday", "sunday"]:
            choice=input("You chose the day "+day.title()+"\nWould you like to continue?[y/n]")
            if choice.lower() in ['y','yes']:
                break
            else:
                continue
        else:
            continue
            


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
    #getting the start time then changing it to a datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filtering data according to the user input
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        
        df = df[df['month'] == month]

   
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month=df['month'].mode()[0]

    # TO DO: display the most common day of week
    common_day=df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    df['common_hour'] = df['Start Time'].dt.hour
    common_hour = df['common_hour'].mode()[0]
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[common_month-1] #because we want to get the month name in addition to its number
    
    print(f'The most common month is {common_month} -> {month.title()}\nThe most common day in the week is {common_day}\nAnd the most common hour is {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start=df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    common_end=df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    #combining the two end points then see what is the most frequent combination
    df['combination']=df['Start Station']+" --> "+df['End Station']
    common_path=df['combination'].mode()[0]

    print(f'The most common start station is {common_start}\nThe most common end station is {common_end}\nAnd the most frequent combination of start & end stations are {common_path}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time=df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_time=df['Trip Duration'].mean()
    
    total_hours=datetime.timedelta(seconds=int(total_time))
    mean_hours = datetime.timedelta(seconds=int(mean_time))
    print(f'The total time in seconds is {total_time} sec.\n& the mean travel time is {mean_time} sec.')
    print(f"The total travel time is {total_hours}  \nThe mean travel time is {mean_hours} ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count=df['User Type'].value_counts()
    print(f'The number Users is\n{user_count}')
    # TO DO: Display counts of gender
    #check to see if gender exists if not return that the data is not found as in the case of washington
    if 'Gender' in df :
        
        gender_count=df['Gender'].value_counts()

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year=df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print(f'The number of Users according to gender is\n{gender_count} ')
        print(f'The earliest birth year is {int(earliest_year)} the most recent is {int(recent_year)} & the most common birth year is {int(common_year)}')
    else:
        print('Sorry, We don\'t have that information in Washington')
        

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def more_data(df):
    answer=input("Do you want to see the first 5 rows of data?")
    answer=answer.lower()
    start_loc=0
    #the end location is always greater than the start location by 5
    while answer in ['yes','y','ya'] and start_loc+5 < df.shape[0]:
        print(df.iloc[start_loc:start_loc+5].to_dict())
        start_loc+=5
        answer=input("Do you want to see the next 5 rows of data?")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #cheking if the user wants to see 5 rows of data
        more_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()