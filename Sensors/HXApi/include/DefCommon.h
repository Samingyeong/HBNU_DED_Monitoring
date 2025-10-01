#pragma once
//------------------------------
// 사용자가 정의한 파라미터 11000개, - double 
// User parameter - PU
//------------------------------
enum systemPU {
	PU_STEP = 0,
	PU_TARGET = 1,
	PU_JOGVEL = 2,
	PU_STEPVEL = 34, // 32축
	PU_TARGETVEL = 66,// 32축
};

//------------------------------
// User define - color
//------------------------------
#define COLSKIN				RGB(240,240,240)
#define COLBRU_TITLE		RGB(80,80,80)
#define COLT_TITLE			RGB(250,250,250)
