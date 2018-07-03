import unittest
from unittest import mock

import pandas as pd

from mangachecker.modules.file_assistant import Assistant
from mangachecker.modules.mangasites import DataFrameRow

class TestAssistant(unittest.TestCase):

    class MagicArgs:
        """
        Stand-In for the ArgParse
        """
        MOCKED_ARGS = ['file', 'clear']
        ARGS = ['database', *MOCKED_ARGS]
        def __init__(self, file_location):
            self.database = file_location

            for arg in self.MOCKED_ARGS:
                setattr(self, arg, mock.MagicMock())

    def setup_method(self, _method):
        location = 'tests/fake_db.csv'
        self.magic_args = self.MagicArgs(location)

        self.data = {
            'manga': ["WEEBO"],
            'chapter': ["192"],
            'title': ["Attack of the Weebs"],
            'link': ["https://github.com/DerekYu177"],
        }

        self.data2 = {
            'manga': ["Nobushi"],
            'chapter': ["101"],
            'title': ["For Honor"],
            'link': ["Ubisoft"],
        }

    def test_init_args_clear(self):
        """
        Clears the args.database if args.clear option is set
        """
        with mock.patch('mangachecker.modules.util.clear_file') as clear_mock:
            Assistant(self.magic_args)
            self.magic_args.clear.__bool__.assert_called_once()
            clear_mock.assert_called_once()

    def test_init_args_noclear(self):
        """
        Does not clear the args.database if args.clear option is not set
        """
        pass

    def test_init_args_creates(self):
        """
        Creates a file in the specificed location if the file does not
        currently exist
        """
        pass

    def test_fetch_old_file_empty(self):
        """
        if there is currently an empty file
        create an empty datafram with columns,
        else read from the .db
        """
        pass

    def test_compare(self):
        """
        check that the diff between an empty dataframe and a new dataframe is
        the new dataframe
        """
        old_dataframe = DataFrameRow.empty_manga_list()
        new_dataframe = pd.DataFrame.from_dict(self.data)

        diff_dataframe = Assistant.compare(old_dataframe, new_dataframe)

        self.assert_equivalent(diff_dataframe, new_dataframe)

    def test_compare_larger(self):
        """
        Checks the diff between two non-empty dataframes
        """
        old_dataframe = pd.DataFrame.from_dict(self.data)
        new_dataframe = pd.DataFrame.from_dict(self.data2)
        modified_dataframe = new_dataframe.append(old_dataframe, ignore_index=True)

        diff_dataframe = Assistant.compare(old_dataframe, modified_dataframe)

        # the symmetric difference should be the new dataframe
        self.assert_equivalent(new_dataframe, diff_dataframe)

    def assert_equivalent(self, old, new):
        for column in old.columns:
            assert old[column].values, \
                   new[column].values

