import oracledb
import clickhouse_connect
import clickhouse_connect.driver
from pathlib import Path
from sqlalchemy import create_engine, Engine
from common import connect_source

# Oracle Instant Client 路径（相对于当前文件所在目录）
ORACLE_CLIENT_LIB_DIR = str(
    Path(__file__).parent
    / "source"
    / "instantclient-basic-windows.x64-19.31.0.0.0dbru"
    / "instantclient_19_31"
)

_client_initialized = False


def _ensure_thick_mode() -> None:
    global _client_initialized
    if not _client_initialized:
        oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_LIB_DIR)
        _client_initialized = True


def create_connection(conn_type: connect_source) -> Engine:
    _ensure_thick_mode()
    if conn_type == connect_source.EAS:
        return create_engine(
            "oracle+oracledb://easselect:easselect@172.18.1.121:1521/?service_name=eas",
            max_identifier_length=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )
    elif conn_type == connect_source.MES_CG or \
            conn_type == connect_source.MES_CT or \
            conn_type == connect_source.MES_JC:
        return create_engine(
            "oracle+oracledb://unimax_cg:unimax_cg@10.24.212.17:1521/?service_name=ORCL",
            max_identifier_length=30,   # Oracle 11g 标识符限制
            pool_pre_ping=True,          # 使用前检查连接有效性
            pool_recycle=3600,           # 1 小时后回收（防止 Oracle 杀空闲连接）
            echo=False,
        )
    elif conn_type == connect_source.MES_ZXJ:
        return create_engine(
            "oracle+oracledb://unimax_zxj_zelc:unimax_zxj_zelc@10.24.1.49:1521/?service_name=ORCL",
            max_identifier_length=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )
    elif conn_type == connect_source.MES_TZ:
        return create_engine(
            "oracle+oracledb://unimax_tz_zelc:unimax_tz_zelc@10.24.206.2:1521/?service_name=ORCL",
            max_identifier_length=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )
    else:
        raise RuntimeError("不支持的数据源")


def create_clickhouse_client() -> clickhouse_connect.driver.Client:
    """创建 ClickHouse 原生客户端连接（非 SQLAlchemy）。"""
    return clickhouse_connect.get_client(
        host="10.24.5.59",
        port=8123,
        username="cheakf",
        password="Swq8855830.",
        database="default",
    )
