import dlt
import time
from ingestion_settings import Settings
from dlt.sources.helpers import requests
from datetime import datetime, timedelta


class Ingestion:
    """A class used to ingest data from an API and store it in a database.

    Attributes:
        api_key (str): The API key used for authentication.
        start_date (datetime): The start date for data ingestion.
        end_date (datetime): The end date for data ingestion.
        pipeline (dlt.Pipeline): The data pipeline for storing the data.
        table_name (str): The name of the table where data will be stored.
        sleep_time (int): The time to sleep between API requests.
        dates (list[str]): A list of dates for which data will be fetched.
    """
    def __init__(
        self,
        api_key: str,
        start_date: datetime,
        end_date: datetime,
        pipeline_name: str,
        table_name: str,
        sleep_time: int = 12,
    ) -> None:
        """Initializes the Ingestion class.

        Args:
            api_key (str): The API key used for authentication.
            start_date (datetime): The start date for data ingestion.
            end_date (datetime): The end date for data ingestion.
            pipeline_name (str): The name of the data pipeline.
            table_name (str): The name of the table where data will be stored.
            sleep_time (int, optional): The time to sleep between API requests. Defaults to 12.
        """
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date
        self.sleep_time = sleep_time
        self.pipeline = dlt.pipeline(
            pipeline_name=pipeline_name,
            destination="duckdb",
            dataset_name=f"{pipeline_name}_data"
        )
        self.table_name = table_name
        self.dates = self.generate_weekly_dates()

    def generate_weekly_dates(self) -> list[str]:
        """Generates a list of dates on a weekly basis between the start and end dates.

        Returns:
            list[str]: A list of dates in 'YYYY-MM-DD' format.
        """
        current_date = self.start_date
        weekly_dates = []
        while current_date <= self.end_date:
            weekly_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(weeks=1)
        return weekly_dates

    def fetch_and_store_data(self) -> None:
        """Fetches data from the API for each date and stores it in the database.

        It constructs the API URL using the provided dates and API key, fetches the data,
        and stores it in the specified table. If an error occurs during data fetching,
        it prints an error message. The method also pauses for a specified sleep time
        between requests.
        """
        for date in self.dates:
            base_url = "https://api.nytimes.com/svc/books/v3/lists/overview.json"
            url = f"{base_url}?published_date={date}&api-key={self.api_key}"

            try:
                data = requests.get(url).json()["results"]
                self.pipeline.run([data], table_name=f"{self.table_name}")

            except Exception as e:
                print(f"Error fetching data for {date}: {e}")

            print(f"Data fetched and stored for {date}")

            time.sleep(self.sleep_time)


if __name__ == "__main__":
    settings = Settings()
    api_key = settings.API_KEY
    start_date = datetime.strptime(settings.START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(settings.END_DATE, "%Y-%m-%d")

    ingestor = Ingestion(
        api_key=api_key,
        start_date=start_date,
        end_date=end_date,
        pipeline_name="nyt_books",
        table_name="nyt_books"
    )

    ingestor.fetch_and_store_data()
