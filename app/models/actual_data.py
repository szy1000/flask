# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/5 11:07
@Author     : jack_shen
@File       : actual_data.py
@Description: 
"""
# app/models/actual_data.py
# -*- coding: utf-8 -*-
"""
@Description: 实际值聚合数据表
"""
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime
from app.models.book import db


class ActualData(db.Model):
    __tablename__ = "actual_data"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    data_type = Column(
        String(32),
        nullable=False,
        comment="数据类型枚举（da_wind/da_solar/da_price/rt_price/da_social_load/price_spread）"
    )
    data_sub_type = Column(
        String(32),
        nullable=False,
        default="",
        comment="数据子类型（同一dataType下区分不同数据，默认空字符串）"
    )
    region_id = Column(
        Integer,
        nullable=False,
        default=32,
        comment="区域ID（默认32=江苏省）"
    )
    region_type = Column(
        String(32),
        nullable=False,
        default="all",
        comment="区域类型（默认all）"
    )
    record_date = Column(
        Date,
        nullable=False,
        comment="数据日期"
    )
    actual_values = Column(
        JSONB,
        nullable=False,
        comment="96点位实际值（JSONB-List<Double>，15分钟粒度，00:00~23:45）"
    )
    ext_type = Column(
        Integer,
        nullable=False,
        default=0,
        comment="扩展类型（0=汇总, 1=江南, 2=江北，仅统调风光）"
    )
    unit = Column(
        String(32),
        nullable=True,
        comment="数据单位（标准单位：KW、KWh、元/KWh）"
    )
    create_time = Column(
        DateTime,
        default=datetime.utcnow,
        comment="创建时间"
    )
    update_time = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="修改时间"
    )

    # 唯一约束，和库表 uk_actual_data 对齐
    __table_args__ = (
        db.UniqueConstraint(
            "data_type",
            "data_sub_type",
            "record_date",
            "ext_type",
            "region_id",
            "region_type",
            name="uk_actual_data"
        ),
        # 如果需要在模型里声明索引（可选，建表 SQL 已经建好了）
        # db.Index("idx_actual_data_query", "data_type", "data_sub_type", "record_date", "ext_type", "region_id"),
        # db.Index("idx_actual_data_record_date", "record_date"),
        # db.Index("idx_actual_data_region", "region_id"),
    )

    def to_dict(self):
        """序列化工具，接口返回用"""
        return {
            "id": self.id,
            "data_type": self.data_type,
            "data_sub_type": self.data_sub_type,
            "region_id": self.region_id,
            "region_type": self.region_type,
            "record_date": self.record_date.isoformat() if self.record_date else None,
            "actual_values": self.actual_values,
            "ext_type": self.ext_type,
            "unit": self.unit,
            "create_time": self.create_time.isoformat() if self.create_time else None,
            "update_time": self.update_time.isoformat() if self.update_time else None,
        }
