#include "application.h"
#include "ui_exflash_address_map.h"
#include "nrf_delay.h"

#define SAVE_UI(X)    		app_flash_write(X,X##_ADDR,sizeof(X))

void save_ui2flash(void)
{
	flash_device_power_down_set(false);
	SAVE_UI(Hour_0_21X23)
	SAVE_UI(Hour_1_21X23)
	SAVE_UI(Hour_10_15X23)
	SAVE_UI(Hour_2_21X23)
	SAVE_UI(Hour_3_21X23)
	SAVE_UI(Hour_4_21X23)
	SAVE_UI(Hour_5_21X23)
	SAVE_UI(Hour_6_21X23)
	SAVE_UI(Hour_7_21X23)
	SAVE_UI(Hour_8_21X23)
	SAVE_UI(Hour_9_21X23)
	SAVE_UI(Min_0_21X23)
	SAVE_UI(Min_1_21X23)
	SAVE_UI(Min_2_21X23)
	SAVE_UI(Min_3_21X23)
	SAVE_UI(Min_4_21X23)
	SAVE_UI(Min_5_21X23)
	SAVE_UI(Min_6_21X23)
	SAVE_UI(Min_7_21X23)
	SAVE_UI(Min_8_21X23)
	SAVE_UI(Min_9_21X23)
	end_addr = UI_FINISH_ADDR / 1024;
	app_flash_write(flash_id,UI_EXFLASH_BASE_ADDR-10,10);

}
