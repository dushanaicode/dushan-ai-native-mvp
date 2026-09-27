from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from framework.common.enums import StatusEnum
from framework.starter_data_permission.decorators.data_permission import public_data
from framework.starter_database.public import BaseDO


@public_data()
class SmsChannelDO(BaseDO):
    __tablename__ = "system_sms_channel"
    __table_args__ = ({**BaseDO.__table_args__, **{"comment": "短信渠道信息表"}},)

    signature: Mapped[str] = mapped_column(String(12), nullable=False, comment="短信签名")
    code: Mapped[str] = mapped_column(
        String(63), nullable=False, comment="渠道编码【SmsChannelEnum】"
    )
    status: Mapped[int] = mapped_column(
        SmallInteger, default=StatusEnum.ENABLE.code, comment="开启状态（1-启用，0-禁用）"
    )
    remark: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="备注")
    api_key: Mapped[str] = mapped_column(String(128), nullable=False, comment="短信 API 的账号")
    api_secret: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="短信 API 的秘钥"
    )
    callback_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="短信发送回调 URL"
    )
