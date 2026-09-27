from sqlalchemy.orm.mapper import _all_registries

from framework.common.component.component_metadata import ComponentMetadata
from framework.common.enums.component_type_enum import ComponentTypeEnum
from framework.starter_scanner.annotation.scanner_decorator import scanner


class ModelScanner:
    """多个独立模型声明共用一个发现标记，各声明仍自行拒绝重复装饰。"""

    @staticmethod
    def mark(model):
        metadata = vars(model).get(ComponentMetadata.ATTRIBUTE)
        if metadata is None:
            return scanner(model)
        if metadata != ComponentMetadata(ComponentTypeEnum.COMPONENT):
            raise ValueError("模型与已有扫描类别冲突")
        return model

    @staticmethod
    def collect(packages, components):
        """读取已启用包的映射快照，确保未声明访问策略的模型也被启动校验发现。"""
        models = {model for model in components if "__table__" in vars(model)}
        for registry in _all_registries():
            for mapper in tuple(registry.mappers):
                model = mapper.class_
                if any(
                    model.__module__ == p or model.__module__.startswith(p + ".") for p in packages
                ):
                    models.add(model)
        return tuple(sorted(models, key=lambda model: (model.__module__, model.__qualname__)))
