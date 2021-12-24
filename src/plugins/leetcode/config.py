from pydantic import BaseSettings, Extra, Field
import typing


class Time(BaseSettings):
    hour: int = Field(0,alias="HOUR")
    minute: int = Field(0,alias="MINUTE")

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True


class Config(BaseSettings):
    # plugin custom config
    plugin_setting: str = "default"

    leetcode_qq_friends:  typing.List[int]
    leetcode_qq_groups:  typing.List[int]

    leetcode_inform_time:  typing.List[Time] 

    class Config:
        extra = Extra.allow
        case_sensitive = False
