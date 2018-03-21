# alsa card name
PC_SPEAKER_NAME = 'PCH'
DO_POWER_OFF = False


def check_acpi_event(event)-> bool:
    return event[0] == 'ac_adapter'

