
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from src.db_client import DatabaseClient
from src.utils import high_contrast_color
import pandas as pd
from typing import Optional, Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import re
import psycopg.sql as sql
from datetime import datetime
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.colors as mcolors


def get_heat_map_query() -> str:
    """
    Constructs a PostgreSQL query to select all columns and rows
    from the 'spotify_songs_2024' table.

    Note that the table name is hard-coded into the query. The function will
    return a valid query string, but it will fail at execution time if the
    'spotify_songs_2024' table does not exist in the connected database.

    Returns:
        str: The SQL query string.
    """
    return """
    SELECT *
    FROM
        spotify_songs_2024
    """

def df_to_corr_matrix(
        db_client: DatabaseClient,
        query: str,
        row_filters: Optional[Dict[str,any]] = None,
        col_2_corr: Optional[List[str]] = None,
        numeric_cols: Optional[List[str]] = None
        ) -> pd.DataFrame:
    
    """
    Retrieves data from a database, filters it by rows and columns,
    and then calculates the correlation matrix for the specified numeric columns.

    Args:
        db_client (DatabaseClient): An instance of a database client object
            with a `get_data` method that returns a pandas DataFrame.
        query (str): The SQL query string to execute via `db_client.get_data`
            to retrieve the initial DataFrame.
        row_filters (Optional[Dict[str, any]], optional): A dictionary
            where keys are column names and values are the exact values to
            filter by. For example, `{"country": "CA"}` would filter rows
            where the 'country' column equals 'CA'. If `None` or an empty
            dictionary, no row filtering is applied. Defaults to `None`.
        col_2_corr (Optional[List[str]], optional): A list of column names
            for which the correlation matrix should be calculated. These columns
            must be present in the DataFrame and identified as numeric. If `None`,
            an error message will be printed, and the function will not return
            a correlation matrix. Defaults to `None`.
        numeric_cols (Optional[List[str]], optional): A list of column names
            that are expected to contain numeric data. This list is used to
            validate that all columns specified in `col_2_corr` are indeed numeric
            before attempting correlation calculation. If `None`, this validation
            step is skipped (though `col_2_corr` still needs to be numeric in practice).
            Defaults to `None`.

    Returns:
        pd.DataFrame: A pandas DataFrame representing the correlation matrix
            of the filtered and selected numeric columns. Returns an empty
            DataFrame or raises an error if correlation cannot be calculated
            due to missing or non-numeric columns.

    Prints:
        - A warning if a column specified in `row_filters` does not exist in the DataFrame.
        - An error if any column in `col_2_corr` is not found in `numeric_cols` or
          does not exist in the DataFrame after row filtering.
        - A confirmation message if the correlation matrix is successfully calculated.
    """
    #call get_data method on DatabaseClient object to retrieve the dataframe
    df = db_client.get_data(query)

    if row_filters:
        # 1. Filter rows
        mask = pd.Series([True] * len(df))
        for col, val in row_filters.items():
            if col in df.columns:
                # Note: Use a boolean False here, not the string "False"
                mask &= df[col] == val
            else:
                print(f"Warning: Column '{col}' does not exist in the DataFrame. Skipping filter.")

        # Apply row filter
        df_rows_filtered = df[mask].copy()
    else:
        df_rows_filtered = df

    # 2. Filter columns and calculate correlation
    if all(elem in numeric_cols for elem in col_2_corr):
        # This is the key fix: Filter columns from the already filtered rows
        df_final = df_rows_filtered.loc[:, col_2_corr].copy()
        
        # This is the second fix: Move the correlation calculation inside the if block
        corr_matrix = df_final.corr()
        
        print("Correlation Matrix successfully calculated:")
        print(corr_matrix)
        return corr_matrix # Return an empty DataFrame if correlation cannot be calculated
    else:
        print(f"Error: At least one column in {col_2_corr} is not numeric or does not exist.")
        
def plot_heat_map(
    corr_matrix: pd.DataFrame,
    row_filters: Optional[Dict[str, any]] = None,
    save_path: Optional[str] = 'output/heatmap'
) -> None:
    
    """
    Generates and displays a styled correlation heatmap from a given matrix.

    This function plots a correlation matrix, customizing the figure size,
    color palette, annotations, and other visual aesthetics for clarity.
    The title of the plot is dynamically generated based on a dictionary
    of applied row filters, including converting a country code to its full name
    if present.

    Args:
        corr_matrix (pd.DataFrame): The correlation matrix to be plotted.
            This should be a square pandas DataFrame.
        row_filters (Optional[Dict[str, any]]): A dictionary of filters that
            were used to generate the `corr_matrix`. If the dictionary contains
            a "country" key with an ISO 3166-1 alpha-2 code, it will be
            converted to the full country name for the plot title. If `None` or
            empty, the title will not include any filter information.
            Defaults to `None`.

    Returns:
        None: This function displays the plot directly and does not return any value.
    """

    if corr_matrix.empty:
        print("Warning: Correlation matrix is empty. Skipping heatmap plot.")
        return
    
    plt.figure(figsize=(14, 12))  # Increased figure size for better readability
    sns.heatmap(
        corr_matrix, 
        annot=True,  
        cmap='vlag', 
        fmt=".2f",  
        #linewidths=.5,  # Add lines between cells.
        linecolor='gray', 
        cbar_kws={'label': 'Correlation Coefficient', 'shrink': 0.8}, 
        annot_kws={"fontsize": 9, "weight": "bold"} 
    )

    if row_filters:
        # Create a copy to avoid modifying the original dictionary passed to the function
        title_filters = row_filters.copy()
        
        # Convert country code if present
        if "country" in title_filters:
            if title_filters["country"] == "ZZ":
                title_filters["country"] = "Global"
            else:
                try:
                    country = pycountry.countries.get(alpha_2=title_filters["country"])
                    if country:
                        title_filters["country"] = country.name
                except KeyError:
                    # In case the country code is not recognized by pycountry
                    print(f"Warning: Country code '{title_filters['country']}' not recognized. Keeping as is.")

        # Build subtitle and set title
        plain_text = ' | '.join(f"{key}: {value}" for key, value in title_filters.items())
        plt.title(
            f'Correlation Matrix of Numeric Spotify Song Features\n Applied Filters -> ({plain_text})',
            fontsize=14, pad=20, weight='bold'
        )
    else:
        plt.title(
            "Correlation Matrix of Numeric Spotify Song Features",
            fontsize=14, pad=20, weight='bold'
        )
        plain_text = "no_filters"
            
        

    plt.xticks(rotation=45, ha='right', fontsize=10)  # Adjusted rotation and font size for x-ticks
    plt.yticks(rotation=0, fontsize=10)  # Adjusted font size for y-ticks

    # Get the current axes object and remove all four spines (the outer box)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f"{save_path}_{re.sub(r'[^a-zA-Z0-9]', '_', plain_text)}.png", dpi=300, bbox_inches='tight')
    plt.show()

def get_monthly_correlation_query() -> str:
    """
    Constructs a PostgreSQL query to calculate the monthly correlation
    between two specified columns.

    Returns:
        str: The SQL query string.
    """
    return"""
    WITH by_month AS (
        SELECT
            EXTRACT(MONTH FROM snapshot_date) AS month,
            TO_CHAR(snapshot_date, 'Mon') AS month_name,
            {feature_col} AS feature_col,
            {target_col} AS target_col
        FROM
            spotify_songs_2024
        WHERE
            snapshot_date IS NOT NULL
            AND danceability IS NOT NULL
            AND popularity IS NOT NULL
            AND country = %s
    )
    SELECT
        month,
        month_name,
        CORR(feature_col, target_col) AS correlation
    FROM
        by_month
    GROUP BY
        month,
        month_name
    ORDER BY
        month;
    """

def plot_monthly_correlations(
    db_client: DatabaseClient,
    query: str,
    target_country_values: List[str],
    features_to_correlate: List[str],
    target_col: str = 'popularity',
    correlation_threshold: float = 0.3,
    show_min: bool = True,
    show_max: bool = True,  
    text_separation: float = 0.05,
    save_path: str = 'output/monthly_correlations.png'      
) -> None:
    
    plt.figure(figsize=(12, 7))
    plot_any = False #in case the correlation thresholg is too high and any figure is drawn
    color_idx = 0 # Initialize color index for line colors

    # Define a list of colors for the lines in the plot

    colors = [
        "#08273d",  # deep navy blue
        "#7c1616",  # strong red
        "#0a400a",  # dark green
        "#b64093",  # vibrant magenta
        "#696900",  # dark olive
        "#17becf",  # cyan
        "#ff9896",  # light red
        "#393b79",  # navy purple
        "#ad494a",  # brick red
        "#4a668a",  # steel blue
        "#c49c94",  # warm beige
        "#98df8a",  # soft green
        "#843c39",  # earthy red
        "#9edae5",  # pastel teal
        "#a55194",  # purple
        "#658119",  # olive green
        "#9a6735",  # light orange
        "#c7c7c7",  # neutral gray
        "#743e0e",  # brown
        "#535336",  # light yellow
    ]

    # --- Define Correlation Ranges for Visualization ---
    correlation_ranges = [
        {
            'label': 'Very Weak',
            'min': 0.00,
            'max': 0.09,
            'pos_color': '#D3D3D3',   # light gray
            'neg_color': '#D3D3D3'
        },
        {
            'label': 'Weak',
            'min': 0.10,
            'max': 0.29,
            'pos_color': '#E6A8A8',   # light red-gray
            'neg_color': '#E6A8A8'
        },
        {
            'label': 'Moderate',
            'min': 0.30,
            'max': 0.49,
            'pos_color': '#E97474',   # soft red
            'neg_color': '#E97474'
        },
        {
            'label': 'Strong',
            'min': 0.50,
            'max': 0.69,
            'pos_color': '#DC143C',   # crimson
            'neg_color': '#DC143C'
        },
        {
            'label': 'Very Strong',
            'min': 0.70,
            'max': 1.00,
            'pos_color': '#8B0000',   # dark red
            'neg_color': '#8B0000'
        }
    ]



    # Get the current axes object for plotting ranges
    ax = plt.gca()

    # So, 11.5 places the text just past the last month tick.
    x_text_position = 11.5

    # Plot shaded regions for correlation ranges
    for r in reversed(correlation_ranges):
        ax.axhspan(r['min'], r['max'], facecolor=r['pos_color'], alpha=0.2, zorder=0)
        ax.axhspan(-r['max'], -r['min'], facecolor=r['neg_color'], alpha=0.2, zorder=0)
        
        ax.text(
            x=x_text_position,
            y=(r['min'] + r['max']) / 2,
            s=r['label'],
            ha='right', va='center', fontsize=9, color='dimgray',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.6),
            zorder=1
        )
        ax.text(
            x=x_text_position,
            y=-(r['min'] + r['max']) / 2,
            s=r['label'],
            ha='right', va='center', fontsize=9, color='dimgray',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.6),
            zorder=1
        )

    # Iterate over each target country value and feature to correlate
    # to generate the correlation plots.

    for target_country_value in target_country_values:
        
        for feature_to_correlate in features_to_correlate:

            
            current_line_color = colors[color_idx % len(colors)] #% don't allow to select an indice bigger than 19, 20%20 =0, 
           

            composed_query = sql.SQL(query).format(
                feature_col=sql.Identifier(feature_to_correlate),
                target_col=sql.Identifier(target_col)
            )

            df = db_client.get_data(composed_query,(target_country_value,))
            monthly_correlations = df.copy()
            
            if (abs(monthly_correlations['correlation']) >= correlation_threshold).any():

                color_idx += 1

                sns.lineplot(
                    data=monthly_correlations,
                    x='month_name', # Use month names for x-axis labels
                    y='correlation',
                    marker='o',
                    color=current_line_color,
                    linewidth=2,
                    label=f"{feature_to_correlate.replace('_', ' ').title()} vs {target_col.title()}-{pycountry.countries.get(alpha_2=target_country_value).name if pycountry.countries.get(alpha_2=target_country_value) else "Global" }"  
                    )
                
                if show_min:
                    # Calculate absolute correlations ( returna pandas series)
                    abs_correlations = abs(monthly_correlations['correlation'])
                    
                    # Find index of correlation closest to zero and use .loc(to extract values)
                    idx_closest_to_zero = abs_correlations.idxmin()
                    corr_closest_to_zero = monthly_correlations.loc[idx_closest_to_zero, 'correlation']
                    month_closest_to_zero = monthly_correlations.loc[idx_closest_to_zero, 'month_name']

                    # Annotate point closest to zero
                    plt.annotate(
                        f'{corr_closest_to_zero:.2f}', # Format to 2 decimal places
                        xy=(month_closest_to_zero, corr_closest_to_zero),
                        xytext=(month_closest_to_zero, corr_closest_to_zero + text_separation if corr_closest_to_zero >= 0 else corr_closest_to_zero - text_separation),
                        textcoords='data',
                        arrowprops=None, # Removed the arrow
                        horizontalalignment='center',
                        verticalalignment='bottom' if corr_closest_to_zero >= 0 else 'top',
                        fontsize=8,
                        color=current_line_color # Set annotation color to match line color
                        )
                    
                
                if show_max:
                    # Calculate absolute correlations ( returns a pandas series)
                    abs_correlations = abs(monthly_correlations['correlation'])

                    # Find index of correlation farthest from zero and use .loc(to extract values)
                    idx_farthest_from_zero = abs_correlations.idxmax()
                    corr_farthest_from_zero = monthly_correlations.loc[idx_farthest_from_zero, 'correlation']
                    month_farthest_from_zero = monthly_correlations.loc[idx_farthest_from_zero, 'month_name']
                
                    # Annotate point farthest from zero
                    plt.annotate(
                        f'{corr_farthest_from_zero:.2f}', # Format to 2 decimal places
                        xy=(month_farthest_from_zero, corr_farthest_from_zero),
                        xytext=(month_farthest_from_zero, corr_farthest_from_zero + text_separation if corr_farthest_from_zero >= 0 else corr_farthest_from_zero - text_separation),
                        textcoords='data',
                        arrowprops=None, 
                        horizontalalignment='center',
                        verticalalignment='bottom' if corr_farthest_from_zero >= 0 else 'top',
                        fontsize=8,
                        color=current_line_color # Set annotation color to match line color
                        )
                    

                plot_any = True 
            else:
                print(f"{feature_to_correlate} is not betwen -{correlation_threshold} and {correlation_threshold}")
    if plot_any:

        # Add a horizontal line at y=0 for easy reference (no correlation)
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        plt.xlabel('Month', fontsize=12)
        # Dynamically set the Y-axis label based on the feature
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.ylim(-1, 1) # Ensure y-axis covers the full correlation range


        ax = plt.gca()
        # Remove all four spines (the "box" and the x/y axis lines)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False) # Remove x-axis line
        ax.spines['left'].set_visible(False) 
            
        plt.legend(title='Correlation', bbox_to_anchor=(1.02, 1), loc='upper left', ncol=1, borderaxespad=0.)
        plt.tight_layout()
        plt.savefig(f"{save_path}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png", dpi=300, bbox_inches='tight') # Adjust layout to prevent labels/legend from overlapping
        plt.show() #
    else:
        plt.figure(figsize=(12, 7))
        plt.plot([0], [0], alpha=0)  # Invisible point just to create a figure
        plt.text(0, 0, 'No data to plot', ha='center', va='center', fontsize=14)
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.axis('off')  # Hide axes
        plt.show()
        
def get_explicit_popularity_query() -> str:
    """
    Constructs a PostgreSQL query to calculate the average popularity of
    explicit songs per country.

    The query works in two stages: it first computes the average popularity
    for each explicit song within each country, and then it calculates the
    overall average of these song popularities for each country. Results
    exclude the global ('ZZ') country code and are ordered from highest
    to lowest average popularity.

    Returns:
        str: The SQL query string.
    """
    return """
    WITH song_average_popularity_per_country AS (
        SELECT
            country,
            spotify_id,
            AVG(popularity) AS song_avg_popularity 
        FROM
            spotify_songs_2024
        WHERE
            is_explicit = 1
            AND country <> 'ZZ'
        GROUP BY
            country,
            spotify_id
    )
    SELECT
        country,
        AVG(song_avg_popularity) AS avg_explicit_popularity
    FROM
        song_average_popularity_per_country
    GROUP BY
        country
    ORDER BY
        avg_explicit_popularity DESC;
    """

def plot_explicit_popularity_map(
        db_client: DatabaseClient,
        explicit_popularity_query: str,
        save_path: str = 'output/world_map_average_popularity.png' 
        ) -> None:
    """
    Fetches explicit song popularity data from the database and plots it on a world map.

    This function retrieves the average popularity of unique explicit songs by country,
    normalizes the popularity values, and visualizes them on a world map using Cartopy.
    It also adds country names as labels on the map.

    Args:
        db_client (DatabaseClient): An instance of the DatabaseClient to fetch data.
        explicit_popularity_query (str): The SQL query string to fetch explicit song popularity data.
        save_path (str): The file path to save the generated map image. Defaults to 'output/world_map_average_popularity.png'.
    """

    # 2. Use the get_data_from_db function to fetch the data into a Pandas DataFrame
    try:
        df_explicit_popularity = db_client.get_data(explicit_popularity_query)
    except Exception as e:
        print(f"ERROR: Could not fetch data for explicit song popularity by country. Details: {e}")
        df_explicit_popularity = pd.DataFrame() # Ensure an empty DataFrame if an error occurs

    # 3. Data preparation: Prepare data for mapping
    if not df_explicit_popularity.empty:
        print(f"\nSuccessfully fetched {len(df_explicit_popularity)} rows for explicit song popularity by country (refined).")
        print("\nExplicit Song Popularity Data Preview (first 10 rows - Refined):")
        print(df_explicit_popularity.head(10))

        # Convert country codes to full names for potential use (though not directly used for map coloring)
        df_explicit_popularity['country_name'] = df_explicit_popularity['country'].apply(
            lambda x: pycountry.countries.get(alpha_2=x).name if pycountry.countries.get(alpha_2=x) else x
        )

        # Convert popularity to a format suitable for color mapping
        # Normalize popularity values to a 0-1 range for colormap
        min_pop = df_explicit_popularity['avg_explicit_popularity'].min()
        max_pop = df_explicit_popularity['avg_explicit_popularity'].max()
        # Avoid division by zero if all popularities are the same
        if max_pop == min_pop:
            df_explicit_popularity['normalized_popularity'] = 0.5
        else:
            df_explicit_popularity['normalized_popularity'] = (df_explicit_popularity['avg_explicit_popularity'] - min_pop) / (max_pop - min_pop)

        # Define a colormap this object contains all the information about 
        # the color gradient, how colors transition, and how to map numerical
        #  values to those colors.
        cmap = cm.magma #  other sequential colormaps are 'plasma', 'magma', 'cividis'

        # 4. Create the world map using Cartopy 
        plt.figure(figsize=(15, 10)) # Set the figure size for the map
        ax = plt.axes(projection=ccrs.Robinson()) # Use PlateCarree projection for a simple rectangular map
        #ccrs.PlateCarree() returns a Cartopy projection object. ccrs.Robinson() ccrs.Mercator() ccrs.Mollweide()

        # Add standard map features
        ax.add_feature(cfeature.LAND, facecolor='lightgray')
        ax.add_feature(cfeature.OCEAN, facecolor='#a6cee3') #'#1f78b4''#a6cee3', '#66c2a5'
        ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=0.3)
        #ax.add_feature(cfeature.LAKES, facecolor='lightblue')
        #ax.add_feature(cfeature.RIVERS, edgecolor='lightblue')

        # Set the extent of the map (optional, but good for focus)
        # ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree()) # Global view

        # --- START OF REPLACED/UPDATED CODE FOR PLOTTING COUNTRIES ---
        # Load shapefile path using shpreader
        shp_path = shpreader.natural_earth(
            resolution="110m",
            category="cultural",
            name="admin_0_countries"
        )

        reader = shpreader.Reader(shp_path)
        records = list(reader.records()) # Get a list of all country records
        #Each "record" represents a single geographical feature 
        # (in this case, a country). each record contains
        #  both the geometry (the shape of the country, like a polygon) 
        # and its attributes (country's name, ISO codes, population, etc.).

        # Plot each country
        for rec in records:
            iso = rec.attributes.get("ISO_A2") # Access ISO_A2 from attributes
            geom = rec.geometry # Get the geometry of the country

            if iso in df_explicit_popularity["country"].array:
                # If we have data for this country, color it based on popularity
                norm_val = float(df_explicit_popularity.loc[ #label-based indexer keeps only the rows where the corresponding value in the boolean mask is True
                    df_explicit_popularity["country"] == iso,
                    "normalized_popularity"
                ].values[0]) 
                face = cmap(norm_val) # Get color from colormap
                z = 2 # Higher zorder to be on top

                # Get the country name for the label
                country_name_for_label = rec.attributes.get("ABBREV")
                if not country_name_for_label: # If ABBREV is None or empty
                    country_name_for_label = rec.attributes.get("NAME")

                # Try to get a centroid for text placement
                try:
                    # Use the centroid of the geometry for text placement
                    lon_text = geom.centroid.x
                    lat_text = geom.centroid.y
                    # Add country name as text label
                    if geom.area > 30:
                        ax.text(
                            lon_text, lat_text,
                            country_name_for_label,
                            transform=ccrs.PlateCarree(), # Text coordinates are in PlateCarree
                            fontsize=7,
                            ha='center', va='center',
                            color=high_contrast_color(face), # You can adjust text color for readability
                            zorder=3 # Ensure text is above the colored country
                        )
                except Exception as e:
                    print(f"Could not place text for {country_name_for_label} ({iso}): {e}")
                    # Fallback or skip if centroid is problematic (e.g., for multi-part geometries spread out)

            else:
                # If no data, color it lightgray
                face = "lightgray"
                z = 1 # Lower zorder to be behind colored countries

            ax.add_geometries(
                [geom],
                ccrs.PlateCarree(), #
                facecolor=face,
                edgecolor="black",
                linewidth=0.3,
                zorder=z
            )
        

        # Add a colorbar to explain the popularity scale
        sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_pop, vmax=max_pop))
        sm.set_array([]) # Empty array for scalarmappable
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
        cbar.set_label('Average Popularity Score (Unique Explicit Songs)', fontsize=10)

        # Set title
        plt.title('Average Popularity of Unique Explicit Songs by Country', fontsize=16, weight='bold', pad=20)

        plt.tight_layout()
        plt.savefig(save_path, format='png', bbox_inches='tight', dpi=300)
        plt.show()

def main() -> None:
    """
    Main function to execute the script for generating plots.
    Initializes the database client and calls the plotting functions.
    """
    # Initialize the database client with credentials from config
    db_client = DatabaseClient(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    """    # List of non-numeric columns (excluded from correlation analysis)
    no_num_col = [
        "id", "spotify_id", "name", "artists", "daily_movement", "weekly_movement",
        "country", "snapshot_date", "album_name", "album_release_date"
    ]
    """
    # List of numeric columns (eligible for correlation analysis)
    num_cols = [
        "daily_rank", "popularity", "is_explicit", "duration_ms", "danceability",
        "energy", "key", "loudness", "mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo", "time_signature"
    ]

    # Columns to include in the correlation matrix
    col_2_corr = [
        "daily_rank", "popularity", "is_explicit", "duration_ms", "danceability",
        "energy", "key", "loudness", "mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo", "time_signature"
    ]

    # Row filters for data selection (e.g., filter by country)
    row_filters = {
        "country": "US"  # Filter for United States
    }

    # Features to correlate against the target column
    features_to_correlate = [
        "daily_rank", "is_explicit", "duration_ms", "danceability",
        "energy", "key", "loudness", "mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo", "time_signature"
    ]

    # Target column for correlation analysis
    target_col = 'popularity'

    # Correlation threshold for filtering results (set to 0 to show all)
    correlation_threshold = 0

    # List of country codes for analysis (can be expanded as needed)
    target_country_values = ['US']

    # Generate and plot the correlation matrix heatmap
    df_filtered = df_to_corr_matrix(
        db_client=db_client,
        query=get_heat_map_query(),
        row_filters=row_filters,
        col_2_corr=col_2_corr,
        numeric_cols=num_cols
    )

    plot_heat_map(
        df_filtered,
        row_filters=row_filters
    )

    # Plot monthly correlations for selected features and countries
    plot_monthly_correlations(
        db_client=db_client,
        query=get_monthly_correlation_query(),
        target_country_values=target_country_values,
        features_to_correlate=features_to_correlate,
        target_col=target_col,
        correlation_threshold=correlation_threshold,
        show_min=True,
        show_max=True,
        text_separation=0.05,
        save_path='output/monthly_correlations'
    )

    # Plot world map of average explicit song popularity by country
    plot_explicit_popularity_map(
        db_client=db_client,
        explicit_popularity_query=get_explicit_popularity_query()
    )


# Initialize the database client with the provided configuration
if __name__ == "__main__":
    main()
