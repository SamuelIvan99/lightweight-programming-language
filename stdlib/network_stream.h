#ifndef NETWORK_STREAM_H
#define NETWORK_STREAM_H

#include "stream.h"

typedef struct {
    const char *details;
} NetworkWriter;

StreamWriter create_network_writer(const char *details);

#endif
