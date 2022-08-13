import win32ui
import win32gui
import win32con
import win32api
import numpy as np

from numpy import ndarray

from .structure import Region


def validate_region(region: Region | None) -> Region:
    if region is None:
        return Region(
            width=win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN),
            height=win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN),
            left=win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN),
            top=win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        )

    elif type(region) is Region:
        # region.width = region.width - region.left + 1
        # region.height = region.height - region.top + 1

        return region

    raise NotImplementedError(
        'Region should have type of Region class'
    )


def grab_screen(region: Region) -> ndarray:
    hwin = win32gui.GetDesktopWindow()

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()

    bmp.CreateCompatibleBitmap(
        srcdc, region.width, region.height
    )
    memdc.SelectObject(bmp)
    memdc.BitBlt(
        (0, 0), (region.width, region.height),
        srcdc, (region.left, region.top), win32con.SRCCOPY
    )

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (region.height, region.width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return np.array(img)
