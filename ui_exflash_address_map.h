#include "UI.h" 

#define UI_EXFLASH_BASE_ADDR              10
#define UI_ADDR(UI_ID)			        (UI_ID##_ADDR)
#define UI_END_ADDR(UI_ID)		        (UI_ID##_ADDR + sizeof(UI_ID))
#define UI_ADDR_ARRAY(UI_ID, INDEX)   	(UI_ID##_ADDR + sizeof(UI_ID##[0])*(INDEX))
#define 8_54X54__ADDR     (UI_EXFLASH_BASE_ADDR)
#define UI_FINISH_ADDR    (8_54X54__ADDR + sizeof(8_54X54))
