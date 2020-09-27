import pytest
import app.print


@pytest.mark.asyncio
async def test_build_print_command():
    """
    Tests that print command is built correctly
    """

    command = app.print.build_print_command(image_path="IMAGE",
                                            printer_model="MODEL",
                                            label_type="LABEL",
                                            printer_backend="BACKEND",
                                            printer_url="URL",
                                            red=True,
                                            low_quality=True,
                                            high_dpi=True,
                                            compress=True)
    assert " IMAGE" in ' '.join(command)
    assert " --model MODEL " in ' '.join(command)
    assert " --label LABEL " in ' '.join(command)
    assert " --backend BACKEND " in ' '.join(command)
    assert " --printer URL " in ' '.join(command)
    assert " --red " in ' '.join(command)
    assert " --lq " in ' '.join(command)
    assert " --600dpi " in ' '.join(command)
    assert " --compress " in ' '.join(command)

    command = app.print.build_print_command(image_path="IMAGE",
                                            printer_model="MODEL",
                                            label_type="LABEL",
                                            printer_backend="BACKEND",
                                            printer_url="URL",
                                            red=False,
                                            low_quality=False,
                                            high_dpi=False,
                                            compress=False)
    assert " --red " not in ' '.join(command)
    assert " --lq " not in ' '.join(command)
    assert " --600dpi " not in ' '.join(command)
    assert " --compress " not in ' '.join(command)
