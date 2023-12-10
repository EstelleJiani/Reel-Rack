"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This helpers includes common functions.
"""

import datetime as dt
from enum import Enum
import requests

import api_info
from config import Config

# The maximum request timeout (10s).
TIMEOUT = 10
# If there is no poster with a movie,
# show a default image.
DEFAULT_POSTER = "assets/no_poster.svg"
# This is the index for image size.
IMAGE_QUALITY = 2


class ImageType(Enum):
    """
    The ImageType class.
    Enum class defining the types of image.
    """
    BACKDROP = "backdrop_sizes"
    LOGO = "logo_sizes"
    POSTER = "poster_sizes"
    PROFILE = "profile_sizes"
    STILL = "still_sizes"


class FileType(Enum):
    """
    The FileType class.
    Enum class defining the types of files to write.
    """
    WATCHED = "database/watched.txt"
    WATCHLIST = "database/watchlist.txt"
    FAVOURITES = "database/favourites.txt"


def fetch_data_from_url(url: str, params: dict = None) -> dict:
    """
    Function:   Fetch the data from url.
    Parameters: a string which is a url
                a dictionary which is the parameters
    Return:     a dictionary which is the response.json()
    """
    if not isinstance(url, str):
        raise TypeError("'url' must be a string")
    if params is not None and \
       not isinstance(params, dict):
        raise TypeError("'params' must be a dictionary")

    try:
        response = requests.get(
            url,
            params,
            headers=api_info.HEADERS,
            timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        return {}
    if response.status_code != 200:
        return {}

    return response.json()


def save_list_to_file(file_type: FileType, lines: list) -> bool:
    """
    Save data to file depending on the FileType.
    """
    if not isinstance(file_type, FileType):
        raise TypeError("'file_type' must be a 'FileType' enum")
    if not isinstance(lines, list):
        raise TypeError("'lines' must be a list")

    try:
        with open(file_type.value, 'w', encoding="utf-8") as file:
            for line in lines:
                file.write(line)
            return True
    # except FileNotFoundError:
    #     return False
    # except PermissionError:
    #     return False
    except OSError:
        return False


def append_data_to_file(file_type: FileType, data: str) -> bool:
    """
    Append data to file depending on the FileType.
    """
    if not isinstance(file_type, FileType):
        raise TypeError("'file_type' must be a 'FileType' enum")
    if not isinstance(data, str):
        raise TypeError("'data' must be a string")

    try:
        with open(file_type.value, 'a', encoding="utf-8") as file:
            file.write(data)
            return True
    except OSError:
        return False


def read_list_from_file(file_type: FileType) -> list:
    """
    Read list from the file depending on the FileType.
    """
    if not isinstance(file_type, FileType):
        raise TypeError("'file_type' must be a 'FileType' enum")

    lines = []
    try:
        with open(file_type.value, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    except OSError:
        return []


def parse_data(data: list, sep: str = '|') -> list:
    """
    Parse the data.
    """
    if not isinstance(data, list):
        raise TypeError("'data' must be a list")
    if not isinstance(sep, str):
        raise TypeError("'sep' must be a string")

    # Reverse the order of the data
    data.reverse()

    data_list = []
    for line in data:
        data_list.append(line.strip().split(sep))
    return data_list


def get_image_config(image_type: ImageType) -> tuple:
    """
    Get the image configuration depending on the ImageType.
    """
    if not isinstance(image_type, ImageType):
        raise TypeError("'image_type' must be a 'ImageType' enum")

    config = fetch_data_from_url(api_info.CONFIGURATION_DETAILS_URL)

    base_url = config["images"]["secure_base_url"]
    file_size = {}
    file_size[ImageType.BACKDROP.value] = \
        config["images"][ImageType.BACKDROP.value]
    file_size[ImageType.LOGO.value] = \
        config["images"][ImageType.LOGO.value]
    file_size[ImageType.POSTER.value] = \
        config["images"][ImageType.POSTER.value]
    file_size[ImageType.PROFILE.value] = \
        config["images"][ImageType.PROFILE.value]
    file_size[ImageType.STILL.value] = \
        config["images"][ImageType.STILL.value]

    return base_url, file_size[image_type.value][IMAGE_QUALITY]


def get_image_url(image_type: ImageType, img_path: str) -> str:
    """
    Compose the image url.
    """
    if not isinstance(image_type, ImageType):
        raise TypeError("'image_type' must be a 'ImageType' enum")
    if img_path is not None and not isinstance(img_path, str):
        raise TypeError("'img_path' must be a string")

    # If there is no image with the movie, show the default image.
    if img_path is None or img_path == "":
        return DEFAULT_POSTER
    # If base_url and file_size were NOT fetched, then fetch them.
    # If base_url and file_size were fetched, we well NOT fetch them again.
    if Config.base_url == "" and Config.file_size is None:
        Config.base_url, Config.file_size = \
            get_image_config(image_type)

    return Config.base_url + Config.file_size + img_path


def string_to_date(date_str: str, sep: str = '-') -> dt.date:
    """
    Parse the string into date type.
    """
    if not isinstance(date_str, str):
        raise TypeError("'date_str' must be a string")
    if not isinstance(sep, str):
        raise TypeError("'sep' must be a string")

    if date_str == "" or date_str is None:
        return None
    year, month, day = date_str.split(sep)
    return dt.date(int(year), int(month), int(day))


def string_to_datetime(
        datetime_str: str,
        datetime_format: str = "%Y-%m-%d %H:%M:%S.%f"
) -> dt.datetime:
    """
    Parse the string into datetime type.
    """
    if not isinstance(datetime_str, str):
        raise TypeError("'datetime_str' must be a string")
    if not isinstance(datetime_format, str):
        raise TypeError("'datetime_format' must be a string")

    return dt.datetime.strptime(datetime_str, datetime_format)
