#
# The original code is under the following copyright:
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE_GS.md file.
#
# For inquiries contact george.drettakis@inria.fr
#
# The modifications of the code are under the following copyright:
# Copyright (C) 2024, University of Liege, KAUST and University of Oxford
# TELIM research group, http://www.telecom.ulg.ac.be/
# IVUL research group, https://ivul.kaust.edu.sa/
# VGG research group, https://www.robots.ox.ac.uk/~vgg/
# All rights reserved.
# The modifications are under the LICENSE.md file.
#
# For inquiries contact jan.held@uliege.be
#

from pathlib import Path

import torch
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

ROOT = Path(__file__).resolve().parent
GLM_INCLUDE = ROOT / "third_party" / "glm"
IS_ROCM = bool(getattr(torch.version, "hip", None))


def _nvcc_flags():
    flags = [f"-I{GLM_INCLUDE}"]
    if not IS_ROCM:
        flags.append("--use_fast_math")
    return flags

setup(
    name="diff_triangle_rasterization",
    packages=['diff_triangle_rasterization'],
    ext_modules=[
        CUDAExtension(
            name="diff_triangle_rasterization._C",
            sources=[
            "cuda_rasterizer/rasterizer_impl.cu",
            "cuda_rasterizer/forward.cu",
            "cuda_rasterizer/backward.cu",
            "cuda_rasterizer/utils.cu",
            "rasterize_points.cu",
            "ext.cpp"],
            extra_compile_args={"nvcc": _nvcc_flags()})
        ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
