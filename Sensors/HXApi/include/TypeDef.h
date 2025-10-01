#ifndef TYPEDEF_H_
#define TYPEDEF_H_

// 타입과 크기를 명확하게 하기 위해 타입을 재정의하여 사용한다.

typedef int				Int32;
typedef unsigned int	UInt32;
typedef int				Bool;
typedef double			Double;
typedef float			Float;
typedef char			Char;	// 문자
typedef signed char		SChar;	// 1byte -128 ~ 
typedef unsigned char	UChar;	// 1byte 0 ~

typedef short			Int16;
typedef unsigned short	Uint16;
typedef signed char		Int8;
typedef unsigned char	Uint8;

typedef unsigned char	Byte;	// 문자

#define TEXT_MAXSIZE	255

enum {False = 0, True = 1};
enum {COM_ETHERNET = 0, COM_RTX, COM_RTX_CH};

#endif