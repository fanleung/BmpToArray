#include "application.h"
#include "ui_exflash_address_map.h"
#include "nrf_delay.h"

#define SAVE_UI(X)    		app_flash_write(X,X##_ADDR,sizeof(X))

void save_ui2flash(void)
{
	flash_device_power_down_set(false);
