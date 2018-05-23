#include "application.h"
#include "ui_exflash_address_map.h"
#include "nrf_delay.h"

#define SAVE_UI(X)    		app_flash_write(X,X##_ADDR,sizeof(X))

void save_ui2flash(void)
{
	flash_device_power_down_set(false);
	SAVE_UI(8_54X54)
	end_addr = UI_FINISH_ADDR / 1024;
	app_flash_write(flash_id,UI_EXFLASH_BASE_ADDR-10,10);

}
