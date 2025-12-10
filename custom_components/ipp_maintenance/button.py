import os
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from pyipp.enums import IppOperation

from .const import DOMAIN
from .coordinator import IPPConfigEntry
from .pwg import create_cmyk_pwg


async def async_setup_entry(
    hass: HomeAssistant, entry: IPPConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator = entry.runtime_data
    async_add_entities([DemoPrinterTestPageButton(coordinator)])


class DemoPrinterTestPageButton(ButtonEntity):
    def __init__(self, data):
        self.ipp = data.ipp
        self.device_id = data.device_id

        self._attr_name = "Print CMYK Page"
        self._attr_unique_id = f"print_cmyk_page_{data.device_id}"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self.device_id)}}

    async def async_press(self):
        """按钮按下时打印四色测试页"""
        image_data = await self.hass.async_add_executor_job(create_cmyk_pwg)

        async with self.ipp as ipp:
            ipp.request_timeout = 60
            await ipp.execute(
                IppOperation.PRINT_JOB,
                {
                    "operation-attributes-tag": {
                        "requesting-user-name": "HA",
                        "job-name": "CMYK Page",
                        "document-format": "image/pwg-raster",
                    },
                    "data": image_data,
                },
            )
