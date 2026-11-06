# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/5 11:21
@Author     : jack_shen
@File       : actual_data.py
@Description: actual_data（实际值聚合数据）的查询与新增接口
"""
from datetime import datetime

from flask import request

from .blueprint import main_bp
from app.models.book import db
from app.models.actual_data import ActualData
from app.utils.responses import ok, fail
from app.utils.base_request import fetch_daily_load
def parse_date(value):
    """把 'YYYY-MM-DD' 字符串转成 date，非法返回 None。"""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


@main_bp.route('/actual_data', methods=['GET'])
def list_actual_data():
    """查询实际值数据，所有参数均可选，可任意组合。

    精确筛选：?data_type=&data_sub_type=&region_type=&region_id=&ext_type=
    日期：?record_date=2026-11-05 或 ?start_date=&end_date=（含边界）
    分页：?page=1&per_page=20（per_page 上限 100）
    """

    query = ActualData.query
    region_id_str = request.args.get("region_id")
    if not region_id_str:
        return fail(message="region_id 不能为空")
    try:
        region_id = int(region_id_str)
    except ValueError:
        return fail(message="region_id 必须为整数")

    record_date = request.args.get("record_date")
    if not record_date:
        return fail(message="record_date 不能为空")

    record_date = parse_date(record_date)
    if not record_date:
        return fail(message="record_date 格式应为 YYYY-MM-DD")


    base_filter = [
        ActualData.region_id == region_id,
        ActualData.record_date == record_date
    ]
    data_type = request.args.get("data_type")

    if not data_type:
        base_filter.append(ActualData.region_id == region_id)

    rows = query.filter(*base_filter).order_by(
        ActualData.id.desc()
    ).all()

    total = len(rows)

    # total = query.filter(ActualData.region_id == region_id, ActualData.record_date == record_date).order_by(
    #     ActualData.id.desc()
    # ).count()
    print(total)
    if not rows:
        return ok(message="暂无数据", data=[])

    # print(len(first_row.to_dict().get("actual_values")))
    return ok(data=[item.to_dict() for item in rows])
    # 按日期倒序、id 倒序，拿第一条（最新一条）
    # first_row = query.order_by(
    #     ActualData.record_date.desc(),
    #     ActualData.id.desc()
    # ).all()
    # 字符串精确匹配
    for field in ("data_type", "data_sub_type", "region_type"):
        value = request.args.get(field)
        if value:
            query = query.filter(getattr(ActualData, field) == value)

    # 整数字段
    for field in ("region_id", "ext_type"):
        value = request.args.get(field)
        if value is not None:
            if not value.lstrip("-").isdigit():
                return fail(message=f"{field} 必须是整数")
            query = query.filter(getattr(ActualData, field) == int(value))

    # 单日
    record_date = request.args.get("record_date")
    if record_date:
        d = parse_date(record_date)
        if not d:
            return fail(message="record_date 格式应为 YYYY-MM-DD")
        query = query.filter(ActualData.record_date == d)

    # 日期区间
    for field, op in (("start_date", "ge"), ("end_date", "le")):
        value = request.args.get(field)
        if value:
            d = parse_date(value)
            if not d:
                return fail(message=f"{field} 格式应为 YYYY-MM-DD")
            col = ActualData.record_date
            query = query.filter(col >= d if op == "ge" else col <= d)

    # 分页
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
    except ValueError:
        return fail(message="page/per_page 必须是整数")

    pagination = (
        query.order_by(ActualData.record_date.desc(), ActualData.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    print(page[0])

    return ok(data={
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "list": [item.to_dict() for item in pagination.items],
    })




@main_bp.route('/crawler_actual_data')
def crawler_actual_data():
    region_id = request.args.get("region_id")
    record_date = request.args.get("record_date")
    data_type = request.args.get("data_type")
    # region_id
    # record_date
    # data_type

    # 这些值必填
    if not record_date:
        return fail(message="时间不能为空")

    dt = check_query_date(record_date)
    if dt is None:
        return fail(message="时间格式错误，请使用 YYYY-MM-DD，例如：2026-11-04")

    res = fetch_daily_load(query_date=record_date)

    if res.get("message") == 'Success':
        rows = res.get('data',{}).get('list',[])
        data = rows[0] if rows else {}

        result = [data.get(f"v{i}",0) for i in range(1,97)]



        return ok(data={
            "data":data,
            "result": result
        })
    else:
        return fail(message=f"查询失败：{res.get('message', '未知错误')}")

def check_query_date(date_str: str):
    try:
        # 强制 YYYY-MM-DD
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None



@main_bp.route('/actual_data', methods=['POST'])
def create_actual_data():
    """新增实际值数据（JSON 请求体）。

    必填：data_type、record_date（YYYY-MM-DD）、actual_values（96 个元素的数值数组）
    选填：data_sub_type（默认 ""）、region_id（默认 32）、region_type（默认 "all"）、
          ext_type（默认 0）、unit
    """
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return fail(message="请求体必须是 JSON 对象")

    data_type = body.get("data_type")
    if not data_type:
        return fail(message="data_type 不能为空")

    record_date = parse_date(body.get("record_date"))
    if not record_date:
        return fail(message="record_date 不能为空，格式应为 YYYY-MM-DD")

    actual_values = body.get("actual_values")
    if not isinstance(actual_values, list) or len(actual_values) != 96:
        return fail(message="actual_values 必须是 96 点位的数组（15 分钟粒度）")
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in actual_values):
        return fail(message="actual_values 元素必须是数值")

    data_sub_type = body.get("data_sub_type") or ""
    region_id = body.get("region_id", 32)
    region_type = body.get("region_type") or "all"
    ext_type = body.get("ext_type", 0)

    # 与库表 uk_actual_data 唯一约束对齐，提前查重
    exist = ActualData.query.filter_by(
        data_type=data_type,
        data_sub_type=data_sub_type,
        record_date=record_date,
        ext_type=ext_type,
        region_id=region_id,
        region_type=region_type,
    ).first()
    if exist:
        return fail(message="相同条件下记录已存在，请勿重复新增", code=409)

    record = ActualData(
        data_type=data_type,
        data_sub_type=data_sub_type,
        region_id=region_id,
        region_type=region_type,
        record_date=record_date,
        actual_values=actual_values,
        ext_type=ext_type,
        unit=body.get("unit"),
    )
    db.session.add(record)
    try:
        db.session.commit()
    except Exception as exc:  # 并发插入撞唯一约束等兜底
        db.session.rollback()
        return fail(message=f"新增失败：{exc}", code=500)

    return ok(data=record.to_dict(), message="新增成功")
