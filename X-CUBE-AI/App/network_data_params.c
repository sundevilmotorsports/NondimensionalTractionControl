/**
  ******************************************************************************
  * @file    network_data_params.c
  * @author  AST Embedded Analytics Research Platform
  * @date    2025-11-13T18:24:50-0700
  * @brief   AI Tool Automatic Code Generator for Embedded NN computing
  ******************************************************************************
  * Copyright (c) 2025 STMicroelectronics.
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
const ai_u64 s_network_weights_array_u64[74] = {
  0x81040105f68106dcU, 0x781fbfa1dfcb89fU, 0xff1aeae1813f02f6U, 0x511bff07fa7f0809U,
  0xfa0a7fac7f5397e9U, 0x1ed122f58810107U, 0x7d8102f80c1aca81U, 0xcf31fd7fff03fd01U,
  0xfc09fbe15081c1ceU, 0xa47ff903ff7f0804U, 0xf0107fb000fe03feU, 0x2da1ea4aa7f010aU,
  0x100c00fd0e7f0acfU, 0xfc7a557fff02f781U, 0xb0cf481d7b4092aU, 0x7f1d11feff7f3ae8U,
  0x4816bf9e81fbdU, 0x1fb04e87faf0202U, 0xfffe48cb0000a2f7U, 0xffff57b6fffedbdbU,
  0x1c9da00000e91U, 0xffff47bd00005011U, 0xfffff250ffffca04U, 0xffff35e100019667U,
  0x475300012451U, 0x13e730000cd21U, 0x1f76fffed8b3U, 0xc8dd000097c2U,
  0xffff887e000179b2U, 0x4eb5ffffcfa1U, 0xe39cd0ad68357f09U, 0xfcc2b18a5ea2e908U,
  0xa08c58755ef2dc2U, 0x3f1a09d90491fef4U, 0x9ee4184ee108161aU, 0xe5100420f00b057fU,
  0xe408f91afb09030aU, 0x29fd7f04effb03f7U, 0xe40f030718fbfcf1U, 0xf8fc0859226fcfdcU,
  0x3c1e81acfa1c9b0dU, 0x6b0012d52a1feb85U, 0xdff8eed0db81f7a1U, 0xe4f5115af30808eaU,
  0xe4f8d459d0160c46U, 0xe2b2c7f43fc217d5U, 0x1d0681d014f1d3fbU, 0x10fecc02bcec1eeaU,
  0xf7ff414bafae113U, 0x2916e1f4e501472aU, 0x794f30c3afe1bf5U, 0x281080952f04c03U,
  0xdace1dece5091e08U, 0x910102d0cedaf7fbU, 0x9522197ff4f717U, 0x26a6fad4e00f25f2U,
  0xcf152fe61817f008U, 0x4c2dee7facd792c7U, 0x132b54fb08500ab8U, 0xe915144cc550e02dU,
  0x451909fef3eef92bU, 0xe7fa812719f90bccU, 0xfce51b0e14dbfc1eU, 0x54d74cb53101b6d0U,
  0xf0ee6af9f754cc18U, 0x63384b02db407f93U, 0xffffe2b200019107U, 0x1761ffff6e5dU,
  0x1538e000034fcU, 0x12479ffff2643U, 0xffff2d3500006aa7U, 0xffff1f31000024c0U,
  0xc12a2137efb35550U, 0xffffef437f44c9abU,
};


ai_handle g_network_weights_table[1 + 2] = {
  AI_HANDLE_PTR(AI_MAGIC_MARKER),
  AI_HANDLE_PTR(s_network_weights_array_u64),
  AI_HANDLE_PTR(AI_MAGIC_MARKER),
};

