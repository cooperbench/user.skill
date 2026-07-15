[DEVELOPER]: Edit @kernel/hip/hip_kernel_prepacked.cu and @kernel/hip/hip_kernel_prepacked.py to make it a torch custom operator with Python stable ABI and libtorch stable ABI. Note that the kernel mutates `c`, and we don't need a fake impl in Python because it does not return a tensor. See https://docs.pytorch.org/tutorials/advanced/cpp_custom_ops.html . For now don't consider autotune. When you finish, use test_scaled_mm_hip_prepacked_e5m2.py to test the correctness of each autotune config.

[AGENT]: I’m inspecting the current HIP prepacked extension and the existing test flow, then I’ll convert it to the torch custom-op stable-ABI pattern the PyTorch docs require.

[AGENT]: I found the two target files and there are unrelated untracked analysis artifacts in the worktree, which I’ll leave alone. Next I’m reading the current extension entrypoints and the prepacked test harness to align the conversion with existing build/runtime patterns.

[AGENT]: The PyTorch tutorial confirms the key constraints: use `torch::stable::Tensor`, `STABLE_TORCH_LIBRARY[_IMPL]`, `TORCH_BOX(...)`, mark the mutated output as `Tensor(a!)`, and avoid `pybind11` if we want `Py_LIMITED_API`. I’m now mapping that onto this repo’s current HIP extension loader and test entrypoints.

[AGENT]: I have the current binding shape now: it’s a `pybind11` extension that allocates and returns `c`. I’m checking the local torch headers next so the replacement uses the exact stable-ABI APIs available in this environment rather than guessing from the tutorial alone.