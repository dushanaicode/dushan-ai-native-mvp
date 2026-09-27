from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from framework.common.importing.package_locator import PackageLocator


class ModuleDefinition(BaseModel):
    """module.toml 的完整静态契约，不创建服务、路由或生命周期对象。

    scan_roots 相对 package，点号表示整个包；definitions 是包内 module:Class 列表，
    不受自动扫描开关和筛选器影响。
    所有字段显式提供，新增模块不需要框架枚举或目录名称推断。
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    package: str
    scan_roots: tuple[str, ...]
    definitions: tuple[str, ...]
    requires: tuple[str, ...]

    @field_validator("name", "package")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """标识字段单独校验，使错误能定位到声明的具体字段。"""
        if not PackageLocator.is_valid_name(value):
            raise ValueError("必须使用合法点分标识符")
        return value

    @field_validator("scan_roots", "definitions", "requires")
    @classmethod
    def validate_list(cls, values: tuple[str, ...], info: ValidationInfo) -> tuple[str, ...]:
        """拒绝重复关系，扫描根不允许跳出声明包。"""
        if len(values) != len(set(values)):
            raise ValueError("不允许重复项")
        for value in values:
            if info.field_name == "definitions":
                module, separator, name = value.partition(":")
                if (
                    not separator
                    or not (module == "." or PackageLocator.is_valid_name(module))
                    or not PackageLocator.is_valid_name(name)
                    or "." in name
                ):
                    raise ValueError("显式定义使用包内 module:Class，根模块用 .:Class")
            elif not (
                info.field_name == "scan_roots" and value == "."
            ) and not PackageLocator.is_valid_name(value):
                raise ValueError("必须使用包内点分名称，扫描整个包可填写 .")
        return values
