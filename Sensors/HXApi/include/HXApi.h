#pragma once

#include "extern.h"
#include "HXApi_Extern.h"
#include "HXApi_ExternAxis.h"

#if 0

// STR
#define	HX_STR_AXIS         121
#define	HX_STR_MACHINE      122
#define	HX_STR_SEQPROG      123
#define	HX_STR_ERRPROG      124
#define	HX_STR_NCPATH       125
#define	HX_STR_MAINPROG     126
#define	HX_STR_SUBPROG      127
#define	HX_STR_MDIPROG      128

#define	HX_DEVICE           129

#define	HX_STR_SYSPATH      130
#define	HX_STR_ALARMMSG     131
#define	HX_STR_OPMSG        132
#define	HX_STR_DATAPATH     133
#define	HX_STR_PLCFILE      134
#define	HX_STR_MAPFILE      135
#define	HX_STR_LANGUAGE     136
#endif

// define 정의
#define PSADDR(_axis, _addr) ((_axis * MAP_MAX_PS) + _addr)


enum {HX_ETHERNET = 0, HX_RTX};
enum {HX_FAIL = 0, HX_SUCCESS = 1, HX_NONE = -1};
enum {HX_OFF = 0, HX_ON };
enum { eCW = 0, eCCW };

#define HX_SIGNALSLEEP	200

#ifdef __cplusplus
extern "C"{
#endif
	// 기본 API ---------------------------------------------------------------------------------

	// 초기화, comtype : HX_ETHERNET/HX_RTX
	HXAPI_API long HXInitialize(long comtype, long ip1, long ip2, long ip3, long ip4, long port);
	
	// 초기화
	HXAPI_API long HXInit(long comtype);
	// 접속
	HXAPI_API long HXConnect(long ip1, long ip2, long ip3, long ip4, long port);
	
	// 종료
	HXAPI_API void HXTerminate();

	// 연결 상태 확인
	HXAPI_API long HXConnectState();

	HXAPI_API long HXGetRegister32(long name, long addr);
	HXAPI_API void HXSetRegister32(long name, long addr, long value);
	HXAPI_API double HXGetRegister64(long name, long addr);
	HXAPI_API void HXSetRegister64(long name, long addr, double value);
	HXAPI_API long HXGetBit(long name, long addr, long bitno);
	HXAPI_API void HXSetBit(long name, long addr, long bitno, long value);

	HXAPI_API void HXGetRegister32B(long count, long name[], long addr[], long* result);
	HXAPI_API void HXSetRegister32B(long count, long name[], long addr[], long value[]);
	HXAPI_API void HXGetRegister64B(long count, long name[], long addr[], double* result);
	HXAPI_API void HXSetRegister64B(long count, long name[], long addr[], double value[]);
	HXAPI_API void HXGetBitB(long count, long name[], long addr[], long bitno[], long* result);
	HXAPI_API void HXSetBitB(long count, long name[], long addr[], long bitno[], long value[]);

	HXAPI_API void HXGetString(int nName, char caStrVal[]);
	HXAPI_API void HXSetString(int nName, char caStrVal[]);
	// -------------------------------------------------------------------------------------------



	//----------------------------------------------// sjlee 20170717
	// Nc List
	HXAPI_API bool HXFtpConnect(char *ip);
	HXAPI_API int HXChangeDirNc();
	HXAPI_API int HXChangeDirMacro();
	HXAPI_API int HXChangeDir(char *path);
	HXAPI_API void HXGetNcIndex(int index, char *name);
	
	HXAPI_API void HXSetMainProgram(char *name);
	HXAPI_API void HXSetSubProgram(char *name);
	HXAPI_API void HXGetSystemPath(char *path);
	
	//----------------------------------------------// sjlee 20170717
	HXAPI_API void HXDownloadFile(const char* dir, const char* target, const char* name);
	HXAPI_API void HXUploadFile(const char* dir, const char* target, const char* name);
	HXAPI_API void HXDeleteFile(const char* name);

	HXAPI_API bool HXGetNcFileStr(int index, char* str);
	HXAPI_API int HXGetNcFileCount();
	


	// 2019-11-15 sisong
	
	HXAPI_API void HXSetNcPath(char *path);
	HXAPI_API void HXGetNcPath(char *path);





	// 다중 접속 API ---------------------------------------------------------------------------------

	// 초기화, comtype : HX_ETHERNET/HX_RTX
	HXAPI_API long XHXInitialize(int ncid, long comtype, long ip1, long ip2, long ip3, long ip4, long port);

	// 초기화
	HXAPI_API long XHXInit(long comtype);
	// 접속
	HXAPI_API long XHXConnect(int ncid, long ip1, long ip2, long ip3, long ip4, long port);

	// 종료
	HXAPI_API void XHXTerminate(int ncid);

	// 연결 상태 확인
	HXAPI_API long XHXConnectState(int ncid);

	HXAPI_API long XHXGetRegister32(int ncid, long name, long addr);
	HXAPI_API void XHXSetRegister32(int ncid, long name, long addr, long value);
	HXAPI_API double XHXGetRegister64(int ncid, long name, long addr);
	HXAPI_API void XHXSetRegister64(int ncid, long name, long addr, double value);
	HXAPI_API long XHXGetBit(int ncid, long name, long addr, long bitno);
	HXAPI_API void XHXSetBit(int ncid, long name, long addr, long bitno, long value);

	HXAPI_API void XHXGetRegister32B(int ncid, long count, long name[], long addr[], long* result);
	HXAPI_API void XHXSetRegister32B(int ncid, long count, long name[], long addr[], long value[]);
	HXAPI_API void XHXGetRegister64B(int ncid, long count, long name[], long addr[], double* result);
	HXAPI_API void XHXSetRegister64B(int ncid, long count, long name[], long addr[], double value[]);
	HXAPI_API void XHXGetBitB(int ncid, long count, long name[], long addr[], long bitno[], long* result);
	HXAPI_API void XHXSetBitB(int ncid, long count, long name[], long addr[], long bitno[], long value[]);

	HXAPI_API void XHXGetString(int ncid, int nName, char caStrVal[]);
	HXAPI_API void XHXSetString(int ncid, int nName, char caStrVal[]);

	HXAPI_API bool XHXAddUpdateMap(int ncid, long count, long name[], long ch[], long addr[]);
	HXAPI_API bool XHXRemoveUpdateMap(int ncid, long count, long name[], long ch[], long addr[]);
	// -------------------------------------------------------------------------------------------

	//----------------------------------------------// sjlee 20170717
	// Nc List
	HXAPI_API bool XHXFtpConnect(int ncid, char *ip);
	HXAPI_API int XHXChangeDirNc(int ncid);
	HXAPI_API int XHXChangeDirMacro(int ncid);
	HXAPI_API int XHXChangeDir(int ncid, char *path);
	HXAPI_API void XHXGetNcIndex(int ncid, int index, char *name);
	HXAPI_API void XHXSetMainProgram(int ncid, char *name);
	HXAPI_API void XHXSetSubProgram(int ncid, char *name);
	HXAPI_API void XHXGetSystemPath(int ncid, char *path);
	
	//----------------------------------------------// sjlee 20170717
	HXAPI_API void XHXDownloadFile(int ncid, const char* dir, const char* target, const char* name);
	HXAPI_API void XHXUploadFile(int ncid, const char* dir, const char* target, const char* name);
	HXAPI_API void XHXDeleteFile(int ncid, const char* name);

	//----------------------------------------------// sjlee 20170717


	// Read me - 반드시 한번 읽고 시작하세요. ----------------------------------------------------
	// 윗쪽에 있는 기본 API는 수정하지 마세요.
	// 함수명 가장 앞에는 "HX"를 붙여주세요.
	// 단어구문은 대/소문자로 하고, '_'(언더바)는 사용하지 마세요.
	// 타입을 구분할때는 반드시 enum을 사용하세요.
	// -> 숫자는 절대금지, #define 보다는 enum으로.
	// 의미없는 이름으로 함수 명을 만들지 마세요.
	// 함수1(), 함수2()등.. 의미를 알 수 없는 1, 2또는 문자를 사용하지마세요.
	// 약어를 사용하지마세요. 약어 꼭 필요하다면 약어의 의미를 주석으로 표기해주세요.
	// 입, 출력 파라미터로는 long,double만 사용하세요. VB와 연동하려면 반드시 지켜야합니다.
	// -------------------------------------------------------------------------------------------

	// 축 파라미터 
	HXAPI_API long HXSetAxisParameter(U32 nAxis, U32 addr, F64 value);
	HXAPI_API double HXGetAxisParameter(U32 nAxis, U32 addr);

	// 가공 파라미터 
	HXAPI_API long HXSetProcessingParameter(U32 nParam, F64 dVal);	//HXMachining::
	HXAPI_API double HXGetProcessingParameter(U32 nParam);

	// 시스템 파라미터 
	HXAPI_API long HXSetSystemParameter(U32 nParam, F64 dVal);
	HXAPI_API double HXGetSystemParameter(U32 nParam);

	// IO 파라미터 
	HXAPI_API long HXSetIOParameter(U32 nParam, F64 dVal);
	HXAPI_API double HXGetIOParameter(U32 nParam);

	// 모니터링 파라미터 
	HXAPI_API double HXGetStateParameter(U32 nParam);
	HXAPI_API double HXGetInfoParameter(U32 nParam);

	// NC 
	// 프로그램 파라미터 : 여러 맵 접근 
	HXAPI_API long		HXSetProgramParameter(U32 nParam, F64 dVal);
	HXAPI_API double	HXGetProgramParameter(U32 nParam);

	// 사용자 파라미터 : 여러 맵 접근 
	HXAPI_API long		HXSetUserParameter(U32 nParam, F64 dVal);
	HXAPI_API double	HXGetUserParameter(U32 nParam);

	// 매크로 파라미터 : 여러 맵 접근 
	HXAPI_API long		HXSetMacroParameter(U32 nParam, F64 dVal);
	HXAPI_API double	HXGetMacroParameter(U32 nParam);

	// HMI 파라미터 : 여러 맵 접근 
	HXAPI_API long		HXSetHMIParameter(U32 nParam, F64 dVal);
	HXAPI_API double	HXGetHMIParameter(U32 nParam);

	// GF 맵 API 
	// 0: low, 1: high, -1: read fail

	
	// No.1 : 준비완료			// enum HXGF_Ready
	HXAPI_API long HXGFReadySate(U32 nMode, U32 nAxis = -1);	

	// No.2 :NC 모드 설정(기본)	// enum HXGF_ncmode
	HXAPI_API long HXSetMode(U32 nMode);
	HXAPI_API long HXGetMode();	

	// No.3 : NC 모드 설정(보조)	// enum HXGF_NCmodeSub
	HXAPI_API long HXSetNCSUbMode(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetNCSUbMode(U32 nMode, U32 nIndex = -1);

	// No.4 : 리셋 비상정지		//enum HXGF_Reset
	HXAPI_API long HXSetReset(U32 nMode, U32 nON); 
	HXAPI_API long HXGetReset(U32 nMode);

	// No.5 : NC 제어 신호		// enum HXGF_NCRun
	HXAPI_API long HXSetNCRun(U32 nMode, U32 nON); 
	HXAPI_API long HXGetNCRun(U32 nMode);

	// NO.6 : NC 상태			// enum HXGF_NCstate
	HXAPI_API long HXGetNCState(U32 nMode);

	// NO.7 : 수동 운전 모드		// enum HXGF_ManualMode
	HXAPI_API long HXSetManualRunMode(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetManualRunMode(U32 nMode, U32 nIndex = -1);

	// NO.8 : 원점 복귀 기능		// enum HXGF_Home
	HXAPI_API long HXSetHomeMode(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetHomeMode(U32 nMode, U32 nIndex = -1);

	// NO.9 : 외부 조작 신호		// enum HXGF_ExternalSignal
	HXAPI_API long HXSetExternalSignal(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetExternalSignal(U32 nMode, U32 nIndex = -1);

	// NO.10 : 축 설정 그룹		// enum HXGF_AxisSetting
	HXAPI_API long HXSetMainAxis(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetMainAxis(U32 nMode, U32 nIndex = -1);

	// NO.11 : M기능		// enum HXGF_M
	HXAPI_API long HXSetMFunction(U32 nMode, U32 nON);
	HXAPI_API long HXGetMFunction(U32 nMode, U32 nIndex = -1);

	// NO.12 : S기능		// enum HXGF_Spindle
	HXAPI_API long HXSetSFunction(U32 nMode, U32 nON);
	HXAPI_API long HXGetSFunction(U32 nMode, U32 nIndex = -1);

	// NO.14 : T기능		// enum HXGF_T
	HXAPI_API long HXSetTFunction(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetTFunction(U32 nMode, U32 nIndex = -1);

	// NO.15 : Chopping기능		// enum HXGF_Chopping
	HXAPI_API long HXSetChopping(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetChopping(U32 nMode, U32 nIndex = -1);

	// NO.16 : NC 내부 정보		// enum HXGF_NCInternal	
	HXAPI_API long HXGetNCInternalState(U32 nMode, U32 nIndex = -1);

	// NO.17 : 동기 제어			// enum HXGF_SyncControl
	HXAPI_API long HXSetSyncControl(U32 nMode, U32 nON, U32 nIndex = -1);
	
	// NO.18 : 커스텀 매크로기능		// enum HXGF_CustomMacro
	HXAPI_API long HXSetCustomMacro(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetCustomMacro(U32 nMode, U32 nIndex = -1);
	
	// NO.19 : PLC 축 제어 		// enum HXGF_PLCAxis
	HXAPI_API long HXSetPLCAxis(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetPLCAxis(U32 nMode, U32 nIndex = -1);

	// NO.20 : 특수 제어 		// enum HXGF_AdvancedControl
	HXAPI_API long HXSetAdvancedControl(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetAdvancedControl(U32 nMode, U32 nIndex = -1);
	
	// NO.21 : 스크린/Key 정보 		// enum HXGF_SCreen
	HXAPI_API long HXSetScreen(U32 nMode, U32 nON, U32 nIndex = -1);
	HXAPI_API long HXGetScreen(U32 nMode, U32 nIndex = -1);
	
	// NO.22 : PLC 알람 		// enum HXGF_PLCmessage
	HXAPI_API long HXSetPLCAlarm(U32 nMode, U32 nAddr, U32 nIndex, U32 nON);
	HXAPI_API long HXGetPLCAlarm(U32 nMode, U32 nAddr, U32 nIndex = 0);

	// NO.23 : Lettering 정보 		// enum HXGF_Lettering	
	HXAPI_API long HXGetLetteringState(U32 nMode);

	// NO.24 : 선단제어 정보 		// enum HXGF_ToolEndcontrol	
	HXAPI_API long HXGetG43Run();

	// NO.23 : C상 측정 정보 		// enum HXGF_CPhase	
	HXAPI_API long HXGetCPhaseMeasure(U32 nMode, U32 nIndex );


	// 확장 API ----------------------------------------------------------------------------------


	// 상태/ 설정 
	// 계통에 이상이 없는 경우 ON 
	// 제어장치 전원 인가 후, 자기 진단이 정상으로 완료한 경우에 ON
	// CPU 이상 또는 메모리 이상 등 제어장치 자체의 에러 검출시 OFF
	HXAPI_API long HXGetReadyState();

	// 서보/스핀들 계통에 이상이 없는 경우 ON
	HXAPI_API long HXGetSlaveReadyState();

	
	

	// 리셋 /비상 정지 
	HXAPI_API long HXGetStateReset();
	HXAPI_API long HXGetStateEMG();

	// 수동 운전 모드 
	// nDicrection 0: +, 1: - 
	// return : 1 : Moving, 0: stop 
	HXAPI_API long HXGetJogState(U32 nAxis, U32 &nDirection);
	
	// 원점 복귀 
	// return ex : stateHome::HOME_RUNNING 
	// return -1 = state 
	HXAPI_API long HXGetHomeSate(U32 nAxis);

	// 원점 복귀 home bound 체크 
	// return : 0 : 금지 영역 
	HXAPI_API long HXCheckHomeLimit(U32 nAxis);

	//void HXMoveStart(long nAxis, double dDistance, double dFeed);	
	HXAPI_API long HXMoveStart(long nAxis, double dDistance, double dFeed);
	//void HXStop(long nAxis, double dFeed);

	// -------------------------------------------------------------------------------------------
	//----------------------------------------------

#ifdef __cplusplus
}
#endif

