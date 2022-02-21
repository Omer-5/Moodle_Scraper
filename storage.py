import datetime
import sqlite3
import string
class Storage():
    """ Handles all OS and database queries
        database scheme:
            course text
            section text
            file_name text
            extra_details text
            url text
            date text
    """
    def __init__(self) -> None:
        self.course_name = ""
        self.section_name = ""

        try:
            self.conn = sqlite3.connect('HIT_current_database.db')
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS main (
                course text,
                section text,
                file_name text,
                extra_details text,
                url text,
                date text
            )""")
        except Exception as error:
            print(f"""
                **** Failed establishing connection to database \n
                {error=}
            """)
            raise
        self.os_path = "" # import from config file later \ other class

    def _add_new_entry(self, entry_name, url, extra_details) -> None:
        """ add new record the database
        """

        date = self._get_date()
        entry_name = self._remove_problematic_chars(entry_name)

        try:
            self.cursor.execute("INSERT INTO main VALUES (?, ?, ?, ?, ?, ?)", (
                self.course_name,
                self.section_name,
                entry_name,
                extra_details,
                url,
                date
            ))
            self.conn.commit()
        except Exception as error:
            print(f"""
                ***** Failed adding new row to database
                {self.course_name=}, {self.section_name=} \n
                {entry_name=}, {extra_details=} \n
                {url=}, {date=} \n
                {error=}
            """)
            raise

    @staticmethod
    def _get_date() -> string:
        """return string represting the date as DD/MM/YYYY

        Returns:
            string: return date as DD/MM/YYYY
        """
        date = datetime.datetime.now()
        date = date.strftime("%d/%m/%Y")
        return date

    def change_course(self, raw_course_name) -> None:
        """ change context to new course, create folder if necessary

        Args:
            raw_course_name (string): the raw course name
        """
        self.course_name = self._remove_problematic_chars(raw_course_name)
        # handle folder

    def change_section(self, new_section) -> None:
        """ change context to new section, create folder if necessary

        Args:
            new_section (string): new section name
        """
        self.section_name = self._remove_problematic_chars(new_section)
        # handle Folder

    def is_new_item(self, entry_name, url) -> bool:
        """check if the file already exist, but doesn't add it

        Args:
            entry_name (string): file/url name
            url (string): link to file

        Returns:
            bool: True if new, False if old
        """
        try:
            temp_cursor = self.cursor.execute(
                "SELECT * FROM main WHERE url=:url AND file_name=:entry_name", {
                'entry_name': entry_name,
                'url': url,
            })
            list_result = temp_cursor.fetchall()
        except Exception as error:
            print(f"""
                Failed to check if {entry_name} with URL: {url} exist in the database
                {self.course_name=}, {self.section_name=}
                {error=}
            """)
            raise
        return True if len(list_result) == 0 else False

    def add_if_summary_is_new(self, summary) -> None:
        """check if the summary already exist
        Args:
            summary (string): summary
        Returns:
            bool: True if add, False if already in database
        """
        try:
            temp_cursor = self.cursor.execute(
                "SELECT * FROM main WHERE extra_details=:summary AND file_name='summary'", {
                'summary': summary
            })
            list_result = temp_cursor.fetchall()
        except Exception as error:
            print(f"""
                Failed to check if {summary=} exist in the database
                {self.course_name=}, {self.section_name=} \n
                {error=}
            """)
            raise

        if len(list_result) == 0:
            self._add_new_entry("summary", "", summary)
            print(f"""
                **** new summary,
                {self.course_name=},
                {summary=}
            """)

    @staticmethod
    def _remove_problematic_chars(raw_name) -> string:
        """ remove problematic symbols

        Args:
            raw_name (string): raw name
        """
        return str.strip(raw_name.replace("'","").replace('"',"").replace('\n',""))

    def close_connection(self) -> None:
        """ Close connection to database
        """
        try:
            self.conn.close()
        except Exception as error:
            print(f"There has been an error closing the connection to the database\n{error=}")
            raise
