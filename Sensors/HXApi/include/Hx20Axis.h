#pragma once

#include "TypeDef.h"
#include "extern.h"

class Hx20Channel;
class Hx20System;

class HXAPI_API Hx20Axis
{
public:
	Hx20Axis(Int32 port, Int32 axis){ m_port = port; m_axis = axis; }
private:
	Int32 m_port;
	Int32 m_axis;
};