from common import filter_data

def get_select_eas_pbom_sql(data: filter_data) -> str:
    '''获取EAS的工序BOM信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("START_TRACK"."FNUMBER", -4)) <= {data.track_number} AND TO_NUMBER(SUBSTR("END_TRACK"."FNUMBER", -4)) >= {data.track_number}'
    if data.process is not None:
        _where += f' AND "OPERATION"."FNUMBER" = \'{data.process}\''
    if data.material is not None:
        _where += f' AND "MATERIAL"."FNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "PROJECT"."FNUMBER" AS "项目号",
    "START_TRACK"."FNUMBER" AS "开始车号",
    "END_TRACK"."FNUMBER" AS "结束车号",
    "ROOTING"."FNUMBER" AS "工艺路线编码",
    "ROOTING"."FNAME_L2" AS "工艺路线名称",
    "OPERATION"."FNUMBER" AS "工序编码",
    "OPERATION"."FNAME_L2" AS "工序名称",
    "MATERIAL"."FNUMBER" AS "物料编码",
    "MATERIAL"."FNAME_L2" AS "物料名称",
    "BILL"."FNAME_L2" AS "名称",
    "BILL"."FNUMBER" AS "单据编码",
    "BILL"."FCREATETIME" AS "创建时间",
    "BILL"."FLASTUPDATETIME" AS "最后修改时间",
    "BILL"."FBOMID" AS "BOMID",
    "BILL"."CFISTCMDATA" AS "是否同步TCM",
    "BILL"."CFBOMTYPE" AS "BOM类型",
    "BILL"."CFMVERSION" AS "物料版本号",
    "BILL_ENTRY"."FSEQ" AS "单据分录序列号",
    "BILL_ENTRY"."CFALLINKOPERATIONNO" AS "关联工序号",
    "RWP"."FWPSEQ" AS "工艺路线分录工序号",
    "BILL_ENTRY"."CFISTCMDATA" AS "子单是否同步TCM",
    "BILL_ENTRY"."FUNITQTY" AS "单位用量",
    "BILL_ENTRY"."FPARTNUMBER" AS "件号",
    "BILL_ENTRY"."FISMUSTREQ" AS "是否必领料",
    "BILL_ENTRY"."FREMARK" AS "备注",
    "BILL_ENTRY"."FCONSUMERATE" AS "消耗比率",
    "BILL_ENTRY"."FCONSUMEQUOTA" AS "消耗定额",
    "BILL_ENTRY"."FMATERIALATTR" AS "物料属性",
    "BILL_ENTRY"."FISOWNOBJECT" AS "是否自带件",
    "BILL_ENTRY"."FISSUEMODE" AS "生产领料方式",
    "BILL_ENTRY"."FASSEMBLESEQ" AS "装配序号",
    "BILL_ENTRY"."CFCHILDMVERSION" AS "子项版本号",
    "BILL_ENTRY"."CFDASSEMBLESEQ" AS "设计装配序号",
    "BILL_ENTRY"."CFDITEMID" AS "设计图号",
    "BILL_ENTRY"."CFDASSEMBLENUM" AS "设计装配数量",
    "BILL_ENTRY"."FBOMITEMID" AS "fbomitemid"
FROM
    "ZJEAS7"."T_MM_PBOM" "BILL" 
    LEFT JOIN "ZJEAS7"."T_MM_PBOMENTRY" "BILL_ENTRY" ON "BILL_ENTRY"."FPARENTID" = "BILL"."FID"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT" ON "PROJECT"."FID" = "BILL"."FPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "START_TRACK" ON "START_TRACK"."FID" = "BILL_ENTRY"."CFSTRACEID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "END_TRACK" ON "END_TRACK"."FID" = "BILL_ENTRY"."CFETRACEID"
    LEFT JOIN "ZJEAS7"."T_MM_STANDARDROOTING" "ROOTING" ON "ROOTING"."FID" = "BILL"."FROUTINGID"
    LEFT JOIN "ZJEAS7"."T_MM_MATERIALRWP" "RWP" ON "RWP"."FID" = "BILL_ENTRY"."FROUTINGITEMID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "OPERATION" ON "OPERATION"."FID" = "RWP"."FOPERATIONID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "MATERIAL" ON "MATERIAL"."FID" = "BILL_ENTRY"."CFMATERIALID"
WHERE
    {_where}
    """


def get_select_eas_order_sql(data: filter_data) -> str:
    '''获取EAS的订单相关信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("TRACK"."FNUMBER", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("JCH"."FNUMBER") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OPERATION"."FNUMBER" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "MATERIAL"."FNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "PROJECT"."FNUMBER" AS "项目号",
    "PROJECT"."FNAME_L2" AS "项目名称",
    "TRACK"."FNUMBER" AS "车号",
    "JCH"."FNUMBER" AS "节车号",
    "ROOTING"."FNUMBER" AS "工艺路线编码",
    "ROOTING"."FNAME_L2" AS "工艺路线名称",
    "OPERATION"."FNUMBER" AS "工序编码",
    "OPERATION"."FNAME_L2" AS "工序名称",
    "MATERIAL"."FNUMBER" AS "物料编码",
    "MATERIAL"."FNAME_L2" AS "物料名称",
    "BILL"."FCREATETIME" AS "创建时间",
    "BILL"."FLASTUPDATETIME" AS "最后修改时间",
    "BILL"."FNUMBER" AS "单据编码",
    "BILL"."FBIZDATE" AS "业务日期",
    "BILL"."FHASEFFECTED" AS "是否曾经生效",
    "BILL"."FSOURCEBILLID" AS "源单据ID",
    "BILL"."FAUDITTIME" AS "审核时间",
    CASE
        WHEN "BILL"."FBASESTATUS" = -3
        THEN '历史版本'
        WHEN "BILL"."FBASESTATUS" = -2
        THEN '变更中'
        WHEN "BILL"."FBASESTATUS" = -1
        THEN '空'
        WHEN "BILL"."FBASESTATUS" = 0
        THEN '新增'
        WHEN "BILL"."FBASESTATUS" = 1
        THEN '保存'
        WHEN "BILL"."FBASESTATUS" = 2
        THEN '提交'
        WHEN "BILL"."FBASESTATUS" = 3
        THEN '作废'
        WHEN "BILL"."FBASESTATUS" = 4
        THEN '审核'
        WHEN "BILL"."FBASESTATUS" = 5
        THEN '下达'
        WHEN "BILL"."FBASESTATUS" = 6
        THEN '冻结'
        WHEN "BILL"."FBASESTATUS" = 7
        THEN '关闭'
        WHEN "BILL"."FBASESTATUS" = 8
        THEN '完工'
        WHEN "BILL"."FBASESTATUS" = 10
        THEN '发布'
        WHEN "BILL"."FBASESTATUS" = 11
        THEN '结案'
        WHEN "BILL"."FBASESTATUS" = 12
        THEN '已转'
        WHEN "BILL"."FBASESTATUS" = 13
        THEN '修改完毕'
        WHEN "BILL"."FBASESTATUS" = 14
        THEN '评审中'
        WHEN "BILL"."FBASESTATUS" = 15
        THEN '评审完毕'
        WHEN "BILL"."FBASESTATUS" = 16
        THEN '确认'
        WHEN "BILL"."FBASESTATUS" = 17
        THEN '处理中'
        WHEN "BILL"."FBASESTATUS" = 18
        THEN '开工'
        WHEN "BILL"."FBASESTATUS" = 90
        THEN '完成'
        ELSE TO_CHAR("BILL"."FBASESTATUS")
    END AS "基本状态",
    "BILL"."FQTY" AS "计划数量",
    "BILL"."FBASEQTY" AS "基本数量",
    "BILL"."FPLANBEGINDATE" AS "计划开工日期",
    "BILL"."FPLANENDDATE" AS "计划完工日期",
    "BILL"."FACTUREBEGINDATE" AS "实际开工日期",
    "BILL"."FACTUREENDDATE" AS "实际完工日期",
    "BILL"."FDELIVERYQTY" AS "预计产出数量",
    "BILL"."FDELIVERYBASEQTY" AS "预计产出基本数量",
    "BILL"."FBOMID" AS "BOM编码",
    "BILL"."FBOMNUM" AS "BOM编号",
    "BILL"."FEXTRARATIO" AS "入库上限允差",
    "BILL"."FLACKRATIO" AS "入库下限允差",
    "BILL"."FFINISHEDQTY" AS "完工数量",
    "BILL"."FPASSQTY" AS "合格数量",
    "BILL"."FSCRAPQTY" AS "报废数量",
    "BILL"."FFINISHEDBASEQTY" AS "完工基本数量",
    "BILL"."FPASSBASEQTY" AS "合格基本数量",
    "BILL"."FSCRAPBASEQTY" AS "报废基本数量",
    "BILL"."FREPAIRQTY" AS "返工数量",
    "BILL"."FREPAIRBASEQTY" AS "返工基本数量",
    "BILL"."FTOSTROREQTY" AS "入库数量",
    "BILL"."FTOSTOREBASEQTY" AS "入库基本数量",
    "BILL"."FTESTEDQTY" AS "送检数量",
    "BILL"."FTESTEDBASEQTY" AS "送检基本数量",
    "BILL"."FISLIMITEDQTY" AS "控制入库数量",
    "BILL"."FFIRSTOPERNO" AS "首道工序号",
    "BILL"."FLASTOPERNO" AS "末道工序号",
    "BILL"."FSRCBILLNUM" AS "来源单据编号",
    "BILL"."FYIELD" AS "成品率",
    "BILL"."FREMARK_L2" AS "备注",
    "BILL"."FBUDGETKITTINGTIME" AS "预计齐套日期",
    "BILL"."CFMESSTATUS" AS "MES发送状态",
    "BILL"."CFOLDNUMBER" AS "原生产订单号",
    "BILL"."CFCAASTATUS" AS "CAA状态"
FROM
    "ZJEAS7"."T_MM_MANUFACTUREORDER" "BILL"
    LEFT JOIN "ZJEAS7"."T_MM_MFTORDERSTOCK" "BILL_ENTRY" ON "BILL_ENTRY"."FPARENTID" = "BILL"."FID"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT" ON "PROJECT"."FID" = "BILL"."FPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "TRACK" ON "TRACK"."FID" = "BILL"."FTRACKID"
    LEFT JOIN "ZJEAS7"."T_PRO_PROJECTJCH" "JCH" ON "JCH"."FID" = "BILL"."FPROJECTJCHID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "OPERATION" ON "OPERATION"."FID" = "BILL_ENTRY"."FOPERATIONID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "MATERIAL" ON "MATERIAL"."FID" = "BILL_ENTRY"."FMATERIALID"
    LEFT JOIN "ZJEAS7"."T_MM_STANDARDROOTING" "ROOTING" ON "ROOTING"."FID" = "BILL"."FROUTINGID"
WHERE
    {_where}
    """


def get_select_eas_production_material_sql(data: filter_data) -> str:
    '''获取EAS的生产备料时序簿相关信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("TRACK"."FNUMBER", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("JCH"."FNUMBER") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OPERATION"."FNUMBER" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "MATERIAL"."FNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    "BILL"."FID" AS "FID",
    "ORG"."FNUMBER" AS "供货库存组织编码",
    "ORG"."FNAME_L2" AS "供货库存组织",
    "WH"."FNAME_L2" AS "领料仓库",
    "BILL"."FISBACKFLUSH" AS "倒冲",
    "TT"."FNUMBER" AS "生产事务类型编码",
    "TT"."FNAME_L2" AS "生产事务类型",
    "MO"."FNUMBER" AS "生产订单编码",
    "MO"."CFMESSTATUS" AS "生产订单MES发送状态",
    "PROJECT"."FNUMBER" AS "项目号",
    "PROJECT"."FNAME_L2" AS "项目名称",
    "TRACK"."FNUMBER" AS "跟踪号",
    "JCH"."FNUMBER" AS "节车号",
    CASE "MO"."FBASESTATUS"
        WHEN -3 THEN '历史版本'
        WHEN -2 THEN '变更中'
        WHEN -1 THEN '空'
        WHEN 0 THEN '新增'
        WHEN 1 THEN '保存'
        WHEN 2 THEN '提交'
        WHEN 3 THEN '作废'
        WHEN 4 THEN '审核'
        WHEN 5 THEN '下达'
        WHEN 6 THEN '冻结'
        WHEN 7 THEN '关闭'
        WHEN 8 THEN '完工'
        WHEN 10 THEN '发布'
        WHEN 11 THEN '结案'
        WHEN 12 THEN '已转'
        WHEN 13 THEN '修改完毕'
        WHEN 14 THEN '评审中'
        WHEN 15 THEN '评审完毕'
        WHEN 16 THEN '确认'
        WHEN 17 THEN '处理中'
        WHEN 18 THEN '开工'
        WHEN 90 THEN '完成'
        ELSE '未知状态(' || "MO"."FBASESTATUS" || ')'
    END AS "生产订单状态",
    "OPERATION"."FNUMBER" AS "工序编码",
    "OPERATION"."FNAME_L2" AS "工序名称",
    "MATERIAL"."FNUMBER" AS "物料编码",
    "MATERIAL"."FNAME_L2" AS "物料名称",
    "UNIT"."FNAME_L2" AS "计量单位",
    "BILL"."FQTY" AS "标准用量",
    "BILL"."FBASEQTY" AS "标准基本用量",
    "BILL"."FLOSSQTY" AS "损耗数量",
    "BILL"."FLOSSBASEQTY" AS "损耗基本数量",
    "BILL"."FACTISSUEQTY" AS "实际发料数量",
    "BILL"."FACTISSUEBASEQTY" AS "发料基本数量",
    "BILL"."FACTLOSSQTY" AS "实际损耗数量",
    "BILL"."FACTLOSSBASEQTY" AS "实际损耗基本数量",
    "BILL"."FREJECTEDQTY" AS "退料数量",
    "BILL"."FREJECTEDBASEQTY" AS "退料基本数量",
    "BILL"."FFEEDINGQTY" AS "工废补料数量",
    "BILL"."FFEEDINGBASEQTY" AS "工废补料基本数量",
    "BILL"."FSCRAPQTY" AS "工废数量",
    "BILL"."FSCRAPBASEQTY" AS "工废基本数量",
    "BILL"."FPLANNEDQTY" AS "需求数量",
    "BILL"."FPLANNEDBASEQTY" AS "计划基本用量",
    "BILL"."FUNITQTY" AS "单位用量",
    "BILL"."FUNITBASEQTY" AS "单位基本用量",
    "BILL"."FMATERIALSCRAPQTY" AS "料废数量",
    "BILL"."FMATERIALSCRAPBASEQTY" AS "料废基本数量",
    "BILL"."FMATERIALFEEDINGQTY" AS "料废补料数量",
    "BILL"."FMATERIALFEEDINGBASEQTY" AS "料废补料基本数量",
    "BILL"."FUNISSUEQTY" AS "未发料数量",
    "BILL"."FUNISSUEBASEQTY" AS "未发料基本数量",
    "BILL"."FTOSTOREQTY" AS "入库数量",
    "BILL"."FTOSTOREBASEQTY" AS "入库基本数量",
    "BILL"."CFACTMOVEQTY" AS "实调拨数量",
    "BILL"."CFALRMOVEQTY" AS "已调拨数量",
    "BILL"."FPICKTYPE" AS "领料类型",
    "BILL"."FDEMANDTIME" AS "需求日期",
    "BILL"."FACTUEISSUETIME" AS "实际发料时间",
    "BILL"."FBOMENTRYID" AS "BOMENTRYID"
FROM
    "ZJEAS7"."T_MM_MFTORDERSTOCK" "BILL"
    LEFT JOIN "ZJEAS7"."T_MM_MANUFACTUREORDER" "MO" ON "MO"."FID" = "BILL"."FPARENTID"
    LEFT JOIN "ZJEAS7"."T_PRO_PROJECTJCH" "JCH" ON "JCH"."FID" = "MO"."FPROJECTJCHID"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT" ON "PROJECT"."FID" = "MO"."FPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "TRACK" ON "TRACK"."FID" = "MO"."FTRACKID"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "ORG" ON "ORG"."FID" = "BILL"."FSTORAGEORGUNITID"
    LEFT JOIN "ZJEAS7"."T_MM_PRODUCTTRANSACTIONTYPE" "TT" ON "TT"."FID" = "MO"."FTRANSACTIONTYPEID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "OPERATION" ON "OPERATION"."FID" = "BILL"."FOPERATIONID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "MATERIAL" ON "MATERIAL"."FID" = "BILL"."FMATERIALID"
    LEFT JOIN "ZJEAS7"."T_DB_WAREHOUSE" "WH" ON "WH"."FID" = "BILL"."FWAREHOUSEID"
    LEFT JOIN "ZJEAS7"."T_BD_MEASUREUNIT" "UNIT" ON "UNIT"."FID" = "BILL"."FUNITID"
WHERE
    {_where}
    """


def get_select_eas_material_request_sql(data: filter_data) -> str:
    '''获取EAS的领料单相关信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("TRACK"."FNUMBER", -4)) = {data.track_number}'
    if data.jch_num is not None:
        _where += f' AND UPPER("JCH"."FNUMBER") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OPERATION"."FNUMBER" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "MATERIAL"."FNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "PROJECT"."FNUMBER" AS "项目号",
    "PROJECT"."FNAME_L2" AS "项目名称",
    "TRACK"."FNUMBER" AS "车号",
    "JCH"."FNUMBER" AS "节车号",
    "OPERATION"."FNUMBER" AS "工序编码",
    "OPERATION"."FNAME_L2" AS "工序名称",
    "MATERIAL"."FNUMBER" AS "物料编码",
    "MATERIAL"."FNAME_L2" AS "物料名称",
    "BILL"."FNUMBER" AS "单据编号",
    "BILL"."CFDISTNUMBER" AS "所属配送清单号",
    "BILL"."FSOURCBILLNUMBER" AS "来源单据编码",
    CASE "BILL"."FBASESTATUS"
        WHEN 1 THEN '保存'
        WHEN 2 THEN '提交'
        WHEN 4 THEN '审核'
        WHEN 10 THEN '业务关闭'
        ELSE TO_CHAR ("BILL"."FBASESTATUS")
    END AS "单据状态",
    "BILL"."FBIZDATE" AS "业务日期",
    "BILL"."CFWMSPTBILLCODE" AS "WMS作业单号",
    "BILL"."FCREATETIME" AS "制单时间",
    "BILL"."FLASTUPDATETIME" AS "最后修改时间",
    "BILL"."FAUDITTIME" AS "审核时间",
    "BILL"."FDESCRIPTION" AS "备注"
FROM
    "ZJEAS7"."T_IM_MATERIALREQBILL" "BILL"
    LEFT JOIN "ZJEAS7"."T_IM_MATERIALREQBILLENTRY" "BILL_ENTRY" ON "BILL_ENTRY"."FPARENTID" = "BILL"."FID"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT" ON "PROJECT"."FID" = "BILL_ENTRY"."FPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "TRACK" ON "TRACK"."FID" = "BILL_ENTRY"."FTRACKNUMBERID"
    LEFT JOIN "ZJEAS7"."T_PRO_PROJECTJCH" "JCH" ON "JCH"."FID" = "BILL_ENTRY"."CFPROJECTJCHID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "OPERATION" ON "OPERATION"."FID" = "BILL_ENTRY"."FOPERATIONID" 
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "MATERIAL" ON "MATERIAL"."FID" = "BILL_ENTRY"."FMATERIALID"
WHERE
    {_where}
    """


def get_select_eas_rework_order_sql(data: filter_data) -> str:
    '''获取EAS的返工订单/返工制造单信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "T_6"."FNUMBER" = \'{data.project}\' ' 
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("BILL_ENTRY"."CFTRACKNUMBER", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("BILL_ENTRY"."CFPROJECTJCH") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "ET_2"."FNUMBER" = \'{data.process}\''
    if data.material is not None:
        _where += f' AND "ET_3"."FNUMBER" = \'{data.material}\''
    return f"""SELECT
    DISTINCT
    "BILL"."FID" AS "FID",
    "T_1"."FNAME_L2" AS "创建者",
    "BILL"."FCREATETIME" AS "创建时间",
    "T_2"."FNAME_L2" AS "最后修改者",
    "BILL"."FLASTUPDATETIME" AS "最后修改时间",
    "BILL"."FNUMBER" AS "单据编号",
    "BILL"."FBIZDATE" AS "业务日期",
    "T_5"."FNAME_L2" AS "审核人",
    "BILL"."FSOURCEBILLID" AS "原始单据ID",
    "BILL"."FSOURCEFUNCTION" AS "来源功能",
    "BILL"."FFIVOUCHERED" AS "是否生成凭证",
    "T_6"."FNUMBER" AS "项目号",
    "T_7"."FNAME_L2" AS "工序路线",
    "BILL"."CFCONTENT" AS "变更内容",
    "T_8"."FNAME_L2" AS "库存组织",
    "BILL"."CFBILLSTATUS" AS "状态",
    "BILL"."CFSENDSTATE" AS "发送状态",
    "T_10"."FNAME_L2" AS "发送人",
    "BILL"."CFSENDDATE" AS "发送日期",
    "BILL_ENTRY"."FID" AS "单据分录FID",
    "BILL_ENTRY"."FSEQ" AS "单据分录序列号",
    "BILL_ENTRY"."FPARENTID" AS "返工制造单ID",
    "BILL_ENTRY"."CFSEQ" AS "自定义分录序号",
    "ET_1"."FNUMBER"  AS "生产订单编码",
    "ET_2"."FNUMBER" AS "工序编码",
    "BILL_ENTRY"."CFOPERATIONNAME" AS "工序名称",
    "ET_3"."FNUMBER" AS "物料编码",
    "BILL_ENTRY"."CFMATERIALNAME" AS "物料名称",
    "BILL_ENTRY"."CFQTY" AS "定额",
    "BILL_ENTRY"."CFENTRUSTTYPE" AS "委外类型",
    "ET_4"."FNAME_L2" AS "工作中心",
    "BILL_ENTRY"."CFISCHECKPOINT" AS "检验点",
    "BILL_ENTRY"."CFISREPORTPOINT" AS "汇报点",
    "BILL_ENTRY"."CFISPICKINGPOINT" AS "入库点",
    "ET_5"."FNAME_L2" AS "委外厂商",
    "ET_6"."FNAME_L2" AS "开工台位",
    "BILL_ENTRY"."CFOPERTIONALIAS" AS "工序别号",
    "BILL_ENTRY"."CFPROINSTRUCTION" AS "加工说明",
    "BILL_ENTRY"."CFISSUEMODE" AS "领送料方式",
    "ET_7"."FNAME_L2" AS "供货库存组织",
    "BILL_ENTRY"."CFUNITQTY" AS "单位用量",
    "BILL_ENTRY"."CFPROVIDETYPE" AS "供应类型",
    "BILL_ENTRY"."CFISMUSTREQ" AS "是否必领料",
    "BILL_ENTRY"."CFPLANNEDQTY" AS "计划用量",
    "BILL_ENTRY"."CFFLOW" AS "流程",
    "BILL_ENTRY"."CFOPERATIONNO" AS "工序号",
    "BILL_ENTRY"."CFTLSL" AS "退料数量",
    "BILL_ENTRY"."CFKEY" AS "KEY",
    "BILL_ENTRY"."CFTRACKNUMBER" AS "跟踪号",
    "BILL_ENTRY"."CFPROJECTJCH" AS "节车号",
    "ET_8"."FNAME_L2" AS "仓库",
    "BILL_ENTRY"."CFISADDSTOCK" AS "新增备料",
    "BILL_ENTRY"."CFISADDSTOCKQTY" AS "增加备料数量",
    "BILL_ENTRY"."CFISSUBSTOCKQTY" AS "减少备料数量",
    "BILL_ENTRY"."CFISDELETESTOCK" AS "删除备料",
    "BILL_ENTRY"."CFSTOCKQTY" AS "变更数量",
    "BILL_ENTRY"."CFISDELETEREQ" AS "删除领料单",
    "BILL_ENTRY"."CFISADDREQQTY" AS "增加领料单数量",
    "BILL_ENTRY"."CFISSUBREQQTY" AS "减少领料单数量",
    "BILL_ENTRY"."CFISADDREQ" AS "新增领料单"
FROM
    "ZJEAS7"."CT_REW_REWORKMANUFACTUREBILL" "BILL"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "T_1" ON "T_1"."FID" = "BILL"."FCREATORID"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "T_2" ON "T_2"."FID" = "BILL"."FLASTUPDATEUSERID"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "T_5" ON "T_5"."FID" = "BILL"."FAUDITORID"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "T_6" ON "T_6"."FID" = "BILL"."CFPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_STANDARDROOTING" "T_7" ON "T_7"."FID" = "BILL"."CFSTANDARDROOTINGI"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "T_8" ON "T_8"."FID" = "BILL"."CFSTORAGEORGUNITID"
    LEFT JOIN "ZJEAS7"."T_BD_PERSON" "T_10" ON "T_10"."FID" = "BILL"."CFSENDPERSONID"
    LEFT JOIN "ZJEAS7"."CT_REW_REWORKMBEE" "BILL_ENTRY" ON  "BILL_ENTRY"."FPARENTID" = "BILL"."FID"
    LEFT JOIN "ZJEAS7"."T_MM_MANUFACTUREORDER" "ET_1" ON "ET_1"."FID" = "BILL_ENTRY"."CFMANUFACTUREORDER"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "ET_2" ON "ET_2"."FID" = "BILL_ENTRY"."CFOPERATIONID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "ET_3" ON "ET_3"."FID" = "BILL_ENTRY"."CFMATERIALID"
    LEFT JOIN "ZJEAS7"."T_MM_WORKCENTER" "ET_4" ON "ET_4"."FID" = "BILL_ENTRY"."CFWORKCENTERID"
    LEFT JOIN "ZJEAS7"."T_BD_SUPPLIER" "ET_5" ON "ET_5"."FID" = "BILL_ENTRY"."CFENTRUSTSUPPLIERI"
    LEFT JOIN "ZJEAS7"."CT_BAS_STARTPOSITION" "ET_6" ON "ET_6"."FID" = "BILL_ENTRY"."CFTAIWEIF7ID"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "ET_7" ON "ET_7"."FID" = "BILL_ENTRY"."CFSTORAGEORGUNITID"
    LEFT JOIN "ZJEAS7"."T_DB_WAREHOUSE" "ET_8" ON "ET_8"."FID" = "BILL_ENTRY"."CFWAREHOUSEID"
WHERE
    {_where}
    """

def get_select_eas_order_exec_record_sql(data: filter_data) -> str:
    '''获取生产订单变更执行记录'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += (
            f' AND (TO_NUMBER(SUBSTR("ENTRYTRACK"."FNUMBER", -4)) = {data.track_number}'
            f' OR (TO_NUMBER(SUBSTR("START_TRACK"."FNUMBER", -4)) <= {data.track_number}'
            f' AND TO_NUMBER(SUBSTR("END_TRACK"."FNUMBER", -4)) >= {data.track_number})) '
        )
    if data.jch_num is not None:
        _where += f' AND UPPER("PROJECTJCH"."FNUMBER") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OPERATION"."FNUMBER" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "STOCKMATERIAL"."FNUMBER" = \'{data.material}\' '
    return f'''
SELECT
    "PROJECT"."FNUMBER" AS "项目号",
    "PROJECT"."FNAME_L2" AS "项目名称",
    "START_TRACK"."FNUMBER" AS "开始车号",
    "START_TRACK"."FNAME_L2" AS "开始车号名称",
    "END_TRACK"."FNUMBER" AS "结束车号",
    "END_TRACK"."FNAME_L2" AS "结束车号名称",
    "STORAGEORG"."FNUMBER" AS "库存组织编码",
    "STORAGEORG"."FNAME_L2" AS "库存组织名称",
    "PRODUCT"."FNUMBER" AS "产品编码",
    "PRODUCT"."FNAME_L2" AS "产品名称",
    "BILL"."FNUMBER" AS "单据编号",
    "BILL"."FBIZDATE" AS "业务日期",
    "BILL"."CFMANUORDERNUMBER" AS "表头生产订单号",
    "BILL"."CFISEXPANDCHILD" AS "是否展开下层",
    "BILL"."CFISADDOPERATION" AS "是否增加工序",
    "BILL"."CFISEDITOPERATION" AS "是否修改工序",
    "BILL"."CFISREMOVEOPERATION" AS "是否删除工序",
    "BILL"."CFISADDMSTOCK" AS "是否增加备料",
    "BILL"."CFISSUBMSTOCK" AS "是否减少备料",
    "BILL"."CFMAXROWS" AS "最大分析行数",
    "BILL"."CFISHANDSTOP" AS "是否手工终止",
    "BILL"."CFISAUTOEXC" AS "是否自动执行",
    "BILL"."CFYLTOMES" AS "业联订单直接发送MES",
    "BILL"."CFISORDERCLOSE" AS "生产订单考虑关闭状态",
    "ENTRY"."FSEQ" AS "分录序号",
    "MANUORDER"."FNUMBER" AS "分录生产订单号",
    "ENTRY"."CFORDERQTY" AS "订单数量",
    "ENTRYTRACK"."FNUMBER" AS "跟踪号",
    "ENTRYTRACK"."FNAME_L2" AS "跟踪号名称",
    "PROJECTJCH"."FNUMBER" AS "节车号",
    "ENTRY"."CFBASESTATUS" AS "订单状态",
    "ENTRY"."CFENTRYBASESTATUS" AS "工序行状态",
    "OPERATION"."FNUMBER" AS "工序编码",
    "OPERATION"."FNAME_L2" AS "工序名称",
    "ENTRY"."CFOPERATIONNO" AS "工序号_新",
    "ENTRY"."CFOLDOPERATIONNO" AS "工序号_旧",
    "WORKCENTER_NEW"."FNUMBER" AS "工作中心编码_新",
    "WORKCENTER_NEW"."FNAME_L2" AS "工作中心名称_新",
    "WORKCENTER_OLD"."FNUMBER" AS "工作中心编码_旧",
    "WORKCENTER_OLD"."FNAME_L2" AS "工作中心名称_旧",
    "COOSTORAGE_NEW"."FNUMBER" AS "加工组织编码_新",
    "COOSTORAGE_NEW"."FNAME_L2" AS "加工组织名称_新",
    "COOSTORAGE_OLD"."FNUMBER" AS "加工组织编码_旧",
    "COOSTORAGE_OLD"."FNAME_L2" AS "加工组织名称_旧",
    "ENTRY"."CFISPICKINGPOINT" AS "入库点_新",
    "ENTRY"."CFISOLDPICKINGPOINT" AS "入库点_旧",
    "ENTRY"."CFISCHECKPOINT" AS "检验点_新",
    "ENTRY"."CFISOLDCHECKPOINT" AS "检验点_旧",
    "LOCATION_NEW"."FNUMBER" AS "工位编码_新",
    "LOCATION_NEW"."FNAME_L2" AS "工位名称_新",
    "LOCATION_OLD"."FNUMBER" AS "工位编码_旧",
    "LOCATION_OLD"."FNAME_L2" AS "工位名称_旧",
    "STOCKMATERIAL"."FNUMBER" AS "备料物料编码",
    "STOCKMATERIAL"."FNAME_L2" AS "备料物料名称",
    "SUPPORGUNIT"."FNUMBER" AS "供货库存组织编码",
    "SUPPORGUNIT"."FNAME_L2" AS "供货库存组织名称",
    "MEASUREUNIT"."FNUMBER" AS "计量单位编码",
    "MEASUREUNIT"."FNAME_L2" AS "计量单位名称",
    "ENTRY"."CFNEWQTY" AS "数量_新",
    "ENTRY"."CFOLDQTY" AS "数量_旧",
    "ENTRY"."CFISSUEMODE" AS "领料方式",
    "ENTRY"."CFPROVIDETYPE" AS "供应类型",
    "ENTRY"."CFPICKTYPE" AS "领料类型",
    "ENTRY"."CFISSUEQTY" AS "已领数量",
    "ENTRY"."CFNEWDEMANDDATE" AS "需求时间_新",
    "ENTRY"."CFOLDDEMANDDATE" AS "需求时间_旧",
    "ENTRY"."CFCHANGETYPE" AS "变更类型",
    "ENTRY"."CFISSELECT" AS "是否选中",
    "ENTRY"."CFBEGINTIME" AS "执行开始时间",
    "ENTRY"."CFENDTIME" AS "执行结束时间",
    "ENTRY"."CFEXECTIME" AS "执行时长_秒",
    "ENTRY"."CFEXECRESULT" AS "执行结果",
    "ENTRY"."CFPBOMENTRYID" AS "工序BOM分录ID",
    "ENTRY"."CFROUTINGITEMID" AS "工艺路线分录ID",
    "RWP"."FWPSEQ" AS "标准工艺路线工序号",
    "RWP_OPERATION"."FNUMBER" AS "标准工艺路线工序编码",
    "RWP_OPERATION"."FNAME_L2" AS "标准工艺路线工序名称",
    "ENTRY"."CFORDERSEQ" AS "排序号",
    "BILL"."FID" AS "主键ID",
    "BILL"."FFIVOUCHERED" AS "是否生成凭证",
    "BILL"."FHASEFFECTED" AS "是否已生效",
    "BILL"."FDESCRIPTION" AS "描述",
    "CREATOR"."FNUMBER" AS "创建人编码",
    "CREATOR"."FNAME_L2" AS "创建人名称",
    "BILL"."FCREATETIME" AS "创建时间",
    "LASTUPDATER"."FNUMBER" AS "最后修改人编码",
    "LASTUPDATER"."FNAME_L2" AS "最后修改人名称",
    "BILL"."FLASTUPDATETIME" AS "最后修改时间",
    "HANDLER"."FNUMBER" AS "经办人编码",
    "HANDLER"."FNAME_L2" AS "经办人名称",
    "AUDITOR"."FNUMBER" AS "审核人编码",
    "AUDITOR"."FNAME_L2" AS "审核人名称",
    "BILL"."FSOURCEBILLID" AS "来源单据ID",
    "BILL"."FSOURCEFUNCTION" AS "来源功能",
    "ENTRY"."FID" AS "分录主键ID",
    "ENTRY"."FPARENTID" AS "父记录ID",
    "ENTRY"."CFMANUORDERID" AS "生产订单表头ID",
    "ENTRY"."CFMANUTECHID" AS "生产工艺ID",
    "ENTRY"."CFMANUSTOCKID" AS "生产备料ID",
    "BILL"."FCREATORID" AS "创建人ID",
    "BILL"."FLASTUPDATEUSERID" AS "最后修改人ID",
    "BILL"."FCONTROLUNITID" AS "控制单元ID",
    "BILL"."FHANDLERID" AS "经办人ID",
    "BILL"."FAUDITORID" AS "审核人ID",
    "BILL"."CFSTORAGEORGUNITID" AS "库存组织ID",
    "BILL"."CFPROJECTID" AS "项目号ID",
    "BILL"."CFBEGINTRACKID" AS "开始跟踪号ID",
    "BILL"."CFENDTRACKID" AS "结束跟踪号ID",
    "BILL"."CFMATERIALID" AS "产品编码ID",
    "ENTRY"."CFOPERATIONID" AS "工序ID",
    "ENTRY"."CFWORKCENTERID" AS "工作中心ID_新",
    "ENTRY"."CFOLDWORKCENTERID" AS "工作中心ID_旧",
    "ENTRY"."CFOLDCOOSTORAGEORG" AS "加工组织ID_旧",
    "ENTRY"."CFCOOSTORAGEORGUNI" AS "加工组织ID_新",
    "ENTRY"."CFLOCATIONDEFINEDI" AS "工位ID_新",
    "ENTRY"."CFOLDLOCATIONDEFIN" AS "工位ID_旧",
    "ENTRY"."CFMATERIALID" AS "备料物料ID",
    "ENTRY"."CFSUPPORGUNITID" AS "供货库存组织ID",
    "ENTRY"."CFUNITID" AS "计量单位ID",
    "ENTRY"."CFTRACKNUMBERID" AS "跟踪号ID",
    "ENTRY"."CFPROJECTJCHID" AS "节车号ID"
FROM
    "ZJEAS7"."CT_MO_MANUORDEREXECRECORD" "BILL"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT"
        ON "PROJECT"."FID" = "BILL"."CFPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "START_TRACK"
        ON "START_TRACK"."FID" = "BILL"."CFBEGINTRACKID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "END_TRACK"
        ON "END_TRACK"."FID" = "BILL"."CFENDTRACKID"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "STORAGEORG"
        ON "STORAGEORG"."FID" = "BILL"."CFSTORAGEORGUNITID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "PRODUCT"
        ON "PRODUCT"."FID" = "BILL"."CFMATERIALID"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "CREATOR"
        ON "CREATOR"."FID" = "BILL"."FCREATORID"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "LASTUPDATER"
        ON "LASTUPDATER"."FID" = "BILL"."FLASTUPDATEUSERID"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "HANDLER"
        ON "HANDLER"."FID" = "BILL"."FHANDLERID"
    LEFT JOIN "ZJEAS7"."T_PM_USER" "AUDITOR"
        ON "AUDITOR"."FID" = "BILL"."FAUDITORID"
    LEFT JOIN "ZJEAS7"."CT_MO_MANUORDEREXECRECORDENTRY" "ENTRY"
        ON "ENTRY"."FPARENTID" = "BILL"."FID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "OPERATION"
        ON "OPERATION"."FID" = "ENTRY"."CFOPERATIONID"
    LEFT JOIN "ZJEAS7"."T_MM_WORKCENTER" "WORKCENTER_NEW"
        ON "WORKCENTER_NEW"."FID" = "ENTRY"."CFWORKCENTERID"
    LEFT JOIN "ZJEAS7"."T_MM_WORKCENTER" "WORKCENTER_OLD"
        ON "WORKCENTER_OLD"."FID" = "ENTRY"."CFOLDWORKCENTERID"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "COOSTORAGE_NEW"
        ON "COOSTORAGE_NEW"."FID" = "ENTRY"."CFCOOSTORAGEORGUNI"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "COOSTORAGE_OLD"
        ON "COOSTORAGE_OLD"."FID" = "ENTRY"."CFOLDCOOSTORAGEORG"
    LEFT JOIN "ZJEAS7"."CT_EMM_LOCATIONDEFINED" "LOCATION_NEW"
        ON "LOCATION_NEW"."FID" = "ENTRY"."CFLOCATIONDEFINEDI"
    LEFT JOIN "ZJEAS7"."CT_EMM_LOCATIONDEFINED" "LOCATION_OLD"
        ON "LOCATION_OLD"."FID" = "ENTRY"."CFOLDLOCATIONDEFIN"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "STOCKMATERIAL"
        ON "STOCKMATERIAL"."FID" = "ENTRY"."CFMATERIALID"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "SUPPORGUNIT"
        ON "SUPPORGUNIT"."FID" = "ENTRY"."CFSUPPORGUNITID"
    LEFT JOIN "ZJEAS7"."T_BD_MEASUREUNIT" "MEASUREUNIT"
        ON "MEASUREUNIT"."FID" = "ENTRY"."CFUNITID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "ENTRYTRACK"
        ON "ENTRYTRACK"."FID" = "ENTRY"."CFTRACKNUMBERID"
    LEFT JOIN "ZJEAS7"."T_PRO_PROJECTJCH" "PROJECTJCH"
        ON "PROJECTJCH"."FID" = "ENTRY"."CFPROJECTJCHID"
    LEFT JOIN "ZJEAS7"."T_MM_MANUFACTUREORDER" "MANUORDER"
        ON "MANUORDER"."FID" = "ENTRY"."CFMANUORDERID"
    LEFT JOIN "ZJEAS7"."T_MM_MATERIALRWP" "RWP"
        ON "RWP"."FID" = "ENTRY"."CFROUTINGITEMID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "RWP_OPERATION"
        ON "RWP_OPERATION"."FID" = "RWP"."FOPERATIONID"
WHERE
    {_where}
    '''
    

def get_select_eas_material_kitting_sql(data: filter_data) -> str:
    '''获取物料齐套性分析信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "KAH"."FPROJECT" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("KAH"."FTRACKNUMBER", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("KAH"."FJCHNO") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "KAH"."FOPRATION" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "KAH"."FMATERIALNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "KAH"."FORDERID" AS "订单ID",
    "KAH"."FORDERNUMBER" AS "订单编号",
    "KAH"."FPROJECTID" AS "项目ID",
    "KAH"."FPROJECT" AS "项目号",
    "KAH"."FTRACKNUMBERID" AS "车号ID",
    "KAH"."FTRACKNUMBER" AS "车号",
    "KAH"."FPRODUCTID" AS "产品ID",
    "KAH"."FPRODUCTNUMBER" AS "产品编码",
    "KAH"."FPRODUCTNAME" AS "产品名称",
    "KAH"."FMATERIALID" AS "物料ID",
    "KAH"."FMATERIALNUMBER" AS "物料编码",
    "KAH"."FMATERIALNAME" AS "物料名称",
    "KAH"."FMATERIALMODEL" AS "物料规格型号",
    "KAH"."FMATERIALUNIT" AS "物料单位",
    "KAH"."FPLANQTY" AS "计划数量",
    "KAH"."FPLANSTARTTIME" AS "计划开始时间",
    "KAH"."FPLANENDTIME" AS "计划结束时间",
    "KAH"."FREQQTY" AS "需求数量",
    "KAH"."FREQDATE" AS "需求日期",
    "KAH"."FJCHNO" AS "节车号",
    "KAH"."FWORKCENTER" AS "工作中心",
    "KAH"."FLOCATIONDE" AS "工位",
    "KAH"."FOPRATION" AS "工序编码",
    "KAH"."FOPTRATIONNAME" AS "工序名称",
    "KAH"."FINVENTORY" AS "库存数量",
    "KAH"."FWRITEOFFINV" AS "已核销库存",
    "KAH"."FUSEDINVENTORY" AS "已使用库存",
    "KAH"."FPURDELIVERYQTY" AS "采购在途数量",
    "KAH"."FDIRECTDELIVERYQTY" AS "直送在途数量",
    "KAH"."FMANUFACTUREQTY" AS "生产在制数量",
    "KAH"."FEXPECTKITTINGTIME" AS "预计齐套时间",
    "KAH"."FDELAYDAYS" AS "延迟天数",
    "KAH"."FSHORTQTY" AS "短缺数量",
    "KAH"."FSOURCE" AS "数据来源"
FROM
    "ZJEAS7"."CT_MKA_MATERIALKAH" "KAH"
WHERE
    {_where}
    """


def get_select_eas_project_plan_sql(data: filter_data) -> str:
    '''获取项目计划信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("TRACK"."FNUMBER", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("JCH"."FNUMBER") = \'{data.jch_num.upper()}\' '
    if data.material is not None:
        _where += f' AND "MATERIAL"."FNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "PLAN"."FNUMBER" AS "计划编号",
    "PLAN"."FBIZDATE" AS "业务日期",
    "PLAN"."FDESCRIPTION" AS "描述",
    "PLAN"."FWBSNUMBER" AS "WBS编号",
    "PROJECT"."FNUMBER" AS "项目号",
    "PROJECT"."FNAME_L2" AS "项目名称",
    "PLAN"."FPROJECTPLANMODELID" AS "计划模型ID",
    "PLAN"."FSTARTTIME" AS "计划开始时间",
    "PLAN"."FFINISHTIME" AS "计划完成时间",
    "PLAN"."FQTY" AS "数量",
    "PLAN"."FLEVEL" AS "层级",
    "PLAN"."FMATERIALID" AS "物料ID",
    "MATERIAL"."FNUMBER" AS "物料编码",
    "MATERIAL"."FNAME_L2" AS "物料名称",
    "PLAN"."FTRACKNUMBERID" AS "车号ID",
    "TRACK"."FNUMBER" AS "车号",
    "PLAN"."FPROJECTJCHID" AS "节车号ID",
    "JCH"."FNUMBER" AS "节车号",
    "PLAN"."FSTATE" AS "状态",
    "PLAN"."FADMINORGUNITID" AS "行政组织ID",
    "PLAN"."FAUDITTIME" AS "审核时间",
    "PLAN"."FCREATETIME" AS "创建时间",
    "PLAN"."FLASTUPDATETIME" AS "最后修改时间"
FROM
    "ZJEAS7"."T_PCP_PROJECTCP" "PLAN"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT" ON "PROJECT"."FID" = "PLAN"."FPROJECTID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "MATERIAL" ON "MATERIAL"."FID" = "PLAN"."FMATERIALID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "TRACK" ON "TRACK"."FID" = "PLAN"."FTRACKNUMBERID"
    LEFT JOIN "ZJEAS7"."T_PRO_PROJECTJCH" "JCH" ON "JCH"."FID" = "PLAN"."FPROJECTJCHID"
WHERE
    {_where}
    """


def get_select_eas_rooting_sql(data: filter_data) -> str:
    '''获取EAS工艺路线信息'''
    _where = ' 1=1 '
    if data.project is not None:
        _where += f' AND "PROJECT"."FNUMBER" = \'{data.project}\' '
    if data.track_number is not None:
        _where += f' AND TO_NUMBER(SUBSTR("TRACK"."FNUMBER", -4)) = {data.track_number} '
    if data.jch_num is not None:
        _where += f' AND UPPER("JCH"."FNUMBER") = \'{data.jch_num.upper()}\' '
    if data.process is not None:
        _where += f' AND "OP"."FNUMBER" = \'{data.process}\' '
    if data.material is not None:
        _where += f' AND "MATERIAL"."FNUMBER" = \'{data.material}\' '
    return f"""
SELECT
    DISTINCT
    "ROOTING"."FID" AS "工艺路线ID",
    "ROOTING"."FNUMBER" AS "工艺路线编码",
    "ROOTING"."FNAME_L2" AS "工艺路线名称",
    "ROOTING"."FROOTINGTYPE" AS "工艺路线类型",
    "ROOTING"."FSTATUS" AS "工艺路线状态",
    "ROOTING"."FISMAINROOTING" AS "主工艺路线",
    "ROOTING"."FISCHILDROOTING" AS "子工艺路线",
    "ROOTING"."FISREFERENCE" AS "参考",
    "ROOTING"."FHASEFFECTED" AS "是否曾经生效",
    "ROOTING"."FBIZDATE" AS "业务日期",
    "ROOTING"."FFIXEDLEADTIME" AS "固定提前期",
    "ROOTING"."CFMVERSION" AS "版本号",
    "ROOTING"."CFISLOCATION" AS "是否工位制",
    "ROOTING"."FISLOCATION" AS "是否工位制(旧)",
    "ROOTING"."FTCMID" AS "TCMID",
    "MATERIAL"."FNUMBER" AS "物料编码",
    "MATERIAL"."FNAME_L2" AS "物料名称",
    "MATERIAL"."FMODEL" AS "规格型号",
    "REF_MAT"."FNUMBER" AS "参考物料编码",
    "REF_MAT"."FNAME_L2" AS "参考物料名称",
    "ROOTING"."FMATERIALROOTINGID" AS "物料工艺路线ID",
    "ROOTING"."FSTORAGEORGUNITID" AS "库存组织ID",
    "ORG"."FNUMBER" AS "组织编码",
    "ORG"."FNAME_L2" AS "组织名称",
    "WH"."FNAME_L2" AS "完工仓库",
    "ROOTING"."FSTANDARDROOTINGGROUPID" AS "工艺路线分组ID",
    "ROOTING"."FCURRENCYID" AS "工价币别ID",
    "ROOTING"."CFADDRESSEEWORKCEN" AS "收件单位ID",
    "ROOTING"."FREFERENCEROOTINGID" AS "参考工艺路线ID",
    "ROOTING"."FSOURCEBILLID" AS "原始单据ID",
    "ROOTING"."FSOURCEFUNCTION" AS "来源功能",
    "ROOTING"."FHANDLERID" AS "经手人ID",
    "ROOTING"."FAUDITORID" AS "审核人ID",
    "ROOTING"."FAUDITTIME" AS "审核时间",
    "ROOTING"."FCONTROLUNITID" AS "控制单元",
    "ROOTING"."FCREATORID" AS "创建者",
    "ROOTING"."FCREATETIME" AS "创建时间",
    "ROOTING"."FLASTUPDATEUSERID" AS "最后修改者",
    "ROOTING"."FLASTUPDATETIME" AS "最后修改时间",
    "ROOTING"."FREMARK_L2" AS "备注",
    "PROJECT"."FNUMBER" AS "项目号",
    "PROJECT"."FNAME_L2" AS "项目名称",
    "TRACK"."FNUMBER" AS "车号",
    "JCH"."FNUMBER" AS "节车号",
    "OP"."FNUMBER" AS "工序编码",
    "OP"."FNAME_L2" AS "工序名称"
FROM
    "ZJEAS7"."T_MM_STANDARDROOTING" "ROOTING"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "MATERIAL" ON "MATERIAL"."FID" = "ROOTING"."FMATERIALID"
    LEFT JOIN "ZJEAS7"."T_BD_MATERIAL" "REF_MAT" ON "REF_MAT"."FID" = "ROOTING"."FREFERMATERIALID"
    LEFT JOIN "ZJEAS7"."T_ORG_STORAGE" "ORG" ON "ORG"."FID" = "ROOTING"."FSTORAGEORGUNITID"
    LEFT JOIN "ZJEAS7"."T_DB_WAREHOUSE" "WH" ON "WH"."FID" = "ROOTING"."FWAREHOUSEID"
    LEFT JOIN "ZJEAS7"."T_MM_MATERIALRWP" "RWP" ON "RWP"."FPARENTID" = "ROOTING"."FMATERIALROOTINGID"
    LEFT JOIN "ZJEAS7"."T_MM_OPERATION" "OP" ON "OP"."FID" = "RWP"."FOPERATIONID"
    LEFT JOIN "ZJEAS7"."T_MM_MANUFACTUREORDER" "MO" ON "MO"."FROUTINGID" = "ROOTING"."FID"
    LEFT JOIN "ZJEAS7"."T_MM_PROJECT" "PROJECT" ON "PROJECT"."FID" = "MO"."FPROJECTID"
    LEFT JOIN "ZJEAS7"."T_MM_TRACKNUMBER" "TRACK" ON "TRACK"."FID" = "MO"."FTRACKID"
    LEFT JOIN "ZJEAS7"."T_PRO_PROJECTJCH" "JCH" ON "JCH"."FID" = "MO"."FPROJECTJCHID"
WHERE
    {_where}
"""