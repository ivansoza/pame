from django.forms.widgets import ClearableFileInput
from django.forms.widgets import CheckboxInput

FILE_INPUT_CONTRADICTION = object()

class ClearableMultipleFilesInput(ClearableFileInput):
    def value_from_datadict(self, data, files, name):
        upload = files.getlist(name) # files.get(name) in Django source

        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):

            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # objects that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload