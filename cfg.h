//
// Created by bytedance on 19.1.23.
//

#ifndef CFG_H
#define CFG_H

#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <memory.h>
#include <list>
#include <vector>

//按行读取文件
void readFile(char const* filename, std::vector<std::string>& lines, char const* skip);

#endif