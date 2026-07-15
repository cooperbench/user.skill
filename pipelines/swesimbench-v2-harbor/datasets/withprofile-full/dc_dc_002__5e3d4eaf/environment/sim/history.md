[DEVELOPER]: Read doc/GFX1151_REFERENCE.md , doc/HIP_OPTIMIZATION_PLAN_PREPACKED_E5M2.md , kernel/hip/hip_kernel_prepacked.cu , kernel/hip/hip_kernel_prepacked.py for context. Your task is to write a new kernel and its Python wrapper that computes A@B.T rather than A@B. Do we no longer need prepacking when B is transposed? When you finish, write a test script like test_scaled_mm_hip_prepacked_e5m2.py to test its correctness.

[AGENT]: I’m reading the referenced docs and HIP kernel files first to map the current `A @ B` prepacked path, then I’ll add the `A @ B.T` variant and a correctness test alongside the existing prepacked test pattern.

[AGENT]: I have the baseline prepacked path in view now. Next I’m reading the rest of the kernel/export code and the existing prepacked test so the new `B.T` path matches the current launch, autotune, and validation conventions.

[AGENT]: The current prepack format is not just “store `B.T` contiguously”; it also changes which dimension is major in memory. I’m checking the surrounding kernels/utilities now so I can decide whether the new `A @ B.T` path should consume plain contiguous `B` or a transpose-specific packed layout.

[AGENT]: There’s an existing FP16 path that already thinks in terms of a pre-transposed `B` layout. I’m reading that next because it likely answers both the memory-layout question and the cleanest way to structure the new fp8 `A @ B.T` kernel.

[AGENT]: The FP16 path confirms the distinction: “transposed” and “prepacked” are separate. A plain contiguous `B` with shape `[N, K]` is easier to consume than `[K, N]`, but it still doesn’t match the kernel’s ideal K-tile-major transport pattern. I’m now checking whether there’s already a transposed-input wrapper pattern I can mirror before I patch files.

[AGENT]: I’ve got enough context to patch this cleanly. Plan: 1. Add a new HIP extension and Python wrapper for `A @ B.T` that takes `B` as contiguous `[N, K]` fp8. 2. Reuse the existing WMMA/LDS structure, but change the B global-load path and shape/stride checks for transposed input. 3. Add a correctness test script mirroring the current e5m2 test, with reference `a @ b.t()`. 4. Run the new test and fix any compile/runtime issues before closing.

[AGENT]: I’m patching the existing fp8 source now to add a second entry point for transposed `B` input, rather than creating a separate duplicate implementation. After that I’ll add the wrapper function and a new correctness test script for the `A @ B.T` path.

[AGENT]: The C++ and Python entry points are in. I’m adding the dedicated correctness test now, using the same per-config sweep as the current prepacked test but with reference `b_t.t()` so it validates `A @ B.T`.

[AGENT]: The new entry points and test are on disk. I’m doing a quick source read before running the test so I can catch any obvious signature or binding mistakes without paying a full compile cycle first.

[AGENT]: I found one likely compile trap before running: the shared B loader now has a `ktile` temporary that’s unused in the transposed specialization and will trip `-Werror`. I’m tightening that up first, then I’ll run the new correctness test.

[AGENT]: The test build is running now. Once it either compiles or fails, I’ll inspect the first failure in the extension build or the first bad config and iterate from there.