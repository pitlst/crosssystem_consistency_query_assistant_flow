from dataclasses import dataclass
from pydantic import BaseModel
from enum import StrEnum
from sqlalchemy import Engine
from logger import logger
from typing import Any
import pandas as pd
import asyncio
import json
import clickhouse_connect.driver

@dataclass
class filter_data:
    project: str | None
    track_number: int | None
    jch_num: str | None
    process: str | None
    material: str | None
    order_code: str | None
    
class query_request(BaseModel):
    """查询请求体，字段对应 filter_data 筛选条件。"""
    project: str | None = None
    track_number: int | None = None
    jch_num: str | None = None
    process: str | None = None
    material: str | None = None
    order_code: str | None = None


class clickhouse_query_request(BaseModel):
    """ClickHouse 通用查询请求体。"""
    sql: str
    name: str = "clickhouse_query"


class connect_source(StrEnum):
    EAS = "eas"
    MES_CG = "cgmes"
    MES_CT = "ctmes"
    MES_JC = "jcmes"
    MES_ZXJ = "zxjmes"
    MES_TZ = "tzmes"
    
async def engine_query_to_json(engine: Engine, sql: str, name: str) -> dict[str, Any]:
    """在线程池中执行 SQL 查询，将 pandas DataFrame 转为 records 列表。"""
    try:
        df: pd.DataFrame = await asyncio.to_thread(pd.read_sql, sql, engine)
        records: dict = json.loads(df.to_json(orient="records", date_format="iso", force_ascii=False))
        logger.info(f"[{name}] 查询成功，返回 {len(df)} 条记录")
        return {"name": name, "data": records, "error": None}
    except Exception as e:
        logger.opt(exception=True).error(f"[{name}] SQL 查询失败 | 错误: {e}")
        return {"name": name, "data": [], "error": str(e)}


async def clickhouse_query_to_json(client: clickhouse_connect.driver.Client, sql: str, name: str) -> dict[str, Any]:
    """在线程池中执行 ClickHouse 查询，将 DataFrame 转为 records 列表。"""
    try:
        df: pd.DataFrame = await asyncio.to_thread(client.query_df, sql)
        records: dict = json.loads(df.to_json(orient="records", date_format="iso", force_ascii=False))
        logger.info(f"[{name}] ClickHouse 查询成功，返回 {len(df)} 条记录")
        return {"name": name, "data": records, "error": None}
    except Exception as e:
        logger.opt(exception=True).error(f"[{name}] ClickHouse 查询失败 | 错误: {e}")
        return {"name": name, "data": [], "error": str(e)}