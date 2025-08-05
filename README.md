# What Makes a Song Popular? <br> Untangling the Chaos with a Data-Driven Approach.

Decoding the DNA of Hit Songs

1. [Project Overview](#part-1-project-overview)  
    - [Description](#description)  
        - [Dataset](#dataset)  
        - [Technologies Used](#technologies-used)  
        - [Key Analyses & Insights](#key-analyses--insights)  
    - [Features](#features)  
2. [Setup](#part-2--setup)  
    - [Prerequisites](#prerequisites)  
    - [Installation](#installation)  
    - [Database Setup](#database-setup)  
3. [Data Analysis](#part-3--data-analisis)  
4. [Contact](#contact)

## Part 1: Project Overview
### Description

This project analyzes a dataset of daily top 50 Spotify songs from 72 countries and globally, covering the period from October 18, 2023, to June 11, 2025 (date of download; the latest data may vary). The primary goal is to determine how music features obtained through the Spotify API, such as danceability, loudness, and explicitness, relate to a song's popularity and daily rank.

While multiple exploratory analyses are included, the main focus is on understanding how static song attributes (e.g., danceability, loudness, explicitness) relate to dynamic performance metrics (e.g., popularity score, daily chart position). It focuses on understanding the impact of fixed song attributes on listener reception, aiming to shed light on crucial decisions like optimal release timing or predicting a song's acceptance in specific regions.

The initial phase of this project involved extensive data cleaning using PostgreSQL. The raw dataset presented significant challenges, including empty rows, inconsistencies, and out-of-range values. For the subsequent analysis, only data from the year 2024 was extracted to ensure a clear and well-defined study period. The second part of the project utilizes Jupyter Notebooks for in-depth exploration and visualization. All cleaning scripts and analytical notebooks have been structured into a well-organized Python program, also included in this repository.


#### Dataset

The dataset used for this analysis is sourced from Kaggle: [Top Spotify Songs in 73 Countries (Daily Updated)](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated)

---

#### Technologies Used

* **PostgreSQL:** For robust data cleaning, transformation, and management.
* **Python:**
    * **Jupyter Notebooks:** For interactive data exploration, analysis, and visualization.
    * **Pandas:** For data manipulation and analysis.
    * **Matplotlib/Seaborn:** For creating insightful visualizations.
    * **Psycopg:** For Python-PostgreSQL database interaction.

---

#### Key Analyses & Insights
* Identifying **correlations** between all numerical features across the entire dataset
* Analyzing **temporal** trends in song popularity and feature distribution across months of 2024.
* Uncovering **geographical** variations in musical explicitness and popularity across different countries.

### Features
-   **Comprehensive Data Cleaning:** Robust PostgreSQL scripts to handle missing values, inconsistencies, and out-of-range data in the raw Spotify dataset.
-   **Music Feature Analysis:** In-depth exploration of how Spotify API-derived features (e.g., danceability, loudness, explicitness) correlate with song popularity and daily rank.
-   **Temporal Trend Analysis:** Investigate how song popularity and feature distribution evolve across months (specifically focusing on 2024 data).
-   **Geographical Popularity Insights:** Uncover variations in musical preferences and chart performance across 72 countries and global charts.
-   **Reproducible Analysis:** Jupyter Notebooks for interactive exploration and visualization, complemented by a well-structured Python program for repeatable analysis.

## Part 2 : Setup

### Prerequisites
* **Python 3.8+** (or a distribution like **Anaconda** which includes Python and pip)
* **pip** (Python package installer, usually included with Python or Anaconda)
* **PostgreSQL database**

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/itsmeluisc/spotify_data_analysis.git](https://github.com/itsmeluisc/spotify_data_analysis.git)
    cd spotify_data_analysis
    ```
2.  **Create and activate a virtual environment (recommended):**
**Using `venv`:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate   # On Windows
    ```

    **Using Conda:**
    ```bash
    conda create -name spotify_env python=3.12  # Create an environment named 'spotify_env' with Python 3.9
    conda activate spotify_env                  # Activate the environment
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Database Setup:**
    * Ensure your PostgreSQL database is running.
    * Update database connection details in `config.py` (or your equivalent config file).
    * Modify the file path in [sql/02_ingest_raw_data.sql](../sql/02_ingest_raw_data.sql) to point to your downloaded CSV. [Top Spotify Songs in 73 Countries (Daily Updated)](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated)

## Part 3 : Data Analisis 
### Introduction
The dataset used in this project was downloaded from [Top Spotify Songs in 73 Countries (Daily Updated)](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated) in CSV format. It was then imported, cleaned, and stored in a PostgreSQL database to ensure consistency and enable efficient querying.

Subsequently, a Jupyter Notebook was used to perform data visualization, deeper analysis, and generate meaningful plots. This structured approach enables both exploratory and targeted analysis of how various musical features relate. 

<div style="overflow-x: auto">
| id      | name              | artists                             | daily_rank | country | snapshot_date | popularity | is_explicit | danceability | loudness  | tempo  |
|---------|-------------------|-----------------------------------|------------|---------|---------------|------------|-------------|--------------|-----------|--------|
| 885393  | Sofa urtubörn     | Hafdís Huld                       | 30         | IS      | 2024-09-21    | 44         | False       | 0.715        | -13.713   | 119.95 |
| 885394  | Too Sweet         | Hozier                            | 31         | IS      | 2024-09-21    | 46         | False       | 0.74         | -5.446    | 117.03 |
| 885395  | Ljós              | Hafdís Huld                       | 32         | IS      | 2024-09-21    | 43         | False       | 0.742        | -13.086   | 146.17 |
| 885396  | Til í allt, Pt. III| Friðrik Dór, Herra Hnetusmjör... | 33         | IS      | 2024-09-21    | 44         | False       | 0.863        | -7.103    | 99.99  |
| 885397  | Bíum bíum bambaló | Hafdís Huld                       | 34         | IS      | 2024-09-21    | 44         | False       | 0.777        | -14.009   | 99.98  |
</div>



### Contact

Luis Castillo - itsmeluisc@gmail.com

Project Link: [https://github.com/itsmeluisc/spotify_data_analysis](https://github.com/itsmeluisc/spotify_data_analysis)