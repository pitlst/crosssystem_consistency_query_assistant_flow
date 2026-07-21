from collections.abc import Callable
from common import connect_source
from sql.eas import (
    get_select_eas_material_request_sql,
    get_select_eas_production_material_sql,
    get_select_eas_order_sql,
    get_select_eas_rework_order_sql,
    get_select_eas_order_exec_record_sql,
    get_select_eas_material_kitting_sql,
    get_select_eas_project_plan_sql,
    get_select_eas_rooting_sql,
    get_select_eas_pbom_sql
)
from sql.cg_mes import (
    get_select_cg_mes_bom_sql,
    get_select_cg_mes_diagnose_order_bom_sql,
    get_select_cg_mes_diagnose_pick_sql,
    get_select_cg_mes_record_sql,
    get_select_cg_mes_request_sql,
    get_select_cg_mes_scheduling_sql,
    get_select_cg_mes_order_scheduling_sql,
    get_select_cgmes_rework_order_sql,
    get_select_cgmes_rework_production_request_sql,
)
from sql.ct_mes import get_select_ct_mes_record_sql
from sql.jc_mes import get_select_jc_mes_record_sql
from sql.tz_mes import get_select_tz_mes_record_sql
from sql.zxj_mes import get_select_zxj_mes_record_sql


QUERY_REGISTRY: dict[str, tuple[Callable, connect_source, str]] = {
    "eas_pbom": (get_select_eas_pbom_sql, connect_source.EAS, "EAS - PBOM/工序BOM信息"),
    "eas_order": (get_select_eas_order_sql, connect_source.EAS, "EAS - 生产订单信息"),
    "eas_rooting": (get_select_eas_rooting_sql, connect_source.EAS, "EAS - 工艺路线信息"),
    "eas_production_material": (get_select_eas_production_material_sql, connect_source.EAS, "EAS - 生产备料/备料计划时序簿信息"),
    "eas_material_request": (get_select_eas_material_request_sql, connect_source.EAS, "EAS - 领料单信息"),
    "eas_rework_order": (get_select_eas_rework_order_sql, connect_source.EAS, "EAS - 返工订单/返工制造单信息"),
    "eas_order_exec_record": (get_select_eas_order_exec_record_sql, connect_source.EAS, "EAS - 生产订单变更执行记录"),
    "eas_material_kitting": (get_select_eas_material_kitting_sql, connect_source.EAS, "EAS - 物料齐套性分析"),
    "eas_project_plan": (get_select_eas_project_plan_sql, connect_source.EAS, "EAS - 项目计划"),

    "cgmes_pbom": (get_select_cg_mes_bom_sql, connect_source.MES_CG, "城轨MES - 工序BOM信息"),
    "cgmes_diagnose_order_bom": (get_select_cg_mes_diagnose_order_bom_sql, connect_source.MES_CG, "城轨MES - 订单BOM信息"),
    "cgmes_scheduling": (get_select_cg_mes_scheduling_sql, connect_source.MES_CG, "城轨MES - 模板排程信息"),
    "cgmes_order_scheduling": (get_select_cg_mes_order_scheduling_sql, connect_source.MES_CG, "城轨MES - 订单排程结果"),
    "cgmes_record": (get_select_cg_mes_record_sql, connect_source.MES_CG, "城轨MES - 派工单信息"),
    "cgmes_request": (get_select_cg_mes_request_sql, connect_source.MES_CG, "城轨MES - 配送需求单"),
    "cgmes_diagnose_pick": (get_select_cg_mes_diagnose_pick_sql, connect_source.MES_CG, "城轨MES - 领料单信息"),
    "cgmes_rework_order": (get_select_cgmes_rework_order_sql, connect_source.MES_CG, "城轨MES - 返工订单信息"),
    "cgmes_rework_production_request": (get_select_cgmes_rework_production_request_sql, connect_source.MES_CG, "城轨MES - 返工制造单信息"),

    "ctmes_request": (get_select_ct_mes_record_sql, connect_source.MES_CT, "车体MES - 派工单信息"),
    "jcmes_request": (get_select_jc_mes_record_sql, connect_source.MES_JC, "机车MES - 派工单信息"),
    "zxjmes_request": (get_select_zxj_mes_record_sql, connect_source.MES_ZXJ, "转向架MES - 派工单信息"),
    "tzmes_request": (get_select_tz_mes_record_sql, connect_source.MES_TZ, "涂装MES - 派工单信息"),
}
