"""
custom-portfolio-analyzer - A tool to model, back-test, and compare the performance of your own custom portfolios.
Copyright (C) 2025  Fevzi Babaoğlu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


from datetime import datetime, date


class DateUtils:
    DATE_FORMAT = "%d.%m.%Y"

    @classmethod
    def set_date_format(cls, date_format: str):
        cls.DATE_FORMAT = date_format

    @classmethod
    def get_date_format(cls) -> str:
        return cls.DATE_FORMAT


    @staticmethod
    def parse_date(date_str: str) -> date:
        return datetime.strptime(date_str, DateUtils.DATE_FORMAT).date()

    @staticmethod
    def format_date(date_obj: date) -> str:
        return date_obj.strftime(DateUtils.DATE_FORMAT)

    @staticmethod
    def get_today() -> date:
        return date.today()
