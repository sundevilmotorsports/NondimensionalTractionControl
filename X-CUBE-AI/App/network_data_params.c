/**
  ******************************************************************************
  * @file    network_data_params.c
  * @author  AST Embedded Analytics Research Platform
  * @date    2026-02-17T11:12:14-0700
  * @brief   AI Tool Automatic Code Generator for Embedded NN computing
  ******************************************************************************
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  ******************************************************************************
  */

#include "network_data_params.h"


/**  Activations Section  ****************************************************/
ai_handle g_network_activations_table[1 + 2] = {
  AI_HANDLE_PTR(AI_MAGIC_MARKER),
  AI_HANDLE_PTR(NULL),
  AI_HANDLE_PTR(AI_MAGIC_MARKER),
};




/**  Weights Section  ********************************************************/
AI_ALIGNED(32)
const ai_u64 s_network_weights_array_u64[265] = {
  0x3ec99be23f843765U, 0x3f455543bd85a31bU, 0x3e11d5f4be2bedf1U, 0xbf1727b0bd26566aU,
  0x3d8853263e531b46U, 0x3e5d56313e07ebb0U, 0xbdae6d3dbdba87b7U, 0xbd1ece7abd6ea498U,
  0xbe8969e9be898e4dU, 0xbe3ef727bd3ecc9dU, 0x3e28323ebde73950U, 0x3dbc679fbca087a5U,
  0xbe7a839f3db4b795U, 0xbe31b600bdf13921U, 0xbe90ffc9bd4f56a4U, 0x3dbab1e5be297753U,
  0x3d4a8421bccd0460U, 0x3da604623d7d53fcU, 0xbef554b7be56d68cU, 0x3e32eeacbe0900ffU,
  0xbeac566a3f3833e4U, 0x3f2922cebca3f9e4U, 0x3e2562e2be487e14U, 0xbe45ecd2bd87406eU,
  0x3e991cae3ecb9999U, 0x3f19e0863e9d50a8U, 0x3d3921eebe4a2f7fU, 0xbe6fae4f3c711138U,
  0xbcb5553ebe89089dU, 0xbd9d36b6bdd3032dU, 0x3dd44db03e5b8ac2U, 0x3ed0edd23dccd66dU,
  0x3f0568bd3d21c3a4U, 0x3af8f1983e083f02U, 0xbe0136b83d465330U, 0x3c2aab4d3d6517a2U,
  0xbeb4b8e8bc780947U, 0xbe80d034bea58ab9U, 0x3f0bbb793e78ef0aU, 0xbece0f0ebda83653U,
  0xbddcfe1ebf96648aU, 0xbf93efc73e1e8447U, 0xbddd4f5b3ca3d5aeU, 0x3f3090113e7d9c3dU,
  0xbc70d4443f3807c1U, 0x3fb4277bbdbaa38bU, 0x3d701295bdc22bc2U, 0xbf4f89ef3deace41U,
  0xb4aeeaee36b691d6U, 0x3777ab97b7847a02U, 0x370d498eb6418c85U, 0x369f7bd336ad5ec8U,
  0xbe1bb7f0bec6274dU, 0xbe70feeebe2130c7U, 0x3d4c6a3fbed1afa5U, 0x3ec57928bd5ab010U,
  0x3e3df6453e7be69aU, 0x3cd50d653e42781bU, 0x3ded93bcbaaa1e8eU, 0xbd2ce49f3deeb7d7U,
  0xbe81eaacbf3211a1U, 0xbec2b07ebdcd24cfU, 0x3e88923a3dd2c500U, 0x3ec7abfa3d8915d3U,
  0x3f0c912a3ea85940U, 0x3e525cb73d2f0007U, 0x3e8ac2313dc25b41U, 0x3d8031ad3e5bddbfU,
  0xbf41c11a3ef013aaU, 0xbe57e919be083bebU, 0xbe90d5803eb38730U, 0xbefa78013d3ab51dU,
  0xbf6e9f1b3e898c0fU, 0xbef526d3bd5d7b29U, 0xbed26fbf3ea45d05U, 0xbdc75a63bd283ab1U,
  0x3e5dbee83dffa165U, 0xbd96c61e3c19c8bdU, 0xbeb82bb7bccee3f8U, 0xbd826b09bd880182U,
  0x3f009c583d921ba9U, 0x3f732ff9be639eb8U, 0xbd9faf123d2ca5bbU, 0xbea2a6e73cc79173U,
  0xbe247a56be97e5efU, 0xbe268d9e3d8b95e2U, 0x3e0f561ebdb47ebbU, 0x3da3f8d8bcd88202U,
  0xbe02a979bd2ddce5U, 0x3ed4594ebd1f10acU, 0x3d120e9cbe2d3a51U, 0x3f0e3a0d3d8dca2cU,
  0xbf3cb7743d3971ffU, 0xbeac932bbd97b4bdU, 0xbc94ff193d8329d8U, 0x3d292c133d0349c9U,
  0x3e7e67c43f5edc8dU, 0xbee9b228bf9b90f2U, 0xbd442718bf8db67eU, 0x3fa6f43cbef57b26U,
  0x3eaf45403fa63956U, 0xbfe2aba83f9d5ed7U, 0x3f3e1e0dbf4e4b0cU, 0xbeefb419be0a94c1U,
  0xbf85f3513efa0171U, 0x3e92ca95c00068ddU, 0xbdd6da62bf69cf46U, 0x3e767175bee3759aU,
  0x3f05b6a63e614e29U, 0x3c1118113d8d4339U, 0xbef18a783e1e21d2U, 0x3e8f60f23f2df5fcU,
  0x3e1a52e73ed0d041U, 0x3d0d0575bf644551U, 0xbeac5e843cbc3a5aU, 0xbe720de9bea21dabU,
  0xbe7be1adbd2f4251U, 0x3efa7f08bf89d47eU, 0xbf4ddda93f57b3b6U, 0xbf2840533e41a885U,
  0x3db37751bdf381adU, 0x3f12e9fabe806412U, 0x3e443eba3f3c2fb0U, 0xbf43b81f3e883bdfU,
  0xbf39a0b73e9de698U, 0x3f661c2abe47a5c4U, 0x3dd920583e1427ccU, 0xbf0653f6bf294487U,
  0xbe44b800bf40557cU, 0x3e6c26343e780f14U, 0xbdebec393d2d0cabU, 0x3d2353963e02c265U,
  0x3f4d37d240aaab0cU, 0xbed728bf40183cedU, 0x40900bbbbff511faU, 0xc06c6e3dc0c6f665U,
  0xbe8d34a5c0290909U, 0xc138730740e7e36dU, 0xc06a5fac3d27cc73U, 0xbfcaa053c00ad508U,
  0xbfa192333fe8ab0fU, 0x40940d58408c7597U, 0x408869afbfc9665bU, 0xbf5487b3bea844b5U,
  0x3f0f2e303e9be52aU, 0x3ecf768abf293ae3U, 0x3e0de8c73f03f481U, 0xbec9cd1f3eabbc8dU,
  0xbf419a8b3e8b5530U, 0xbe4876e33e911878U, 0x3ece142b3db5acd5U, 0xbf1abc8d3e7838b1U,
  0xbdf6c0273c33ff4dU, 0x3eb8e6a03df9a073U, 0xbef155773e86645cU, 0xbd88afbe3e2965feU,
  0x3ea8b74ec01d1989U, 0x3f4bd84cbfc7371cU, 0x3f8498693d451da7U, 0xbdce7b15bfe52957U,
  0x3eab0508bf100207U, 0xc044e1d64016bb8eU, 0x3f0eca1bbc885e27U, 0x3eb97d823f9c06efU,
  0xc015be863f2c9385U, 0x3f2979b8bfa6afceU, 0x3edb3a18bff5d9a6U, 0x3fa673b2bfb3d191U,
  0xbdcd46653e9b9a97U, 0xbdb7e4a3bed6bf9eU, 0xbe7e176c3f16fcb7U, 0x3d75adbf3ed4412eU,
  0xbe9d625b3d0303f1U, 0x3f77dd2abd5766e1U, 0xbd8febd23cff8e82U, 0xbf8a7bc93e6721d5U,
  0x3e9ee2783dc13209U, 0xbd787df0bdc810e5U, 0xbfa72bc63f10ffafU, 0xbede4aeebb1c1921U,
  0xbf92fba6bf233465U, 0x3ee4a4493f292e36U, 0xbf1d83dabe77b066U, 0x3d9ebcfdbe26fb7dU,
  0x3e5616e43df04f35U, 0xbe950a61be07b2f4U, 0xbeb9e9c43e299008U, 0x3eb3de67bf011d5cU,
  0x3ce1f204be55b2ecU, 0xbe5c4058beb8688fU, 0xbe20750b3ecf760bU, 0x3eeba7cdbe10d139U,
  0xbec8c7e93eced6b3U, 0xbeced5dabf3d20bcU, 0xbef8fef93ebf4b6aU, 0x3f17dd7b3ea32ecdU,
  0x3ec90d543eaf22c7U, 0xbf5dff833eb255b0U, 0xbe120a863d9cb357U, 0xbed4fd66be6e9fd4U,
  0xbf98a9cb3f5e770cU, 0x3dedf0e1bf844272U, 0xbf1289b1bdbd98b2U, 0xbf010580bebd7fbeU,
  0x3b65bb6a3db8c6a2U, 0x3eed64ea3f021c38U, 0x3e9c52e53f3430d8U, 0xbef57e953f09e92fU,
  0xbd2fff78beaafb1eU, 0xbf587eef3efeb51eU, 0x3fe94eb8bd707ce8U, 0x3ea6fe14bf37a863U,
  0xbf17c84ebe5d70feU, 0x3e4a286e3f6d9cecU, 0x3f435a5abfa11a80U, 0xbcd0ab543f0925e2U,
  0x3ea1f9a1be8a0a2bU, 0xbf496646bea2022eU, 0xbefc120ebf35b4a2U, 0x3eb79feabf050a01U,
  0xbddd91f33f01d0e1U, 0x3f589ee2bebed8baU, 0xbfaf7b6bbc9df6deU, 0xbda74cdebdb08116U,
  0xbf0e371c3f29a238U, 0xbea774ebbf6b7a90U, 0xbe02a34d3f76d93fU, 0xbdc22a0abe5965e0U,
  0xbee411fcbebeb694U, 0x3f002d7c3f649caeU, 0xbf14b3fb3dbfe99dU, 0x3ede636d3e58d9f4U,
  0x3effd1b4be6dea31U, 0xbf7f28d93e494e77U, 0x3ec81b08be5dd88cU, 0x3f1265db3ed82817U,
  0xbe057b67beceae04U, 0xbf0ba8083e47b5c9U, 0x3f8d775a3d8afa35U, 0x3cc69860bd27ff2dU,
  0x3ed5aa543d602191U, 0xbd7f315ebf4016dfU, 0xbf8f36b73f0238d9U, 0xbfeb8970bf44cf7aU,
  0xc009ec9b3eea5789U, 0xbc8ac0abbf9b8d8aU, 0x3f951c823f1f49adU, 0xbf8ec57dbd219fbeU,
  0x3f3413853ef08e76U, 0x3e87589e3f18a624U, 0x3d86c4cb3f5b3bc1U, 0xbf58a61b3f25e43bU,
  0x3f410e163e6ba96eU, 0xbf4e3365bfec87f6U, 0x3f025c703f320058U, 0x3e45ab0e3fa544ccU,
  0x3fb1b4a5bfcfd457U, 0x40090035bf2fb46fU, 0x3e84d8a13f0400eeU, 0xbf2eab31be38a2c9U,
  0x3e91b81b3ec6edd5U, 0xbf351c4dbd80fe6eU, 0x3f11aeb43e8aa47cU, 0x3d78a96bbec99276U,
  0xbd53c06aU,
};


ai_handle g_network_weights_table[1 + 2] = {
  AI_HANDLE_PTR(AI_MAGIC_MARKER),
  AI_HANDLE_PTR(s_network_weights_array_u64),
  AI_HANDLE_PTR(AI_MAGIC_MARKER),
};

