from typing import (
    List,
    Optional,
    Union,
    Dict,
)
from enum import Enum
import pandas as pd


class ColumnType(Enum):
    DATETIME = 'datetime'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def extract_column_names(cls, column_definition: Dict[str, str]) -> Dict[str, List[str]]:
        column_names = {}
        for key in ColumnType.list():
            column_names.update(
                {
                    key: list(map(lambda x: x[0], filter(lambda x: x[1] == key, column_definition.items())))
                }
            )
        return column_names


class PandasHandler:

    def __init__(
            self,
            file_name: Optional[str] = None,
            df: Optional[pd.DataFrame] = None,
            columns_definition: Optional[Dict[str, ColumnType]] = None,
    ) -> None:
        self.__columns_definition = columns_definition
        if df is None and file_name is not None:
            self.__file_name: str = file_name
            try:
                self.__df = pd.read_csv(self.__file_name)
            except FileNotFoundError:
                self.__df = None
        elif df is not None:
            self.__df = df
        else:
            raise ValueError("Please provide either a file name or a dataframe")

        self.process_dataframe()

    @property
    def df(self) -> Optional[pd.DataFrame]:
        return self.__df if self.is_data_loaded else None

    def __get_df(self, df: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        if df is not None:
            return df

        if self.is_data_loaded:
            return self.__df

        return None

    def process_dataframe(self):
        if self.is_data_loaded and self.__columns_definition is not None:
            columns_name = ColumnType.extract_column_names(self.__columns_definition)
            for c_type, column_name in columns_name.items():
                if c_type == ColumnType.DATETIME:
                    self.change_column_type_to_datetime(column_name)

    @property
    def is_data_loaded(self) -> bool:
        """
        This function checks if the dataframe is loaded
        :return: True if the dataframe is loaded, False otherwise
        """
        return self.__df is not None

    def get_column_names(self) -> Optional[List[str]]:
        """
        This function returns the column names of the dataframe, or None if the dataframe is not loaded
        :return:
        """
        if self.is_data_loaded:
            return list(self.__df.columns)
        return None

    def is_column(self, column_name: str) -> bool:
        """
        This function checks if the given column name is a valid column name of the dataframe
        :param column_name: A string that represents the column name
        :return: True if the column name is a valid column name of the dataframe, False otherwise
        """
        column_names = self.get_column_names()
        return column_names is not None and column_name in column_names

    def change_column_split_string(self, column_name: Union[str, List[str]], sep: str = ",") -> None:
        """
        This method expect either a string or a list of strings, if the column nade is a valid column name then that
        column is changed to be a list, split a string by the sep parameter.
        :param column_name:
        :param sep:
        :return: None
        """
        if self.is_data_loaded:
            if isinstance(column_name, str):
                if self.is_column(column_name):
                    self.__df[column_name] = self.__df[column_name].apply(lambda x: x.split(sep))
            elif isinstance(column_name, list):
                for cn in column_name:
                    self.change_column_split_string(cn, sep=sep)

    def change_column_type_to_datetime(self, column_name: Union[str, List[str]]) -> None:
        """
        This method expect either a string or a list of strings, if the column nade is a valid column name then that
        column is changed to be a datatime
        :param column_name:
        :return: None
        """
        if self.is_data_loaded:
            if isinstance(column_name, str):
                if self.is_column(column_name):
                    self.__df[column_name] = pd.to_datetime(self.__df[column_name])
            elif isinstance(column_name, list):
                for cn in column_name:
                    self.change_column_type_to_datetime(cn)

    def add_column(self, column_name: str, column_data: List[object]) -> None:
        if self.is_data_loaded and not self.is_column(column_name):
            self.__df[column_name] = column_data

    def get_columns(self, columns_name: List[str]) -> Optional[pd.Series]:
        if self.is_data_loaded:
            columns_name = list(
                filter(
                    lambda c: self.is_column(c),
                    columns_name
                )
            )
            return self.__df[columns_name]
        return None

    def get_columns_values(
            self,
            columns_name: List[str],
            unique: bool = True,
            exclude_na: bool = True
    ) -> Dict[str, pd.Series]:
        columns_values = {}
        if self.is_data_loaded:
            for cn in columns_name:
                column_values = self.get_columns([cn])[cn]
                if exclude_na:
                    column_values = column_values.dropna()
                if unique:
                    column_values = column_values.unique()
                columns_values.update(
                    {
                        cn: column_values
                    }
                )
        return columns_values

    def filter_by_date_range(
            self,
            column_name: str,
            start: Optional[str] = None,
            end: Optional[str] = None,
            df: Optional[pd.DataFrame] = None,
    ) -> Optional[pd.DataFrame]:
        if self.is_data_loaded and self.is_column(column_name):
            selected_df = self.__get_df(df=df)

            if start is not None and end is not None:
                return selected_df[
                    selected_df[column_name].between(start, end)
                ]
            elif start is not None:
                return selected_df[
                    selected_df[column_name] == start
                    ]
            elif end is not None:
                return selected_df[
                    selected_df[column_name] == end
                    ]
        return None

    def filter_by_na_value(self, column_name: str, df: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        if self.is_data_loaded and self.is_column(column_name):
            selected_df = self.__get_df(df=df)

            return selected_df[
                selected_df[column_name].isna()
            ]
        return None

    def filter_by_no_na_value(self, column_name: str, df: Optional[pd.DataFrame] = None) -> Optional[pd.DataFrame]:
        if self.is_data_loaded and self.is_column(column_name):
            selected_df = self.__get_df(df=df)

            return selected_df[
                ~selected_df[column_name].isna()
            ]
        return None

    def filter_by_column_value(
            self,
            column_name: str,
            value: str,
            df: Optional[pd.DataFrame] = None,
    ) -> Optional[pd.DataFrame]:
        if self.is_data_loaded and self.is_column(column_name):
            selected_df = self.__get_df(df=df)
            return selected_df[
                selected_df[column_name] == value
                ]
        return None

    def filter_by_value_in_list_items(
            self, value: str, column_name: str, df: Optional[pd.DataFrame] = None
    ) -> Optional[pd.DataFrame]:
        if self.is_data_loaded and self.is_column(column_name):
            selected_df = self.__get_df(df=df)

            return selected_df[
                selected_df[column_name].apply(lambda i: value in i)
            ]
        return None
