#ifndef _MAP_DEFINE_
#define _MAP_DEFINE_


// GX Map
enum {
	GX_P	= 1,
	GX_D	= 2,
	GX_G	= 3,
	GX_F	= 4,
	GX_I	= 5,
	GX_O	= 6,
	GX_X	= GX_I,
	GX_Y	= GX_O,
	GX_S	= 7,
	GX_U	= 8,
	GX_UL	= 9,
	GX_R	= 10,
	GX_RL	= 11,
	GX_RF	= 12,
	GX_E	= 13,
	GX_A	= 14,
	GX_Q	= 15,
	GX_RP	= 21,
	GX_TR	= 22,
	GX_EL	= 23,
	GX_OL	= 24,
	GX_ML	= 25,
	GX_FS	= 26,
	GX_P_EXT= 30,
	GX_H	= 31,
	GX_U1	= 32,
	GX_UX	= 48,

	// HX Map Name
	HX_X		= 100,
	HX_Y		= 101,
	HX_G		= 102,
	HX_F		= 103,
	HX_SR		= 104,
	HX_PA		= 105, // double
	HX_PI		= 106, // double
	HX_PM		= 107, // double
	HX_PP		= 108, // double
	HX_PU		= 109, // double
	HX_PS		= 110, // double
	HX_SV		= 111, // double
	HX_ML		= 112, // double
	HX_MGV		= 113, // double
	HX_B		= 114, // double
	HX_T		= 115,
	HX_C		= 116,
	HX_D		= 117,
	HX_BR		= 118, // double
	HX_SN		= 119, // double
	HX_MGN		= 120, // double
	HX_R        = 140,
	HX_SH		= 160,
	HX_STR_AXIS = 121,
	HX_STR_MACHINE = 122,
	HX_STR_SEQPROG = 123,
	HX_STR_ERRPROG = 124,
	HX_STR_NCPATH = 125,
	HX_STR_MAINPROG = 126,
	HX_STR_SUBPROG = 127,
	HX_STR_MDIPROG = 128,
	HX_DEVICE = 129,
	HX_STR_SYSPATH = 130,
	HX_STR_ALARMMSG = 131,
	HX_STR_OPMSG = 132,
	HX_STR_DATAPATH = 133,
	HX_STR_PLCFILE = 134,
	HX_STR_MAPFILE = 135,
	HX_STR_LANGUAGE = 136,
	HX_STR_TEMP1 = 161,
	HX_STR_TEMP2 = 162,
	HX_STR_TEMP3 = 163,
	HX_STR_TEMP4 = 164,
	HX_STR_TEMP5 = 165,
	HX_STR_TEMP6 = 166,
};

#define NC_LIST_MAX 200
#define NC_STR_MAX 400

typedef struct {
	char searchPath[255];

	int isDirectory[NC_LIST_MAX];
	char fileName[NC_LIST_MAX][NC_STR_MAX];
	int fileSize[NC_LIST_MAX];
	char lastModified[NC_LIST_MAX][NC_STR_MAX];
} CSUCom_NCList_ITEM;

#endif