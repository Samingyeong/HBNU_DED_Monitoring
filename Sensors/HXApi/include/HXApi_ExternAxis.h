#pragma once

// param 
enum AxisType{ AXISNONE = 0, SERVO_AXIS, SPINDLEA_XIS};
enum AxisInterface{ IntType_AIB =1, IntType_2, IntType_ECAT, IntType_AIB32, IntType_AIB30V, IntType_AIB30P, IntType_EDIO7246};

// 극성 설정 
enum {eEncCPhase =0, eEnc, eServoReady, eServoAlarm, eVelCmd, eServoOn, eServoReset};



// Spindle 
enum HXSpindle{
	AXIS_SP_MOTOR_TYPE = 21,	// 모터/ 드라이브 종류(1: 일반 스핀들, 2: DIGITAL, 3: 서보모터 
	AXIS_SP_GEARSTEP = 48,
	AXIS_SP_BACKLASH1STEP = 33,	//각 기어단의 백래쉬 양 : 1단
	AXIS_SP_BACKLASH2STEP = 34,	//각 기어단의 백래쉬 양 : 2단
	AXIS_SP_BACKLASH3STEP = 35,	//각 기어단의 백래쉬 양 : 3단
	AXIS_SP_BACKLASH4STEP = 36,	//각 기어단의 백래쉬 양 : 4단

	AXIS_SP_MOTOR_GEAR1STEP = 48,	//각 기어단의 모터측 기어 비 : 1단
	AXIS_SP_MOTOR_GEAR2STEP = 49,	//각 기어단의 모터측 기어 비 : 2단
	AXIS_SP_MOTOR_GEAR3STEP = 50,	//각 기어단의 모터측 기어 비 : 3단
	AXIS_SP_MOTOR_GEAR4STEP = 51,	//각 기어단의 모터측 기어 비 : 4단

	AXIS_SP_MACHINE_GEAR1STEP = 52,	//각 기어단의 기계측 기어 비 : 1단
	AXIS_SP_MACHINE_GEAR2STEP = 53,//각 기어단의 기계측 기어 비 : 2단
	AXIS_SP_MACHINE_GEAR3STEP = 54,//각 기어단의 기계측 기어 비 : 3단
	AXIS_SP_MACHINE_GEAR4STEP = 55,//각 기어단의 기계측 기어 비 : 4단

	AXIS_SP_10V_RPM1STEP = 61, //각 기어단에서 10V에 해당하는 스핀들 회전수 : 1단 
	AXIS_SP_10V_RPM2STEP = 62, //각 기어단에서 10V에 해당하는 스핀들 회전수 : 2단 
	AXIS_SP_10V_RPM3STEP = 63, //각 기어단에서 10V에 해당하는 스핀들 회전수 : 3단 
	AXIS_SP_10V_RPM4STEP = 64, //각 기어단에서 10V에 해당하는 스핀들 회전수 : 4단 

	AXIS_SP_MAX_RPM1STEP = 65, // 각 기어단에서 최대 스핀들 회전수 : 1단 
	AXIS_SP_MAX_RPM2STEP = 66, // 각 기어단에서 최대 스핀들 회전수 : 2단 
	AXIS_SP_MAX_RPM3STEP = 67, // 각 기어단에서 최대 스핀들 회전수 : 3단 
	AXIS_SP_MAX_RPM4STEP = 68, // 각 기어단에서 최대 스핀들 회전수 : 4단 

	AXIS_SP_GEAR_TRANSMISSION_RPM = 69, // 기어변환시 스핀들 회전수 
	AXIS_SP_ENCODER_TYPE	= 86, // ENCODER 체결 방식 (0:없음,1:스핀들모터 직결,2:외부)
	AXIS_SP_ENCODER_PULSE_TYPE = 88, // ENCODER PULSE 출력 방식 (0:LINEAR,1:MODULAR)
	AXIS_SP_ENCODER_RESOLUTION = 93, // ENCODER RESOLUTION(체배 후의 RESOLUTION)

	AXIS_SP_RPM_AGREE_RANGE	= 109,    //스핀들 회전속도 AGREE 범위
	AXIS_SP_ZERO_SPEED_AGREE_RANGE =110,   //스핀들 회전속도 ZERO SPEED AGREE 범위
	AXIS_SP_ORIENTATION_FEED =121,   //스핀들 오리엔테이션 속도
	AXIS_SP_ORIENTATION_DIRECTION =122,   //스핀들 오리엔테이션 방향(0:+, 1 : -)
	AXIS_SP_ORIENTATION_OFFSET =123,   //스핀들 오리엔테이션 옵셋
	AXIS_SP_P_GAIN_1STEP = 174,   //각 기어단의 위치 모드 P 게인: 1단
	AXIS_SP_P_GAIN_2STEP = 175,   //각 기어단의 위치 모드 P 게인: 2단
	AXIS_SP_P_GAIN_3STEP = 176,   //각 기어단의 위치 모드 P 게인: 3단
	AXIS_SP_P_GAIN_4STEP = 177,   //각 기어단의 위치 모드 P 게인: 4단
	AXIS_SP_FEEDFOWARD_GAIN_1STEP = 183,   //각 기어단에서 위치 모드 피드 포워드 게인: 1단
	AXIS_SP_FEEDFOWARD_GAIN_2STEP = 184,   //각 기어단에서 위치 모드 피드 포워드 게인: 2단
	AXIS_SP_FEEDFOWARD_GAIN_3STEP = 185,   //각 기어단에서 위치 모드 피드 포워드 게인: 3단
	AXIS_SP_FEEDFOWARD_GAIN_4STEP = 186,   //각 기어단에서 위치 모드 피드 포워드 게인: 4단
	AXIS_SP_FOLLOW_ERR_TYPEB =194,   //추종오차 허용 범위
	AXIS_SP_MAX_VELOCITY_COMMAND =196,   //속도 지령 최대값
	AXIS_SP_DA_BIT =207,   //D / A CONVERTER RESOLUTION, VELOCITY DATA SCALE
	AXIS_SP_VOLATE_OFFSET_COMPENSATION_TYPE =211,   //입력 전압 옵셋량 보정 방법(0:단일옵셋 1 : 다중옵셋)
	AXIS_SP_VOLATE_OFFSET =212,   //입력 전압 옵셋량(단일옵셋 방식의 경우)
	AXIS_SP_VOLATE_OFFSET_INPUT_INTERVAL =213,   //전압 옵셋량 입력 간격(다중옵셋 방식의 경우)
	AXIS_SP_VOLATE_OFFSET_POSITIVE_DIRECTION =214,   //+방향 입력 전압 옵셋량(다중옵셋 방식의 경우) : #1~#10(~223)
	AXIS_SP_VOLATE_OFFSET_NEGATIVE_DIRECTION=224,   //-방향 입력 전압 옵셋량(다중옵셋 방식의 경우)	: #1~#10(~233)
	AXIS_SP_POLARITY_ENCODER_CPHASE =280,   //ENCODER C상 극성(0:+, 1 : -)
	AXIS_SP_POLARITY_ENCODER = 281,   //ENCODER 방향(0:+, 1 : -)
	AXIS_SP_POLARITY_SERVO_READY = 285,   //서보 READY 극성(0:+, 1 : -)
	AXIS_SP_POLARITY_SERVO_ALARM = 287,   //서보 ALARM 극성(0:+, 1 : -)
	AXIS_SP_POLARITY_VELOCITY_COMMAND = 290,   //속도 지령 극성(0:+, 1 : -)
	AXIS_SP_POLARITY_SERVO_ON = 293,   //서보 ON 극성(0:+, 1 : -)
	AXIS_SP_POLARITY_SERVO_RESET =295,   //서보 RESET 극성(0:+, 1 : -)
	AXIS_SP_USE_ENCODER_OUT_ERR = 298,   //ENCODER 단선 알람 검출 여부(0:검출, 1 : 검출안함)
	AXIS_SP_USE_ENCODER_PHASE_ERR =300,   //ENCODER PHASE 알람 검출 여부(0:검출함 1 : 검출안함)
	AXIS_SP_ENCODER_PHASE_ERR_LIMITCOUNT =302,   //ENCODER PHASE 알람으로 간주하는 PHASE ERROR 누적개수
	AXIS_SP_EXCEPTION_ENCODER_PHASE_ERR =303,   //ENCODER PHASE 알람시의 NC 동작(0:X, 1 : 정지, 2 : SV OFF)
	AXIS_SP_SERVO_READY_ERR_DELAYTIME =311,  //SERVO READY 알람으로 간주하는 신호 입력 지연 시간

	_SP_MAX
};

// Servo 
enum HXServo{
	AXIS_TYPE									= 1,	// AXIS type 0: no Use, 1:Servo, 2:Spindle
	AXIS_PORT_NO								= 2,	// Axis Port No.
	AXIS_INTERFACE_TYPE							= 3,	// CNC & Drive Interface Type (1:Analog, 3:ECAT, 4:AIB32, 5:AIB30V, 6:AIB30P, 7:EDIO7246)
	AXIS_ECAT_NO								= 4,	// AIB No. or ECAT No.

	AXIS_FEED_TYPE								= 21,	// 축 이송 형태 - 1: 직선(V), 2: 회전(V), 3: 직선(P), 2: 회전(P)
	AXIS_MASTER_SLAVE_CPHASE_OFFSET				= 31,	// Master와 Slave의 C상 차이 단위:mm
	AXIS_SET_SYNC_MASTER						= 32,	// nMaster : 동기제어 Master 축 번호 설정
	AXIS_SET_BACKLASHERR						= 44,	// 백래쉬 양 (mm, deg)
	AXIS_SET_FRICTION_COMPENSATION				= 47,	// 마찰 보상 값 (mm, deg)
	AXIS_USE_PITCHERR_COMPENSATION				= 53,	// 피치에러 보정 무효 설정(0: 보정, 1: 보정안함 )
	AXIS_PITCHERR_COMP_INTERVAL					= 57,	// 피치에러 입력 간격 
	AXIS_PITCHERR_ORIGIN_INDEX					= 58,	// 원점과 대응하는 피치에러 테이블 인덱스 
	AXIS_PITCH_ERR_TABLE						= 59,	// 피치에러 테이블(#1~) 200개  
	AXIS_POSITIONAL_STEPOUT_COMPENSATION		= 259,	// 위치형 서보 탈조 보상 기능 
	AXIS_POSITIONAL_RESIDUALPULSE_COMPENSATION	= 260,	// 위치형 서보 잔여 펄스 보상 기능 
	AXIS_MACHINE_GEAR_RATIO						= 269,	// 기계측 기어비
	AXIS_MOTORS_GEAR_RATIO						= 270,	// 모터측 기어비
	AXIS_MM_BALLSCREW_REVOLUTION		        = 271,	// Mm: 1회전당 이송거리 
	AXIS_ENCODER_RESOLUTION						= 284,	// Encoder resolution(체배 후의 Resolution)

	AXIS_USE_ENCODER							= 279,	// Encoder 사용 여부 (0: 사용, 1: 사용안함)
	AXIS_ENCODER_TYPE							= 280,	// Encoder 타입 0:Incremental, 1:Absolute, 2:Single turn Absolute
	AXIS_ENCODER_PULSE_TYPE						= 282,	// Encoder pulse 출력 방식 ( 0: Linear, 1: Modular )
	AXIS_P_GAIN									= 306, 	// 위치제어 P 게인 
	AXIS_SYNC_ERR_COMPESATION_GAIN				= 309, 	// 동기제어 동기오차 보상 게인 
	AXIS_FEEDFORWARD_GAIN						= 312, 	// 피드포워드 게인 
	AXIS_SET_FOLLOW_ERR_TYPEA					= 324,	// 정지 추종오차 허용 범위 
	AXIS_SET_FOLLOW_ERR_TYPEB					= 325,	// 추종오차 허용 범위 
	AXIS_SET_SYNC_ERR							= 326,	// 동기제어의 동기 오차 허용 범위 
	AXIS_MAX_VELOCITY_COMMAND					= 328, 	// 속도지령 최대값
	AXIS_DA_BIT									= 339, 	// D/A convert Resolutio, Velocity Data Scale (ex : 16 bit )
		
	AXIS_POLARITY_ENCODER_CPHASE				= 400,	// Encoder C Phase 극성 방향 ( 0: +, 1: - )
	AXIS_POLARITY_ENCODER						= 401,	// Encoder 극성 방향 ( 0: +, 1: - )
	AXIS_POLARITY_SERVO_READY					= 405,	// Servo Ready 극성 방향 ( 0: +, 1: - )
	AXIS_POLARITY_SERVO_ALARM					= 407,	// Servo Alarm 극성 방향 ( 0: +, 1: - )
	AXIS_POLARITY_VELOCITY_COMMAND				= 410, 	// 속도지령 극성(0:+, 1:-)
	AXIS_POLARITY_SERVO_ON						= 413,	// Servo Ready 극성 방향 ( 0: +, 1: - )
	AXIS_POLARITY_SERVO_RESET					= 415,	// Servo Alarm 극성 방향 ( 0: +, 1: - )
	AXIS_USE_ENCODER_OUT_ERR					= 418,	// Encoder 단선 알람 검출 여부 (0: 검출, 1: 검출 안함 ) 
	AXIS_USE_ENCODER_PHASE_ERR					= 420,	// Encoder Phase 단선 알람 검출 여부 (0: 검출, 1: 검출 안함 ) 
	AXIS_ENCODER_PHASE_ERR_LIMITCOUNT		= 422,	// Encoder Phase 단선 알람으로 간주하는 phase error 누적개수
	AXIS_EXCEPTION_ENCODER_PHASE_ERR		= 423,	// Encoder Phase 단선 알람시의 NC 동작 ( 0: 설정 안함, 1: 정지, 2: Servo Off )
	AXIS_USE_ENCODER_CPHASE_ERR					= 425,	// Encoder C Phase 단선 알람 검출 여부 (0: 검출, 1: 검출 안함 ) 
	AXIS_EXCEPTION_ENCODER_CPHASE_ERR		= 428,	// Encoder C Phase 단선 알람시의 NC 동작 ( 0: 설정 안함, 1: 정지, 2: Servo Off )
	AXIS_SERVO_READY_ERR_DELAYTIME			= 431,	// Servo Ready 알람으로 간주하는 신호 입력 지연 시간 
	AXIS_USE_INFINIT_AXIS						= 432,	// 무한축 설정여부(0: 사용안함, 1: 사용) 
	AXIS_FOLLOW_ERR_AUTO_COMPENSATION		= 435,	// 자동 전압 옵셋 보정 (추종오차 자동보정, 0:사용안함, 1:사용함)
	AXIS_MAX_RPM								= 436,	// Motor Max RPM
	
	_MAX
};

