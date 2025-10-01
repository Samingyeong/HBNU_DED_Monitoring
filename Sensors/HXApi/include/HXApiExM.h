#pragma once

#include "extern.h"
#include "HXApi.h"


extern "C" {

	
	HXAPI_API long HXServoOn();			
	HXAPI_API long HXServoAlramReset();
	HXAPI_API long HXCycleStart();
	HXAPI_API long HXCycleStop();
	HXAPI_API long HXReset();
	HXAPI_API long HXEMG();
	HXAPI_API long HXEMGClear();
	HXAPI_API long HXPowerOff();

	// Jog 이송 
	// 주의 : JOG 모드에서만 작동 합니다. 
	HXAPI_API long HXJOGMove(U32 nAxis, U32 nDirection = eCCW, U32 nMove = HX_ON);

	// 수동 이송 속도 테이블 (1~32)
	HXAPI_API long HXSetManualFeedIndex(U32 nIndex);

	// Rapid jog ( 0: Off, 1: On)
	HXAPI_API long HXSetRapidJog(U32 nOn);
	HXAPI_API long HXGetRapidJog();

	// Step 이송 거리 테이블 (1~32)
	HXAPI_API long HXSetStepDistanceIndex(U32 nIndex);
	
	// MPG 배율 (0: X1, 1: X10, 2: X100)
	HXAPI_API long HXMPGMultiplier(U32 nIndex);

	// 제 1MPG에 의한 수동 이송 축 선택 
	HXAPI_API long HXMPGAxis(U32 nIndex);

	// 제 1MPG interrup에 의한 수동 이송 축 선택 
	HXAPI_API long HXMPGInterruptAxis(U32 nIndex);

// 외부 조작 --------------------
	// Over Tavel 
	HXAPI_API long HXOverTravel(U32 nAxis, U32 nDirection = eCCW, U32 nMove = HX_ON);

	// interlock
	HXAPI_API long HXInterLock(U32 nAxis, U32 nDirection = eCCW, U32 nLock = HX_ON);

	// 모든 축 interlock
	HXAPI_API long HXInterLockAll(U32 nDirection = eCCW, U32 nLock= HX_ON);

	// 선택 축 close 
	HXAPI_API long HXSetServoClose(U32 nAxis, U32 nOk);

	// 선택 축 servo off
	HXAPI_API long HXSetServoOff(U32 nAxis, U32 nOk);

	// 선택 축 서보 레디 상태 확인 
	HXAPI_API long HXGetServoReady(U32 nAxis);

	// 급송 이송 override index 설정 
	HXAPI_API long HXSetRapidOverrideIndex(U32 nIndex);

	// 이송 feed index 설정 
	HXAPI_API long HXSetFeedOverrideIndex(U32 nIndex);

	//스핀들 override index 설정 
	HXAPI_API long HXSetSpindleOverrideIndex(U32 nIndex);

	// 소프트 리미트 OFF 
	HXAPI_API long HXOffSoftLimit(U32 nAxis, U32 nDirection = eCCW, U32 nLock = HX_ON);

	// 외부 감속 OFF
	HXAPI_API long HXOuternalDeccel(U32 nAxis, U32 nDirection = eCCW, U32 nLock = HX_ON);

// 축 설정 그룹 
	//HXAPI_API long HXSetMainSpindle(U32 nAxis);
	//HXAPI_API long HXGetMainSpindle();
	////HXAPI_API long HXSetZAxis(U32 nAxis);
	//HXAPI_API long HXGetZAxis();

// S 및 스핀들 기능 
	// 수동 운전 스핀들 RPM 

	// 트윈 테이블 동기제어 
	// nMaster :  마스터 축 
	// nSlave :  슬레이브 축 
	// nType : 0: 일반 운전 , 1: 마스터 단독 운전, 2: 슬레이브 단독 운전, 3: 동기 운전 
	HXAPI_API long HXTwinTable(U32 nMaster, U32 nSlave, U32 nType);
//-------------------------------------------

	//PLC가 정상적인 동작을 수행됨을 알려줌
	HXAPI_API long HXGetPLCRunSate();

	//CNC 계통에 이상이 없는 경우 ON
	//제어장치 전원 인가 후, 자기진단이 정상으로 완료한 경우에 ON
	HXAPI_API long HXGetCNCRunSate();

	//서보/스핀들 계통에 이상이 없는 경우 ON
	//EM-STOP, 서보 OFF, 서보 Alarm 인 경우 
	HXAPI_API long HXGetSubSystemRunSate();

	
	
	// PLC 축 ------------------------------------------------------------------------------------
	// 해당 축을 PLC 축으로 선언하고 초기화 , 초기속도 100 
	HXAPI_API long HXMotionAxisInit(int nAxis); 

	// 축 지령 시작 
	HXAPI_API long HXMovingStart(U32 nAxis, F64 dDist, F64 dFeed );

	// 축 지령 종료 
	HXAPI_API long HXMovingStop(U32 nAxis);

	// 축 지령 취소 
	HXAPI_API long HXMoveCancel(U32 nAxis);

	
	// Homing 
	// dFeed : 원점복귀 속도
	// dDecel1st : 1차 감속 속도 
	// dDecel2nd : 2차 감속 속도 
	// dAccer: 가감속 
	// bUseArbitraryOrig : 0: 임의 원점 사용 1: 사용안함 
	// bUseDog : 0: Dog 사용안함  1: 사용
	// nDirection : homing 방향 
	HXAPI_API long HXHoming(U32 nAxis, F64  dFeed, F64 dDecel1st, F64 dDecel2nd, F64 dAcce
		, U32 bUseArbitraryOrig = 0, U32 bUseDog = 0, U32 nDirection = eCW);

	// Goto 지령 : 증분 
	// dPosmm : 이동 시킬 위치 량 
	// dFeed : 지령 속도 
	HXAPI_API long HXGoto_INC(U32 nAxis, double dPosmm, double dFeed);

	// Goto 지령 : 절대 
	// dPosmm : 이동시킬 절대 위치
	// dFeed : 지령 속도 
	HXAPI_API long HXGoto_ABS(U32 nAxis, double dPosmm, double dFeed);
	


}