#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <time.h>
#include <algorithm>
#include "math.h"
#include <iostream>
#include <memory>
#include <utility>
#include <sys/types.h>
#include <sstream>
#include <fstream>
#include <stdio.h>
#include <string>
#include <stdlib.h>
#include <map>
#include "s3s.h"

#include "cfg.h"
#include "funcC.h"
namespace py = pybind11;

void testS3sLogic(){
    //游戏逻辑类
    S13S::CGameLogic				g;
    //所有玩家手牌
    uint8_t							handCards[GAME_PLAYER][MAX_COUNT];
    //手牌牌型分析结果
    S13S::CGameLogic::handinfo_t	handInfos[GAME_PLAYER];
    //枚举多少组最优墩，开元/德胜是3组
    int enum_group_sz = 1000;
    //初始化
    g.InitCards();
    //洗牌
    g.ShuffleCards();
    {
        //给各个玩家发牌
        restart:
        assert(GAME_PLAYER <= 4);
        for (int i = 0; i < GAME_PLAYER; ++i) {
            if (true) {
                //余牌不够则重新洗牌，然后重新分发给各个玩家
                if (g.Remaining() < MAX_COUNT) {
                    g.ShuffleCards();
                    goto restart;
                }
                //发牌
                g.DealCards(MAX_COUNT, &(handCards[i])[0]);
            }
        }
    }
    {
        //各个玩家手牌分析
        for (int i = 0; i < GAME_PLAYER; ++i) {
            if (true) {
                clock_t start,end;
                start = clock();
                //手牌排序
                S13S::CGameLogic::SortCards(&(handCards[i])[0], MAX_COUNT, true, true, true);
                printf("\n\n========================================================================\n");
                printf("--- *** chairID = [%d]\n", i);
                //一副手牌
                S13S::CGameLogic::PrintCardList(&(handCards[i])[0], MAX_COUNT);
                //手牌牌型分析
                int c = S13S::CGameLogic::AnalyseHandCards(&(handCards[i])[0], MAX_COUNT, enum_group_sz, handInfos[i]);
                //查看所有枚举牌型
                //handInfos[i].rootEnumList->PrintEnumCards(false, S13S::Ty123sc);
                //查看手牌枚举三墩牌型
                end = clock();   //结束时间
                std::cout<<"time = "<<double(end-start)/CLOCKS_PER_SEC<<"s"<<std::endl;  //输出时间（单位：ｓ）

                handInfos[i].PrintEnumCards();
                //查看重复牌型和散牌
                //handInfos[i].classify.PrintCardList();
                printf("--- *** c = %d %s\n\n\n\n", c, handInfos[i].StringSpecialTy().c_str());
            }
        }
    }

}

py::array_t<uint8_t> getS3Sarr(py::array_t<uint8_t> xs,bool test){
    int size = xs.size();
    assert(size == 13);
    py::buffer_info xs_buff = xs.request();
    uint8_t* xs_ptr = (uint8_t*)xs_buff.ptr;
    uint8_t handCards[13];
    int enum_group_sz = 1000;
    for(int i = 0;i < 13;i ++){
        handCards[i] = xs_ptr[i];
    }
    //手牌牌型分析结果
    S13S::CGameLogic::handinfo_t	handInfos;
    int c = S13S::CGameLogic::AnalyseHandCards(&(handCards)[0], MAX_COUNT, enum_group_sz, handInfos);

    if(test)handInfos.PrintEnumCards();

    int group_size = handInfos.enum_groups.size();

    auto result = py::array_t<uint8_t>(group_size * 13);
    py::buffer_info result_buff = result.request();
    uint8_t* result_ptr = (uint8_t*)result_buff.ptr;

    int i = 0;
    for (auto it = handInfos.enum_groups.rbegin();
         it != handInfos.enum_groups.rend(); ++it){
        for(auto dun: {S13S::DunFirst,S13S::DunSecond,S13S::DunLast}) {
            auto one_cards = it->duns[dun];
            for(int j = 0;j < one_cards.c;j ++){
                result_ptr[i] = one_cards.cards[j];
                i ++ ;
            }
        }
    }
    return result;

}

PYBIND11_MODULE(s3spy, m) {
    m.doc() = "S3s python package"; // optional module docstring
    m.def("testS3sLogic", &testS3sLogic, "test s3s logic");
    m.def("getS3Sarr", &getS3Sarr, "get S3S arrangments");


#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
m.attr("__version__") = "dev";
#endif
}
