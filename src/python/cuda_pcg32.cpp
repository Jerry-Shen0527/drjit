#include <enoki/random.h>
#include "common.h"

void bind_cuda_pcg32(py::module& m) {
    using PCG32C = PCG32<FloatC, 1>;

    py::class_<PCG32C>(m, "PCG32C")
        .def(py::init<UInt64C, UInt64C>(), "initstate"_a = PCG32_DEFAULT_STATE,
             "initseq"_a = PCG32_DEFAULT_STREAM)
        .def("seed", &PCG32C::seed, "initstate"_a = PCG32_DEFAULT_STATE,
             "initseq"_a = PCG32_DEFAULT_STREAM)
        .def("next_uint32", [](PCG32C &pcg) { return pcg.next_uint32(); })
        .def("next_uint32",
             [](PCG32C &pcg, const MaskC &mask) {
                 return pcg.next_uint32(mask);
             },
             "mask"_a)
        .def("next_uint64", [](PCG32C &pcg) { return pcg.next_uint64(); })
        .def("next_uint64",
             [](PCG32C &pcg, const MaskC &mask) {
                 return pcg.next_uint64(mask);
             },
             "mask"_a)
        .def("next_uint32_bounded",
             [](PCG32C &pcg, uint32_t bound) {
                 return pcg.next_uint32_bounded(bound);
             },
             "bound"_a)
        .def("next_uint32_bounded",
             [](PCG32C &pcg, uint32_t bound, const MaskC &mask) {
                 return pcg.next_uint32_bounded(bound, mask);
             },
             "bound"_a, "mask"_a)
        .def("next_uint64_bounded",
             [](PCG32C &pcg, uint64_t bound) {
                 return pcg.next_uint64_bounded(bound);
             },
             "bound"_a)
        .def("next_uint64_bounded",
             [](PCG32C &pcg, uint64_t bound, const MaskC &mask) {
                 return pcg.next_uint64_bounded(bound, mask);
             },
             "bound"_a, "mask"_a)
        .def("next_float32", [](PCG32C &pcg) { return pcg.next_float32(); })
        .def("next_float32",
             [](PCG32C &pcg, const MaskC &mask) {
                 return pcg.next_float32(mask);
             },
             "mask"_a)
        .def_readwrite("state", &PCG32C::state)
        .def_readwrite("inc", &PCG32C::inc);
}