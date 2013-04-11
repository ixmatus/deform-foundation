from colander import null
from deform.widget import SelectWidget
from deform.widget import _normalize_choices


def _normalize_optgroup_choices(values):
    result = []
    for group in values:
        result.append({
            'label': group['label'],
            'values': _normalize_choices(group['values']),
        })
    return result

class ChosenSingleWidget(SelectWidget):
    template = 'chosen_single'
    requirements = (('chosen', None), )


class ChosenOptGroupWidget(SelectWidget):
    template = 'chosen_optgroup'
    requirements = (('chosen', None), )

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = self.null_value
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct,
                              values=_normalize_optgroup_choices(self.values))


class ChosenMultipleWidget(SelectWidget):
    template = 'chosen_multiple'
    values = ()
    size = 1
    requirements = (('chosen', None), )

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ()
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct,
                              values=_normalize_choices(self.values))

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        if isinstance(pstruct, str):
            return (pstruct,)
        return tuple(pstruct)
