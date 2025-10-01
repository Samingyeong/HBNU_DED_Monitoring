#pragma once

typedef char				S08;      // 1  byte : -128           -> 127
typedef unsigned char		U08;     // 1  byte : 0              -> 255
typedef short				S16;      // 2  byte : -32,768        -> 32,767
typedef unsigned short		U16;     // 2  byte : 0              -> 65,536
typedef long				S32;       // 4  byte : -2,147,483,648 -> 2,147,483,647
typedef unsigned long		U32;      // 4  byte : 0              -> 4,294,967,295
//typedef float				F32;      // 4  byte : 1.2e-38        -> 3.4e38
typedef double				F64;       // 8  byte : 2.2e-308       -> 1.8e308
typedef int					B32;       // 4  byte : -2,147,483,648 -> 2,147,483,647

#define MAP_MAX_PS      800         // PS MAP


enum eAxis {
	Axis1, Axis2, Axis3, Axis4, Axis5, Axis6, Axis7, Axis8,
	Axis9, Axis10, Axis11, Axis12, Axis13, Axis14, Axis15, Axis16,
	Axis17, Axis18, Axis19, Axis20, Axis21, Axis22, Axis23, Axis24,
	Axis25, Axis26, Axis27, Axis28, Axis29, Axis30, Axis31, Axis32
};

//------------------------------
// system parameter - G-F 
//------------------------------
enum HXsystemGF {
	SG_PLCRUN	=0,// PLC가 정상적인 동작을 수행됨을 알려줌 
	SF_MA = 0,
	SF_SA = 0,
	SG_MODE = 1,
	SF_MODE = 1,
	SG_SUB_MODE = 2,
	SG_AXIS_MACHINELOCK = 3,
	SG_MULTISKIP = 4,				// Key Lock, 메모리 보호, 키/편집 보호
	SG_KEYLOCK = 5,				// Key Lock, 메모리 보호, 키/편집 보호
	SG_BDT = 6,				// 다단 Optional Block Skip
	SF_PROGRAM_SIGNAL = 7,
	SG_RESET = 8,
	SF_RESET = 8,
	SG_ST = 9,
	SF_ST = 8,
	SG_PROGRAM_NUMBER = 10,
	SG_JOGPMOVE = 11,		// + 방향 JOG 이송 (32축)
	SG_JOGNMOVE = 12,		// - 방향 JOG 이송 (32축) 
	SG_RAPIDJOG = 13,
	SG_MANUALFEED = 14,		// jog feed ( 1~32) 
	SG_STEPDISTANCE = 15,	// step distance  ( 1~32) 
	SG_1MPGAXIS = 17,		// 1MPG 에 의한 수동 이송 축(1 ~3)- 2MPG : 18, - 3MPG :19
	SG_1MPGINTERRUPTAXIS = 21,// 1MPG interrupt 에 의한 수동 이송 축(1 ~3), 22, 23
	
	SG_HOMEDOG_SWITCH = 25,	// 

	SG_OVERTRAVEL_PMOVE = 32, 
	SG_OVERTRAVE_NPMOVE = 33,
	SG_RAPID_OVERRIDE = 36,
	SG_FEED_OVERRIDE = 37,	// FEED OVERRIDE (37.00~ 30.04, 32가지 ) 
	SG_SPINDLE_OVERRIDE = 38, 
	SG_INTERLOCK_ALL = 39,
	SG_INTERLOCK_P = 40,
	SG_INTERLOCK_N = 41,
	SG_SERVO_CLOSE = 43, // 해당 축을 서보 off시키고, 모든 지령 및 알람을 무시, 단 엔코더 피드백은 이루어짐 
	SG_SERVO_OFF	= 44, // 해당 축을 서보 Off시킴 (SA신호[F0.01]는 유지됨 )
	SG_MAINSPINDLE = 52,	// 메인 스핀 들 선택 
	SG_MAIN_ZAXIS = 52,	// 메인 Z축 선택 
	SG_SPINDLE_GEAR = 64,	// 스핀들 기어 선택 
	SG_TWINTABLE	= 103,	// 트윈 테이블 신호( twin table )
	SG_PLCMOVESIGN = 120,
	SG_PLCMOVECANCEL = 121,
	SG_PLCVELMODE = 123,	// PLC 축 속도 지정 모드 ON/OFF (124 : 속도)
	SG_PLCMOVEDISTANCE = 131,
	SG_PLCMOVEFEED = 132,

	SF_SERVOREADY = 28,
	SF_MAINSPINDLE = 33,	//  메인 스핀들 확인 
	SF_MAIN_ZAXIS = 34,		//  메인 Z축 확인 
	SF_ECAT_ABS_OK = 93,		//  절대치 엔코더 EtherCAT 수신 완료 신호
};
enum HXstateHome {	
	HOME_NONE,
	HOME_RUNNING,			// 원점 복귀 중 
	HOME_FIN,				// 원점 복귀 완료 상태 신호 
	HOME_ZERORETURN_1,		// 제1 원점 복귀 구간 내 신호 
	HOME_ZERORETURN_2,		// 제2 원점 복귀 구간 내 신호 
	HOME_ZERORETURN_3,		// 제3 원점 복귀 구간 내 신호 
	HOME_ZERORETURN_4		// 제4 원점 복귀 구간 내 신호 
};

//----------------------
// no 1.
enum HXGF_Ready{
	PLCRUN,		//G0.00 PLC가 정상적인 동작을 수행됨을 알려줌
	MA,			//F0.00 CNC 계통에 이상이 없는 경우 ON
	SA,			//F0.01 서보/스핀들 계통에 이상이 없는 경우 ON
	iFABSOK//, 	// F93.00~F93.1f	ECAT으로 절대치엔코더 수신완료 신호 ( n Axis)
		
};
// no 2.
enum HXGF_ncmode {
	AUTO = 0, 	MDI = 1,	DNC = 2,	ZRN = 3,	JOG = 4,
	MPG = 5,	STEP = 6,	EDIT = 7,	AUTOL = 10, 	MDIL = 11,
	DNCL = 12,	ZRNL = 13,	JOGL = 14,	MPGL = 15,	STEPL = 16, EDITL = 17
};
// no 3.
enum HXGF_NCmodeSub{
	SINGLEBLOCK				,//SBK	g2.00 single block
	OPTIONALBLOCKSTOP		,//OPS	g2.01 optional block stop
	DRYRUN					,//DRN	G2.02 dry run
	MANUALABSOLUTE			,//MABS	G2.03 Manual Absolute 모드
	MULTI_OPTIONALBLOCKSTOP	,//AUXL	G2.04 다단Optional Block Skip
	MACHINELOCK_ALL			,//MLK	G2.06 전축Machine Lock
	MACHINELOCK_EACH		,//MLK1 ~ MLK32	G3.00~G3.1F 각 축별Machine Lock
	MST_CODELOCK			,//BDT1 ~ BDT9	G6.00 ~ G6.08 M/S/T Code Lock (Auxiliary Function Lock : AFL)
	OVERRIDECANCEL			,//OVC	G2.07 Override Cancel
	PROTECT_MEMORY			,//KLOCK	G5.00 메모리보호 키/편집 보호
	MULTI_SKIP				,//SKIP1 ~ SKIP4	G4.00~G4.03 다단계 SKIP신호
};
enum MST_CODELOCK{
	BDT1 = 0, BDT2, BDT3, BDT4, BDT5, BDT6, BDT7, BDT8, BDT9
};
enum MULTI_SKIP{
	SKIP1 = 0, SKIP2, SKIP3, SKIP4
};
// no 4.
enum HXGF_Reset{
	ERS = 0,	//G8.00 외부 리셋 지령 신호 (NC를 초기화 합니다)
	SVRS,	//G8.01 서보 Alram Reset.
	ESP,	//G8.02 비상정지 신호
	PWOFF,	//G8.08 POWER OFF 신호
	RST,	//F6.00 외부 리셋 상태 신호
	RSTK	//F6.01	MDI 기판의 Reset 키 ON 상태
};

// no 5.
enum HXGF_NCRun{
	ST = 0		,//G9.00 Cycle Start
	SP			,//G9.02 Feed Hold (Feed Stop)
	SCST		,//F7.00 스케줄링 기능 Cycle Start신호
	PRGCH		,//G9.08 프로그램 변경 지령 신호
	PRGNO		,//G10	 변경할 프로그램 번호
	PRGCHFIN	,//F7.08 프로그램 변경 완료 신호
};
// no 6.
enum HXGF_NCstate{
	STL = 0,//F8.00	자동 운전 기동 중
	SPL	,//F8.01	자동 운전 휴지 중
	OP	,//F8.02	자동 운전 중
};
// no 7.
enum HXGF_ManualMode{
	PJ1		 = 0,// ~ PJ32	G11.00~	G11.1F	+ 방향 JOG 이송(32축)
	NJ1			,// ~ NJ32	G12.00~	G12.1F	- 방향 JOG 이송(32축)
	RT			,//G13.04	Rapid JOG 이송 ON/OFF
	MANF0		,// ~ MANF4	G14.00~	G14.04	수동 이송 속도 Table Index (파라메터를 참조)
	SDIST0		,//~ SDIST4	G15.00~	G15.04	Step 이송 거리Table Index (파라메터를 참조)
	MP1			,//G13.00	MPG Multiplier (X1, X10, X100)
	MP2			,//G13.01			
	MPGA1		,// ~ MPGA32	G17.00~G17.1F	제 1 MPG에 의한 수동 이송 축 선택
	MPGB1		,// ~ MPGB32	G18.00~	G18.1F	제 2 MPG에 의한 수동 이송 축 선택
	MPGC1		,// ~ MPGC32	G19.00~	G19.1F	제 3 MPG에 의한 수동 이송 축 선택
	MPGINTA1	,//~MPGINTA32	G21.00~	G21.1F	제 1 MPG Interrupt에 의한 수동이송 축 선택
	MPGINTB1	,//~MPGINTB32	G22.00~G22.1F	제 2 MPG Interrupt에 의한 수동이송 축 선택
	MPGINTC1	,//~MPGINTC32	G23.00~	G23.1F	제 3 MPG Interrupt에 의한 수동이송 축 선택
};
// no 8.
enum HXGF_Home{
	DEC1	,//~Dec-32		G25.00~	G25.1F		원점복귀 감속 Dog 스위치 인식 신호
	ZR1		,//~ ZR32		F16.00~F16.1F	원점 복귀(Zero Return)  중
	ZF1		,//~ ZF32		F17.00~F17.1F	원점 복귀 완료 상태 신호(원점 복귀 수행 후 “High”상태로 유지)
	ZP1		,//~ ZP32		F18.00~F18.1F	제1원점복귀 구간 내 신호
	ZP201	,//~ ZP232		F19.00~F19.1F		제 2원점복귀 구간 내 신호
	ZP301	,// ~ ZP332		F20.00~F20.1F		제 3원점복귀 구간 내 신호
	ZP401	,// ~ ZP432		F21.00~	F21.1F	제 4원점복귀 구간 내 신호
	ZST1	,// ~ ZST32		G28.00~	G28.1F		제 1원점복귀 시작신호
	ZST201	,// ~ ZST232	G29.00~	G29.1F			제 2원점복귀 시작신호
	ZST301	,// ~ ZST332	G30.00~	G30.1F		제 3원점복귀 시작신호
	ZST401	,// ~ ZST432	G31.00~	G31.1F			제 4원점복귀 시작신호
	ZDSP1	// ~ ZDSP32		F22.00~	F22.1F원점 복귀 금지 영역 신호
};
// no 9.
enum HXGF_ExternalSignal{
	POT			,//G32.00~	G32.1F			+방향에 Over Travel 신호		
	NOT			,//G33.00~	G33.1F			-방향에 Over Travel 신호				
	PIT			,//G39.00					+방향에 대해 모든 축에 대해Interlock
	PIT1		,//~ PIT32	G40.00~G40.1F	+방향에 대해 축별 Interlock			
	NIT			,//G39.01					-방향에 대해 모든 축에 대해Interlock
	NIT1		,//~NIT32	G41.00~G41.1F	-방향에 대해 축별 Interlock			
	CLOFF1		,//~	G43.00~				해당 축을 서보 OFF시키고 모든 지령 및 알람을 무시합니다. 단, 엔코더 Feed Back은 이루어집니다.
	SVOFF1		,//~	G44.00~				해당 축을 서보 OFF 시킴 (SA 신호 [F0.01]는 유지됨)
	SVRDY1		,//~	F28.00~F28.1F		축별 서보 READY 상태
	MIR1		,// ~ MIR32	G45.00~	G45.1F		Mirror Image 신호, AUTO, MDI 운전에 의한 축 이동 방향이 지령치와 반대				
	MIRL1		,// ~ MIRL32	F29.00~F29.1F	Mirror Image 확인 신호
	RTOVR0		,// ~ RTOVR4	G36.00~G36.04	급속 이송 Override,32가지 Override Factor의 System Table로 Mapping				
	FDOVR0		,// ~ FDOVR4	G37.00~G37.04	이송 Override, 32가지 Override Factor의 System Table로 Mapping			
	SPOVR0		,// ~ SPOVR4	G38.00~G38.04	스핀들 Override, 32가지 Override Factor의 System Table로 Mapping			
	RVS		,//	G39.08	RVSL	F30.08			역운전 개시 신호/ 역운전 중 신호
	TPRS		,//	G46.00						입력 보정량 입력 모드 선택 신호
	PSLDS1		,//~	G47.00~G47.1F			+방향 소프트 리미트 OFF
	NSLDS1		,//~	G48.00~G48.1F			-방향 소프트 리미트 OFF
	EDECP1		,//~	G49.00~G49.1F			+방향 외부 감속	
	EDECN1		//~	G49.00~	G49.1F			-방향 외부 감속			

};
// no 10.
enum HXGF_AxisSetting{
	SPNO0		,// ~ SPNO5 G52.00~	G52.05		
	SPNOL0		,//~ SPNOL5	F33.00~F33.05		메인 스핀들 설정/확인 신호
	ZNO0		,// ~ ZNO5 	G53.00~G53.05	
	ZNOL0		// ~ ZNOL5	F34.00~F34.05	메인 Z축 설정/확인 신호
};
// no 11.
enum HXGF_M{
	M0		,// ~ M31	F38.00~F38.1F	M Code Data (Binary Data)
	MF		,//	F37.00	General M Code Strobe signal
	MDEN	,//	F37.01	General M Code Distribute Finish signal
	MFIN	,//	G56.00			M Code Finish 
	DM00	,//,DM01,DM02,DM30 F37.08~F37.0B	Special M Code Signal (M00, M01, M02, M30)
	DM01,DM02,DM30
};
// no 12.
enum HXGF_Spindle{
	S0		,// ~ S31	F46.00~F46.1F	S Code Data (Binary Data)
	SF		,//	F45.00	S Code Strobe signal
	SDEN	,//	F45.01	S Code Distribute Finish signal
	SFIN	,//	G64.00	S Code Finish (스핀들 아날로그 출력 유효)
	SRPMB0	,// ~SRPMB31 F47.00~F47.1F	NC에서 스핀들 Drive로 속도지령 전압 출력 , 
				//(디지털 입력인 경우) Binary 데이터임
	GR1		,// ~ GR4	G64.04~	G64.07		Gear 선택 신호(4단)
	GRS1	,// ~ GRS4	F49.00~F49.03	M Code를 이용한 Gear 절환 방식인 경우 사용
	GRST	,//	G64.08	스핀들 기어 Change RPM으로 회전 지령
	GRSFT	,//	F49.04	스핀들 기어 Change 허가 신호
	SPRPM0	,// ~SPRPM4	G65.00~G65.03			수동 운전 스핀들 RPM Index
	SSTP	,//	G66.10	스핀들 Stop 지령 중인 상태 
	SPCW	,//	G66.11	스핀들 CW 지령 중인 상태
	SPCCW	,//	G66.12	스핀들 CCW 지령 중인 상태
	SOR		,//	G66.13	스핀들 Orientation 상태  
	SAR		,//	G66.14	스핀들 속도 도달 상태  
	SZAR	,//	G66.15	Zero Speed 도달 상태  
	SPOS	,//	G66.16	스핀들 위치제어 모드 상태  
	DSSTP	,//	G66.00	스핀들 Stop 지령 신호
	DSPCW	,//	G66.01	스핀들 CW 지령 신호
	DSPCCW	,//	G66.02	스핀들 CCW 지령 신호
	DSOR	,//	G66.03	스핀들 Orientation 지령 신호
	DSPOS	,//	G66.06	스핀들 위치 모드 지령 신호

	SSTPST	,//	F48.00	스핀들 Stop 상태 신호
	SPCWST	,//	F48.01	스핀들 CW 지령 상태 신호
	SPCCWST	,//	F48.02	스핀들 CCW 지령 상태 신호
	SORST	,//	F48.03	스핀들 Orientation 상태 신호
	SARST	,//	F48.04	스핀들 속도 도달 상태 신호
	SZARST	,//	F48.05	Zero Speed 도달 상태 신호
	SPOSST	,//	F48.06	스핀들 위치 모드 상태 신호
	SSC		,//	G67.00	스핀들 SS제어모드
	SSCL	//	F50.00	스핀들 SS제어모드 중

};
// no 13.
// no 14.
enum HXGF_T{
	T0		,// ~ T31	F62	T Code Data (Binary Data)
	TF		,//	F61.00	T Code Strobe signal
	TDEN	,//	F61.01	T Code Distribute Finish signal
	TFIN	,//	G75.00			T Code Finish 
	TRMODL	,//	F64.00	공구도피 및 복귀 모드 신호
	TLESC	,//	G79.10	
	TRESCL	,//	F64.01	- 공구도피 / 복귀신호
	TLRTN	,//	G79.11	
	TRRTNL	//	F64.02	- 공구도피모드/공구도피중/공구복귀중 확인신호
};

// no 15.
enum HXGF_Chopping{
	CHPST	,//	G90.00			Chopping 기동/정지 신호
	CHPSP	,//	G90.01			Chopping 일시 정지 신호
	CHPOVR0	,//~CHPOVR3	G90.08~G90.0B	Chopping 오버라이드 신호					
	CHPL	//	F75.00	Chopping 중 신호
};

// no 16.
enum HXGF_NCInternal{
	MV1		,//~MV32  F84.00~F84.1F	축 이송 중					  
	PMV1	,//~PMV32 F85.00~F85.1F	+ 축 이송 중					  
	NMV1	,//~NMV32 F86.00~F86.1F	- 축 이송 중					  
	INP1	,//~INP32 F87.00~F87.1F	In Position 상태			
	PASL	,//	F90.00~F90.1F +방향 위치 신호		
	CASL	,//	F91.00~F91.1F 중심 위치 신호		
	NASL	,//	F92.00~F92.1F -방향 위치 신호	
	PTP		,// F99.00/급속이송
	CP		,//	F99.01/절삭이송 중 신호		
	CSS		,//	F99.03	주속 일정 제어 중 신호
	RTAP	,//	F99.06	TAP CYCLE 중
	THRD	,//	F99.05	나사 절삭 중
	HSM		,//	F99.10	고속 가공 중

};

// no 17.
enum HXGF_SyncControl{
	TWNCTRL1	 //~TWNCTRL32	G103.00~G103.1F	TWIN TABLE 입력 신호
};
// no 18.
enum HXGF_CustomMacro{
	UI000	,// ~ UI031	G115.00~G115.1F			G115의 어드레스에 대한 32개의 접점은 커스텀 매크로의 #7000 ~ #7031로 사용
	//			(단 G115의 32bit 데이터는 #7032로 사용함 )
	UI100	,// ~ UI131	G116.00~G116.1F			G116는 시스템 화면에서 공구번호의 값을 바꾸는데 사용되며, #7033로 사용				
	UI200	,// ~ UI231	G117.00~G117.1F			접점 단위가 아닌 어드레스 단위로 사용 가능 하며 G117은 #7034로 사용				
	UI300	,// ~ UI331	G118.00~G118.1F			접점 단위가 아닌 어드레스 단위로 사용 가능 하며 G118은 #7035로 사용				
	UO000	,// ~ UO031	F105.00~G105.1F	F105의 어드레스에 대한 32개의 접점은 커스텀 매크로의 #7500 ~ #7531로 사용
	//	(단 F105는 32bit 데이터는 #7532로 사용함 )
	UO100	,// ~ UO131	F106.00~G106.1F	F106는 시스템 화면에서 공구번호의 값을 바꾸는데 사용되며, #7521로 사용		
	UO200	,// ~ UO231	F107.00~G107.1F		접점 단위가 아닌 어드레스 단위로 사용 가능 하며 F107은 #7534로 사용	
	UO300	// ~ UO331	F108.00~G108.1F	접점 단위가 아닌 어드레스 단위로 사용 가능 하며 F108은 #7535로 사용		
};
// no 19.
enum HXGF_PLCAxis{
	PX_ST1	,//~PX_ST32	G120.00~G120.1F	 PLC Axis 이송 시작 신호		
	PX_CAN1	,//~PX_CAN32 G121.00~G121.1F PLC Axis 이송 취소 신호				
	PX_MF1	,//~PX_MF32	G123.00~G123.1F	 PLC Axis 이송속도 선택 신호				
	PX_MO1	,//~PX_MO32	G124.00~G124.1F	 PLC Axis 오버라이드 선택 신호					
	PX_BLK1	,//~PX_BLK32	G131~	G193 PLC Axis 지령 BLOCK					
	PX_FO1	,//~PX_FO3	G132~G194		 PLC 축 이송속도 또는 오버라이드 지령
	//			- PX_MF[G123]의 해당 축 비트가‘1’à 이송속도
	//			- PX_MO[G124]의 해당 축 비트가‘1’à 오버라이드 
	PX_NAK1	,//~PX_NAK32	F111.00~F111.1F	이송 중 에러 발생 신호(NC가 PLC축 제어를 못하는 경우)		
	PX_POS1	,//~ PX_POS32	F121~F183	PLC Axis 현재 위치			
	PX_FIN1	//~PX_FIN32	F110.00~F110.1F	PLC Axis 이송완료 FIN
			//- 속도형 : 속도 도달 신호
			// - 인덱스/위치형 : 지령한 위치로 이송완료 신호
};
// no 20.
enum HXGF_AdvancedControl{
	ZGTRC1	,//~ZGTRC4	G200.00~G200.03			Z GAP Trace 신호
					
	ZGFAR1	,//~ ZGFAR4	G200.08~G200.0B			Z GAP Trace Sensor 측정범위 이탈신호
				
	ZGTRCL1	,//~ZGTRCL4	F200.00~F200.03	Z GAP Trace 중 신호
		

	MVCF	,//	F200.18	이송속도 등속구간 출력 신호
	MVFO	,//	F201	이송속도 출력 (설정축에 이송 속도를 PLC로 출력)
	PPFW	,//,	G201.09,			프레스 동작 대기 신호,
	PPFS	,//	G201.08			프레스 동작 Skip 신호
	PPMM	,//,	G201.0E,			수동 프레스 모드 선택 신호,
	PPMF	,//	G201.0F			수동 프레스 동작 시작 신호
	PPMP1	,//,	G201.10,			복수가공 선택 신호
	PPMP2	,//	G201.11			
	PPMTC	,//	G201.13			공구교환 위치 선택 신호(MDI 공구교환)
	PPE	,//,	G201.18			프레스 동작 정지 신호
	PPFIN	,//,	G201.19			프레스 동작 완료 신호
	NPFIN	,//	G201.1A			연속 프레스 동작 완료 신호
	PPF	,//	F202.00	프레스 동작 시작 신호
	NPF	//,//	F202.01	연속 프레스 동작 시작 신호
	//	,//G202.00	자동가공완료신호(공구수명 Z Shift)

};
// no 21.
enum HXGF_SCreen{
	SCR0	,//~SCR7	G3004.00G3004.07			화면 전환 번호					
	STRANS	,//	G3005.00			화면 전환 시작 신호
	SCRL0	,//~SCRL7	F3004.00F3004.07	현재 화면 번호			
	SCFIN	,//	F3005.00	화면 전환 완료 신호
	KEY0	//,//~KEY63	F3000.00F3001.1F	KEY 입력 신호 [F1 ~ F10는 F3000.00~F3000.09]			

};
// no 22.
enum HXGF_PLCmessage{
	PLCAL0	,// ~	G900.00 ~  G949.1F			PLC USER  ALARM  Message (PLCAlmDt.txt)
	PLCOP0	//,//~	G950.00 ~  G999.1F			PLC USER  Operating  Message (PLCOpDt.txt)

};
// no 23.
enum HXGF_Lettering{
	bPMON	,//	F76.01	Profile measure ON 
	bPMOFF	,//	F76.02	Profile measure OFF 
	bPMST	,//	F76.03	
	bPMOK	,//	F76.04	
	bPMERR	//,//	F76.05	

};
// no 24.
enum HXGF_ToolEndcontrol{
	iFTEC//,//	G78.00	G43.4의 시작 /End 

};
// no 25.
enum HXGF_CPhase{
	iFSGD, //	F82.00~F82.1f		Slave Grid Shift 적용 신호	
	iFMCP//, //	F82.00~	F82.1f	On/off Master만 C상을 잡는다는 신호	
};

enum HXState {
	SN_POSITION_COMMAND_MACHINE = 205, //지령 기계위치 (1 ~ 32축)
	SN_POSITION_REAL_MACHINE = 237, //실제 기계위치(1 ~ 32축)
	SN_POSITIO_REAL_ABSOLUTE_MACHINEN = 269, //실제 절대 기계위치(1 ~ 32축)
	SN_POSITION_CURRENT_COMMAND_MACHINE = 301, //현재 지령 기계위치(1 ~ 32축)
	SN_POSITION_PREV_COMMAND_MACHINE = 311, //이전 지령 기계위치(1 ~ 32축)
	SN_POSITION_SKIP = 319, //Skip 신호가 나타난 기계 위치값(1 ~ 32축)

	SN_POSITION_SKIP1 = 351, //Skip 신호 1  나타난 축별  기계 위치값(1 ~ 32축)
	SN_POSITION_SKIP2 = 360, //Skip 신호 2  나타난 축별  기계 위치값(1 ~ 32축)
	SN_POSITION_SKIP3 = 369, //Skip 신호 3  나타난 축별  기계 위치값(1 ~ 32축)
	SN_POSITION_SKIP4 = 378, //Skip 신호 4  나타난 축별  기계 위치값(1 ~ 32축)

	SN_ENCODER = 451, //엔코더 값
	SN_ENCODER_VALUE2 = 820, //엔코더 값 / 1000
	SN_ABS_ROTATE_NUM = 515, //ABS Rotate Number
	SN_ABS_INIT_ENCODER = 643, //ABS Init Encoder Value
	SN_ABS_ENCODER = 675, //ABS Encoder Value
	SN_ABS_INIT_TOTAL_ENCODER = 611, //ABS Init Total Encoder Value

	SN_MAIN_PROGRAM_BLOCK_NO = 714, //메인 프로그램의 블록 Number
	SN_MAIN_PROGRAM_BLOCK_ADDR = 715, //메인 프로그램의 블록 Seek Address
	SN_CURRENT_BLOCK_NO = 716, //현재 수행 중인 블록 Number
	SN_CURRENT_BLCOK_ADDR = 717, //현재 수행 중인 블록 Seek Address
	SN_MODAL_G = 718, //G code Modal Value ( #1~#32) 
	SN_MAIN_PROGRAM_RUN_COUNT = 752, //메인 프로그램 반복 횟수
	SN_RESTART_RETURN_BLOCK_NO = 753, //Return Block Number for Restart ( #1~#10) 
	SN_RESTART_RETURN_BLOCK_ADDR = 763, //Return Seek Address for Restart ( #1~#10) 
	SN_RESTART_LOOP_BLOCK_NO = 773, //Loop Block Number for Restart ( #1~#10) 
	SN_RESTART_LOOP_SEEK_ADDR = 783, //Loop Seek Address for Restart ( #1~#10) 
	SN_RESTART_SUB_PROGRAM_START_COUNT = 793, //프로그램 재개시 부프로그램 시작 탐색 횟수 ( #1~#10) 
	SN_MODAL_FEED = 803, //Modal Feed
	SN_MODAL_S_CODE = 804, //Modal S Code
	SN_MODAL_M_CODE = 805, //Modal M Code

	SN_WORK_COORDINATE_BASIS_OFFSET = 102, //작업물좌표계 기본 옵셋값  ( #1~#10) 
	SN_WORK_COORDINATE_SHIFT_OFFSET = 112, //작업물좌표계 이동(shift) 옵셋값 ( #1~#10) 
	SN_TOOL_LENGTH_OFFSET = 122, //공구길이 옵셋값 ( #1~#10) 
	SN_LOCAL_COORDINATE_OFFSET = 132, //로컬좌표계 옵셋값 ( #1~#10) 
	SN_TOOL_SHAPE_OFFSET = 142, //공구형상 옵셋값 ( #1~#10) 
	SN_TOOL_ABRASION_OFFSET = 152, //공구마모 옵셋값 ( #1~#10) 

	// 모니터링 
	SN_SYSTEM_INTERRUPT_TIME = 990, // System Interrupt Time		
	SN_IPO_RUNNING_TIME = 991, // 	   IPO 수행 시간				
	SN_POS_RUNNING_TIME = 992, // 	   POS 수행 시간				
	SN_PLC_SCAN_TIME = 993, // 		   PLC 총 Scan 시간			
	SN_PLC_1LEVEL_RUNNING_TIME = 994, // PLC 1Level 수행시간 
	SN_PLC_TOTAL_RUNNING_TIME = 995, //PLC 1Level + 2Level 수행시간
	SN_PLC_2LEVEL_RUNNING_TIME = 996, // PLC 2Level 수행시간


	// restart 
	SN_X_POSITION_AT_AUTO_RESET = 162, //AUTO  운전 중 Reset 시 X축 기계좌표
	SN_Y_POSITION_AT_AUTO_RESET = 163, //AUTO  운전 중 Reset 시 Y축 기계좌표
	SN_Z_POSITION_AT_AUTO_RESET = 164, //AUTO  운전 중 Reset 시 Z축 기계좌표
	SN_A_POSITION_AT_AUTO_RESET = 165, //AUTO  운전 중 Reset 시 A축 기계좌표
	SN_B_POSITION_AT_AUTO_RESET = 166, //AUTO  운전 중 Reset 시 B축 기계좌표
	SN_C_POSITION_AT_AUTO_RESET = 167, //AUTO  운전 중 Reset 시 C축 기계좌표
	SN_U_POSITION_AT_AUTO_RESET = 168, //AUTO  운전 중 Reset 시 U축 기계좌표
	SN_V_POSITION_AT_AUTO_RESET = 169, //AUTO  운전 중 Reset 시 V축 기계좌표
	SN_W_POSITION_AT_AUTO_RESET = 170, //AUTO  운전 중 Reset 시 W축 기계좌표
	SN_RESTART_SPINDLE_RPM = 171, //Restart Spindle RPM	
	SN_RESTART_FEED = 172, //Restart Feed		   
	SN_RESTART_BLOCK = 173, //Restart Block		   
	SN_RESTART_HSP_MODE = 174, //Restart HSP mode		
	SN_RESTART_WORK_COORDINATE = 175, //Restart Work Coordinate
	SN_RESTART_H_CODE = 176, //Restart H code		
	SN_RESTART_M_CODE = 177, //Restart M code2		

	SN_CNT_ZERORETURN = 814, // 원점 복귀 횟수 (1축~32축)
	SN_FIN_ZERORETUNR_ABSENCTYPE = 483, // ABS Encoder(절대치엔코더)사용시 원점복귀 완료 여부(1축~32축)
	SN_ZERORETURN_ENCODEROFFSETPULSE_ABSENCTYPE = 483, // ABS Encoder(절대치엔코더)사용시 원점복귀 Encoder offset pulse(1축~32축)
};
enum HXInfo {	
	SV_MMI_VERSION = 3, // MMI Version
	SV_MMI_DVERSION = 4, // MMI Debug Version

	SV_RUNNING_RATIO_MAIN_PROGRAM = 5, // Main Program 진행률
	SV_RUNNING_RATIO_SUB_PROGRAM = 6, // Sub Program 진행률

	SV_IPR_RUN_SATE = 11, // 가동유무(0:정지 1 : 수행)
	SV_IPR_HEART_BIT = 12, // IPR Heart Bit
	SV_IPR_VERSION = 13, // IPR Version
	SV_IPR_WAIT_EOM = 15, // Wait EOM(0:기다리지않음 1 : 기다림)
	SV_IPR_AF = 16, // AF 사용량
	SV_IPR_DVERSION = 17, // IPR Debug Version

	SV_IPO_RUN_STATE = 20, // IPO의 RUN 상태
	SV_IPO_HEART_BIT = 21, // IPO Heart Bit
	SV_POS_HEART_BIT = 22, // POS Heart Bit
	SV_PLC_HEART_BIT = 23, // PLC Heart Bit		
	SV_IPO_VERSION = 24, // IPO Version
	SV_POS_VERSION = 25, // POS Version
	SV_PLC_VERSION = 26, // PLC Version
	SV_PLC_LADDER_VERSION = 27, // PLC Ladder Version
	SV_HW_VERSION = 28, // H / W Version
	SV_HW_ROM_VERSION = 29, // H / W ROM Version
	SV_SW_TIMER = 30, // Timer

	SV_NO_AXIS_X = 41, // CNC 제어축의 실제 축번호(X)
	SV_NO_AXIS_Y = 42, // CNC 제어축의 실제 축번호(Y)
	SV_NO_AXIS_Z = 43, // CNC 제어축의 실제 축번호(Z)
	SV_NO_AXIS_A = 44, // CNC 제어축의 실제 축번호(A)
	SV_NO_AXIS_B = 45, // CNC 제어축의 실제 축번호(B)
	SV_NO_AXIS_C = 46, // CNC 제어축의 실제 축번호(C)
	SV_NO_AXIS_U = 47, // CNC 제어축의 실제 축번호(U)
	SV_NO_AXIS_V = 48, // CNC 제어축의 실제 축번호(V)
	SV_NO_AXIS_W = 49, // CNC 제어축의 실제 축번호(W)
	SV_NO_AXIS_S = 50, // CNC 제어축의 실제 축번호(S)

	SV_OFFSET_BETWEEN_MACHINECOORD_WORKCOORD = 51, // 기계좌표계에서 작업물 좌표계까지의 옵셋값( 1~ 32축 ) 
	SV_ABSOLUTE_COORDINATION = 83, // 작업물 좌표계를 기준으로 한 현재위치(절대좌표)( 1~ 32축 ) 
	SV_RELATIVE_COORDINATION = 115, // 상대좌표( 1~ 32축 ) 
	SV_MPG_INTERRUPT = 215, // 핸들(MPG) 인터럽트 개입량( 1~ 32축 ) 
	SV_REMAIN_DISTANCE = 247, // 남은거리( 1~ 32축 ) 
	SV_SERVO_POSITION_DEVIATION_FOLLOWING = 379, // 서보위치 편차량(추종오차)( 1~ 32축 ) 
	SV_SERVO_POSITION_DEVIATION_SYNCHRONIZE = 411, // 동기위치 편차량(동기오차)( 1~ 32축 ) 
	SV_RIGID_TAP_PITCH_ERR = 443, // Rigid Tapping 시 Pitch 오차량
	SV_C_PHASE_STATE = 542, // C상 상태 
	SV_C_PHASE_PULSE = 543, // C상 펄스( 1~ 32축 ) 	

	SV_FEED_OVERRIDE = 675, // Feed Override
	SV_RAPID_OVERRIDE = 676, // Rapid Override
	SV_SPINDLE_OVERRIDE = 681, // Spindle Override
	SV_COMMAND_FEED = 721, // 지령된 이송속도(F지령 값)
	SV_COMMAND_VECTOR_FEED = 722, // 지령된 벡터 이송속도(오버라이드 고려)
	SV_REAL_FEED = 755, // 실제 이송 속도	( 1~ 32축 ) 
	SV_REAL_VECTOR_DISTANCE = 787, // 실제 벡터 이송량
	SV_COMMAND_SPINDLE_FEED = 792, // 스핀들의 지령 속도(S지령 값)
	SV_COMMAND_SPINDLE_FEEDOVERRIDE = 793, // 스핀들의 지령속도(오버라이드 고려)
	SV_REAL_SPINDLE_FEEDOVERRIDE = 794, // 실제 스핀들의 속도(오버라이드 고려)
	SV_DWELL_COUNT = 800, // Dwell Count
	SV_MPG_PULSE = 805, // MPG 입력 Pulse 수

	SV_SERVO_ON_STATE = 812, //Servo ON 신호 상태
	SV_SERVO_READY_STATE = 813, //Servo Ready 신호 상태
	SV_SERVO_RESET_STATE = 814, //Servo Reset 신호 상태
	SV_SERVO_ALARM_STATE = 815, //Servo Alarm 신호 상태

	SV_SERVO_COMMNAD_VELOCITY = 820, // 서보 제어 출력값(속도 지령값) ( 1~ 32축 ) 

	SV_IO_X_STATE = 855, //NC I / O X접점 상태
	SV_IO_Y_STATE = 856, //NC I / O Y접점 상태
	SV_M2_CONNECT_STATE = 901, //M2 Connect 상태
	


	SV_EOM = 866, // EOM
	SV_IPR_ERR_BLOCK_NO = 867, // IPR해석시 Error Block Number
	SV_MDI_BLOCK_NO = 873, // MDI프로그램의 현재 수행 Block Number
	SV_MDI_BLOCK_ADDRESS = 874, // MDI프로그램의 현재 수행 Block Seek ADDR.
	SV_CURRENT_BLOCK_TYPE = 876, // 현재 수행 중인 블록 형태
	SV_CURRENT_TOOL_NO = 881, // 현재 공구의 번호
	SV_CURRENT_TOOL_COMPENSATION_OFFSET_NO = 882, // 현재 공구의 공구경 보정 옵셋번호
	SV_CURRENT_TOOL_LENGTH_COMPENSATION_OFFSET_NO = 883, // 현재 공구의 공구길이 보정 옵셋번호
	SV_TOOL_PATH_CHECK_ABSOLUTE_COORDINATION = 887, // 공구경로 검사 현재 좌표(1~32 축)

	

};


//------------------------------
// parameter - IO
//------------------------------
enum HXIO {
	PP_PLC_2LEVEL_STEP_BY_SAMPLINGTIME =1605, // 한 SAMPLING 당 2레벨 처리 갯수
	PP_IO_GROUP1_TYPE = 1610, //I / O 종류(0:X 1 : SERCOS 2 : CAN 3 : NC B'D 4:DRIVE 5:S/W OP 6:M2 
	PP_IO_GROUP1_X_ADDRESS = 1618, //X / Y 접점 시작 번지
	PP_IO_GROUP1_X_COUNT = 1626, //X / Y 접점 개수

	PP_IO_GROUP2_TYPE = 1611, //I / O 종류(0:X 1 : SERCOS 2 : CAN 3 : NC B'D 4:DRIVE 5:S/W OP 6:M2 
	PP_IO_GROUP2_X_ADDRESS = 1619, //X / Y 접점 시작 번지
	PP_IO_GROUP2_X_COUNT = 1627, //X / Y 접점 개수

	PP_IO_GROUP3_TYPE = 1612, //I / O 종류(0:X 1 : SERCOS 2 : CAN 3 : NC B'D 4:DRIVE 5:S/W OP 6:M2 
	PP_IO_GROUP3_X_ADDRESS = 1620, //X / Y 접점 시작 번지
	PP_IO_GROUP3_X_COUNT = 1628, //X / Y 접점 개수

	PP_IO_GROUP4_TYPE = 1613, //I / O 종류(0:X 1 : SERCOS 2 : CAN 3 : NC B'D 4:DRIVE 5:S/W OP 6:M2 
	PP_IO_GROUP4_X_ADDRESS = 1621, //X / Y 접점 시작 번지
	PP_IO_GROUP4_X_COUNT = 1629, //X / Y 접점 개수
};

//------------------------------
// parameter - system
//------------------------------
enum HXsystem{
	PP_PLCAXISTYPE = 319,
	PP_PLCAXISSamplingTime = 351,

	PP_USE_SIMULATION = 26, //  시뮬레이션 모드 여부(0 : REAL 1 : 시뮬레이션) 
	
	PP_NC_TYPE = 1410, // NC CARD TYPE(0:SERCOS 1 : ANALOG 2 : MODEX 3 : LITE TYPE 4 : M2 5 : HX2.0
	PP_CARD_TYPE = 1411, // 통신 CARD TYPE(0:기본 1 : M2 2 : ECAT)				
	PP_AIB_TYPE = 1412, // AIB C PHASE 적용여부, 신형 AIB 는 "1" 선택(0:미적용, 1 : 적용)
	PP_USE_SRAM = 1415, //  SRAM 사용 여부(0:사용안함, 1 : 사용함) 
	PP_FILE_SAVE_INTERVAL = 1416, // SRAM을 사용하지 않을 경우 FILE SYSTEM에 저장 간격
	PP_USE_PARAM_BACKUP = 1417, // 종료시 파라미터 백업기능(0:사용안함, 1 : 시분초, 2 : 시, 3 : 날짜 
	PP_USE_WATCHDOG = 1418, //  WATCHDOG 기능 사용 여부(0:사용안함, 1 : 사용함) 
	PP_USE_MONITORING_BLACKOUT = 1420, // 전원 감시 기능 사용 여부(0:사용안함, 1 : 사용함)
	PP_BLACKOUT_TIME_ERR = 1422, // 정전 허용 시간 
	PP_BLACKOUT_TIME = 1423, // 정전 판단 시간 
	PP_USE_BLACKOUT_WARNING = 1424, // 정전 상태 메시지 출력 여부(0:출력 안함, 1 : 출력함)
	PP_USE_COM_FILTER_1425, // 통신 필터 적용 0: 사용안함, 1 : 사용함 		

	PP_CNT_EVENTLOG_FILE = 21, // EVENT LOG 등록 파일 최대 개수
	PP_CURRENT_EVENTLOG_FILE = 22, // 현재 등록중인 EVENT LOG 파일 번호
	PP_DATE_DB_FIRST_DAY = 23, // 생산관리 DB 생성 일자 설정
	PP_UPDATE_INTERVAL_DB = 24, // 생산관리 DB 업데이트 주기 설정
	PP_OPT_HX_INITIAL_MINIMIZATION = 25, // HX MINIMIZE(0:기본 1 : 트레이)
	PP_SAMPLINGTIME_SYSTEM = 50, // 시스템 SAMPLING TIME
	PP_SAMPLINGTIME_POSITION = 51, // 위치제어 SAMPLING TIME
	PP_RETREAT_RUN_BUFFER = 55, // 역방향 운전 버퍼 크기
	
	PP_SET_NAME_CNCAXIS = 73, // CNC축 설정(X:1 Y : 2 Z : 3 A : 4 B : 5 C : 6 U : 7 V : 8 W : 9 S : 10)
	PP_USE_SIMULTANEOUSLY_INTERPOLATION = 106, // 동시 제어축(보간축) 선택(0:비동시 1 : 동시)
	PP_NO_MAIN_SPINDLE = 140, // 메인 스핀들 번호
	PP_NO_MAIN_Z = 143, // 메인 Z축 번호
	PP_NO_MASTER_TWIN_TABLE = 237, // TWIN TABLE 제어에서 SLAVE축의 MASTER축 번호 설정
	PP_TYPE_PLC_AXIS = 319, // PLC축 선택(0:비사용 1 : INDEX 2 : 위치 3 : 속도1 4 : 속도2)
	PP_PLC_AXIS_SAMPLINGTIME = 351, // PLC축의 기본 제어단위
	PP_MODULAR_DISTANCE = 447, // 모듈러 좌표 표시 기능 설정 (EX  : 360 DEG)

	PP_TYPE_TOOL_CHANGE = 543, // 공구교환 방법 설정
	PP_TOTAL_TOOL = 544, // 총 공구 개수
	PP_USE_ALARM_TOOL_LIFE_BY_TIME = 545, // 공구수명 도달 PRE - ALARM 설정(가공시간 방식)
	PP_USE_ALARM_TOOL_LIFE_BY_COUNT = 546, // 공구수명 도달 PRE - ALARM 설정(가공개수 방식)
	PP_SET_MCODE_TOOL_CHANGE = 547, // 공구교환 M CODE
	PP_SET_ALARM_COUNT_MCODE_TOOL_CHANGE = 548, // 가공 개수 COUNT M CODE
};

//
//------------------------------
// parameter - Program
//------------------------------
enum HXProgram{
	PA_WORK_TARGET_CNT = 1431, // 목표 가공 수량 
	PI_PG_RADIUS_CMD = 73, // X축 지령 방법(0: 직경, 1: 반경)
	PI_IGNORE_DECIMALPOINT = 76, // 소수점 검사(0:유, 1:무)
	PI_UNIT_COMMADN = 170, // 최소 지령 단위(기본:0.001), 소수점 검사시 적용됨 (mm)
	PI_METHOD_90CHAMPERRING = 82, // 90도 챔퍼링 방법(0:I, J, K로 지령, 1: C지령)
	PI_METHOD_DWELL = 120, // 휴지 방법(0: 시간, 1: 회전수)
	PI_START_BLOCK_AFTER_RESET = 133, // 리셋시 진행 블록 선택(0: 유지, 1: 초기 블록, 2: 호출 블록)
	PI_USE_SEARCH_statement_number = 134, // 문번호 검색 유무(0:유, 1:무)
	PI_MAX_ERROR_CIRCLE_RADIUS = 151, // 원호 반경 허용 오차 (mm)
	PI_USE_REPOSITION_CIRCLECENTER = 171, // 원호 알람 발생시 원호 중심 재생성(0:무, 1:재생성)
	PI_ROTATE_AXIS_CYLINDER_INTERPOLATION = 155, // 원통보간 회전축(0:X, 1:Y, 2:Z)
	PI_METHOD_RESTART_PG = 183, //프로그램 재개시 방법 (0:선택 블록부터, 1: 처음부터)
	PI_METHOD_MODULAR_COMMAND = 173, // 모듈라 축 지령 방법(0:지령치, 1: 근거리, 2:한 방향)
	PI_MAX_ERROR_NURBS = 177, //NURBS 보간 허용오차(mm)
	PI_NURBS_TOOL_RADIUS = 178, //NURBS 보간용 공구 반경(mm)
	PI_NURBS_STEP_OVER = 179, //NURBS 보간용 Step Over량(mm)
	PI_NURBS_ROUGH = 180, //NURBS 보간 표면 거칠기(mm)
	PI_Z_AXIS_DESCEND_FEED = 181, // Z축 하강 FEED (0: 무시)
	PI_INPOSITION_CHECK_Z_AXIS_DESCEND_FEED = 182, // Z축 하강 FEED 적용시 Inposition 검사 유무(1:검사)

	// 경보정 관련
	PI_METHOD_D_COMP = 72, //공구경 보정값 적용방법 (0: 직경치, 1: 반경치)
	PI_METHOD_D_COMP_CHANGE_TYPE = 127, //경보정값 변경 타입(0:직접, 1:굴절)
	PI_METHOD_D_COMP_TYPE = 128, //공구 경보정 타입(0:우회,1:직접)
	PI_METHOD_D_COMP_TOOL_CHECK = 172, //공구 경보정시 공구간섭 체크 유무(0:안함, 1:체크함, 2:무시(해당블럭제거))
	PI_METHOD_D_COMP_APPLY_TYPE = 184, //공구 경보정 적용 타입(0:시작점,1:끝점)

	//Buffering 하지 않는 M코드
	PI_MCODE_NOT_BUFFERING = 165, //Buffering 버퍼링 하지 않는 M코드(#1 ~ #5) Value:  0~1999(0은 무시)

	// 디폴트 Modal 설정
	PI_MODAL_MOVE_TYPE = 144, //모달 이송(0:급송(G00) 1:절삭(G01)
	PI_MODAL_PLANE = 145, //모달 평면(0:XY(G17) 1:ZX(G18), 2:YZ(G19))
	PI_MODAL_INCREMENTAL = 146, // 모달 절대/ 증분(0:절대(G90) 1:증분(G91)
	PI_MODAL_INCH = 147, //모달 지령 단위(0:Metric(G21), 1:Inch(G20))
	PI_MODAL_BOUND_UNCHEK = 148, // 모달 금지 영역 검사(0:수행(G22) 1:취소(G23))
	PI_MODAL_COORDINATE_ROTATING = 150, //모달 좌표계 회전(0:취소(G59), 1:적용(G68))
	PI_ANGLE_COORDINATE_ROTATING = 117, // 좌표계 회전각 

	// 사이클 설정
	PI_ROUGHING_CYCLE_DEPTH						=   51, // 황삭 사이클 절입량(D)					
	PI_ROUGHING_CYCLE_WITHDRAWAL_AMOUNT			=   52, //황삭사이클 후퇴량 (R)			
	PI_PATTERN_CYCLE_X_REMOVAL_AMOUNT			=   53, //모방사이클 X제거량 (XR)			
	PI_PATTERN_CYCLE_Z_REMOVAL_AMOUNT			=   54, //모방사이클 Z제거량 (ZR)			
	PI_PATTERN_CYCLE_MACHINING_ITERATION_COUNT	=   55, //모방사이클 가공반복횟수			
	PI_DRILL_CYCLE_WITHDRAWAL_AMOUNT			=   56, //드릴사이클 후퇴량			
	PI_FINE_BORING_CYCLE1_AXIS_SHIFT_DIRECTION	=   70, //파인보링 사이클 1축 SHIFT 방향	
	PI_FINE_BORING_CYCLE_2_AXIS_SHIFT_DIRECTION =   71, //파인보링 사이클 2축 SHIFT 방향	
	PI_PECK_DRILL_CYCLE_ALLOWANCE				=  129, //펙드릴 사이클 여유량		

	//복합나사 사이클
	PI_FINISHING_ITERATION_COUNT			=   57 , // 정삭 반복 횟수							
	PI_TOOL_INSERT_ANGLE					=   58 , // 공구 인서트 끝 각도 (0,29,30,55,60,80)
	PI_MINIMUM_DEPTH						=   59 , // 최소 절입량								
	PI_FINISHINGVALLOWANCE					=   60 , // 정삭 여유량								


	//자동코너 오버라이드 설정
	PI_STARTING_LENGTH								= 52, //시작 구간								
	PI_ENDING_LENGTH								= 53, //종료 구간								
	PI_DECELERATION_RATE							= 54, //감속 배율 (범위: 10-100)
	PI_INTERNAL_ANGLE								= 55, //사이각 (범위: 2-178)				
	PI_APPLIED_TYPE									= 56, //타입 (0:경보정시 1:항시)
	PI_FEED_AT_CORNER								= 70, //코너부 속도				
	PI_INTERNAL_ARC_CUTTING_SPEED_MINIMIZING_RATE	= 71, //내부원호 절삭속도 최소율 (0.00-1.00)

	// 기계 원점에서의 각 축의 작업물 좌표계 설정 값
	PI_AUTOMATIC_COORDINATE					= 174, //자동 좌표계 사용유무(0:사용안함, 1:사용함)
	PI_AXIS_X_AUTOMATIC_COORDINATE_VALUE	= 156, //X축 자동 좌표계 설정값				
	PI_AXIS_Y_AUTOMATIC_COORDINATE_VALUE	= 157, //Y축 자동 좌표계 설정값				
	PI_AXIS_Z_AUTOMATIC_COORDINATE_VALUE	= 158, //Z축 자동 좌표계 설정값				
	PI_AXIS_A_AUTOMATIC_COORDINATE_VALUE	= 159, //A축 자동 좌표계 설정값				
	PI_AXIS_B_AUTOMATIC_COORDINATE_VALUE	= 160, //B축 자동 좌표계 설정값				
	PI_AXIS_C_AUTOMATIC_COORDINATE_VALUE	= 161, //C축 자동 좌표계 설정값				
	PI_AXIS_U_AUTOMATIC_COORDINATE_VALUE	= 162, //U축 자동 좌표계 설정값				
	PI_AXIS_V_AUTOMATIC_COORDINATE_VALUE	= 163, //V축 자동 좌표계 설정값				
	PI_AXIS_W_AUTOMATIC_COORDINATE_VALUE	= 164, //W축 자동 좌표계 설정값				

	//자동공구 옵셋
	PI_AUTOMATIC_TOOL_OFFSET_INPUT_TYPE							= 119, //자동공구 옵셋 입력방법(0:기계위치,1:기준점에 대한 상대위치)}
	PI_SHIFT_DISTANCE_BETWEEN_STANDARD_POINT_AND_CENTER_AXIS_X	= 121, //자동공구보정 기준점에서 CENTER까지의 SHIFT 거리 (X축)}		
	PI_SHIFT_DISTANCE_BETWEEN_STANDARD_POINT_AND_CENTER_AXIS_Y	= 122, //자동공구보정 기준점에서 CENTER까지의 SHIFT 거리 (Y축)}		
	PI_SHIFT_DISTANCE_BETWEEN_STANDARD_POINT_AND_CENTER_AXIS_Z	= 123, //자동공구보정 기준점에서 CENTER까지의 SHIFT 거리 (Z축)}		
	PI_PLUS_MEASUREMENT_STANDARD_DISTANCE_X_AXIS				= 135, //+ 측정 기준거리 (X축)}										
	PI_PLUS_MEASUREMENT_STANDARD_DISTANCE_Y_AXIS				= 136, //+ 측정 기준거리 (Y축)}										
	PI_PLUS_MEASUREMENT_STANDARD_DISTANCE_Z_AXIS				= 137, //+ 측정 기준거리 (Z축)}										
	PI_MINUS_MEASUREMENT_STANDARD_DISTANCE_X_AXIS				= 138, //- 측정 기준거리 (X축)}										
	PI_MINUS_MEASUREMENT_STANDARD_DISTANCE_Y_AXIS				= 139, //- 측정 기준거리 (Y축)}										
	PI_MINUS_MEASUREMENT_STANDARD_DISTANCE_Z_AXIS				= 140, //- 측정 기준거리 (Z축)}										
	PI_DECELERATION_STARTING_LENGTH								= 141, //자동 공구 감속 시작 길이}										
	PI_MEASUREMENT_SENSING_RANGE								= 142, //자동 공구 측정 감지 가능 구간}								
	PI_DECELERATION_FEED										= 143, //자동 공구 감속 속도}										1 
	
	// T 코드 옵셋 설정
	PI_TOOL_OFFSET_APPLICATION_METHOD	=  78, //공구 Geometric 옵셋 적용방법(0:shift 1:축이송)
	PI_TOOL_GEOMETRIC_OFFSET			=  79, //공구 Geometric 옵셋 적용유무(0:무 1:유)		
	PI_TOOL_COMMAND_DIGITS				=  80, //공구지령 자릿수 (0:4자리 1:2자리)			
	PI_2_DIGIT_TOOL_COMMAND_METHOD		=  81, //2자리 공구지령방법 (0:T0_0_ 1:T0_00)			
	PI_TOOL_OFFSET_CANCELLATION			= 118, //공구옵셋 취소(0:유 1:무)	

	//스케일 설정
	PI_MODAL_SCALE_SETTING	= 149, //모달 스케일 설정 (0:스케일 취소(G50) 1:스케일 적용(G51))} 
	PI_MODAL_SCALE_X_AXIS		= 108, //X축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_Y_AXIS		= 109, //Y축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_Z_AXIS		= 110, //Z축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_A_AXIS		= 111, //A축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_B_AXIS		= 112, //B축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_C_AXIS		= 113, //C축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_U_AXIS		= 114, //U축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_V_AXIS		= 115, //V축 (DEFAULT = 1000)										
	PI_MODAL_SCALE_W_AXIS		= 116, //W축 (DEFAULT = 1000)		

	// 한방향 위치결정 오버런 이송량	
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_X_AXIS	= 61, //X축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_Y_AXIS	= 62, //Y축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_Z_AXIS	= 63, //Z축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_A_AXIS	= 64, //A축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_B_AXIS	= 65, //B축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_C_AXIS	= 66, //C축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_U_AXIS	= 67, //U축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_V_AXIS	= 68, //V축 (DEFAULT = 1000)										
	PI_SINGLE_DIRECTION_POSITIONING_OVERRUN_RANGE_W_AXIS	= 69 //W축 (DEFAULT = 1000)	
};	

enum HXUser{
	// 시스템
	PA_BUFFER_ERASES_AT_RESET_IN_THE_MDI_MODE	= 3  , //	리셋 시 MDI 버퍼 삭제 유뮤 (0:유 1:무)						
	PI_DEFAULT_ROTATING_ANGLE_IN_THE_MDI_MODE	= 175, //	MDI 디폴트 회전 각도 사용 유무 (0:사용 안 함 1: 사용)	
	PI_INPUT_WINDOW_IN_THE_MDI_MODE				= 176, //	MDI 입력창 사용 유무 (0:사용 안 함 1: 사용)

	// TPG 관련 
	PP_TPG_TYPE									= 20  , //TPG 적용 타입 (0:밀링 1:선반 2:NCT 3:POINT)}							
	PA_TPG_REVERSE_X_DIRECTION					= 361, //TPG X축 표시 방향 변경 적용 (0: 적용 안 함 1: 적용)}				
	PA_TPG_REVERSE_Y_DIRECTION					= 362, //TPG Y축 표시 방향 변경 적용 (0: 적용 안 함 1: 적용)}				
	PA_INITIAL_VIEW_DIRECTION_SETTING			= 363, //TPG 표시 화면의 초기 VIEW 방향 설정 (0-9)}						
	PA_0_VIEW_DIRECTION_ISOMETRIC_0_DEGREE		= 364, //0번 VIEW 방향 : 삼각  0도 (0:비사용 1 ~ :순서)}					
	PA_1_VIEW_DIRECTION_ISOMETRIC_90_DEGREE		= 365, //1번 VIEW 방향 : 삼각 90도 (0:비사용 1 ~ :순서)}				
	PA_2_VIEW_DIRECTION_ISOMETRIC_180_DEGREE	= 366, //2번 VIEW 방향 : 삼각180도 (0:비사용 1 ~ :순서)}				
	PA_3_VIEW_DIRECTION_ISOMETRIC_270_DEGREE	= 367, //3번 VIEW 방향 : 삼각270도 (0:비사용 1 ~ :순서)}				
	PA_4_VIEW_DIRECTION_PLANE_XY				= 368, //4번 VIEW 방향 : 평면 XY   (0:비사용 1 ~ :순서)}				
	PA_5_VIEW_DIRECTION_PLANE_XZ				= 369, //5번 VIEW 방향 : 평면 XZ   (0:비사용 1 ~ :순서)}				
	PA_6_VIEW_DIRECTION_PLANE_YX				= 370, //6번 VIEW 방향 : 평면 YX   (0:비사용 1 ~ :순서)}				
	PA_7_VIEW_DIRECTION_PLANE_YZ				= 371, //7번 VIEW 방향 : 평면 YZ   (0:비사용 1 ~ :순서)}				
	PA_8_VIEW_DIRECTION_PLANE_ZX				= 372, //8번 VIEW 방향 : 평면 ZX   (0:비사용 1 ~ :순서)}				
	PA_9_VIEW_DIRECTION_PLANE_ZY				= 373, //9번 VIEW 방향 : 평면 ZY   (0:비사용 1 ~ :순서)}				
	PA_REAL_TPG_TRACING_DISPLAY_STATUS			= 407, //REAL TPG 경로추적 표시 유무 (0:무 1:유-DEFAULT 2:유-십자선)}	
	PA_REAL_TPG_TRACING_EVIDENCE_DISPLAY_STATUS	= 408, //REAL TPG 경로추적 자취 표시 유무 (0:무 1:유)}					
	PA_REAL_TPG_SCREEN_MODE						= 409, //REAL TPG 화면 모드 (0:경로 선표시 1:미리보기 후 표시)}		
	PA_TEST_TPG_TRACING_DISPLAY_STATUS			= 410, //TEST TPG 경로추적 표시 유무 (0:무 1:유)}						
	PA_TRACER_DISPLAY_WIDTH						= 411, //경로추적 표시 폭 (0-20)  DEFAULT=10}							
	PA_TRACER_DISPLAY_HEIGHT					= 412, //경로추적 표시 높이 (0-50)  DEFAULT=20}							
	PA_TRACER_DISPLAY_COLOR						= 413, //경로추적 표시 색 (0:녹색 1:파랑 2:빨강 3:보라 4:하늘)}			
	PA_TRACING_EVIDENCE_DISPLAY_RADIUS_PIXEL	= 414, //경로자취 표시 반경 (DEFAULT = 2)}								
	PA_TRACING_EVIDENCE_COLOR					= 415, //경로자취 표시 색 (0:빨강 1:파랑 2:녹색 3:보라 4:하늘)}		
	PA_REAL_TPG_PREVIEW_HALT_M_CODE				= 416, //REAL TPG 미리보기 중단 M코드(0:적용안함)}						
	PA_XC_PLANE_SELECTION_ON_TPG				= 417, //TPG 상의 XC평면 선택 (0:XY평면 -1:-XC평면 1:+XC평면)}			
	PA_TPG_BMP_CREATION_TYPE					= 440, //REAL TPG BMP 생성 타입 (0:흑백 1:256칼라)}						
	PA_RADIUS_OF_PUNCH_HOLE_IN_NCT_TPG			= 441, //TPG에서 PUNCH HOLE 표시 반경 (DEFAULT=10)}						
	PA_USAGE_OF_G00_LINE_DISPLAY_AT_TPG			= 442, //TPG에서 G00 점선 표시 유무(0:유, 1:무)}						
	PA_REAL_TPG_TYPE							= 443, //REAL TPG TYPE 선택(0:기본화면, 1:가로화면) }					
	PA_REAL_TPG_BASIC_SHAPE_FILE_NUMBER			= 444, //REAL TPG 기본 형상 파일 번호(0:선택하지 않음) }				
	PA_REAL_TPG_SEREEN_SCALE_DISPLAY			= 447, //REAL TPG 화면 자 사용여부(0:사용 안 함 1:사용) }				
	PA_ARRAY_FUNCTION_TYPE						= 448, //반복기능 TYPE(0:TYPE 1 1:TYPE 2) }							
	PA_ARRAY_STARTING_DIRECTION					= 449, //반복 시작 방향 (0:X축 1:Y축) }								
	PA_PATH_TRACING_DISPLAY_TYPE				= 450, //경로추적 표시 TYPE(0:일반 1:법선) }							
	PA_TOOL_PATH_DISPLAY_TYPE					= 453, //Tool Path Display Type(0:Work 1:Machine)}								
	
	//프로그램 관리자
	PA_DEFAULT_NC_FILE_DIRECTORY				= 451, //디폴터 NC 경로 사용(0:사용, 1:사용 안 함) 
	PA_PREVIEWING_OF_CUTTING_SHAPE				= 451, //가공 형상 미리 보기 사용(0:사용 안 함, 1:동시보기, 2:형상보기)
	
	// DNC
	PP_COMMUNICATION_PORT						= 2, //통신 포트 (0:COM1, 1:COM2, 2이상:TCP/IP 포트번호)		
	PI_BAUDRATE									= 1 , //BAUDRATE (1200,2400,4800,9600,19200)						
	PI_PARITY_BIT									= 3 , //PARITY BIT (0:NONE,1:ODD,2:EVEN)							
	PI_DATA_BIT										= 5 , //DATA BIT													
	PI_STOP_BIT										= 7 , //STOP BIT													
	PI_EOT_CODE										= 9 , //EOT CODE (0:NONE,1:0X03,2:0X04,3:0X14)					
	PI_USER_CONFIRM_ON_THE_CLIENT_CONNECTING		= 11, //클라이언트 접속시, 관리자 확인 절차(0:생략, 1:확인)		
	PI_SWITCHING_TO_RECEIVING_READY_AFTER_BOOTING	= 12, //부팅시, 기계상태 송신용 소켓을 자동으로 수신대기 모드로 전환
	PI_PERIODIC_SENDING_THE_MACHINE_STATUS_TO_CLIENT= 13 //DNC모드에서, 클라이언트에 기계상태를 주기적으로 송신		


};
enum HXMacro{
	//매크로 프로그램
	PA_MACRO_PROGRAM_EDITION								= 2   , //매크로 프로그램 편집 가능 (0:불가 1:가능)}  			
	PI_MACRO_PROGRAM_STOP_ON_SINGLE_BLOCK					= 83  , //매크로 프로그램 싱글블록 정지 (0:유 1:무)}				
	PI_MACRO_PROGRAM_BLOCK_DISPLAY							= 84  , //매크로 프로그램 블록 표시 (0:무 1:유)}      			
	PI_MACRO_PROGRAM_NUMBER_CALLED_FOR_T_CODE_INSTRUCTION	= 105 , //T 코드 지령시 호출되는 매크로 프로그램 번호(9000~9009)} 
	PI_MACRO_CALL_FOR_T_CODE_INSTRUCTION					= 106 , //T 코드 지령시 매크로 호출 (0:안함 1:함)}    			
	
	//매크로 변수
	PI_GLOBAL_MACRO_VARIABLE_INITIALIZE_AT_RESET			= 74, //리셋시 전역 매크로(비저장형 매크로) 변수 초기화 (0:유 1:무)

	// 매크로 호출 G Code/ Mcode 
	PI_9010NC_CALLING_G_CODE	= 85 , //	9010.nc 호출 G Code
	PI_9011NC_CALLING_G_CODE	= 86 , //	9011.nc 호출 G Code
	PI_9012NC_CALLING_G_CODE	= 87 , //	9012.nc 호출 G Code
	PI_9013NC_CALLING_G_CODE	= 88 , //	9013.nc 호출 G Code
	PI_9014NC_CALLING_G_CODE	= 89 , //	9014.nc 호출 G Code
	PI_9015NC_CALLING_G_CODE	= 90 , //	9015.nc 호출 G Code
	PI_9016NC_CALLING_G_CODE	= 91 , //	9016.nc 호출 G Code
	PI_9017NC_CALLING_G_CODE	= 92 , //	9017.nc 호출 G Code
	PI_9018NC_CALLING_G_CODE	= 93 , //	9018.nc 호출 G Code
	PI_9019NC_CALLING_G_CODE	= 94 , //	9019.nc 호출 G Code
	PI_9020NC_CALLING_M_CODE	= 95 , //	9020.nc 호출 M Code
	PI_9021NC_CALLING_M_CODE	= 96 , //	9021.nc 호출 M Code
	PI_9022NC_CALLING_M_CODE	= 97 , //	9022.nc 호출 M Code
	PI_9023NC_CALLING_M_CODE	= 98 , //	9023.nc 호출 M Code
	PI_9024NC_CALLING_M_CODE	= 99 , //	9024.nc 호출 M Code
	PI_9025NC_CALLING_M_CODE	= 100, //	9025.nc 호출 M Code
	PI_9026NC_CALLING_M_CODE	= 101, //	9026.nc 호출 M Code
	PI_9027NC_CALLING_M_CODE	= 102, //	9027.nc 호출 M Code
	PI_9028NC_CALLING_M_CODE	= 103, //	9028.nc 호출 M Code
	PI_9029NC_CALLING_M_CODE	= 104, //	9029.nc 호출 M Code
	PI_9100NC_CALLING_G_CODE	= 190, //	9100.nc 호출 G Code
	PI_9101NC_CALLING_G_CODE	= 191, //	9101.nc 호출 G Code
	PI_9102NC_CALLING_G_CODE	= 192, //	9102.nc 호출 G Code
	PI_9103NC_CALLING_G_CODE	= 193, //	9103.nc 호출 G Code
	PI_9104NC_CALLING_G_CODE	= 194, //	9104.nc 호출 G Code
	PI_9105NC_CALLING_G_CODE	= 195, //	9105.nc 호출 G Code
	PI_9106NC_CALLING_G_CODE	= 196, //	9106.nc 호출 G Code
	PI_9107NC_CALLING_G_CODE	= 197, //	9107.nc 호출 G Code
	PI_9108NC_CALLING_G_CODE	= 198, //	9108.nc 호출 G Code
	PI_9109NC_CALLING_G_CODE	= 199, //	9109.nc 호출 G Code
	PI_9110NC_CALLING_G_CODE	= 200, //	9110.nc 호출 G Code
	PI_9111NC_CALLING_G_CODE	= 201, //	9111.nc 호출 G Code
	PI_9112NC_CALLING_G_CODE	= 202, //	9112.nc 호출 G Code
	PI_9113NC_CALLING_G_CODE	= 203, //	9113.nc 호출 G Code
	PI_9114NC_CALLING_G_CODE	= 204, //	9114.nc 호출 G Code
	PI_9115NC_CALLING_G_CODE	= 205, //	9115.nc 호출 G Code
	PI_9116NC_CALLING_G_CODE	= 206, //	9116.nc 호출 G Code
	PI_9117NC_CALLING_G_CODE	= 207, //	9117.nc 호출 G Code
	PI_9118NC_CALLING_G_CODE	= 208, //	9118.nc 호출 G Code
	PI_9119NC_CALLING_G_CODE	= 209, //	9119.nc 호출 G Code
	PI_9120NC_CALLING_G_CODE	= 210, //	9120.nc 호출 G Code
	PI_9121NC_CALLING_G_CODE	= 211, //	9121.nc 호출 G Code
	PI_9122NC_CALLING_G_CODE	= 212, //	9122.nc 호출 G Code
	PI_9123NC_CALLING_G_CODE	= 213, //	9123.nc 호출 G Code
	PI_9124NC_CALLING_G_CODE	= 214, //	9124.nc 호출 G Code
	PI_9125NC_CALLING_G_CODE	= 215, //	9125.nc 호출 G Code
	PI_9126NC_CALLING_G_CODE	= 216, //	9126.nc 호출 G Code
	PI_9127NC_CALLING_G_CODE	= 217, //	9127.nc 호출 G Code
	PI_9128NC_CALLING_G_CODE	= 218, //	9128.nc 호출 G Code
	PI_9129NC_CALLING_G_CODE	= 219, //	9129.nc 호출 G Code
	PI_9130NC_CALLING_G_CODE	= 220, //	9130.nc 호출 G Code
	PI_9131NC_CALLING_G_CODE	= 221, //	9131.nc 호출 G Code
	PI_9132NC_CALLING_G_CODE	= 222, //	9132.nc 호출 G Code
	PI_9133NC_CALLING_G_CODE	= 223, //	9133.nc 호출 G Code
	PI_9134NC_CALLING_G_CODE	= 224, //	9134.nc 호출 G Code
	PI_9135NC_CALLING_G_CODE	= 225, //	9135.nc 호출 G Code
	PI_9136NC_CALLING_G_CODE	= 226, //	9136.nc 호출 G Code
	PI_9137NC_CALLING_G_CODE	= 227, //	9137.nc 호출 G Code
	PI_9138NC_CALLING_G_CODE	= 228, //	9138.nc 호출 G Code
	PI_9139NC_CALLING_G_CODE	= 229, //	9139.nc 호출 G Code
	PI_9140NC_CALLING_G_CODE	= 230, //	9140.nc 호출 G Code
	PI_9141NC_CALLING_G_CODE	= 231, //	9141.nc 호출 G Code
	PI_9142NC_CALLING_G_CODE	= 232, //	9142.nc 호출 G Code
	PI_9143NC_CALLING_G_CODE	= 233, //	9143.nc 호출 G Code
	PI_9144NC_CALLING_G_CODE	= 234, //	9144.nc 호출 G Code
	PI_9145NC_CALLING_G_CODE	= 235, //	9145.nc 호출 G Code
	PI_9146NC_CALLING_G_CODE	= 236, //	9146.nc 호출 G Code
	PI_9147NC_CALLING_G_CODE	= 237, //	9147.nc 호출 G Code
	PI_9148NC_CALLING_G_CODE	= 238, //	9148.nc 호출 G Code
	PI_9149NC_CALLING_G_CODE	= 239, //	9149.nc 호출 G Code
	PI_9150NC_CALLING_G_CODE	= 240, //	9150.nc 호출 G Code
	PI_9151NC_CALLING_G_CODE	= 241, //	9151.nc 호출 G Code
	PI_9152NC_CALLING_G_CODE	= 242, //	9152.nc 호출 G Code
	PI_9153NC_CALLING_G_CODE	= 243, //	9153.nc 호출 G Code
	PI_9154NC_CALLING_G_CODE	= 244, //	9154.nc 호출 G Code
	PI_9155NC_CALLING_G_CODE	= 245, //	9155.nc 호출 G Code
	PI_9156NC_CALLING_G_CODE	= 246, //	9156.nc 호출 G Code
	PI_9157NC_CALLING_G_CODE	= 247, //	9157.nc 호출 G Code
	PI_9158NC_CALLING_G_CODE	= 248, //	9158.nc 호출 G Code
	PI_9159NC_CALLING_G_CODE	= 249, //	9159.nc 호출 G Code
	PI_9160NC_CALLING_G_CODE	= 250, //	9160.nc 호출 G Code
	PI_9161NC_CALLING_G_CODE	= 251, //	9161.nc 호출 G Code
	PI_9162NC_CALLING_G_CODE	= 252, //	9162.nc 호출 G Code
	PI_9163NC_CALLING_G_CODE	= 253, //	9163.nc 호출 G Code
	PI_9164NC_CALLING_G_CODE	= 254, //	9164.nc 호출 G Code
	PI_9165NC_CALLING_G_CODE	= 255, //	9165.nc 호출 G Code
	PI_9166NC_CALLING_G_CODE	= 256, //	9166.nc 호출 G Code
	PI_9167NC_CALLING_G_CODE	= 257, //	9167.nc 호출 G Code
	PI_9168NC_CALLING_G_CODE	= 258, //	9168.nc 호출 G Code
	PI_9169NC_CALLING_G_CODE	= 259, //	9169.nc 호출 G Code
	PI_9170NC_CALLING_G_CODE	= 260, //	9170.nc 호출 G Code
	PI_9171NC_CALLING_G_CODE	= 261, //	9171.nc 호출 G Code
	PI_9172NC_CALLING_G_CODE	= 262, //	9172.nc 호출 G Code
	PI_9173NC_CALLING_G_CODE	= 263, //	9173.nc 호출 G Code
	PI_9174NC_CALLING_G_CODE	= 264, //	9174.nc 호출 G Code
	PI_9175NC_CALLING_G_CODE	= 265, //	9175.nc 호출 G Code
	PI_9176NC_CALLING_G_CODE	= 266, //	9176.nc 호출 G Code
	PI_9177NC_CALLING_G_CODE	= 267, //	9177.nc 호출 G Code
	PI_9178NC_CALLING_G_CODE	= 268, //	9178.nc 호출 G Code
	PI_9179NC_CALLING_G_CODE	= 269, //	9179.nc 호출 G Code
	PI_9180NC_CALLING_G_CODE	= 270, //	9180.nc 호출 G Code
	PI_9181NC_CALLING_G_CODE	= 271, //	9181.nc 호출 G Code
	PI_9182NC_CALLING_G_CODE	= 272, //	9182.nc 호출 G Code
	PI_9183NC_CALLING_G_CODE	= 273, //	9183.nc 호출 G Code
	PI_9184NC_CALLING_G_CODE	= 274, //	9184.nc 호출 G Code
	PI_9185NC_CALLING_G_CODE	= 275, //	9185.nc 호출 G Code
	PI_9186NC_CALLING_G_CODE	= 276, //	9186.nc 호출 G Code
	PI_9187NC_CALLING_G_CODE	= 277, //	9187.nc 호출 G Code
	PI_9188NC_CALLING_G_CODE	= 278, //	9188.nc 호출 G Code
	PI_9189NC_CALLING_G_CODE	= 279, //	9189.nc 호출 G Code
	PI_9190NC_CALLING_G_CODE	= 280, //	9190.nc 호출 G Code
	PI_9191NC_CALLING_G_CODE	= 281, //	9191.nc 호출 G Code
	PI_9192NC_CALLING_G_CODE	= 282, //	9192.nc 호출 G Code
	PI_9193NC_CALLING_G_CODE	= 283, //	9193.nc 호출 G Code
	PI_9194NC_CALLING_G_CODE	= 284, //	9194.nc 호출 G Code
	PI_9195NC_CALLING_G_CODE	= 285, //	9195.nc 호출 G Code
	PI_9196NC_CALLING_G_CODE	= 286, //	9196.nc 호출 G Code
	PI_9197NC_CALLING_G_CODE	= 287, //	9197.nc 호출 G Code
	PI_9198NC_CALLING_G_CODE	= 288, //	9198.nc 호출 G Code
	PI_9199NC_CALLING_G_CODE	= 289 //	9199.nc 호출 G Code
};

enum HXHMI{
	//HMI Setting
	PA_ALT_X_EXIT_USAGE_STATUS			= 328 , //	Alt-X 종료 사용유무 (0:사용, 1:사용안함)  
	PA_WORK_COORDINATE_FONT_SETTING		= 405 , //	작업물 좌표계 Font Setting(0 ~ 6)          
	PP_TOTAL_SCREEN_WIDTH				= 3   , //	전체화면 폭 (0-9999, 0: 자동설정)			 
	PP_TOTAL_SCREEN_HEIGHT				= 4   , //	전체화면 높이 (0-1999, 0: 자동설정)		
	PP_SIZE_OF_MAIN_SCREEN				= 1900, //	Main 화면 크기 (1: 800*600  2:1024*768)	
	//MACHINE_EQUIPMENT_NAME				=   0 , //	기종 이름		
	// MACHINE_EQUIPMENT_NAME  :함수에서 번호 겹침, 다른 함수 하나 만들것 
	// 모드에 따른 자동 화면 전환			
	PA_SCREEN_AUTOMATICAL_CHANGING_BY_MODE	= 323, //모드 전환시 화면 전환 유무 (0:유 1:무)		
	PP_TARGET_SCREEN_FOR_DNC_MODE			= 30, //DNC 모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_EDIT_MODE			= 31, //EDIT모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_AUTO_MODE			= 32, //AUTO모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_MDI_MODE			= 33, //MDI 모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_JOG_MODE			= 34, //JOG 모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_STEP_MODE			= 35, //STEP모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_REF_MODE			= 36, //REF 모드시 전환할 화면(그룹키번호+화면키번호)
	PP_TARGET_SCREEN_FOR_MPG_MODE			= 37, //MPG 모드시 전환할 화면(그룹키번호+화면키번호)

	//	바로가기 화면 지정				
	PA_F1_TARGET_SCREEN 	= 30, //바로가기 F1 전환 화면 (그룹키번호+화면키번호)
	PA_F2_TARGET_SCREEN 	= 31, //바로가기 F2 전환 화면 (그룹키번호+화면키번호)
	PA_F3_TARGET_SCREEN 	= 32, //바로가기 F3 전환 화면 (그룹키번호+화면키번호)
	PA_F4_TARGET_SCREEN 	= 33, //바로가기 F4 전환 화면 (그룹키번호+화면키번호)
	PA_F5_TARGET_SCREEN 	= 34, //바로가기 F5 전환 화면 (그룹키번호+화면키번호)
	PA_F6_TARGET_SCREEN 	= 35, //바로가기 F6 전환 화면 (그룹키번호+화면키번호)
	PA_F7_TARGET_SCREEN 	= 36, //바로가기 F7 전환 화면 (그룹키번호+화면키번호)
	PA_F8_TARGET_SCREEN 	= 37, //바로가기 F8 전환 화면 (그룹키번호+화면키번호)
	PA_F9_TARGET_SCREEN 	= 38, //바로가기 F9 전환 화면 (그룹키번호+화면키번호)

	// 축 표시 설정
	PA_AUTOMATIC_AXIS_DISPLAY_USAGE_STATUS					= 406 , //자동 축 표시 사용 유무 (0:사용 1:사용안함) 						
	PA_AXIS_DISPLAY_FORMAT									= 330 , //FORMAT (전체 자릿수.소수점이하 자릿수) 기본값: 10.3 	
	PA_RADIUS_DIAMETER_DISPLAY_SETTING						= 329 , //반경치/직경치 표시 설정 (0:반경치, 1:직경치)          
	PA_RADIUS_DIAMETER_DISPLAY_USAGE_STATUS_PER_AXIS		= 331 , //축별 직경치/반경치 표시 적용 유무 (0:적용안함 1:적용함)
	PA_DISPLAY_UNIT											= 0   , //길이 표시 단위계 (0:METRIC, 1:INCH)                   
	PA_INCH_METRIC_USAGE_STATUS_PER_AXIS					= 374 , //축별 INCH/METRIC 적용 유무 (0:적용안함 1:적용함)		
	//AX_AXIS_NAME											=    0, //축 이름(MAX. 2)										
	//AX_AXIS_NAME :함수에서 번호 겹침, 다른 함수 하나 만들것 
	
	PA_SCREEN_DISPLAY_OF_AXIS_INFORMATION_STATUS			= 418 , //정보 화면에 AXIS 표시 유무(0:표시함 1:표시안함)		


	PP_0_Font_Width		= 6 , //0번 Font Width  (Default: 6)
	PP_0_Font_Height	= 13, //0번 Font Height (Default: 12)
	PP_1_Font_Width		= 7 , //1번 Font Width  (Default: 10)
	PP_1_Font_Height	= 14, //1번 Font Height (Default: 20)
	PP_2_Font_Width		= 8 , //2번 Font Width  (Default: 16)
	PP_2_Font_Height	= 15, //2번 Font Height (Default: 33)
	PP_3_Font_Width		= 9 , //3번 Font Width  (Default: 35)
	PP_3_Font_Height	= 16, //3번 Font Height (Default: 70)
	PP_4_Font_Width		= 10, //4번 Font Width  (Default: 20)
	PP_4_Font_Height	= 17, //4번 Font Height (Default: 40)
	PP_5_Font_Width		= 11, //5번 Font Width  (Default: 25)
	PP_5_Font_Height	= 18, //5번 Font Height (Default: 50)
	PP_6_Font_Width		= 12, //6번 Font Width  (Default: 8)
	PP_6_Font_Height	= 19 //6번 Font Height (Default: 16)				
				
};																


//------------------------------
// parameter - Machining
//------------------------------
enum HXMachining{
	// 자동 가감속 설정
	PM_SPINDLE_ACCELDECELTIME = 525, // 스핀들(속도형 PLC 제어축)의 가감속 시정수 설정
	PM_RAPID_ACCELDECELTIME = 561, // 급속(수동)이송 가감속 시정수 설정 (32축)
	PM_G01_ADCCELDECELTYPE = 598, // 절삭 이송 가감속 형태(0:직선형, 1 : S자형, 2 : 지수형)
	PM_G01_ACCELDECELTIME = 599, // 절삭 이송 가감속 시정수
	// 보간전 가감속 설정
	PM_USE_ACCELDECELTIME_BEFORE_INTERPOLATION = 605,	// 보간전 가감속 사용 여부(0:사용안함, 1 : 사용함)
	PM_ACCELDECELTIME_BEFORE_INTERPOLATION =  608,	// 보간전 가감속 시정수
	PM_ACCELDECELTIME_AFTER_INTERPOLATION = 611,	// 보간전 가감속의 보간후 가감속 시정수
	PM_MIN_ACCELDECELFEED  = 614,	// 보간전 가감속 최저 속도
	PM_ACCELDECCELFEED_VECTOR_ERR = 617,	// 보간전 가감속 벡터오차 허용값

	// 모서리 속도 제한 기능
	PM_USE_LIMITFEED_AT_CORNER = 660,	// 모서리 속도 제한 기능 모드(0:사용안함, 1 : 각도, 2 : 속도차)
	PM_SET_LIMITANGLE_AT_CORNER = 661,	// 허용 각도 설정(각도 모드)
	PM_SET_LIMI_DEFFERENCE_AT_CORNER = 662,		// 허용 속도차 설정(속도차 모드)
	PM_SET_DECELFEED_AT_CORNER = 663,	// 감속 속도 설정
	PM_SET_FEED_SCALE_AT_CORNER = 664,	// 회전축의 직선축에 대한 속도 배율(속도차 모드)

	// 고속가공 기능 설정
	PM_G10_3_TYPE = 680, // 고속가공 종류 선택(0:TYPE 1, 1 : TYPE 2, 2 : TYPE 3)
	PM_G10_3_ACCELDECELTIME_BEFORE_INTERPOLATION = 701, // 고속가공 보간전 가감속 시정수
	PM_G10_3_ACCELDECELTIME_AFGER_INTERPOLATION = 704, // 고속가공 보간후 가감속 시정수(TYPE2, TYPE3)
	PM_G10_3_MAX_G01FEED = 710, // 고속가공 최고 절삭 속도
	PM_G10_3_MIN_G01FEED = 710, // 고속가공 최저 절삭 속도
	PM_G10_3_VECTOR_ERR = 710, // 고속가공 벡터오차 허용값
	PM_G10_3_SURFACE_ERR = 710, // 고속가공 형상오차 허용치(TYPE 1)
	PM_G10_3_MAX_PRECEDE_FACTOR = 710, // 고속가공 선행 보간 FACTOR
	PM_USE_G10_3_R_CUT_FEED_LIMIT = 710, // R 절삭속도 제한기능 사용 여부(TYPE2, 3) (0:사용안함 1 : 사용함)
	PM_G10_3_R_CUT_MAX_BLOCK = 710, // R 절삭속도 제한기능 적용 최대 블록 길이(TYPE2, TYPE3)
	PM_G10_3_R_CUT_STANDARD_RADIUS = 710, // R 절삭속도 제한기능 기준 반경(TYPE2, TYPE3)
	PM_G10_3_R_CUT_STANDARD_FEED = 710, // R 절삭속도 제한기능 기준 가공속도(TYPE2, TYPE3)
	PM_G10_3_G01FEED_TYPE = 710, // 고속가공 가공속도 선택(0:지령속도, 1 : 최대 고속가공속도)
	PM_G10_3_G00FEED_TYPE = 710, // 고속가공중 급송이송(G00) 블록의 처리(0:고속가공, 1 : 일반가공)
	
	//수동 기능 설정
	PM_MANUAL_MOTION_FEED_TABLE = 1160, // 수동 이송속도 테이블
	PM_FEED_SCALE_AT_MANUAL_MOTION = 1192, // 회전축의 직선축에 대한 수동 이송속도 배율
	PM_RAPID_JOG_SCALE_BEFORE_RETURN_ORIGIN = 1398, // 원점 복귀 전의 급속 JOG 배율
	PM_POLARITY_MPG_PULSE =	1509, // MPG PULSE 입력 극성 설정(0:+, 1 : -)
	PM_MPG_UNIT = 1512, // MPG 이송의 기본 제어 단위
	PM_MPG_MAX_FEED	= 1547, // MPG 이송의 최대 속도
	PM_STEP_MOTION_DISTANCE_TABLE =	1623, // STEP 이송거리 테이블
	PM_FEED_SCALE_AT_STEP_MOTION =1655, // 회전축의 직선축에 대한 STEP 이송거리 배율 설정

	pm_position_orgin = 1710, //  기계 원점 좌표

	PM_USE_ARBITRARY_ORIGIN = 1741, //  임의의 위치 원점 지정 기능(0:사용안함, 1 : 사용)
	PM_USE_ORIGIN_DOG = 1773, //  원점 DOG신호 사용 여부(0:사용, 1 : 사용안함)
	PM_ORIGIN_RETURN_PROHIBITION_AREA = 1805, //  원점 복귀 금지영역(32축)
	PM_ORIGIN_RETURN_RAPID_FEED = 1887, //  원점 복귀 급속이송속도(32축)
	PM_ORIGIN_RETURN_FEED_1STDECEL = 1919, //  원점 복귀 1차 감속이송속도(32축)
	PM_ORIGIN_RETURN_FEED_2NDDECEL = 1951, //  원점 복귀 2차 감속이송속도(C상 검출속도)
	PM_ORIGIN_RETURN_GRIDSHIFT_FEED = 1983, //  GRID SHIFT 이송속도
	PM_ORIGIN_RETURN_GRIDSHIFT = 2015, //  GRID SHIFT 거리
	PM_ORIGIN_RETURN_CPHASE_ERR = 2047, //  C상 검출시의 최대 허용 축 이송량
	PM_POSITION_ORGIN_2ND = 2097, //  2원점의 좌표
	PM_POSITION_ORGIN_3RD = 2129, //  3원점의 좌표
	PM_POSITION_ORGIN_4TH = 2161, //  4원점의 좌표
	PM_POSITION_ORGIN_1ST = 2193, //  제1원점의 좌표 인식범위
	PM_COGNIZANCE_ORIGIN_2ND = 2257, //  제2원점의 좌표 인식범위
	PM_COGNIZANCE_ORIGIN_3RD = 2321, //  제3원점의 좌표 인식범위
	PM_COGNIZANCE_ORIGIN_4TH = 2385, //  제4원점의 좌표 인식범위


	//------------------------ 가공 2 --------------------------------//
	PM_USE_RAPID_SKIP = 4800, //  고속 SKIP 신호 사용 여부(0:사용안함 1 : 사용함) 
	//자동 기능 설정
	PM_USE_INTERPOLATION_G00 = 4720, // 보간형 G00 사용 여부(0:사용안함, 1 : 사용)
	PM_INTERPOLATION_G00_ACCELDECELTIME = 4722, // 보간형 G00 가감속 시정수
	PM_INTERPOLATION_G00_FEED = 4723, // 보간형 G00 이송 속도

	PM_RAPID_FEED = 2759, // 급속 이송 속도 설정
	PM_RAPID_OVERRIDE_TABLE = 2791, // 급속 이송 오버라이드 테이블
	PM_G00FEED_AT_DRNMODE = 2828, // 드라이런 모드에서 G00블록의 이송속도(0:수동설정 1 : 급속이송)
	PM_MAX_G01_FEED = 2870, // 절삭이송 상한 속도 설정
	PM_MIN_G01_FEED = 2871, // 절삭이송 하한 속도 설정
	PM_MAX_G01_FEED_OF_ROTATION = 2872, // 회전축의 절삭이송 상한 속도 설정
	PM_EXCEPTION_OVER_FEED = 2874, // 절삭이송 상한 속도 초과시의 NC조치 동작 설정(0 / 1)
	PM_TIME_FOR_G01_FEED_OVERRIDE = 2889, // 절삭 이송속도 오버라이드 변동 시간
	PM_G01_FEED_OVERRIDE_TABLE = 2891, // 절삭 이송속도 오버라이드 테이블
	PM_INPOSITION = 2928, // IN POSITION 범위


	//스핀들 기능 설정 
	PM_SPINDLE_OVERRIDING_CHANGING_TIME = 3242, // 스핀들 오버라이드 변동 시간
	PM_SPINDLE_OVERRIDE_TABLE = 3244, // 스핀들 오버라이드 테이블
	PM_USE_CMD_ROTATING_SPINDLE_FEED = 3276, // 수동 운전에서 스핀들 회전 속도 지령 여부(0:사용안함 1 : 사용함)
	PM_SPINDLE_ROTATING_FEED_TABLE = 3277, // 수동 운전에서 스핀들 회전 속도 테이블
	PM_SPINDLE_SS_AXIS_NO = 3313, // SS 제어를 사용하는 스핀들의 축번호
	PM_SPINDLE_SS_AXIS_NAME = 3316, // SS 제어시의 스핀들의 축명칭
	PM_SPINDLE_SS_USE_AUTO_ORIGIN_RETURN = 3319, // SS 제어에서 자동원점 복귀 여부(0:사용안함 1 : 사용함)
	PM_SPINDLE_G96_STANDARD_AXIS = 3359, // 주속일정 제어시 기준축(X:1, Y : 2, Z : 3, A : 4, B : 5, C : 6, U : 7, V : 8, W : 9)
	PM_SPINDLE_G96_STANDARD_MAX_TURN = 3360, // 주속일정 제어시 스핀들 최고 회전수
	PM_SPINDLE_G96_STANDARD_MIN_TURN = 3361, // 주속일정 제어시 스핀들 최저 회전수
	PM_SPINDLE_ORIENTATION_MCODE = 3365, // 스핀들 오리엔테이션 M code


	// 소프트 리미트 기능 설정
	PM_USE_SOFTLIMIT = 3378, // 소프트 리미트 사용 여부(0:사용함 1 : 사용안함) #1~#32
	PM_SOFTLIMIT_AREA = 3410, // 소프트 리미트 구역 ( 1축당 2개씩 연결해서 사용 )
	PM_USE_G22_BOUND = 3474, // G22 이송 금지 구역 사용 여부(0:유효 1 : 무효)
	PM_G22_LIMIT_INNERSIDE = 3475, // G22 이송 금지 구역 내 / 외측 설정(0:내측 1 : 외측)
	PM_G22_LIMIT_X = 3476, // X축의 G22 이송 금지 구역 범위
	PM_G22_LIMIT_Y = 3478, // Y축의 G22 이송 금지 구역 범위
	PM_G22_LIMIT_Z = 3480, // Z축의 G22 이송 금지 구역 범위
	PM_USE_G22_LIMIT = 3482, // 제3 이송 금지 구역 사용 여부(0:유효 1 : 무효)
	PM_3RD_LIMIT_X = 3483, // X축의 제3 이송 금지 구역 범위
	PM_3RD_LIMIT_Y = 3485, // Y축의 제3 이송 금지 구역 범위
	PM_3RD_LIMIT_Z = 3487, // Z축의 제3 이송 금지 구역 범위
	PM_LIMIT_AXIS_DIRECTION = 3489, // 축 위치 출력 기능 범위

	// 외부 감속 기능
	PM_USE_EXTERNAL_DECEL_POSITIVE = 3652, // 외부감속기능 설정(+)(0:사용안함 1 : 급속이송 2 : 급속 / 절삭)
	PM_USE_EXTERNAL_DECEL_NEGATIVE = 3684, // 외부감속기능 설정(-)(0:사용안함 1 : 급속이송 2 : 급속 / 절삭)
	PM_EXTERNAL_DECEL_FEED= 3716, // 외부 감속시의 절삭 속도
	PM_EXTERNAL_DECEL_RAPID_FEED = 3717, // 외부 감속시의 급속(수동)이송 속도

	// 보조 코드 기능
	PM_USE_MULTI_MCODE = 4399, // MULTI M CODE 기능 사용 여부(0:사용안함 1 : 사용함)

	// 가공 기능 설정
	PM_ARC_ACCELDECELTIME = 4425, // 원호가공 가감속 시정수
	PM_ARC_INTERPOLATION_ERR = 4428, // 원호 가공 허용 보간오차
	PM_USE_ARC_FEED_LIMIT = 4430, // 원호 가공 속도제한 기능 사용 유무(0:사용안함 1 : 사용함)
	PM_RADIUS_OF_ARC_FEED_LIMIT = 4433, // 원호 가공 속도제한 기능 적용 원호 반지름
	PM_MAX_FEED_OF_ARC = 4434, // 원호 가공 속도제한 상한 절삭 속도
	PM_MIN_FEED_OF_ARC = 4435, // 원호 가공 속도제한 하한 절삭 속도

	PM_SCREW_BACK_ANGLE = 4539, // 불완전 나사 가공시 빠지는 각도
	PM_SCREW_LENGTH = 4540, // 불완전 나사의 길이(피치의 배수) (0.0 ~9.9)

	PM_RIGIDTAP_PASSIVE = 7690, // RIGID TAP PASSIVE(0:OFF 1 : ON)          				1   0   0
	PM_RIGIDTAP_ACCELDECELTIME_TYPE = 4560, // RIGID TAP에서 스핀들과 Z축의 가감속형태(0:직선 1 : S자 2 : 지수)
	PM_RIGIDTAP_ACCELDECELTIME_Z = 4561, // RIGID TAP에서 각 기어단의 스핀들과 Z축의 가감속 시간 (#1 ~ #4)
	PM_RIGIDTAP_RETREAT = 4565, // RIGID TAP에서 각 기어단의 후퇴동작 스핀들과 Z축의 가감속 시간(#1 ~ #4)
	PM_RIGIDTAP_MAX_RPM = 4569, // RIGID TAP에서 각 기어단의 스핀들 최대 회전수(#1 ~ #4)
	PM_RIGIDTAP_RETREAT_OVERRIDE = 4577, // RIGID TAP에서 후퇴동작 오버라이드
	PM_RIGIDTAP_INPOSITION = 4578, // RIGID TAP에서 IN POSITION RANGE
	PM_RIGIDTAP_PITCH_ERR = 4579, // RIGID TAP에서 피치 오차 허용 범위
	PM_RIGIDTAP_BACKLASH = 4581, // RIGID TAP에서 각 기어단의 스핀들 백래쉬 보정량
	PM_RIGIDTAP_Z_GAIN = 4589, // RIGID TAP에서 Z축 위치 게인
	PM_RIGIDTAP_SPINDLE_GAIN = 4590, // RIGID TAP에서 각 기어단의 스핀들 위치 게인
	PM_RIGIDTAP_Z_FORWARD_GAIN = 4595, // RIGID TAP에서 Z축 피드포워드 게인
	PM_RIGIDTAP_SPINDLE_FEEDFORWARD_GAIN = 4596, // RIGID TAP에서 각 기어단의 스핀들 피드포워드 게인
	PM_RIGIDTAP_SYNC_err = 4600, // Rigid Tap에서 각 기어단의 동기 오차 보상 게인

	PM_POLAR_INTERPOLATION_LINEAL_AXIS = 4623, // 극좌표 보간시 직선축(X:1 Y : 2 Z : 3 A : 4 B : 5 C : 6 U : 7 V : 8 W : 9)
	PM_POLAR_INTERPOLATION_ROTATION_AXIS = 4624, // 극좌표 보간시 회전축(X:1 Y : 2 Z : 3 A : 4 B : 5 C : 6 U : 7 V : 8 W : 9)
	PM_POLAR_INTERPOLATION_ROTATION_AXIS_FEED_LIMIT = 4627, // 극좌표 보간시 회전축의 허용 이송속도 설정
	PM_CHOPPING_AXIS = 4636, // CHOPPING 제어축 번호
	PM_CHOPPING_R = 4638, // CHOPPING R점
	PM_CHOPPING_MAX_POSITION = 4639, // CHOPPING 상사점
	PM_CHOPPING_MIN_POSITION = 4640, // CHOPPING 하사점
	PM_CHOPPING_FEED = 4642, // CHOPPING 속도
	PM_CHOPPING_OVERRIDE = 4644, // CHOPPING 오버라이드
	PM_CHOPPING_INPOSITION = 4662, // CHOPPING IN - POSITION RANGE
	PM_USE_HIGH_SPEED_SKIP = 4680, // 고속 SKIP 신호 사용 여부(0:사용안함 1 : 사용함)
	PM_HIGH_SPEED_SKIP_ADDR = 4684, // 고속 SKIP 신호 어드레스 설정
	PM_USE_HIGH_SPEED_AUTO_COMPENSATION = 4695, // 고속 자동 공구보정 신호 사용 여부(0:사용안함 1 : 사용함)
	PM_HIGH_SPEED_AUTO_COMPENSATION_ADDR = 4699, // 고속 자동 공구보정 신호 어드레스 설정

};

enum // Mode 설정 bit
{
	// G1.xx
	HX_MODE_AUTO = 0x00,
	HX_MODE_MDI = 0x01,
	HX_MODE_DNC = 0x02,
	HX_MODE_ZRN = 0x03,
	HX_MODE_JOG = 0x04,
	HX_MODE_MPG = 0x05,
	HX_MODE_EDIT = 0x07,
	HX_MODE_STEP = 0x06,

	// F1.xx
	HX_MODE_AUTO_SIGNAL = 0x10,
	HX_MODE_MDI_SIGNAL = 0x11,
	HX_MODE_DNC_SIGNAL = 0x12,
	HX_MODE_ZRN_SIGNAL = 0x13,
	HX_MODE_JOG_SIGNAL = 0x14,
	HX_MODE_MPG_SIGNAL = 0x15,
	HX_MODE_STEP_SIGNAL = 0x16,
	HX_MODE_EDIT_SIGNAL = 0x17,
};

enum // NC 제어 신호
{
	// G9.xx
	HX_NC_CYCLESTART			= 0x00,
	HX_NC_FEEDHOLD				= 0x02,
	HX_NC_PROGRAM_CHANGE		= 0x08, // 프로그램 변경 지령 신호

	// F7.xx
	HX_NC_SCHEDULE_START_SIGNAL = 0x00, // 스케줄링 기능 Cycle Start 신호
	HX_NC_PROGRAM_CHANGE_SIGNAL = 0x08, // 프로그램 변경 지령 신호

	// F8.xx
	HX_NC_CYCLE_START_SIGNAL	= 0x00, // 자동 운전중(Feed Hold 포함)
	HX_NC_FEEDHOLD_SIGNAL		= 0x01, // 자동 운전 휴지중(Feed Hold)
	HX_NC_OPERATING_SIGNAL		= 0x02, // 자동 운전중(Feed Hold 제외)
};

enum
{
	// G0.xx
	HX_SYSTEM_RUN			= 0x00,	// 상위가 정상적으로 수행중임 PC->NC

	// F0.xx
	HX_SYSTEM_RUN_SIGNAL	= 0x00,	// CNC 계통 이상 없음 신호
	HX_AXIS_RUN_SIGNAL		= 0x01,	// 서보 스핀들 계통 이상없음 신호
	HX_ECAT_OP_SIGNAL		= 0x1F,	// EtherCAT OP 진입 신호
};

enum
{
	HX_SUBMODE_SINGLEBLOCK = 0x00,
	HX_SUBMODE_OPTIONAL_BLOCKSKIP = 0x01,
	HX_SUBMODE_DRY_RUN = 0x02,
	HX_SUBMODE_MANUAL_ABSOLUTE = 0x03,
	HX_SUBMODE_AUX_CODE_LOCK = 0x04,
	// 0x05 - 비었음.
	HX_SUBMODE_SYSTEM_MACHINE_LOCK = 0x06,
	HX_SUBMODE_OVERRIDE_CANCEL = 0x07,
};

enum
{
	HX_KEY_LOCK = 0x00,
};

enum
{
	// G8.xx
	HX_SYSTEM_RESEET = 0x00,
	HX_AXIS_RESEET = 0x01,
	HX_SYSTEM_EMG = 0x02,
	HX_POWER_OFF = 0x08,

	// F6.xx
	HX_SYSTEM_RESEET_SIGNAL = 0x00,
	HX_SYSTEM_RESEET_MDI_SIGNAL = 0x01,

};

enum
{
	// F7.xx
	HX_SCHEDULE_CYCLE_START_SIGNAL = 0x00,
	HX_PROGRAM_CHANGE_SIGNAL = 0x08,
};