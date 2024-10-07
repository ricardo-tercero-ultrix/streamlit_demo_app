from typing import (
    Optional,
    List,
    Tuple,
)

from pandas_handler import (
    PandasHandler,
    ColumnType,
)
import pandas as pd
from datetime import datetime

PATENT_COLUMNS_DEFINITIONS = {
    "filing": ColumnType.DATETIME,
    "publicationdate": ColumnType.DATETIME,
    "grantdate": ColumnType.DATETIME,
}


class PatentsHandler:

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__handler = PandasHandler(file_name=file_path, columns_definition=PATENT_COLUMNS_DEFINITIONS)
        self.__handler.change_column_split_string("inventor")

    @property
    def df(self) -> Optional[pd.DataFrame]:
        return self.__handler.df

    @property
    def inventors(self) -> List[str]:
        column_name = "inventor"
        inventors_columns = self.__handler.get_columns_values([column_name], unique=False).get(column_name, [])

        inventors = []
        for i in inventors_columns:
            inventors += i
        return list(
            set(inventors)
        )

    @staticmethod
    def __generate_year_list(years_range: Optional[Tuple[int, int]]) -> List[int]:
        start, end = years_range
        return [
            y for y in range(start, end)
        ] + [end]

    @property
    def filing_year_range(self) -> Optional[List[int]]:
        years_range = self.__get_year_range("filing")
        if years_range is not None:
            return self.__generate_year_list(years_range)
        return None

    @property
    def publication_year_range(self) -> Optional[List[int]]:
        years_range = self.__get_year_range("publicationdate")
        if years_range is not None:
            return self.__generate_year_list(years_range)
        return None

    @property
    def granted_year_range(self) -> Optional[List[int]]:
        years_range = self.__get_year_range("grantdate")
        if years_range is not None:
            return self.__generate_year_list(years_range)
        return None

    def __get_year_range(self, column_name: str) -> Optional[Tuple[int, int]]:
        years = self.__handler.get_columns_values([column_name], exclude_na=True, unique=True).get(
            column_name, None
        )
        if years is not None:
            start = pd.to_datetime(years.min()).year
            end = pd.to_datetime(years.max()).year
            return start, end
        return None

    def __filter_by_patent_id(self, patent_id: str) -> Optional[pd.DataFrame]:
        if self.__handler.is_column("id"):
            return self.__handler.filter_by_column_value(column_name="id", value=patent_id)
        return None

    def filter_by_year_of_filing(self, year: int, df: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        return self.__filter_by_year(year=year, column_name="filing", df=df)

    def filter_by_year_of_publication(self, year: int, df: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        return self.__filter_by_year(year=year, column_name="publicationdate", df=df)

    def filter_by_year_of_granted(self, year: int, df: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        return self.__filter_by_year(year=year, column_name="grantdate", df=df)

    def __filter_by_year(self, column_name: str, year: int, df: Optional[pd.DataFrame] = None) -> Optional[
        pd.DataFrame]:
        start = datetime(year=year, month=1, day=1).strftime('%Y-%m-%d')
        end = datetime(year=year, month=12, day=31).strftime('%Y-%m-%d')

        return self.__handler.filter_by_date_range(column_name=column_name, start=start, end=end, df=df)

    @property
    def granted(self) -> Optional[pd.DataFrame]:
        return self.__handler.filter_by_no_na_value("grantdate")

    @property
    def no_yet_granted(self) -> Optional[pd.DataFrame]:
        return self.__handler.filter_by_na_value("grantdate")

    def display(
            self,
            is_granted: Optional[bool] = None,
            by_filing: Optional[int] = None,
            by_publication: Optional[int] = None,
            by_granted: Optional[int] = None,
            by_inventor: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        if is_granted is not None:
            df = self.granted if is_granted else self.no_yet_granted
        else:
            df = self.__handler.df

        if by_inventor is not None:
            df = self.__handler.filter_by_value_in_list_items(
                value=by_inventor,
                column_name="inventor",
                df=df
            )

        if by_filing is not None:
            df = self.filter_by_year_of_filing(year=by_filing, df=df)

        if by_publication is not None:
            df = self.filter_by_year_of_publication(year=by_publication, df=df)

        if by_granted is not None:
            df = self.filter_by_year_of_granted(year=by_granted, df=df)

        return df

    def get_patent_website(self, patent_id: str) -> Optional[str]:
        df = self.__filter_by_patent_id(patent_id=patent_id)
        if df is not None:
            return df["resultlink"].to_list()[0]
        return None
