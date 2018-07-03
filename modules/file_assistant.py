import os
import pandas as pd
from .mangasites import DataFrameRow
from . import util

class Assistant:
    """
    The class which performs all data manipulation
    relative to the pandas database
    """
    def __init__(self, args):
        self.file_location = util.find(args.database)

        if args.clear or util.is_file_empty(self.file_location):
            util.clear_file(self.file_location)
            self.write_blank(header=True)

    def write_blank(self, header=False):
        """
        Writes a blank dataframe to file and
        returns one for convenience
        """
        empty_dataframe = DataFrameRow.empty_manga_list()

        with open(self.file_location, 'w+') as writable_file:
            empty_dataframe.to_csv(
                writable_file,
                header=header,
                index=False)

        return empty_dataframe

    def fetch_old_file(self):
        """
        Fetches the old datafile with previous manga info on it.
        If the file is empty, we populate it with the basic scaffold
        (columns only), and then return the empty dataframe
        """
        return pd.read_csv(
            self.file_location,
            index_col=0,
        )

    def update(self, updated_dataframe):
        """
        Updates the database with new manga
        These manga must be unique, and therefore you MUST
        run #compare before updating

        We also create a new file if one does not exist

        We read out the old dataframe, and append the new dataframe,
        and then write the dataframe out
        """
        original_dataframe = pd.read_csv(self.file_location)
        new_dataframe = original_dataframe.append(updated_dataframe)

        with open(self.file_location, 'w+') as appendable_file:
            new_dataframe.to_csv(
                appendable_file,
                header=True,
            )

    @staticmethod
    def compare(old_dataframe, fresh_dataframe):
        """
        Compares two dataframes and returns the symmetric differences between
        the two
        """
        combined_dataframe = pd.concat([old_dataframe, fresh_dataframe])
        combined_dataframe = combined_dataframe.reset_index(drop=True)

        grouped_dataframes = combined_dataframe.groupby(DataFrameRow.REQUIRED)

        # if there is overlap, there will be a column with length > 1
        unique_indices = [col[0] for col in grouped_dataframes.groups.values() if
                          len(col) == 1]

        return combined_dataframe.reindex(unique_indices)
