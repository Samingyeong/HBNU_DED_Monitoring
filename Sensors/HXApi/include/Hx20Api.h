/*
 * HxApi.h
 *
 * Created on: 2017. 11. 3.
 *   Author: cscam
 *
 * GX 전용 소스
 *
 * Set : G맵 입력, Get : G맵 가져오기, Signal : F맵 신호
 */

#ifndef _HXAPI20_H_
#define _HXAPI20_H_

#include "extern.h"
#include "TypeDef.h"
#include "mapDefine.h"
//#include "HxEnum.h"

#define HX_PORT_MAX		10
#define HX_AXIS_MAX		32
#define HX_CHANNEL_MAX	1

#ifdef __cplusplus
class Hx20System;
class Hx20Axis;
class Hx20Channel;
typedef const Hx20System*	HX_SYSTEM;
typedef const Hx20Axis*		HX_AXIS;
typedef const Hx20Channel*	HX_CHANNEL;
#else
typedef const void*			HX_SYSTEM;
typedef const void*			HX_AXIS;
typedef const void*			HX_CHANNEL;
#endif






#ifdef __cplusplus
extern "C"{
#endif

//HXAPI_API const char* HxGetApiVersion();

HXAPI_API void HxGetVersion(Int32 port, char* version);

HXAPI_API Bool HxInitialize(Int32 comtype);
HXAPI_API void HxTerminate();

HXAPI_API Bool HxInitialize2(Int32 comtype, Int32 ip1, Int32 ip2, Int32 ip3, Int32 ip4, Int32 ipport);


HXAPI_API HX_SYSTEM HxGetSystem(Int32 port);
HXAPI_API HX_CHANNEL HxGetChannel(Int32 port, Int32 channel);
HXAPI_API HX_AXIS HxGetAxis(Int32 port, Int32 axis);

// 초기화, comtype : HX_ETHERNET/HX_RTX
HXAPI_API Bool HxConnect(Int32 port, Int32 ip1, Int32 ip2, Int32 ip3, Int32 ip4, Int32 ipport);
HXAPI_API Bool HxBuiltInConnect(Int32 port);

// 종료
HXAPI_API void HxDisconnect(Int32 port);

// 연결 상태 확인
HXAPI_API Bool HxGetConnectState(Int32 port);

// Buffer 내용을 한꺼번에 보낸다.
HXAPI_API void HxSendSetData(Int32 port);

HXAPI_API const char* HxGetString(Int32 port, Int32 ch, Int32 name, Int32 addr);

HXAPI_API void HxSetString(Int32 port, Int32 ch, Int32 name, Int32 addr, char* resstr);

// Basic API
HXAPI_API void HxGetReg32(Int32 port, Int32 count, Int32 name[], Int32 addr[], Int32 word[], Bool direct = false);
HXAPI_API void HxGetReg64(Int32 port, Int32 count, Int32 name[], Int32 addr[], Double real[], Bool direct = false);
HXAPI_API Bool HxGetBit32(Int32 port, Int32 name, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxGetBit(Int32 port, Int32 count, Int32 name[], Int32 addr[], Int32 bit[], Bool onoff[], Bool direct = false);

HXAPI_API void HxSetReg32(Int32 port, Int32 count, Int32 name[], Int32 addr[], Int32 word[]);
HXAPI_API void HxSetReg64(Int32 port, Int32 count, Int32 name[], Int32 addr[], Double real[]);
HXAPI_API void HxSetBit(Int32 port, Int32 count, Int32 name[], Int32 addr[], Int32 bit[], Bool onoff[]);
HXAPI_API void HxSetBit32(Int32 port, Int32 name, Int32 addr, Int32 bit, Bool onoff);

HXAPI_API double HxGetMacro(Int32 port, Int32 addr);
HXAPI_API void HxSetMacro(Int32 port, Int32 addr, double dVal);


HXAPI_API Int32 HxPushReg32(Int32 port, Int32 name, Int32 addr, Int32 word);
HXAPI_API Int32 HxPushReg64(Int32 port, Int32 name, Int32 addr, Double real);
HXAPI_API Int32 HxPushBit(Int32 port, Int32 name, Int32 addr, Int32 bit, Bool onoff);

HXAPI_API bool HxAddUpdateMap(Int32 port, Int32 count, Int32 name[], Int32 ch[], Int32 addr[]);
HXAPI_API bool HxRemoveUpdateMap(Int32 port, Int32 count, Int32 name[], Int32 ch[], Int32 addr[]);


// 확장 API

// X Register
HXAPI_API Bool HxGetXB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetXB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushXB(Int32 port, Int32 addr, Int32 bit, Bool onoff);

HXAPI_API Int32 HxGetXW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetXW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushXW(Int32 port, Int32 addr, Int32 word);

// Y Register
HXAPI_API Bool HxGetYB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetYB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushYB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetYW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetYW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushYW(Int32 port, Int32 addr, Int32 word);

// R Register
HXAPI_API Bool HxGetRB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetRB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushRB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetRW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetRW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushRW(Int32 port, Int32 addr, Int32 word);

// G Register
HXAPI_API Bool HxGetGB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetGB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushGB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetGW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetGW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushGW(Int32 port, Int32 addr, Int32 word);

// F Register
HXAPI_API Bool HxGetFB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetFB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetFW(Int32 port, Int32 addr, Bool direct = false);
//HXAPI_API void HxSetFW(Int32 port, Int32 addr, Bool onoff);

// S Register
HXAPI_API Double HxGetSVF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetSVF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushSVF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetSVW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetSVW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushSVW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Double HxGetSNF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetSNF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushSNF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetSNW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetSNW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushSNW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Double HxGetPPF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPPF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushPPF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetPPW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPPW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushPPW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Double HxGetPAF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPAF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushPAF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetPAW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPAW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushPAW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Double HxGetPIF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPIF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushPIF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetPIW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPIW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushPIW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Double HxGetPMF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPMF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushPMF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetPMW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPMW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushPMW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Double HxGetPSF(Int32 port, Int32 axis, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPSF(Int32 port, Int32 axis, Int32 addr, Double real);
HXAPI_API void HxPushPSF(Int32 port, Int32 axis, Int32 addr, Double real);
HXAPI_API Int32 HxGetPSW(Int32 port, Int32 axis, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPSW(Int32 port, Int32 axis, Int32 addr, Int32 word);
HXAPI_API void HxPushPSW(Int32 port, Int32 axis, Int32 addr, Int32 word);

HXAPI_API Double HxGetPUF(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPUF(Int32 port, Int32 addr, Double real);
HXAPI_API void HxPushPUF(Int32 port, Int32 addr, Double real);
HXAPI_API Int32 HxGetPUW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetPUW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushPUW(Int32 port, Int32 addr, Int32 word);

// T Register
HXAPI_API Bool HxGetTB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetTB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushTB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetTW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetTW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushTW(Int32 port, Int32 addr, Int32 word);

// C Register
HXAPI_API Bool HxGetCB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetCB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushCB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetCW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetCW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushCW(Int32 port, Int32 addr, Int32 word);

// D Register
HXAPI_API Bool HxGetDB(Int32 port, Int32 addr, Int32 bit, Bool direct = false);
HXAPI_API void HxSetDB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API void HxPushDB(Int32 port, Int32 addr, Int32 bit, Bool onoff);
HXAPI_API Int32 HxGetDW(Int32 port, Int32 addr, Bool direct = false);
HXAPI_API void HxSetDW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushDW(Int32 port, Int32 addr, Int32 word);

// Alarm Code / Count
HXAPI_API Int32 HxGetAlarmCode(Int32 port, Int32 code[]);
HXAPI_API void HxGetAlarmText(Int32 alarm, Char str[]);
HXAPI_API void HxLoadAlarmMsg(const char *path, const char *codec, int type);
HXAPI_API Int32 HxGetAlarmLog(Int32 port, Int32 code[], Int32 year[], Char month[], Char day[],
	Char hour[],Char min[],Char sec[]);

HXAPI_API void HxFileRename(const char* path, const char* rename);


HXAPI_API Int32 HxGetNcFileCount();
HXAPI_API Int32 HxGetFileList(void* list);		// 이건 안됨
HXAPI_API Bool HxGetNcFileStr(Int32 index, Char* str);

HXAPI_API Bool HxFileCommand(const Char* cmd, const Char* data);
HXAPI_API int HxFileCommandV2(Int32 port, Int32 type, Char org[], Char target[] = "");


// Nc List
HXAPI_API bool HxFtpConn(Int32 port, char *ip);
HXAPI_API int HxFtpChangeDirNc(Int32 port);
HXAPI_API int HxFtpChangeDirMacro(Int32 port);
HXAPI_API int HxFtpChangeDir(Int32 port, char *path);
HXAPI_API void HxFtpGetNcIndex(Int32 port, int index, char *name);
HXAPI_API void HxSetMainProg(Int32 port, char *name);
HXAPI_API void HxSetSubProg(Int32 port, char *name);
HXAPI_API void HxGetSysPath(Int32 port, char *path);
HXAPI_API void HxGetMainProg(Int32 port, char *name);
HXAPI_API void HxGetSubProg(Int32 port, char *name);

HXAPI_API Int32 HxFtpDownloadFile(Int32 port, const char* dir, const char* target, const char* name);
HXAPI_API Int32 HxFtpUploadFile(Int32 port, const char* dir, const char* target, const char* name);
HXAPI_API void HxFtpDeleteFile(Int32 port, const char* name);
HXAPI_API void HxFtpCreateFile(Int32 port, const char* name);

// 2019-11-11 sisong
HXAPI_API void HxSetNcPath(Int32 port, char *path);
HXAPI_API void HxGetNcPath(Int32 port, char *path);


// 2020-10-07 추가
HXAPI_API Int32 HxGetMemoryInfo(Int32 port, Int32 type);
HXAPI_API void HxSetBlockReadCount(Int32 port, Int32 count);
HXAPI_API void HxSetBlockReadType(Int32 port, Int32 type);
HXAPI_API Int32 HxGetBlockInfo(Int32 port, Int32 type, Char str[]);

// 


HXAPI_API void HxSetAlarmLanguage(int port, int lang);


// Get BuiltIn Alarm Log
HXAPI_API int HxLoadAlarmLog(int port, char path[]);
HXAPI_API bool HxGetAlarmLogData(int port, int idx, char code[], char msg[], char date[], char time[]);

#if 0

// Emergency Stop(Int32 port, System, z, Axis)
HXAPI_API Bool HxGetAxisEMG(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisEMG(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushAxisEMG(Int32 port, Int32 axis, Bool onoff);

// Ready
HXAPI_API Bool HxSignalSystemReady(Int32 port);
HXAPI_API Bool HxSignalChannelReady(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalAxisReady(Int32 port, Int32 axis);

// OT
HXAPI_API Bool HxGetPositiveOt(Int32 port, Int32 axis);
HXAPI_API void HxSetPositiveOt(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushPositiveOt(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Bool HxGetNegativeOt(Int32 port, Int32 axis);
HXAPI_API void HxSetNegativeOt(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushNegativeOt(Int32 port, Int32 axis, Bool onoff);

// MP Start
HXAPI_API void HxSetMpStart(Int32 port, Int32 channel, Bool onoff);
HXAPI_API void HxPushMpStart(Int32 port, Int32 channel, Bool onoff);
HXAPI_API Bool HxGetMpStart(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalMpStart(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalMpBusy(Int32 port, Int32 channel);

// MP Feed Hold
HXAPI_API Bool HxGetMpFeedHold(Int32 port, Int32 channel);
HXAPI_API void HxSetMpFeedHold(Int32 port, Int32 channel, Bool onoff);
HXAPI_API void HxPushMpFeedHold(Int32 port, Int32 channel, Bool onoff);
HXAPI_API Bool HxSignalMpFeedHold(Int32 port, Int32 channel);

// MP Single Block
HXAPI_API void HxSetMpSingleBlock(Int32 port, Int32 channel, Bool onoff);
HXAPI_API void HxPushMpSingleBlock(Int32 port, Int32 channel, Bool onoff);
HXAPI_API Bool HxGetMpSingleBlock(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalMpSingleBlock(Int32 port, Int32 channel);

// 보간 이송 Override
HXAPI_API void HxSetMpFeedOverridePP(Int32 port, Int32 channel, Int32 word);
HXAPI_API void HxPushMpFeedOverridePP(Int32 port, Int32 channel, Int32 word);
HXAPI_API Int32 HxGetMpFeedOverridePP(Int32 port, Int32 channel);

// 급속 이송 Override
HXAPI_API void HxSetMpFeedOverrideCP(Int32 port, Int32 channel, Int32 word);
HXAPI_API void HxPushMpFeedOverrideCP(Int32 port, Int32 channel, Int32 word);
HXAPI_API Int32 HxGetMpFeedOverrideCP(Int32 port, Int32 channel);

// Block Skip
HXAPI_API void HxSetSkip1(Int32 port, Int32 channel, Bool onoff);
HXAPI_API void HxPushSkip1(Int32 port, Int32 channel, Bool onoff);
HXAPI_API Bool HxGetSkip1(Int32 port, Int32 channel);
HXAPI_API void HxSetSkip2(Int32 port, Int32 channel, Bool onoff);
HXAPI_API void HxPushSkip2(Int32 port, Int32 channel, Bool onoff);
HXAPI_API Bool HxGetSkip2(Int32 port, Int32 channel);

// M Code
HXAPI_API void HxSetMCode(Int32 port, Int32 channel, Int32 word);
HXAPI_API void HxPushMCode(Int32 port, Int32 channel, Int32 word);
HXAPI_API Int32 HxGetMCode(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalMCode(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalMCodeEop(Int32 port, Int32 channel);
HXAPI_API Int32 HxGetMCodeNo(Int32 port, Int32 channel);
HXAPI_API Int32 HxGetMCodeData(Int32 port, Int32 channel);

// S Code
HXAPI_API void HxSetSCode(Int32 port, Int32 channel, Int32 word);
HXAPI_API void HxPushSCode(Int32 port, Int32 channel, Int32 word);
HXAPI_API Int32 HxGetSCode(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalSCode(Int32 port, Int32 channel);
HXAPI_API Bool HxSignalSCodeEop(Int32 port, Int32 channel);
HXAPI_API Int32 HxGetSCodeNo(Int32 port, Int32 channel);
HXAPI_API Int32 HxGetSCodeData(Int32 port, Int32 channel);

// MC Vel Mode
HXAPI_API Bool HxGetMcVelMode(Int32 port, Int32 axis);
HXAPI_API void HxSetMcVelMode(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushMcVelMode(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Bool HxSignalMcVelMode(Int32 port, Int32 axis);

// MC Pos Command
HXAPI_API void HxSetPosCommand(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushPosCommand(Int32 port, Int32 axis, Int32 word);
HXAPI_API Int32 HxGetPosCommand(Int32 port, Int32 axis);

// MC Feed Command
HXAPI_API void HxSetFeedCommand(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushFeedCommand(Int32 port, Int32 axis, Int32 word);
HXAPI_API Int32 HxGetFeedCommand(Int32 port, Int32 axis);

// MC Velocity Command
HXAPI_API void HxSetVelocityCommand(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushVelocityCommand(Int32 port, Int32 axis, Int32 word);
HXAPI_API Int32 HxGetVelocityCommand(Int32 port, Int32 axis);

// MC Torque Command
HXAPI_API void HxSetTorqueCommand(Int32 port, Int32 word);
HXAPI_API void HxPushTorqueCommand(Int32 port, Int32 word);
HXAPI_API Int32 HxGetTorqueCommand(Int32 port);

// MC Start
HXAPI_API void HxSetMcStart(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushMcStart(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Bool HxGetMcStart(Int32 port, Int32 axis);
HXAPI_API void HxSetMcStop(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushMcStop(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Bool HxGetMcStop(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalMcStart(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalMcBusy(Int32 port, Int32 axis);

// MC Pos Abs/Inc
HXAPI_API void HxSetMcPosAbsInc(Int32 port, Int32 axis, Bool isabs);
HXAPI_API void HxPushMcPosAbsInc(Int32 port, Int32 axis, Bool isabs);
HXAPI_API Bool HxGetMcPosAbsInc(Int32 port, Int32 axis);

// MC Pos Direction
HXAPI_API void HxSetMcPosDir(Int32 port, Int32 axis, Bool dir);
HXAPI_API void HxPushMcPosDir(Int32 port, Int32 axis, Bool dir);
HXAPI_API Bool HxGetMcPosDir(Int32 port, Int32 axis);

// MC Feed Override
HXAPI_API Int32 HxGetMcFeedOverride(Int32 port, Int32 axis);
HXAPI_API void HxSetMcFeedOverride(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushMcFeedOverride(Int32 port, Int32 axis, Int32 word);

// MC CCM Mode , MC_G_PCCM, G403.00 ~ 31
HXAPI_API Bool HxGetMcCcmMode(Int32 port, Int32 axis);
HXAPI_API void HxSetMcCcmMode(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushMcCcmMode(Int32 port, Int32 axis, Bool onoff);

// Axis 원점 복귀 완료 신호, TMC_F_RF, F420.00 ~ 31
HXAPI_API Bool HxSignalRefFinish(Int32 port, Int32 axis);

// Axis 원점 복귀 감속 신호, TMC_G_RDEC, G422.00 ~ 31
HXAPI_API Bool HxGetStopSenor(Int32 port, Int32 axis);
HXAPI_API void HxSetStopSenor(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushStopSenor(Int32 port, Int32 axis, Bool onoff);

// Axis 별 원점 위치 도착 신호
HXAPI_API Bool HxSignalRefPosition1(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalRefPosition2(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalRefPosition3(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalRefPosition4(Int32 port, Int32 axis);

// Axis별 서보 Reset 신호
HXAPI_API void HxSetServoReset(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushServoReset(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Bool HxGetServoReset(Int32 port, Int32 axis);

// Axis별 서보 Off 신호
HXAPI_API void HxSetServoOff(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushServoOff(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Bool HxGetServoOff(Int32 port, Int32 axis);

// 동작상태
// (Int32 port, +) 방향 이동 확인 신호
HXAPI_API Bool HxSignalMovePlus(Int32 port, Int32 axis);
// (Int32 port, -) 방향 이동 확인 신호
HXAPI_API Bool HxSignalMoveMinus(Int32 port, Int32 axis);
// In-Position 확인 신호
HXAPI_API Bool HxSignalInposition(Int32 port, Int32 axis);
// (Int32 port, 0) 속도 도달 확인 신호
HXAPI_API Bool HxSignalZeroFeed(Int32 port, Int32 axis);
// 지령 속도 도달 확인 신호
HXAPI_API Bool HxSignalCommandFeed(Int32 port, Int32 axis);

// ========= 파라미터(P Map) =========

// 위치 결정 모드 가감속(MP G00, POS, JOG, REF)
HXAPI_API Int32 HxGetPosAxisAccel(Int32 port, Int32 axis);
HXAPI_API void HxSetPosAxisAccel(Int32 port, Int32 axis, Int32 msec);
HXAPI_API void HxPushPosAxisAccel(Int32 port, Int32 axis, Int32 msec);
HXAPI_API Int32 HxGetPosAxisDecel(Int32 port, Int32 axis);
HXAPI_API void HxSetPosAxisDecel(Int32 port, Int32 axis, Int32 msec);
HXAPI_API void HxPushPosAxisDecel(Int32 port, Int32 axis, Int32 msec);

// Han Mode 가감속
HXAPI_API Int32 HxGetHanAxisAccDec(Int32 port, Int32 axis);
HXAPI_API void HxSetHanAxisAccDec(Int32 port, Int32 axis, Int32 msec);
HXAPI_API void HxPushHanAxisAccDec(Int32 port, Int32 axis, Int32 msec);

// Han Mode 가감속 타입
// type - 0:직선, 1:S자, 2:지수
HXAPI_API Int32 HxGetHanAxisAccDecType(Int32 port, Int32 axis);
HXAPI_API void HxSetHanAxisAccDecType(Int32 port, Int32 axis, Int32 type);
HXAPI_API void HxPushHanAxisAccDecType(Int32 port, Int32 axis, Int32 type);

// Home Parameter(P REG)
// 원점복귀 급속 속도
HXAPI_API Int32 HxGetHomeFastFeed(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeFastFeed(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushHomeFastFeed(Int32 port, Int32 axis, Int32 word);

// 원점 복귀 1차 감속 속도
HXAPI_API Int32 HxGetHomeFirstFeed(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeFirstFeed(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushHomeFirstFeed(Int32 port, Int32 axis, Int32 word);

// 원점 복귀 2차 감속 속도
HXAPI_API Int32 HxGetHomeSecondFeed(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeSecondFeed(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushHomeSecondFeed(Int32 port, Int32 axis, Int32 word);

// 원점 위치 Shift 량
HXAPI_API Int32 HxGetHomeShiftDist(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeShiftDist(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushHomeShiftDist(Int32 port, Int32 axis, Int32 word);

// 원점 위치 Shift 이송 속도
HXAPI_API Int32 HxGetHomeShiftFeed(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeShiftFeed(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushHomeShiftFeed(Int32 port, Int32 axis, Int32 word);


// 감속 센서 사용 여부(센서)
HXAPI_API Bool HxGetHomeUseStopSensor(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeUseStopSensor(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushHomeUseStopSensor(Int32 port, Int32 axis, Bool onoff);

// 원점 신호 사용 여부(C상)
HXAPI_API Bool HxGetHomeUseOriginSensor(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeUseOriginSensor(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushHomeUseOriginSensor(Int32 port, Int32 axis, Bool onoff);

// 각 축 OT 검출 후, 재시도 기능 사용 여부
HXAPI_API Bool HxGetHomeUseRetry(Int32 port, Int32 axis);
HXAPI_API void HxSetHomeUseRetry(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushHomeUseRetry(Int32 port, Int32 axis, Bool onoff);

// 원점 복귀 시작
HXAPI_API void HxHomeStart(Int32 port, Int32 axis, Int32 fastVel, Int32 velFirst, Int32 velSecond, Int32 shiftPos, Int32 shiftFeed, Bool useStopSensor, Bool useOriginSenro, Bool retry);

// Han 모드 시작
HXAPI_API void HxStartHanMode(Int32 port, Int32 axis);
HXAPI_API void HxStopHanMode(Int32 port, Int32 axis);

// 파라미터(P Register)
HXAPI_API Int32 HxGetParamW(Int32 port, Int32 param);
HXAPI_API void HxSetParamW(Int32 port, Int32 param, Int32 dword);
HXAPI_API void HxPushParamW(Int32 port, Int32 param, Int32 dword);

HXAPI_API Bool HxGetParamB(Int32 port, Int32 param, Int32 bit);
HXAPI_API void HxSetParamB(Int32 port, Int32 param, Int32 bit, Bool onoff);
HXAPI_API void HxPushParamB(Int32 port, Int32 param, Int32 bit, Bool onoff);

//[B]시뮬레이션 모드 설정(0:X, 1:0)
HXAPI_API Bool HxGetSystemSimulation(Int32 port);
HXAPI_API void HxSetSystemSimulation(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemSimulation(Int32 port, Bool onoff);

// [B]각 축 시뮬레이션 모드 설정(0:X, 1:0)
HXAPI_API Bool HxGetAxisSimulation(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisSimulation(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushAxisSimulation(Int32 port, Int32 axis, Bool onoff);

// [B]설정 단위계(0:Metric, 1:Inch)
HXAPI_API Bool HxGetAxisSimulation(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisSimulation(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushAxisSimulation(Int32 port, Int32 axis, Bool onoff);

// [B]설정 단위계(0:Metric, 1:Inch)
HXAPI_API Bool HxGetSystemUnit(Int32 port);
HXAPI_API void HxSetSystemUnit(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemUnit(Int32 port, Bool onoff);

// [W]길이 단위(PU) 설정
HXAPI_API Int32 HxGetSystemLengthUnit(Int32 port);
HXAPI_API void HxSetSystemLengthUnit(Int32 port, Int32 word);
HXAPI_API void HxPushSystemLengthUnit(Int32 port, Int32 word);

// [W]속도 단위(PU) 설정
HXAPI_API Int32 HxGetSystemFeedUnit(Int32 port);
HXAPI_API void HxSetSystemFeedUnit(Int32 port, Int32 word);
HXAPI_API void HxPushSystemFeedUnit(Int32 port, Int32 word);

// [W]보간 주기(msec)
HXAPI_API Int32 HxGetSystemIpoTime(Int32 port);
HXAPI_API void HxSetSystemIpoTime(Int32 port, Int32 word);
HXAPI_API void HxPushSystemIpoTime(Int32 port, Int32 word);

// [W]위치 제어-H 주기(msec)
HXAPI_API Int32 HxGetSystemPosHTime(Int32 port);
HXAPI_API void HxSetSystemPosHTime(Int32 port, Int32 word);
HXAPI_API void HxPushSystemPosHTime(Int32 port, Int32 word);

// [W]위치 제어-N 주기(msec)
HXAPI_API Int32 HxGetSystemPosNTime(Int32 port);
HXAPI_API void HxSetSystemPosNTime(Int32 port, Int32 word);
HXAPI_API void HxPushSystemPosNTime(Int32 port, Int32 word);

// [W]PLC-N 주기(msec)
HXAPI_API Int32 HxGetSystemPlcNTime(Int32 port);
HXAPI_API void HxSetSystemPlcNTime(Int32 port, Int32 word);
HXAPI_API void HxPushSystemPlcNTime(Int32 port, Int32 word);

// [W]Fieldbus 통신 주기(msec)
HXAPI_API Int32 HxGetSystemFieldbusTime(Int32 port);
HXAPI_API void HxSetSystemFieldbusTime(Int32 port, Int32 word);
HXAPI_API void HxPushSystemFieldbusTime(Int32 port, Int32 word);

// Sample Time Preset
HXAPI_API void HxSetSystemSamplingTime(Int32 port, Int32 posTime);

// 상태정보(S Register)
HXAPI_API Int32 HxGetStatusW(Int32 port, Int32 param);
HXAPI_API Bool HxGetStatusB(Int32 port, Int32 param, Int32 bit);

// 이벤트 로그(E Register)
HXAPI_API Int32 HxGetEventW(Int32 port, Int32 addr);
HXAPI_API void HxSetEventW(Int32 port, Int32 addr, Int32 word);
HXAPI_API void HxPushEventW(Int32 port, Int32 addr, Int32 word);

HXAPI_API Int32 HxGetEventB(Int32 port, Int32 addr, Int32 bit);
HXAPI_API void HxSetEventB(Int32 port, Int32 addr, Int32 bit, Int32 onoff);
HXAPI_API void HxPushEventB(Int32 port, Int32 addr, Int32 bit, Int32 onoff);

HXAPI_API Bool HxGetEvent(Int32 port, Int32* code, Int32* data1, Int32* data2, Int32* data3, Int32* data4);

HXAPI_API Int32 HxGetMpProgram(Int32 port, Int32 channel);
HXAPI_API void HxSetMpProgram(Int32 port, Int32 channel, Int32 program);
HXAPI_API void HxPushMpProgram(Int32 port, Int32 channel, Int32 program);

HXAPI_API void HxDownloadFile(Int32 port, const char* dir, const char* name);
HXAPI_API void HxUploadFile(Int32 port, const char* dir, const char* name);
HXAPI_API void HxDeleteFile(Int32 port, const char* name);

// Motion API

// MP Program Start
HXAPI_API Bool HxStartMpProgram(Int32 port, Int32 channel, Int32 program);

// Jog Start/Stop
HXAPI_API Int32 HxJogStart(Int32 port, Int32 axis, Int32 feed, Bool direction, Int32 accel, Int32 decel);
HXAPI_API Int32 HxJogStop(Int32 port, Int32 axis);

// Move Start/Stop
HXAPI_API Int32 HxMoveStart(Int32 port, Int32 axis, Int32 feed, Int32 position, Int32 accel, Int32 decel);
HXAPI_API Int32 HxMoveStartInc(Int32 port, Int32 axis, Int32 feed, Int32 position, Int32 accel, Int32 decel);

HXAPI_API Bool HxMDI(Int32 port, Int32 channel, char* mdiData);
HXAPI_API Int32 HxGetExeBlockNo(Int32 port, Int32 channel);
#endif

// ----------------------------------- 완료 항목 -------------------------------

// System Run
HXAPI_API Bool HxGetSystemRun(Int32 port);
HXAPI_API void HxSetSystemRun(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemRun(Int32 port, Bool onoff);
HXAPI_API Bool HxSignalSystemRun(Int32 port);
HXAPI_API Bool HxSignalSystemAxisRun(Int32 port);
HXAPI_API Bool HxSignalSystemEcatOp(Int32 port);
HXAPI_API Bool HxSignalAxisEcatAbsOK(Int32 port, Int32 axis);

// Jog Mode // 완료
HXAPI_API Bool HxGetSystemJogMode(Int32 port);
HXAPI_API void HxSetSystemJogMode(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemJogMode(Int32 port, Bool onoff);
HXAPI_API Bool HxSignalSystemJogMode(Int32 port);

// Step Mode // 완료
HXAPI_API Bool HxGetSystemStepMode(Int32 port);
HXAPI_API void HxSetSystemStepMode(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemStepMode(Int32 port, Bool onoff);
HXAPI_API Bool HxSignalSystemStepMode(Int32 port);

// Mpg Mode // 완료
HXAPI_API Bool HxGetSystemMpgMode(Int32 port);
HXAPI_API void HxSetSystemMpgMode(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemMpgMode(Int32 port, Bool onoff);
HXAPI_API Bool HxSignalSystemMpgMode(Int32 port);

// Zrn Mode // 완료
HXAPI_API Bool HxGetSystemZrnMode(Int32 port);
HXAPI_API void HxSetSystemZrnMode(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemZrnMode(Int32 port, Bool onoff);
HXAPI_API Bool HxSignalSystemZrnMode(Int32 port);

// Auto Mode
HXAPI_API void HxSetSystemAutoMode(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemAutoMode(Int32 port, Bool onoff);
HXAPI_API Bool HxGetSystemAutoMode(Int32 port);
HXAPI_API Bool HxSignalSystemAutoMode(Int32 port);

HXAPI_API void HxSetSystemCycleStart(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemCycleStart(Int32 port, Bool onoff);
HXAPI_API Bool HxGetSystemCycleStart(Int32 port);
// 자동 운전 중 - Feed Hold 포함
HXAPI_API Bool HxSignalSystemCycleStart(Int32 port);
// Feed Hold 중
HXAPI_API Bool HxSignalSystemFeedHold(Int32 port);
// 자동 운전 중 - Feed Hold 제외
HXAPI_API Bool HxSignalSystemOperating(Int32 port);
HXAPI_API Bool HxSignalSystemScheduleCycleStart(Int32 port);

HXAPI_API Bool HxGetSystemProgramChange(Int32 port);
HXAPI_API void HxSetSystemProgramChange(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemProgramChange(Int32 port, Bool onoff);
HXAPI_API Bool HxSignalSystemProgramChange(Int32 port);

HXAPI_API Int32 HxGetSystemProgramChangeNumber(Int32 port);
HXAPI_API void HxSetSystemProgramChangeNumber(Int32 port, Int32 word);
HXAPI_API void HxPushSystemProgramChange(Int32 port, Int32 word);


// Jog Start
HXAPI_API Bool HxGetAxisJogPlusStart(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisJogPlusStart(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushAxisJogPlusStart(Int32 port, Int32 axis, Bool onoff);

HXAPI_API Bool HxGetAxisJogMinusStart(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisJogMinusStart(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushAxisJogMinusStart(Int32 port, Int32 axis, Bool onoff);

enum{JOG_PLUS = 0, JOG_MINUS}; // dir
HXAPI_API Bool HxGetAxisJogStart(Int32 port, Int32 axis, Int32 dir);
HXAPI_API void HxSetAxisJogStart(Int32 port, Int32 axis, Int32 dir, Double feed, Double accdec, Bool onoff);
HXAPI_API void HxPushAxisJogStart(Int32 port, Int32 axis, Int32 dir, Double feed, Double accdec, Bool onoff);


// NC 모드 보조 설정
HXAPI_API Bool HxGetSystemSingleBlock(Int32 port);
HXAPI_API void HxSetSystemSingleBlock(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemSingleBlock(Int32 port, Bool onoff);

// Optional Block Skip
HXAPI_API Bool HxGetSystemOptionalBlockSkip(Int32 port);
HXAPI_API void HxSetSystemOptionalBlockSkip(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemOptionalBlockSkip(Int32 port, Bool onoff);

// Dry Run
HXAPI_API Bool HxGetSystemDryRun(Int32 port);
HXAPI_API void HxSetSystemDryRun(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemDryRun(Int32 port, Bool onoff);

// Manual Absolute 모드
HXAPI_API Bool HxGetSystemManualAbsolute(Int32 port);
HXAPI_API void HxSetSystemManualAbsolute(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemManualAbsolute(Int32 port, Bool onoff);

// Aux Lock, M/S/T Code Lock
HXAPI_API Bool HxGetSystemAuxLock(Int32 port);
HXAPI_API void HxSetSystemAuxLock(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemAuxLock(Int32 port, Bool onoff);

// 전축 Machine Lock
HXAPI_API Bool HxGetSystemMachineLock(Int32 port);
HXAPI_API void HxSetSystemMachineLock(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemMachineLock(Int32 port, Bool onoff);

// 각축 Machine Lock
HXAPI_API Bool HxGetAxisMachineLock(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisMachineLock(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushAxisMachineLock(Int32 port, Int32 axis, Bool onoff);

// 다단 Optional Block Skip
// number
enum{ BLOCKSKIP1 = 0, BLOCKSKIP2, BLOCKSKIP3, BLOCKSKIP4, BLOCKSKIP5, BLOCKSKIP6, BLOCKSKIP7, BLOCKSKIP8, BLOCKSKIP9 };
HXAPI_API Bool HxGetSystemMultiOptionalBlockSkip(Int32 port, Int32 number);
HXAPI_API void HxSetSystemMultiOptionalBlockSkip(Int32 port, Int32 number, Bool onoff);
HXAPI_API void HxPushSystemMultiOptionalBlockSkip(Int32 port, Int32 number, Bool onoff);

// Override Cancel
HXAPI_API Bool HxGetSystemOverrideCancel(Int32 port);
HXAPI_API void HxSetSystemOverrideCancel(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemOverrideCancel(Int32 port, Bool onoff);

// Key Lock, 메모리 보호 키/편집 보호
HXAPI_API Bool HxGetSystemKeyLock(Int32 port);
HXAPI_API void HxSetSystemKeyLock(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemKeyLock(Int32 port, Bool onoff);

// 다단계 SKIP 신호
// number
//enum{ SKIP1 = 0, SKIP2, SKIP3, SKIP4 };
HXAPI_API Bool HxGetSystemMultiSkip(Int32 port, Int32 number);
HXAPI_API void HxSetSystemMultiSkip(Int32 port, Int32 number, Bool onoff);
HXAPI_API void HxPushSystemMultiSkip(Int32 port, Int32 number, Bool onoff);

HXAPI_API Bool HxGetSystemReset(Int32 port);
HXAPI_API void HxSetSystemReset(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemReset(Int32 port, Bool onoff);
HXAPI_API void HxSignalSystemReset(Int32 port, Bool onoff);
HXAPI_API void HxSignalSystemResetMdi(Int32 port, Bool onoff);

HXAPI_API Bool HxGetAxisReset(Int32 port);
HXAPI_API void HxSetAxisReset(Int32 port, Bool onoff);
HXAPI_API void HxPushAxisReset(Int32 port, Bool onoff);

HXAPI_API Bool HxGetSystemEmg(Int32 port);
HXAPI_API void HxSetSystemEmg(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemEmg(Int32 port, Bool onoff);

HXAPI_API Bool HxGetSystemPowerOff(Int32 port);
HXAPI_API void HxSetSystemPowerOff(Int32 port, Bool onoff);
HXAPI_API void HxPushSystemPowerOff(Int32 port, Bool onoff);

HXAPI_API Double HxGetAxisManualFeed(Int32 port, Int32 index);
HXAPI_API void HxSetAxisManualFeed(Int32 port, Int32 index, Double real);
HXAPI_API void HxPushAxisManualFeed(Int32 port, Int32 index, Double real);

HXAPI_API void HxSetAxisJogStop(Int32 port, Int32 axis);
HXAPI_API void HxPushAxisJogStop(Int32 port, Int32 axis);

HXAPI_API void HxSetAxisMoveStart(Int32 port, Int32 axis, Int32 position, Int32 feed, Double accdec);
HXAPI_API void HxPushAxisMoveStart(Int32 port, Int32 axis, Int32 position, Int32 feed, Double accdec);

HXAPI_API void HxSetAxisMoveStop(Int32 port, Int32 axis);
HXAPI_API void HxPushAxisMoveStop(Int32 port, Int32 axis);

HXAPI_API void HxSetPosAxisUse(Int32 port, Int32 axis, Bool onoff);
HXAPI_API void HxPushPosAxisUse(Int32 port, Int32 axis, Bool onoff);
HXAPI_API Int32 HxGetPlcAxisType(Int32 port, Int32 axis);
HXAPI_API void HxSetPlcAxisType(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushPlcAxisType(Int32 port, Int32 axis, Int32 word);
HXAPI_API Double HxGetPlcControlUnit(Int32 port, Int32 axis);
HXAPI_API void HxSetPlcControlUnit(Int32 port, Int32 axis, Double real);
HXAPI_API void HxPushPlcControlUnit(Int32 port, Int32 axis, Double real);

HXAPI_API void HxSelectMacro(Int32 port, Int32 programNumber);
HXAPI_API Int32 HxGetMacroNumber(Int32 port);
HXAPI_API void HxSetMacroNumber(Int32 port, Int32 programNumber);
HXAPI_API void HxPushMacroNumber(Int32 port, Int32 programNumber);
HXAPI_API Bool HxGetMacroChange(Int32 port);
HXAPI_API void HxSetMacroChange(Int32 port, Bool onoff);
HXAPI_API void HxPushMacroChange(Int32 port, Bool onoff);

HXAPI_API Int32 HxDownloadFile(Int32 port, const char dir[], const char target[], const char name[]);
HXAPI_API Int32 HxUploadFile(Int32 port, const char dir[], const char target[], const char name[]);
HXAPI_API void HxDeleteFile(Int32 port, const char name[]);
HXAPI_API void HxCreateFile(Int32 port, const char path[]);

// --------------------- Axis -----------------------------
HXAPI_API Int32 HxGetAxisType(Int32 port, Int32 axis);
HXAPI_API void HxSetAxisType(Int32 port, Int32 axis, Int32 word);
HXAPI_API void HxPushAxisType(Int32 port, Int32 axis, Int32 word);

// Inposition
HXAPI_API Bool HxSignalAxisMoving(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalAxisPlusMoving(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalAxisMinusMoving(Int32 port, Int32 axis);
HXAPI_API Bool HxSignalAxisInposition(Int32 port, Int32 axis);

// Axis Position
HXAPI_API Double HxGetAxisMachinePosition(Int32 port, Int32 axis);
HXAPI_API Double HxGetAxisWorkPosition(Int32 port, Int32 axis);
HXAPI_API Double HxGetAxisRemainDistance(Int32 port, Int32 axis);



//add hyunwoo
//HXAPI_API Int32 HXHoming(Int32 port, Int32 nAxis, Double  dFeed, Double dDecel1st, Double dDecel2nd, Double dAcce
//	, Int32 bUseArbitraryOrig, Int32 bUseDog , Int32 nDirection );


HXAPI_API Int32 HXGetHomeStatus(Int32 port, Int32 nAxis);

HXAPI_API Int32 HxTest();

HXAPI_API Int32 HxTest2(char (&aaa)[50][50]);

HXAPI_API Int32 HxTest3(int &aab);

HXAPI_API Int32 HxTest4(char* aa);


// 2021-12-15 추가
HXAPI_API Int32 HxGetMCType(Int32 port);

// 2023-04-05 추가
HXAPI_API bool HxGetSysReady(Int32 port);


#ifdef __cplusplus
}
#endif


#endif /* _HXAPI20_H_ */
