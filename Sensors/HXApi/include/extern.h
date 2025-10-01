#ifndef _EXTERN_H_
#define _EXTERN_H_

#ifdef HXAPI_EXPORTS
#define HXAPI_API __declspec(dllexport)
#else
#define HXAPI_API __declspec(dllimport)
#endif

#endif