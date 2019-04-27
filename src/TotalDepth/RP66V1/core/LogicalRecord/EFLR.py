"""
Implements the Explicitly Formatted Logical Record [RP66V1 Section 3 Logical Record Syntax]

References:
RP66V1: http://w3.energistics.org/rp66/v1/rp66v1.html
Specifically section 3: http://w3.energistics.org/rp66/v1/rp66v1_sec3.html
"""
# import collections
import logging
import typing

from TotalDepth.RP66V1 import ExceptionTotalDepthRP66V1
from TotalDepth.RP66V1.core.File import LogicalData
from TotalDepth.RP66V1.core.LogicalRecord.ComponentDescriptor import ComponentDescriptor
from TotalDepth.RP66V1.core.RepCode import IDENT, UVARI, USHORT, UNITS, code_read, OBNAME, ObjectName, REP_CODE_INT_TO_STR


logger = logging.getLogger(__file__)


class ExceptionEFLR(ExceptionTotalDepthRP66V1):
    pass


class ExceptionEFLRSet(ExceptionEFLR):
    pass


class ExceptionEFLRSetDuplicateObjectNames(ExceptionEFLRSet):
    pass


class ExceptionEFLRAttribute(ExceptionEFLR):
    pass


class ExceptionEFLRTemplate(ExceptionEFLR):
    pass


class ExceptionEFLRTemplateDuplicateLabel(ExceptionEFLRTemplate):
    pass


class ExceptionEFLRObject(ExceptionEFLR):
    pass

class ExceptionEFLRObjectDuplicateLabel(ExceptionEFLRObject):
    pass



class Set:
    def __init__(self, ld: LogicalData):
        component_descriptor = ComponentDescriptor(ld.read())
        if not component_descriptor.is_set_group:
            raise ExceptionEFLRSet(f'Component Descriptor does not represent a set but a {component_descriptor.type}.')
        self.type: bytes = IDENT(ld)
        self.name: bytes = ComponentDescriptor.CHARACTERISTICS_AND_COMPONENT_FORMAT_SET_MAP['N'].global_default
        if component_descriptor.has_set_N:
            self.name = IDENT(ld)

    def __str__(self) -> str:
        return f'EFLR Set type: {self.type} name: {self.name}'


class AttributeBase:
    def __init__(self, component_descriptor: ComponentDescriptor):
        if not component_descriptor.is_attribute_group:
            raise ExceptionEFLRAttribute(
                f'Component Descriptor does not represent a attribute but a {component_descriptor.type}.'
            )
        self.component_descriptor = component_descriptor
        self.label = ComponentDescriptor.CHARACTERISTICS_AND_COMPONENT_FORMAT_ATTRIBUTE_MAP['L'].global_default
        self.count = ComponentDescriptor.CHARACTERISTICS_AND_COMPONENT_FORMAT_ATTRIBUTE_MAP['C'].global_default
        self.rep_code = ComponentDescriptor.CHARACTERISTICS_AND_COMPONENT_FORMAT_ATTRIBUTE_MAP['R'].global_default
        self.units = ComponentDescriptor.CHARACTERISTICS_AND_COMPONENT_FORMAT_ATTRIBUTE_MAP['U'].global_default
        self.value = ComponentDescriptor.CHARACTERISTICS_AND_COMPONENT_FORMAT_ATTRIBUTE_MAP['V'].global_default

    def __eq__(self, other):
        if isinstance(other, AttributeBase):
            return self.__dict__ == other.__dict__
        return NotImplemented

    # def __str__(self) -> str:
    #     return f'CD: {self.component_descriptor} L: {self.label} C: {self.count}' \
    #         f' R: {self.rep_code} U: {self.units} V: {self.value}'
    #
    def __str__(self) -> str:
        return f'CD: {self.component_descriptor} L: {self.label} C: {self.count}' \
            f' R: {REP_CODE_INT_TO_STR[self.rep_code]} U: {self.units} V: {self.value}'


class TemplateAttribute(AttributeBase):
    def __init__(self, component_descriptor: ComponentDescriptor, ld: LogicalData):
        super().__init__(component_descriptor)
        if self.component_descriptor.has_attribute_L:
            self.label = IDENT(ld)
        if self.component_descriptor.has_attribute_C:
            self.count = UVARI(ld)
        if self.component_descriptor.has_attribute_R:
            self.rep_code = USHORT(ld)
        if self.component_descriptor.has_attribute_U:
            self.units = UNITS(ld)
        if self.component_descriptor.has_attribute_V:
            self.value = [code_read(self.rep_code, ld) for _i in range(self.count)]


class Attribute(AttributeBase):
    def __init__(self,
                 component_descriptor: ComponentDescriptor,
                 ld: LogicalData,
                 template_attribute: TemplateAttribute,
                 ):
        super().__init__(component_descriptor)
        if self.component_descriptor.has_attribute_L:
            self.label = IDENT(ld)
        else:
            self.label = template_attribute.label
        if self.component_descriptor.has_attribute_C:
            self.count = UVARI(ld)
        else:
            self.count = template_attribute.count
        if self.component_descriptor.has_attribute_R:
            self.rep_code = USHORT(ld)
        else:
            self.rep_code = template_attribute.rep_code
        if self.component_descriptor.has_attribute_U:
            self.units = UNITS(ld)
        else:
            self.units = template_attribute.units
        if self.component_descriptor.has_attribute_V:
            self.value = [code_read(self.rep_code, ld) for _i in range(self.count)]
        else:
            self.value = template_attribute.value


class Template:
    def __init__(self):
        self.attrs: typing.List[TemplateAttribute] = []
        self.attr_label_map: typing.Dict[bytes, int] = {}

    def read(self, ld: LogicalData):
        while True:
            component_descriptor = ComponentDescriptor(ld.read())
            if not component_descriptor.is_attribute_group:
                raise ExceptionEFLRTemplate(
                    f'Component Descriptor does not represent a attribute but a {component_descriptor.type}.'
                )
            template_attribute = TemplateAttribute(component_descriptor, ld)
            if template_attribute.label in self.attr_label_map:
                raise ExceptionEFLRTemplateDuplicateLabel(f'Duplicate template label {template_attribute.label}')
            self.attr_label_map[template_attribute.label] = len(self.attrs)
            self.attrs.append(template_attribute)
            next_component_descriptor = ComponentDescriptor(ld.peek())
            if next_component_descriptor.is_object:
                break

    def __len__(self) -> int:
        return len(self.attrs)

    def __getitem__(self, item) -> TemplateAttribute:
        return self.attrs[item]

    def __eq__(self, other) -> bool:
        if other.__class__ == Template:
            return self.attrs == other.attrs
        return NotImplemented

    def __str__(self) -> str:
        return '\n'.join(str(a) for a in self.attrs)

    def header_as_strings(self) -> typing.List[str]:
        return [str(attr.label) for attr in self.attrs]


class Object:
    def __init__(self, ld: LogicalData, template: Template):
        component_descriptor = ComponentDescriptor(ld.read())
        if not component_descriptor.is_object:
            raise ExceptionEFLRObject(
                f'Component Descriptor does not represent a object but a {component_descriptor.type}.')
        self.name: ObjectName = OBNAME(ld)
        self.attrs: typing.List[typing.Union[AttributeBase, None]] = []
        self.attr_label_map: typing.Dict[bytes, int] = {}
        index: int = 0
        while True:
            component_descriptor = ComponentDescriptor(ld.read())
            if not component_descriptor.is_attribute_group:
                raise ExceptionEFLRObject(
                    f'Component Descriptor does not represent a attribute but a {component_descriptor.type}.'
                )
            if template[index].component_descriptor.is_invariant_attribute:
                self.attrs.append(template[index])
            elif template[index].component_descriptor.is_absent_attribute:
                self.attrs.append(None)
            else:
                # TODO: Check the attribute label is the same as the template. Reference [RP66V1 Section 4.5]
                self.attrs.append(Attribute(component_descriptor, ld, template[index]))
                if ld.remain == 0 or ComponentDescriptor(ld.peek()).is_object:
                    break
                # next_component_descriptor = ComponentDescriptor(ld.peek())
                # if next_component_descriptor.is_object:
                #     break
            index += 1
        while len(self.attrs) < len(template):
            self.attrs.append(template[len(self.attrs)])
        if len(template) != len(self.attrs):
            raise ExceptionEFLRObject(
                f'Template specifies {len(template)} attributes but Logical Data has {len(self.attrs)}'
            )
        # Now populate self.attr_label_map
        for a, attr in enumerate(self.attrs):
            if attr is None:
                label = template.attrs[a].label
            else:
                label = attr.label
                # TODO: Assert that the attribute label is the same as the template. Reference [RP66V1 Section 4.5]
            if label in self.attr_label_map:
                raise ExceptionEFLRObjectDuplicateLabel(f'Duplicate Attribute label {label}')
            self.attr_label_map[label] = a

    def __len__(self) -> int:
        return len(self.attrs)

    def __getitem__(self, item) -> typing.Union[AttributeBase, None]:
        if item in self.attr_label_map:
            return self.attrs[self.attr_label_map[item]]
        return self.attrs[item]

    def __eq__(self, other) -> bool:
        if other.__class__ == Object:
            return self.name == other.name and self.attrs == other.attrs and self.attr_label_map == other.attr_label_map
        return NotImplemented

    def __str__(self) -> str:
        strs = [
            str(self.name)
        ]
        strs.extend(
            ['  {}'.format(a) for a in self.attrs]
        )
        return '\n'.join(strs)

    def values_as_strings(self) -> typing.List[str]:
        ret = []
        for attr in self.attrs:
            if attr.value is None:
                ret.append('None')
            elif isinstance(attr.value[0], bytes):
                ret.append(str(b', '.join(attr.value)))
            else:
                ret.append(', '.join(str(v) for v in attr.value))
        return ret


class ExplicitlyFormattedLogicalRecordBase:
    def __init__(self, lr_type: int, ld: LogicalData):
        self.lr_type: int = lr_type
        self.set: Set = Set(ld)
        self.template: Template = Template()
        self.objects: typing.List[Object] = []
        self.object_name_map: typing.Dict[bytes, int] = {}


class ExplicitlyFormattedLogicalRecord(ExplicitlyFormattedLogicalRecordBase):
    def __init__(self, lr_type: int, ld: LogicalData):
        super().__init__(lr_type, ld)
        if ld:
            self.template.read(ld)
            while ld:
                obj = Object(ld, self.template)
                if obj.name in self.object_name_map:
                    # Compare and if same ignore, else raise
                    if obj == self[obj.name]:
                        msg = f'Ignoring duplicate Object with {obj.name} already seen in the {self.set}.'
                        logger.info(msg)
                    else:
                        msg = f'Ignoring different Object with {obj.name} already seen in the {self.set}.'
                        logger.warning(msg)
                        logger.warning('WAS:')
                        logger.warning(str(self[obj.name]))
                        logger.warning('NOW:')
                        logger.warning(str(obj))
                        # raise ExceptionEFLRSetDuplicateObjectNames(msg)
                else:
                    self.object_name_map[obj.name] = len(self.objects)
                    self.objects.append(obj)

    def __len__(self) -> int:
        return len(self.objects)

    def __getitem__(self, item) -> Object:
        if item in self.object_name_map:
            return self.objects[self.object_name_map[item]]
        return self.objects[item]

    def __str__(self) -> str:
        ret = [
            f'<ExplicitlyFormattedLogicalRecord {str(self.set)}>',
            f'  Template [{len(self.template)}]:',
        ]
        ret.extend('    {}'.format(line) for line in str(self.template).split('\n'))
        ret.append(f'  Objects [{len(self.objects)}]:')
        for obj in self.objects:
            ret.extend('    {}'.format(line) for line in str(obj).split('\n'))
        return '\n'.join(ret)
