from common import filter_data


def get_select_cg_mes_bom_sql(data: filter_data) -> str:
    '''获取城轨MES的BOM相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND "BILL"."PRO_CODE" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL"."START_CAR_CODE", -4)) <= {data.track_number} AND TO_NUMBER(SUBSTR("BILL"."END_CAR_CODE", -4)) >= {data.track_number} '
    if data.process is not None:
        _where += f' AND "BILL"."OP_CODE" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "BILL"."MRL_CODE" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."PRO_CODE" AS "项目编码",
    "BILL"."PRO_NAME" AS "项目名称",
    "BILL"."START_CAR_CODE" AS "起始车号",
    "BILL"."END_CAR_CODE" AS "结束车号",
    "BILL"."OP_LINE_CODE" AS "工艺路线编码",
    "BILL"."OP_LINE_NAME" AS "工艺路线名称",
    "BILL"."OP_CODE" AS "工序编码",
    "BILL"."OP_NAME" AS "工序名称",
    "BILL"."PRO_MRL_CODE" AS "产品物料编码",
    "BILL"."PRO_MRL_NAME" AS "部件产品名称",
    "BILL"."MRL_CODE" AS "物料编码",
    "BILL"."MRL_NAME" AS "物料名称",
    "BILL"."SUM_UNIT" AS "计量单位",
    "BILL"."TOTAL" AS "数量",
    "BILL"."DIS_TYPE" AS "物料类别",
    CASE 
        WHEN "BILL"."IS_IMPORTANT" = 0 THEN '是' 
        WHEN "BILL"."IS_IMPORTANT" = 1 THEN '否' 
        ELSE TO_CHAR("BILL"."IS_IMPORTANT") 
    END AS "是否关重件",
    "BILL"."COMPOSE_NUM" AS "配盘方案号",
    "BILL"."BOM_CODE" AS "BOM编码",
    "BILL"."BOM_NAME" AS "BOM名称",
    "BILL"."BOM_ITEM_ID" AS "制造BOM分录行id",
    "BILL"."PRCS_BOM_ID" AS "BOMID",
    "BILL"."DITEM_ID" AS "设计图号",
    "BILL"."DA_SSEMBLE_NUM" AS "设计装配数量",
    "BILL"."DA_SSEMBLE_SEQ" AS "设计装配序号",
    "BILL"."FFLOW" AS "流程",
    "BILL"."GID" AS "GID",
    "BILL"."REMARK" AS "备注",
    "BILL"."UDA1" AS "备用字段1",
    "BILL"."UDA2" AS "备用字段2",
    "BILL"."UDA3" AS "备用字段3",
    "BILL"."UDA4" AS "备用字段4",
    "BILL"."UDA5" AS "备用字段5",
    "BILL"."UDA1C" AS "备用字段1编码",
    "BILL"."UDA1N" AS "备用字段1名称",
    "BILL"."UDA2C" AS "备用字段2编码",
    "BILL"."UDA2N" AS "备用字段2名称",
    "BILL"."UDA3C" AS "备用字段3编码",
    "BILL"."UDA3N" AS "备用字段3名称",
    "BILL"."UDA4C" AS "备用字段4编码",
    "BILL"."UDA4N" AS "备用字段4名称",
    "BILL"."UDA5C" AS "备用字段5编码",
    "BILL"."UDA5N" AS "备用字段5名称",
    "BILL"."CREATE_ID" AS "创建人",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."MODIFY_ID" AS "修改人",
    "BILL"."MODIFY_DATE" AS "修改时间",
    CASE 
        WHEN "BILL"."IS_ACTIVE" = 0 THEN '激活' 
        WHEN "BILL"."IS_ACTIVE" = 1 THEN '冻结' 
        ELSE TO_CHAR("BILL"."IS_ACTIVE") 
    END AS "激活标识",
    CASE 
        WHEN "BILL"."IS_DELETE" = 0 THEN '未删除' 
        WHEN "BILL"."IS_DELETE" = 1 THEN '删除' 
        ELSE TO_CHAR("BILL"."IS_DELETE") 
    END AS "删除标识",
    "BILL"."DELETED" AS "DELETED",
    "BILL"."DATA_ROLE" AS "工厂GID",
    "BILL"."DATA_ROLE1" AS "工作中心GID",
    "BILL"."DATA_ROLE2" AS "工作中心层级权值"
FROM "UNIMAX_CG"."OPERATION_BOM" "BILL"
WHERE
    {_where}
"""


def get_select_cg_mes_scheduling_sql(data: filter_data) -> str:
    '''获取城轨MES的模板排程结果相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND "RL"."UDA_PRO_CODE" = \'{data.project}\''
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("RL"."UDA_CAR_CODE", -4)) <= {data.track_number} AND TO_NUMBER(SUBSTR("RL"."UDA_CAR_CODE_END", -4)) >= {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("RL"."UDA_SINGER_CAR_CODE") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OP"."DEF_OP_CODE" = \'{data.process}\' '
    return f"""
SELECT
    DISTINCT
    "RL"."UDA_PRO_CODE" AS "项目编号",
    "RL"."UDA_PRO_NAME" AS "项目名称",
    "RL"."UDA_CAR_CODE" AS "开始车号",
    "RL"."UDA_CAR_CODE_END" AS "结束车号",
    "RL"."UDA_SINGER_CAR_CODE" AS "节车号",
    "RL"."WORK_CENTER_GID" AS "工作中心ID",
    "CENTER"."NAME" AS "工作中心名称",
    "OP"."DEF_OP_CODE" AS "排程工序编码",
    "OP"."DEF_OP_NAME" AS "排程工序名称",
    "OP"."GROUP_NAME" AS "排程工序班组名称",
    "BILL"."OP_SEQ" AS "工艺顺序",
    "BILL"."PC_SEQ" AS "排程顺序",
    "BILL"."OP_CYCLE" AS "工艺循环",
    "RL"."VERSION_CODE" AS "版本号",
    "BILL"."START_TIME" AS "开始时间",
    "BILL"."END_TIME" AS "结束时间",
    "BILL"."GID" AS "GID",
    "BILL"."DEF_OP_GID" AS "排程工序ID",
    "RL"."GID" AS "排程路线ID",
    "BILL"."CREATE_ID" AS "排程工序创建人",
    "BILL"."CREATE_DATE" AS "排程工序创建时间",
    "BILL"."MODIFY_ID" AS "排程工序修改人",
    "BILL"."MODIFY_DATE" AS "排程工序修改时间",
    "RL"."CREATE_ID" AS "排程路线创建人",
    "RL"."CREATE_DATE" AS "排程路线创建时间",
    "RL"."MODIFY_ID" AS "排程路线修改人",
    "RL"."MODIFY_DATE" AS "排程路线修改时间"
FROM
    "UNIMAX_CG"."MBF_APS_ROUTE_OPERATION_MB" "BILL"
    LEFT JOIN "UNIMAX_CG"."MBF_DEF_OPERATION" "OP" ON 
        "BILL"."DEF_OP_GID" = "OP"."GID" 
        AND "OP"."IS_DELETE" <> 1 
        AND "OP"."IS_ACTIVE" = 0
    LEFT JOIN "UNIMAX_CG"."MBF_APS_ROUTE_LINE_MB" "RL" ON 
        "BILL"."APS_ROUTE_LINE_GID" = "RL"."GID"
        AND "RL"."IS_DELETE" <> 1 
        AND "RL"."IS_ACTIVE" = 0
    LEFT JOIN "UNIMAX_CG"."PMBF_WORK_CENTER" "CENTER" ON 
        "RL"."WORK_CENTER_GID" = "CENTER"."GID"
        AND "CENTER"."IS_DELETE" <> 1 
        AND "CENTER"."IS_ACTIVE" = 0
WHERE
    {_where}
"""


def get_select_cg_mes_order_scheduling_sql(data: filter_data) -> str:
    '''获取城轨MES的订单排程结果相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND "BILL"."PRO_CODE" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL"."CAR_CODE", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("BILL"."SINGLE_CAR_CODE") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "BILL"."OP_CODE" = \'{data.process}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."STATE" AS "下发状态",
    "BILL"."PRO_CODE" AS "项目号",
    "BILL"."CAR_CODE" AS "车号",
    "BILL"."SINGLE_CAR_CODE" AS "节车号",
    "BILL"."WORKSHOP" AS "车间",
    "BILL"."OP_CODE" AS "工序编码",
    "BILL"."OP_NAME" AS "工序名称",
    "BILL"."PLAN_START_TIME" AS "计划开始时间",
    "BILL"."PLAN_END_TIME" AS "计划结束时间",
    "BILL"."START_WORK_STAGE" AS "开工台位",
    "BILL"."PRODU_PLACE" AS "场地",
    "BILL"."GROUP_CODE" AS "班组代码",
    "BILL"."GROUP_NAME" AS "班组名称",
    "BILL"."CELL_CODE" AS "工位编码",
    "BILL"."CELL_NAME" AS "工位名称"
FROM "UNIMAX_CG"."UMPP_PLAN_SCHEDULE_RT" "BILL"
WHERE
    {_where}
"""


def get_select_cg_mes_record_sql(data: filter_data) -> str:
    '''获取城轨MES的派工单相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND "BILL"."PROJECT" = \'{data.project}\''
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL"."CAR_CODE", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("BILL"."SINGER_CAR_CODE") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "BILL"."OP_CODE" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "BILL"."MRL_CODE" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."GID" AS "GID",
    "BILL"."DISPATCH_CODE" AS "派工单编号",
    "BILL"."PRODU_UID" AS "产品号",
    "BILL"."PRODU_NAME" AS "产品名称",
    "BILL"."LOT_CODE" AS "批次号",
    "BILL"."MRL_CODE" AS "车型/物料编码",
    "BILL"."ORDER_CODE" AS "订单号",
    "BILL"."ORDER_TYPE" AS "订单类型",
    "BILL"."WORK_ORDER_ID" AS "计划工单编码",
    "BILL"."WORK_ORDER_GID" AS "计划工单主键",
    "BILL"."PRO_TYPE" AS "生产方式",
    "BILL"."WORK_CENTER_GID" AS "工作中心",
    "BILL"."PREDICT_DATE" AS "预计下线时间",
    "BILL"."WORK_CELL_GID" AS "工位主键",
    "BILL"."NOW_DAQ" AS "当前所在采集点",
    "BILL"."NOW_DAQ_ID" AS "当前采集点操作人",
    "BILL"."NOW_DAQ_DATE" AS "当前采集点采集时间",
    "BILL"."NEXT_DAQ" AS "下一采集点",
    "BILL"."NEXT_DAQ_DATE" AS "预计下一采时间",
    "BILL"."FREEZE_LOCATION" AS "冻结位置",
    "BILL"."FREEZE_DATE" AS "冻结时间",
    "BILL"."REASON" AS "冻结原因描述",
    "BILL"."DISPOSE_TYPE" AS "处理类型",
    "BILL"."DISPOSE_CONTENT" AS "处理内容",
    "BILL"."ORDER_STATE" AS "订单状态",
    "BILL"."OPERATE_STATE" AS "操作状态",
    "BILL"."WORK_ORDER_STATE" AS "工单状态",
    "BILL"."PLAN_QTY" AS "计划数量",
    "BILL"."ROUTE_ID" AS "工艺路线编号",
    "BILL"."ROUTE_VERSION" AS "工艺路线版本",
    "BILL"."ROUTE_GID" AS "工艺路线主键",
    "BILL"."PLANNED_START_TIME" AS "计划开始时间",
    "BILL"."PLANNED_FINISH_TIME" AS "计划结束时间",
    "BILL"."UNFREEZE_DATE" AS "解冻时间",
    "BILL"."UNFREEZE_LOCATION" AS "解冻位置",
    "BILL"."FREEZE_ID" AS "冻结人",
    "BILL"."UNFREEZE_ID" AS "解冻人",
    "BILL"."COMPLETE_DATE" AS "完工时间",
    "BILL"."PUBLISH_STATE" AS "发布状态",
    "BILL"."PUBLISH_DATE" AS "发布时间",
    "BILL"."ACTUAL_BEGIN_DATE" AS "实际开始时间",
    "BILL"."ACTUAL_END_DATE" AS "实际结束时间",
    "BILL"."WORK_DATE" AS "工时(秒)",
    "BILL"."OP_PID" AS "父工序",
    "BILL"."OP_GID" AS "工序主键",
    "BILL"."OP_CODE" AS "工序编码",
    "BILL"."PLAN_OP_SEQ" AS "计划工序步骤顺序",
    "BILL"."ACTUAL_OP_SEQ" AS "实际工序步骤顺序",
    "BILL"."EFFECTIVE_QTY" AS "良品数",
    "BILL"."UNEFFECTIVE_QTY" AS "不良品数",
    "BILL"."DISCARD_QTY" AS "报废数",
    "BILL"."TRANS_QTY" AS "转序数量",
    "BILL"."WORK_ORDER_FLAG" AS "工单所在工序标识",
    "BILL"."CHK_ID" AS "录入人",
    "BILL"."CHK_DATE" AS "录入时间",
    "BILL"."LABOUR_GROUP_GID" AS "班组主键",
    "BILL"."FEATURE_LOT_CODE" AS "特征批次号",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."CREATE_ID" AS "创建人",
    "BILL"."MODIFY_DATE" AS "修改时间",
    "BILL"."MODIFY_ID" AS "修改人",
    "BILL"."REMARK" AS "备注",
    "BILL"."UDA2" AS "绑定大梁流水号",
    "BILL"."UDA3" AS "绑定腹板流水号",
    "BILL"."UDA4" AS "流水号",
    "BILL"."UDA5" AS "工作单元",
    "BILL"."UDA6" AS "客户",
    "BILL"."UDA7" AS "根订单号(jydxs)",
    "BILL"."UDA8" AS "台位编码(株机推广)",
    "BILL"."UDA9" AS "排程节拍时间(min)",
    "BILL"."UDA10" AS "载体码[JYDJJ]",
    "BILL"."DELETED" AS "DELETED",
    "BILL"."DATA_ROLE" AS "工厂GID",
    "BILL"."IS_LAST" AS "是否尾单",
    "BILL"."SEQ" AS "任务单工序顺序号",
    "BILL"."REQ_NUM" AS "需求数量",
    "BILL"."PARENT_GID" AS "拆分时父派工单gid",
    "BILL"."DATA_ROLE1" AS "工作中心GID",
    "BILL"."DATA_ROLE2" AS "工作中心层级权值",
    "BILL"."UDA_NCR_CODE" AS "NCR追溯号",
    "BILL"."PROJECT" AS "项目",
    "BILL"."COMPONENT" AS "部件",
    "BILL"."UDA1C" AS "备用字段1编码",
    "BILL"."UDA1N" AS "备用字段1名称",
    "BILL"."UDA2C" AS "挂载设备编码(株机推广)",
    "BILL"."UDA2N" AS "挂载设备名称(株机推广)",
    "BILL"."UDA3C" AS "备用字段3编码",
    "BILL"."UDA3N" AS "备用字段3名称",
    "BILL"."UDA4C" AS "备用字段4编码",
    "BILL"."UDA4N" AS "备用字段4名称",
    "BILL"."UDA5C" AS "备用字段5编码",
    "BILL"."UDA5N" AS "备用字段5名称",
    "BILL"."EQUIP_CD" AS "主设备编码",
    "BILL"."EOUIP_CD" AS "副设备编码",
    "BILL"."CAR_CODE" AS "车号",
    "BILL"."START_DAQ_CODE" AS "开工人员code",
    "BILL"."START_DAQ_NAME" AS "开工人员name",
    "BILL"."END_DAQ_CODE" AS "完工人员code",
    "BILL"."END_DAQ_NAME" AS "完工人员name",
    "BILL"."VER" AS "版本号乐观锁",
    "BILL"."GROUP_CODE" AS "组编码",
    "BILL"."WORK_PERSION" AS "操作人员",
    "BILL"."SINGER_CAR_CODE" AS "节车号",
    "BILL"."PRODU_PLACE" AS "场地",
    "BILL"."TRANSMITER" AS "下达人",
    "BILL"."TRANSMIT_TIME" AS "下达时间",
    "BILL"."STAGE_POSITION" AS "台位",
    "BILL"."FINISH_QTY" AS "完成数量",
    "BILL"."REPEAT_ID" AS "相同板数",
    "BILL"."PROGRAM_NAME" AS "程序名",
    "BILL"."TASK_DISPATCHER" AS "任务派发人",
    "BILL"."BATCH_NO" AS "炉批号",
    "BILL"."CHENK_POSITION_CODE" AS "审核人编码",
    "BILL"."SUPPLIER" AS "供应商",
    "BILL"."ISSUED_CHENK_POSITION" AS "审核人",
    "BILL"."ISSUED_CHENK_DATE" AS "审核时间",
    "BILL"."REPORT_REPEAT_ID" AS "已报工板数",
    "BILL"."ASSISTANTS" AS "协助人员",
    "BILL"."STAGE_EDIT_PERSION" AS "台位变更人",
    "BILL"."STAGE_EDIT_DATE" AS "台位变更时间",
    "BILL"."PRIORITY" AS "优先级(备料)",
    "BILL"."IS_START_CHECK" AS "开工是否检查",
    "BILL"."START_CHECK_EMP" AS "检查人",
    "BILL"."START_CHECK_DATE" AS "检查时间",
    "BILL"."WORK_HOUR_CHECK_EMP" AS "上报审批人",
    "BILL"."WORK_HOUR_CHECK_DATE" AS "上报审批时间",
    "BILL"."WORK_HOUR_DOWN_EMP" AS "上报驳回人",
    "BILL"."WORK_HOUR_DOWN_DATE" AS "上报驳回时间",
    "BILL"."WORK_HOUR_DOWN_CAUSE" AS "上报驳回原因",
    "BILL"."CELL_GSSP_ADDRESS_GID" AS "工位地址对照关系ID",
    "BILL"."ADDRESS_CODE" AS "呼叫物料后的实际地址",
    "BILL"."WORK_ADJUST_DATE" AS "派活时间",
    "BILL"."WORK_HOUR_SUBMIT_EMP" AS "上报提交人",
    "BILL"."WORK_HOUR_SUBMIT_DATE" AS "上报提交时间",
    CASE
        WHEN "BILL"."DIS_CODE_STATE" = 0
        THEN '待开工'
        WHEN "BILL"."DIS_CODE_STATE" = 1
        THEN '开工'
        WHEN "BILL"."DIS_CODE_STATE" = 2
        THEN '暂停'
        WHEN "BILL"."DIS_CODE_STATE" = 3
        THEN '完工'
        ELSE TO_CHAR("BILL"."DIS_CODE_STATE")
    END AS "派工单状态",
    CASE WHEN "BILL"."KPART_FLAG" = 0 THEN '未生成' WHEN "BILL"."KPART_FLAG" = 1 THEN '已生成' ELSE TO_CHAR("BILL"."KPART_FLAG") END AS "生成关键件标志",
    CASE WHEN "BILL"."ISCOMPLETE" = '0' THEN '未完工' WHEN "BILL"."ISCOMPLETE" = '1' THEN '已完工' ELSE TO_CHAR("BILL"."ISCOMPLETE") END AS "是否完工",
    CASE
        WHEN "BILL"."IS_DOWN" = 0
        THEN '未上线'
        WHEN "BILL"."IS_DOWN" = 1
        THEN '未上线进保护区'
        WHEN "BILL"."IS_DOWN" = 2
        THEN '在线'
        WHEN "BILL"."IS_DOWN" = 3
        THEN '已下线'
        WHEN "BILL"."IS_DOWN" = 4
        THEN '质检合格'
        ELSE TO_CHAR("BILL"."IS_DOWN")
    END AS "产线标志位",
    CASE WHEN "BILL"."OP_FLAG" = 0 THEN '工序' WHEN "BILL"."OP_FLAG" = 1 THEN '工步' ELSE TO_CHAR("BILL"."OP_FLAG") END AS "工序标识",
    CASE WHEN "BILL"."IS_ACTIVE" = 0 THEN '激活' WHEN "BILL"."IS_ACTIVE" = 1 THEN '冻结' ELSE TO_CHAR("BILL"."IS_ACTIVE") END AS "激活标识",
    CASE WHEN "BILL"."IS_DELETE" = 0 THEN '未删除' WHEN "BILL"."IS_DELETE" = 1 THEN '删除' ELSE TO_CHAR("BILL"."IS_DELETE") END AS "删除标识",
    CASE WHEN "BILL"."UDA1" = '0' THEN '初始状态' WHEN "BILL"."UDA1" = '1' THEN '返修状态' WHEN "BILL"."UDA1" = '2' THEN '返修完成' ELSE TO_CHAR("BILL"."UDA1") END AS "返修状态[东风贝洱]",
    CASE
        WHEN "BILL"."QUALITY_STATE" = 4
        THEN '正常'
        WHEN "BILL"."QUALITY_STATE" = 5
        THEN '隔离'
        WHEN "BILL"."QUALITY_STATE" = 6
        THEN '冻结'
        WHEN "BILL"."QUALITY_STATE" = 7
        THEN '返修'
        WHEN "BILL"."QUALITY_STATE" = 8
        THEN '终止'
        ELSE TO_CHAR("BILL"."QUALITY_STATE")
    END AS "质量状态",
    CASE WHEN "BILL"."IS_FREEZE" = 0 THEN '解冻' WHEN "BILL"."IS_FREEZE" = 1 THEN '冻结' ELSE TO_CHAR("BILL"."IS_FREEZE") END AS "冻结解冻标志位",
    CASE WHEN "BILL"."IS_CLOSE" = 0 THEN '未关闭' WHEN "BILL"."IS_CLOSE" = 1 THEN '关闭' ELSE TO_CHAR("BILL"."IS_CLOSE") END AS "关闭标志位",
    CASE WHEN "BILL"."IS_SPLIT" = 0 THEN '未拆分' WHEN "BILL"."IS_SPLIT" = 1 THEN '已拆分' ELSE TO_CHAR("BILL"."IS_SPLIT") END AS "拆分标志位",
    CASE WHEN "BILL"."UDA_OUT_STATE" = '0' THEN '正常' WHEN "BILL"."UDA_OUT_STATE" = '1' THEN '委外' ELSE TO_CHAR("BILL"."UDA_OUT_STATE") END AS "委外状态",
    CASE WHEN "BILL"."CHECK_STATE" = 0 THEN '未检查未通过' WHEN "BILL"."CHECK_STATE" = 1 THEN '已检查未通过' WHEN "BILL"."CHECK_STATE" = 2 THEN '已检查已通过' ELSE TO_CHAR("BILL"."CHECK_STATE") END AS "检查状态",
    CASE WHEN "BILL"."FORCED_START" = 0 THEN '未强制' WHEN "BILL"."FORCED_START" = 1 THEN '已强制' ELSE TO_CHAR("BILL"."FORCED_START") END AS "强制开工",
    CASE WHEN "BILL"."UDA_TRANSMIT" = 0 THEN '未下达' WHEN "BILL"."UDA_TRANSMIT" = 1 THEN '已下达' ELSE TO_CHAR("BILL"."UDA_TRANSMIT") END AS "项目下达标志位",
    CASE WHEN "BILL"."SCHEDULE_STATE" = 0 THEN '未排程' WHEN "BILL"."SCHEDULE_STATE" = 1 THEN '已排程' ELSE TO_CHAR("BILL"."SCHEDULE_STATE") END AS "排程状态",
    CASE WHEN "BILL"."IS_LOCK_RESOLVE" = 0 THEN '未锁定分解' WHEN "BILL"."IS_LOCK_RESOLVE" = 1 THEN '已锁定分解' ELSE TO_CHAR("BILL"."IS_LOCK_RESOLVE") END AS "是否锁定分解",
    CASE WHEN "BILL"."BIND_TOOL_FLAG" = 0 THEN '需要' WHEN "BILL"."BIND_TOOL_FLAG" = 1 THEN '不需要' ELSE TO_CHAR("BILL"."BIND_TOOL_FLAG") END AS "是否需要绑定工具工装",
    CASE WHEN "BILL"."CAR_STATE" = '0' THEN '未进车' WHEN "BILL"."CAR_STATE" = '1' THEN '已进车' WHEN "BILL"."CAR_STATE" = '2' THEN '已落车' ELSE TO_CHAR("BILL"."CAR_STATE") END AS "台位状态",
    CASE
        WHEN "BILL"."ISSUED_CHENK_STATE" = 0
        THEN '未审核'
        WHEN "BILL"."ISSUED_CHENK_STATE" = 1
        THEN '不通过'
        WHEN "BILL"."ISSUED_CHENK_STATE" = 2
        THEN '不通过'
        ELSE TO_CHAR("BILL"."ISSUED_CHENK_STATE")
    END AS "审核状态",
    CASE WHEN "BILL"."REVERSE_ISSUED" = 0 THEN '否' WHEN "BILL"."REVERSE_ISSUED" = 1 THEN '是' ELSE TO_CHAR("BILL"."REVERSE_ISSUED") END AS "是否反下达",
    CASE WHEN "BILL"."SEND_REQ_MRL" = 0 THEN '否' WHEN "BILL"."SEND_REQ_MRL" = 1 THEN '是' ELSE TO_CHAR("BILL"."SEND_REQ_MRL") END AS "物料需求是否发送",
    CASE
        WHEN "BILL"."CHK_FLAG" = 0
        THEN '无检验'
        WHEN "BILL"."CHK_FLAG" = 1
        THEN '开工检'
        WHEN "BILL"."CHK_FLAG" = 2
        THEN '完工检'
        WHEN "BILL"."CHK_FLAG" = 3
        THEN '开完工检'
        ELSE TO_CHAR("BILL"."CHK_FLAG")
    END AS "检验标识",
    CASE WHEN "BILL"."IS_REQRM_FILE" = 0 THEN '否' WHEN "BILL"."IS_REQRM_FILE" = 1 THEN '是' ELSE TO_CHAR("BILL"."IS_REQRM_FILE") END AS "转运任务是否生成",
    CASE WHEN "BILL"."IS_MAN_HOUR_RPT" = 0 THEN '否' WHEN "BILL"."IS_MAN_HOUR_RPT" = 1 THEN '是' ELSE TO_CHAR("BILL"."IS_MAN_HOUR_RPT") END AS "工时是否上报",
    CASE WHEN "BILL"."IS_EQUIP_START_CHECK" = 0 THEN '否' WHEN "BILL"."IS_EQUIP_START_CHECK" = 1 THEN '是' ELSE TO_CHAR("BILL"."IS_EQUIP_START_CHECK") END AS "是否进行设备开工检查",
    CASE WHEN "BILL"."IS_FILE_START_CHECK" = 0 THEN '否' WHEN "BILL"."IS_FILE_START_CHECK" = 1 THEN '是' ELSE TO_CHAR("BILL"."IS_FILE_START_CHECK") END AS "是否进行工艺开工检查",
    CASE WHEN "BILL"."IS_FINSH_CHECK" = 0 THEN '否' WHEN "BILL"."IS_FINSH_CHECK" = 1 THEN '是' ELSE TO_CHAR("BILL"."IS_FINSH_CHECK") END AS "是否完工后检测",
    CASE WHEN "BILL"."IS_FINISH_SHOW" = '0' THEN '否' WHEN "BILL"."IS_FINISH_SHOW" = '1' THEN '是' ELSE TO_CHAR("BILL"."IS_FINISH_SHOW") END AS "完工是否显示"
FROM "UNIMAX_CG"."UEX_VTRACK_RECORD" "BILL"
WHERE
    {_where}
"""


def get_select_cg_mes_request_sql(data: filter_data) -> str:
    '''获取城轨MES的配送需求单相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0'
    if data.project is not None:
        _where += f' AND "BILL"."UDA_PROJECT_NUM" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL"."UDA_CAR_NUM", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("BILL"."UDA4") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OP"."OP_CODE" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "BILL_ENTRY"."MRL_CODE" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."GID" AS "zid",
    "BILL"."CODE" AS "需求单号",
    "BILL"."WORK_CENTER_CODE" AS "工作中心代码",
    "BILL"."WORK_CENTER_NAME" AS "工作中心名称",
    CASE WHEN "BILL"."REQ_TYPE" = 0 THEN '计划内' WHEN "BILL"."REQ_TYPE" = 1 THEN '计划外' ELSE TO_CHAR("BILL"."REQ_TYPE") END AS "需求类型",
    "BILL"."DELV_TYPE_CODE" AS "配送类型代码",
    "BILL"."DELV_TYPE_NAME" AS "配送类型名称",
    "BILL"."BEGIN_NODE_NAME" AS "起始点名称",
    "BILL"."END_NODE_NAME" AS "结束点名称",
    "BILL"."WORK_ORDER_CODE" AS "工单号",
    "OP"."OP_CODE" AS "工序编码",
    "OP"."OP_NAME" AS "工序名称",
    "BILL"."PUBLISH_STATE" AS "发布状态",
    "BILL"."REMARK" AS "备注",
    "BILL"."CREATE_ID" AS "创建人",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."MODIFY_ID" AS "修改人",
    "BILL"."MODIFY_DATE" AS "修改时间",
    CASE WHEN "BILL"."IS_ACTIVE" = 0 THEN '激活' WHEN "BILL"."IS_ACTIVE" = 1 THEN '冻结' ELSE TO_CHAR("BILL"."IS_ACTIVE") END AS "激活标识",
    CASE WHEN "BILL"."IS_DELETE" = 0 THEN '未删除' WHEN "BILL"."IS_DELETE" = 1 THEN '删除' ELSE TO_CHAR("BILL"."IS_DELETE") END AS "删除标识",
    "BILL"."UDA1" AS "台位",
    CASE WHEN "BILL"."UDA2" = 0 THEN '未发送' WHEN "BILL"."UDA2" = 1 THEN '配送计划已提交' WHEN "BILL"."UDA2" = 2 THEN '配送结果已提交' ELSE TO_CHAR("BILL"."UDA2") END AS "配送状态",
    "BILL"."UDA3" AS "台位编码",
    "BILL"."UDA4" AS "节车号",
    "BILL"."UDA5" AS "预留字段5",
    "BILL"."UDA6" AS "预留字段6",
    "BILL"."UDA7" AS "预留字段7",
    "BILL"."UDA8" AS "预留字段8",
    "BILL"."UDA9" AS "预留字段9",
    "BILL"."UDA10" AS "预留字段10",
    "BILL"."DELETED" AS "DELETED",
    "BILL"."REJECT_STATE" AS "退料确认状态",
    "BILL"."PUBLISH_TIME" AS "发布时间",
    "BILL"."INIT_DATE" AS "初始化时间",
    "BILL"."KANBAN_CLASS_CODE" AS "看板类别编号",
    CASE
        WHEN "BILL"."STATUS" = 0
        THEN '已发出'
        WHEN "BILL"."STATUS" = 1
        THEN '已配盘'
        WHEN "BILL"."STATUS" = 2
        THEN '部分接收'
        WHEN "BILL"."STATUS" = 3
        THEN '全部接收'
        WHEN "BILL"."STATUS" = 4
        THEN '未发送'
        ELSE TO_CHAR("BILL"."STATUS")
    END AS "状态",
    "BILL"."DATA_ROLE" AS "工厂GID",
    "BILL"."DATA_ROLE1" AS "工作中心GID",
    "BILL"."DATA_ROLE2" AS "工作中心层级权值",
    "BILL"."DUE_QTY" AS "需求数量",
    "BILL"."DIS_QTY" AS "完成数量",
    "BILL"."UDA_PROJECT_NUM" AS "项目号",
    "BILL"."UDA_PROJECT_NAME" AS "项目名称",
    "BILL"."UDA_CAR_NUM" AS "车号",
    "BILL"."UDA_PLAN_ORDER" AS "订单号",
    "BILL"."UDA_SEND_TIME" AS "配送时间",
    "BILL"."UDA_TRACK_ORDER" AS "派工单",
    "BILL"."UDA_WORK_CELL" AS "配送工位",
    "BILL"."UDA_START_TIME" AS "派工单开始时间",
    "BILL"."UDA1C" AS "备用字段1编码",
    "BILL"."UDA1N" AS "备用字段1名称",
    "BILL"."UDA2C" AS "备用字段2编码",
    "BILL"."UDA2N" AS "备用字段2名称",
    "BILL"."UDA3C" AS "备用字段3编码",
    "BILL"."UDA3N" AS "备用字段3名称",
    "BILL"."UDA4C" AS "备用字段4编码",
    "BILL"."UDA4N" AS "备用字段4名称",
    "BILL"."UDA5C" AS "备用字段5编码",
    "BILL"."UDA5N" AS "备用字段5名称",
    "BILL"."STORE_START" AS "文件点检结果标记",
    "BILL"."STORE_ERROR_CAUSE" AS "esb失败原因",
    "BILL"."REQ_SOURCE" AS "需求单来源",
	    "BILL_ENTRY"."MRL_CODE" AS "物料编码",
	    "BILL_ENTRY"."MRL_NAME" AS "物料名称",
	    "BILL_ENTRY"."DUE_QTY" AS "物料数量",
	    "BILL_ENTRY"."PRCS_BOM_ID" AS "prcs_bom_id"
FROM "UNIMAX_CG"."UMM_REQ2" "BILL"
    LEFT JOIN "UNIMAX_CG"."MBF_ROUTE_OPERATION" "OP" ON "BILL"."OP_GID" = "OP"."GID"
        AND "OP"."IS_DELETE" <> 1 AND "OP"."IS_ACTIVE" = 0
    LEFT JOIN "UNIMAX_CG"."UMM_REQ_BILL2" "BILL_ENTRY" ON "BILL_ENTRY"."REQ_GID" = "BILL"."GID"
        AND "BILL_ENTRY"."IS_DELETE" <> 1 AND "BILL_ENTRY"."IS_ACTIVE" = 0
WHERE
    {_where}
"""


def get_select_cgmes_rework_order_sql(data: filter_data) -> str:
    '''获取城轨MES的返工订单信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND "BILL"."PRJ_CODE" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL\".\"CAR_CODE\", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("BILL"."SINGLE_CAR_CODE") = \'{data.jch_num.upper()}\''
    if data.process is not None:
        _where += f' AND ( "CRAFT_ENTRY"."OP_CODE" = \'{data.process}\' OR "CRAFT_ENTRY"."O_OP_CODE" = \'{data.process}\')'
    if data.material is not None:
        _where += f' AND "MRL_ENTRY"."CODE" = \'{data.material}\''
    return f"""
SELECT
    DISTINCT
    "BILL"."GID" AS "ID",
    "BILL"."IS_DEAL" AS "处理状态",
    "BILL"."DEAL_RESULT" AS "处理结果",
    "BILL"."CODE" AS "生产订单号",
    "BILL"."O_CODE" AS "原生产订单号",
    "BILL"."PRJ_CODE" AS "项目号",
    "BILL"."PRJ_NAME" AS "项目名称",
    "BILL"."PRODU_CODE" AS "产品编号",
    "BILL"."PRODU_NAME" AS "产品名称",
    "BILL"."CAR_CODE" AS "车号",
    "BILL"."SINGLE_CAR_CODE" AS "节车号",
    "BILL"."START_DATE" AS "开始日期",
    "BILL"."DELIVERY_DATE" AS "交付日期",
    "BILL"."UNIT" AS "计量单位",
    "BILL"."ROUTE_CODE" AS "工艺路线编码",
    "BILL"."PO_TYPE" AS "订单类型",
    "BILL"."DEPT_CODE" AS "部门编码",
    "BILL"."DEPT_NAME" AS "部门名称",
    "BILL"."FFLOW" AS "产品流程字",
    "BILL"."TRAKING_NBR" AS "跟踪号",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."PO_ID" AS "订单ID",
    "BILL"."DEAL_NUM" AS "处理次数",
    "MRL_ENTRY"."GID" AS "变更物料单据ID",
    "MRL_ENTRY"."FLAG" AS "物料-变更类型",
    "MRL_ENTRY"."CODE" AS "物料-物料编码",
    "MRL_ENTRY"."NAME" AS "物料-物料名称",
    "MRL_ENTRY"."ORG_CODE" AS "物料-供货库存组织编码",
    "MRL_ENTRY"."ORG_NAME" AS "物料-供货库存组织名称",
    "MRL_ENTRY"."QTY" AS "物料-数量",
    "CRAFT_ENTRY"."GID" AS "变更工序单据ID",
    "CRAFT_ENTRY"."FLAG" AS "工序-变更类型",
    "CRAFT_ENTRY"."OP_SEQ" AS "工序-工序号",
    "CRAFT_ENTRY"."OP_CODE" AS "工序-工序编码",
    "CRAFT_ENTRY"."OP_NAME" AS "工序-工序名称",
    "CRAFT_ENTRY"."WORK_CENTER_CD" AS "工序-工作中心编码",
    "CRAFT_ENTRY"."OUTSOURCE_TYPE" AS "工序-委外类型",
    "CRAFT_ENTRY"."O_OP_SEQ" AS "工序-原工序号",
    "CRAFT_ENTRY"."O_OP_CODE" AS "工序-原工序名称",
    "CRAFT_ENTRY"."O_OP_NAME" AS "工序-原工序编码",
    "CRAFT_ENTRY"."O_WORK_CENTER_CD" AS "工序-原工作重心编码",
    "CRAFT_ENTRY"."PLAN_START_DATE" AS "工序-指定计划开始时间",
    "CRAFT_ENTRY"."PLAN_END_DATE" AS "工序-指定计划结束时间",
    "GROUP"."GROUP_NAME" AS "工序-指定班组",
    "CRAFT_ENTRY"."PRO_LINE" AS "工序-指定产线"
FROM
    "UNIMAX_CG"."UMPP_REWORK_ORDER" "BILL"
    LEFT JOIN "UNIMAX_CG"."UMPP_REWORK_ORDER_MRL" "MRL_ENTRY" ON "MRL_ENTRY"."REWORK_ORDER_GID" = "BILL"."GID"
        AND "MRL_ENTRY"."IS_DELETE" <> 1 AND "MRL_ENTRY"."IS_ACTIVE" = 0
    LEFT JOIN "UNIMAX_CG"."UMPP_REWORK_ORDER_CRAFT" "CRAFT_ENTRY" ON "CRAFT_ENTRY"."REWORK_ORDER_GID" = "BILL"."GID"
        AND "CRAFT_ENTRY"."IS_DELETE" <> 1 AND "CRAFT_ENTRY"."IS_ACTIVE" = 0
    LEFT OUTER JOIN "UNIMAX_CG"."MBF_LABOUR_GROUP" "GROUP" ON "CRAFT_ENTRY"."LABOUR_GROUP_GID" = "GROUP"."GID"
        AND "GROUP"."IS_DELETE" <> 1 AND "GROUP"."IS_ACTIVE" = 0
WHERE
    {_where}
"""


def get_select_cgmes_rework_production_request_sql(data: filter_data) -> str:
    '''获取城轨MES的返工制造单信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND ( "BILL"."PJ_CD" = \'{data.project}\' OR SUBSTR("ORDERS_ENTRY"."TRAIN_NBR", 1, 8) = \'{data.project}\' ) '
    if data.track_number is not None:
        _where += f' AND ( TO_NUMBER(SUBSTR("BILL"."CAR_CODE", -4)) = {data.track_number} OR TO_NUMBER(SUBSTR("ORDERS_ENTRY"."TRAIN_NBR", -4)) = {data.track_number} ) '
    if data.jch_num is not None:
        _where += f' AND ( UPPER("BILL"."SINGLE_CAR_CODE") = \'{data.jch_num.upper()}\' OR UPPER("ORDERS_ENTRY"."CARRIAGE_NBR") = \'{data.jch_num.upper()}\' ) '
    if data.process is not None:
        _where += f' AND ( "OP_ENTRY"."OP_CODE" = \'{data.process}\' OR "ORDERS_ENTRY"."OP_CODE" = \'{data.process}\' OR "OP_ENTRY"."OLD_OP_CODE" = \'{data.process}\' ) '
    if data.material is not None:
        _where += f' AND "MRLS_ENTRY"."MTRL_CD" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."GID" AS "ID",
    "BILL"."IS_DEAL" AS "处理状态",
    "BILL"."DEAL_RESULT" AS "处理结果",
    "BILL"."DUE_DATE" AS "需求时间",
    "BILL"."BILL_CODE" AS "返工单号",
    "BILL"."PJ_CD" AS "项目编码",
    "BILL"."PJ_NAME" AS "项目名称",
    "BILL"."CAR_CODE" AS "车号",
    "BILL"."SINGLE_CAR_CODE" AS "节车号",
    "BILL"."PROCODE_CD" AS "产品物料编码",
    "BILL"."MTRL_NAME" AS "产品物料名称",
    "BILL"."ROUTE_CD" AS "工艺路线编码",
    "BILL"."CHANGE_TYPE" AS "变更类型",
    "BILL"."DETP_CODE" AS "部门编码",
    "BILL"."DETP_NAME" AS "部门名称",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."DEAL_NUM" AS "处理次数",
    "MRLS_ENTRY"."GID" AS "变更物料单据ID",
    "MRLS_ENTRY"."FLAG_CD" AS "物料-变更类型",
    "MRLS_ENTRY"."MTRL_CD" AS "物料-物料编码",
    "MRLS_ENTRY"."MTRL_NAME" AS "物料-物料名称",
    "MRLS_ENTRY"."ORG_CODE" AS "物料-供货库存组织编码",
    "MRLS_ENTRY"."ORG_NAME" AS "物料-供货库存组织名称",
    "MRLS_ENTRY"."QUANTITY" AS "物料-数量",
    "OP_ENTRY"."GID" AS "变更工序单据ID",
    "OP_ENTRY"."FLAG_CD" AS "工序-变更类型",
    "OP_ENTRY"."OP_NUM" AS "工序-工序号",
    "OP_ENTRY"."OP_CODE" AS "工序-工序编码",
    "OP_ENTRY"."OP_NAME" AS "工序-工序名称",
    "OP_ENTRY"."WORK_CENTER" AS "工序-工作中心编码",
    "OP_ENTRY"."OUTSOURCE_TYPE" AS "工序-委外类型",
    "OP_ENTRY"."OLD_OP_NUM" AS "工序-原工序号",
    "OP_ENTRY"."OLD_OP_CODE" AS "工序-原工序编码",
    "OP_ENTRY"."OLD_OP_NAME" AS "工序-原工序名称",
    "OP_ENTRY"."OLD_WORK_CENTER" AS "工序-原工作重心编码",
    "OP_ENTRY"."PLAN_START_DATE" AS "工序-指定计划开始时间",
    "OP_ENTRY"."PLAN_END_DATE" AS "工序-指定计划结束时间",
    "GROUP"."GROUP_NAME" AS "工序-指定班组",
    "OP_ENTRY"."PRO_LINE" AS "工序-指定产线",
    "ORDERS_ENTRY"."GID" AS "变更订单ID",
    "ORDERS_ENTRY"."TRAIN_NBR" AS "订单-车号",
    "ORDERS_ENTRY"."CARRIAGE_NBR" AS "订单-节车号",
    "ORDERS_ENTRY"."PO_NBR" AS "订单-生产订单号",
    "ORDERS_ENTRY"."OP_CODE" AS "订单-工序编码",
    "ORDERS_ENTRY"."OP_NAME" AS "订单-工序名称"
FROM
    "UNIMAX_CG"."UEX_REWORK_BILL" "BILL"
    LEFT JOIN "UNIMAX_CG"."UEX_REWORK_BILL_MRLS" "MRLS_ENTRY" ON 
        "MRLS_ENTRY"."BILL_ID" = "BILL"."GID" 
        AND "MRLS_ENTRY"."IS_DELETE" <> 1 
        AND "MRLS_ENTRY"."IS_ACTIVE" = 0
    LEFT JOIN "UNIMAX_CG"."UEX_REWORK_BILL_OP" "OP_ENTRY" ON 
        "OP_ENTRY"."BILL_ID" = "BILL"."GID" 
        AND "OP_ENTRY"."IS_DELETE" <> 1 
        AND "OP_ENTRY"."IS_ACTIVE" = 0
    LEFT JOIN  "UNIMAX_CG"."UEX_REWORK_BILL_ORDERS" "ORDERS_ENTRY" ON 
        "ORDERS_ENTRY"."BILL_ID" = "BILL"."GID" 
        AND "ORDERS_ENTRY"."IS_DELETE" <> 1 
        AND "ORDERS_ENTRY"."IS_ACTIVE" = 0
    LEFT OUTER JOIN "UNIMAX_CG"."MBF_LABOUR_GROUP" "GROUP" ON 
        "OP_ENTRY"."LABOUR_GROUP_GID" = "GROUP"."GID"
        AND "GROUP"."IS_DELETE" <> 1 
        AND "GROUP"."IS_ACTIVE" = 0
WHERE
    {_where}
    """


def get_select_cg_mes_diagnose_order_bom_sql(data: filter_data) -> str:
    '''获取MES订单BOM (mbb_order_bom) 相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 AND "BILL"."IS_ACTIVE" = 0 '
    if data.project is not None:
        _where += f' AND "BILL"."PRO_CODE" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL"."CAR_CODE", -4)) = {data.track_number} '
    if data.process is not None:
        _where += f' AND "BILL"."OP_CODE" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "BILL"."MRL_CODE" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."ORDER_CODE" AS "订单号",
    "BILL"."PRO_CODE" AS "项目编码",
    "BILL"."PRO_NAME" AS "项目名称",
    "BILL"."OP_LINE_CODE" AS "工艺路线编码",
    "BILL"."OP_LINE_NAME" AS "工艺路线名称",
    "BILL"."OP_CODE" AS "工序编码",
    "BILL"."OP_NAME" AS "工序名称",
    "BILL"."MRL_CODE" AS "物料编码",
    "BILL"."MRL_NAME" AS "物料名称",
    "BILL"."PRO_MRL_CODE" AS "产品物料编码",
    "BILL"."PRO_MRL_NAME" AS "部件产品名称",
    "BILL"."CAR_CODE" AS "车号",
    "BILL"."QANA" AS "数量",
    "BILL"."SUM_UNIT" AS "计量单位",
    "BILL"."BOM_CODE" AS "BOM编码",
    "BILL"."BOM_NAME" AS "BOM名称",
    "BILL"."PRCS_BOM_ID" AS "BOMID",
    "BILL"."COMPOSE_NUM" AS "配盘方案号",
    "BILL"."DIS_TYPE" AS "物料类别",
    CASE WHEN "BILL"."IS_CRITICAL" = 0 THEN '否' WHEN "BILL"."IS_CRITICAL" = 1 THEN '是' ELSE TO_CHAR("BILL"."IS_CRITICAL") END AS "是否关重件",
    CASE WHEN "BILL"."IS_IMPORTANT" = 0 THEN '是' WHEN "BILL"."IS_IMPORTANT" = 1 THEN '否' ELSE TO_CHAR("BILL"."IS_IMPORTANT") END AS "是否重要",
    "BILL"."STATE" AS "状态",
    "BILL"."REMARK" AS "备注",
    "BILL"."GID" AS "GID",
    "BILL"."CREATE_ID" AS "创建人",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."MODIFY_ID" AS "修改人",
    "BILL"."MODIFY_DATE" AS "修改时间",
    CASE WHEN "BILL"."IS_ACTIVE" = 0 THEN '激活' WHEN "BILL"."IS_ACTIVE" = 1 THEN '冻结' ELSE TO_CHAR("BILL"."IS_ACTIVE") END AS "激活标识",
    CASE WHEN "BILL"."IS_DELETE" = 0 THEN '未删除' WHEN "BILL"."IS_DELETE" = 1 THEN '删除' ELSE TO_CHAR("BILL"."IS_DELETE") END AS "删除标识",
    "BILL"."UDA1" AS "备用字段1",
    "BILL"."UDA2" AS "备用字段2",
    "BILL"."UDA3" AS "备用字段3",
    "BILL"."UDA4" AS "备用字段4",
    "BILL"."UDA5" AS "备用字段5"
FROM "UNIMAX_CG"."MBB_ORDER_BOM" "BILL"
WHERE
    {_where}
"""


def get_select_cg_mes_diagnose_pick_sql(data: filter_data) -> str:
    '''获取MES领料单 (umm_materialbill) 相关信息'''
    _where = ' "BILL"."IS_DELETE" <> 1 '
    if data.project is not None:
        _where += f' AND "BILL"."PROJECT_NUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL"."TRACK_NUMBER_NO", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("BILL"."PROJECT_JCHNO") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "BILL"."OPERATION_NO" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "BILL"."MATERIAL_NUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "BILL"."MATERIALBILL_NUMBER" AS "领料单号",
    "BILL"."DISTNUMBER" AS "配送单号",
    "BILL"."MATERIAL_NUMBER" AS "物料编码",
    "BILL"."MATERIALNAME" AS "物料名称",
    "BILL"."MATERIAL_MODEL" AS "物料规格型号",
    "BILL"."PROJECT_NUMBER" AS "项目号",
    "BILL"."TRACK_NUMBER_NO" AS "车号",
    "BILL"."PROJECT_JCHNO" AS "节车号",
    "BILL"."OPERATION_NO" AS "工序编码",
    "BILL"."STATION" AS "台位",
    "BILL"."QTY" AS "数量",
    "BILL"."ISSUE_QTY" AS "发料数量",
    "BILL"."LOT" AS "批次",
    "BILL"."BASE_STATUS" AS "基本状态",
    "BILL"."DIS_STATUS" AS "配送状态",
    "BILL"."BIZ_TYPE_NUMBER" AS "业务类型编码",
    "BILL"."SOURCE_BILL_TYPE_ID" AS "源单类型",
    "BILL"."MADE_SUPPLIER_ID" AS "供应商",
    "BILL"."INV_UPDATE_NUMBER" AS "库存更新单号",
    "BILL"."IS_TRAY" AS "是否托盘",
    "BILL"."TYPE" AS "类型",
    "BILL"."TYPE_NUMBER" AS "类型编码",
    "BILL"."BIZ_DATE" AS "业务日期",
    "BILL"."DEMAND_DATE" AS "需求日期",
    "BILL"."DEPT_CODE" AS "部门编码",
    "BILL"."DEPT_NAME" AS "部门名称",
    "BILL"."GID" AS "GID",
    "BILL"."CREATE_ID" AS "创建人",
    "BILL"."CREATE_DATE" AS "创建时间",
    "BILL"."MODIFY_ID" AS "修改人",
    "BILL"."MODIFY_DATE" AS "修改时间",
    CASE WHEN "BILL"."IS_DELETE" = 0 THEN '未删除' WHEN "BILL"."IS_DELETE" = 1 THEN '删除' ELSE TO_CHAR("BILL"."IS_DELETE") END AS "删除标识",
    "BILL"."UDA1" AS "备用字段1"
FROM "UNIMAX_CG"."UMM_MATERIALBILL" "BILL"
WHERE
    {_where}
"""
