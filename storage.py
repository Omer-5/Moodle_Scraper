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
        self.section_name = ", "

        try:
            self.conn = sqlite3.connect('CURRENT_DATABASE_CAREFULL.db')
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

    def new_file_handler(self, entry_name, url, extra_details=""):
        """ Handles Database and local files
        """
        entry_name = self._remove_problematic_chars(entry_name)

        # Send to other class to handle local files

        # IMPORTANT: Adding to DB is the last thing
        self._add_new_entry(entry_name, url, extra_details)

    def _add_new_entry(self, entry_name, url, extra_details) -> None:
        """ IMPORTANT: INSERTING *WITHOUT*! CHECKING """
        date = self._get_date()

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
                ***** Failed adding to the database
                {self.course_name=}, {self.section_name=}, {entry_name=}\n
                {url=} | {date=}\n
                {extra_details=}\n\n
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

    def change_section(self, new_section) -> None:
        """ change context to new section, create folder if necessary

        Args:
            new_section (string): new section name
        """
        self.section_name = self._remove_problematic_chars(new_section)

    def is_new_item(self, entry_name, url) -> bool:
        """check if the file already exist, but doesn't add it

        Args:
            entry_name (string): file/url name
            url (string): link to file

        Returns:
            bool: True if new, False if old
        """
        try:
            entry_name = self._remove_problematic_chars(entry_name)
            temp_cursor = self.cursor.execute(
                "SELECT * FROM main WHERE url=:url AND file_name=:entry_name", {
                'entry_name': entry_name,
                'url': url,
            })

            list_result = temp_cursor.fetchall()
            if len(list_result) == 0:
                return True
        except Exception as error:
            print(f"""
                Failed to check if {entry_name} with URL: {url} exist in the database
                {self.course_name=}, {self.section_name=}
                {error=}
            """)
            raise
        return False

    def add_if_summary_is_new(self, summary) -> None:
        """add a summary if it doesn't exist
        Args:
            summary (string): summary
        """
        summary = self._remove_problematic_chars(summary)
        try:
            temp_cursor = self.cursor.execute(
                "SELECT * FROM main WHERE extra_details=:summary AND file_name='summary'", {
                'summary': summary
            })

            list_result = temp_cursor.fetchall()
            if len(list_result) == 0:
                self._add_new_entry("summary", "", summary)
                # print(f"""
                #     **** new summary, \n
                #     {self.course_name=}, \n
                #     {summary=}
                # """)
        except Exception as error:
            print(f"""
                Failed to check if {summary=} exist in the database
                {self.course_name=}, {self.section_name=} \n
                {error=}
            """)
            raise


    @staticmethod
    def _remove_problematic_chars(raw_name) -> string:
        """ remove problematic symbols

        Args:
            raw_name (string): raw name
        """
        blacklist = ("'", '"', "\n", "*", "%")
        for item in blacklist:
            raw_name = raw_name.replace(item, "")
        return str.strip(raw_name)

    def close_connection(self) -> None:
        """ Close connection to database
        """
        try:
            self.conn.close()
        except Exception as error:
            print(f"There has been an error closing the connection to the database\n{error=}")
            raise
