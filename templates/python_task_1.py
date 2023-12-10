import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df=pd.read_csv("datasets/dataset-1.csv")
    df=df.pivot(index='id_1,columns='id_2,values='car,fill_value=0)

    for index in df.index:
        df.at[index,index]=0

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = np.select(conditions, choices, default='Unknown')

   
    type_count = df['car_type'].value_counts().to_dict()

    
    type_count = dict(sorted(type_count.items()))

    return type_count


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus = df['bus'].mean()

    
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()

    
    bus_indexes.sort()

    return bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()

    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    selected_routes.sort()

    return selected_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = car_matrix.copy()

    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    modified_matrix = modified_matrix.round(1)

    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Extract day of the week and hour from timestamp
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['hour'] = df['timestamp'].dt.hour

    # Check if each (id, id_2) pair has incorrect timestamps
    completeness_check = df.groupby(['id', 'id_2']).apply(lambda group: (group['day_of_week'].nunique() == 7 and
        group['hour'].nunique() == 24 and
        group['timestamp'].min().time() == pd.Timestamp('00:00:00').time() and
        group['timestamp'].max().time() == pd.Timestamp('23:59:59').time()))

    return completeness_check
