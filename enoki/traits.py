from enoki import VarType, Exception, Dynamic
import sys as _sys


def is_array_v(a):
    return getattr(a, 'IsEnoki', False)


def array_size_v(a):
    return getattr(a, 'Size', 1)


def array_depth_v(a):
    return getattr(a, 'Depth', 0)


def scalar_t(a):
    if not isinstance(a, type):
        a = type(a)
    return getattr(a, 'Scalar', a)


def value_t(a):
    if not isinstance(a, type):
        a = type(a)
    return getattr(a, 'Value', a)


def mask_t(a):
    if not isinstance(a, type):
        a = type(a)
    return getattr(a, 'MaskType', bool)


def is_mask_v(a):
    return scalar_t(a) is bool


def is_floating_point_v(a):
    return scalar_t(a) is float


def is_integral_v(a):
    return scalar_t(a) is int


def is_arithmetic_v(a):
    return scalar_t(a) is not bool


def is_cuda_array_v(a):
    return getattr(a, 'IsCUDA', False)


def is_llvm_array_v(a):
    return getattr(a, 'IsLLVM', False)


def is_jit_array_v(a):
    return getattr(a, 'IsJIT', False)


def is_diff_array_v(a):
    return getattr(a, 'IsDiff', False)


def is_complex_v(a):
    return getattr(a, 'IsComplex', False) or isinstance(a, complex)


def is_matrix_v(a):
    return getattr(a, 'IsMatrix', False)


def is_quaternion_v(a):
    return getattr(a, 'IsQuaternion', False)


def is_vector_v(a):
    return getattr(a, 'IsVector', False)


def is_special_v(a):
    return getattr(a, 'IsSpecial', False)


def is_static_array_v(a):
    return getattr(a, 'Size', Dynamic) != Dynamic


def is_unsigned_v(a):
    if not is_array_v(a):
        return False

    vt = a.Type

    return vt == VarType.UInt8 or \
        vt == VarType.UInt16 or \
        vt == VarType.UInt32 or \
        vt == VarType.UInt64


def is_signed_v(a):
    return not is_unsigned_v(a)


def int_array_t(a):
    if not is_array_v(a):
        return int

    size = a.Type.Size
    if size == 1:
        vt = VarType.Int8
    elif size == 2:
        vt = VarType.Int16
    elif size == 4:
        vt = VarType.Int32
    elif size == 8:
        vt = VarType.Int64
    else:
        raise Exception("Unsupported variable size!")

    t = a.ReplaceScalar(vt)
    return t if isinstance(a, type) else t(a)


def uint_array_t(a):
    if not is_array_v(a):
        return int

    size = a.Type.Size
    if size == 1:
        vt = VarType.UInt8
    elif size == 2:
        vt = VarType.UInt16
    elif size == 4:
        vt = VarType.UInt32
    elif size == 8:
        vt = VarType.UInt64
    else:
        raise Exception("Unsupported variable size!")

    t = a.ReplaceScalar(vt)
    return t if isinstance(a, type) else t(a)


def float_array_t(a):
    if not is_array_v(a):
        return int

    size = a.Type.Size
    if size == 2:
        vt = VarType.Float16
    elif size == 4:
        vt = VarType.Float32
    elif size == 8:
        vt = VarType.Float64
    else:
        raise Exception("Unsupported variable size!")

    t = a.ReplaceScalar(vt)
    return t if isinstance(a, type) else t(a)


def uint32_array_t(a):
    t = a.ReplaceScalar(VarType.UInt32) if is_array_v(a) else int
    return t if isinstance(a, type) else t(a)


def int32_array_t(a):
    t = a.ReplaceScalar(VarType.Int32) if is_array_v(a) else int
    return t if isinstance(a, type) else t(a)


def uint64_array_t(a):
    t = a.ReplaceScalar(VarType.UInt64) if is_array_v(a) else int
    return t if isinstance(a, type) else t(a)


def int64_array_t(a):
    t = a.ReplaceScalar(VarType.Int64) if is_array_v(a) else int
    return t if isinstance(a, type) else t(a)


def float32_array_t(a):
    t = a.ReplaceScalar(VarType.Float32) if is_array_v(a) else float
    return t if isinstance(a, type) else t(a)


def float64_array_t(a):
    t = a.ReplaceScalar(VarType.Float64) if is_array_v(a) else float
    return t if isinstance(a, type) else t(a)


def diff_array_t(a):
    if isinstance(a, type):
        if not is_array_v(a):
            raise Exception("diff_array_t(): requires an Enoki input array!")
        if a.IsDiff:
            return a
        mod = a.__module__ \
            .replace('cuda', 'cuda.ad') \
            .replace('llvm', 'llvm.ad')
        if mod == a.__module__:
            raise Exception("diff_array_t(): input type unsupported!")
        return getattr(_sys.modules.get(mod), a.__name__)
    else:
        return diff_array_t(type(a))(a)


def nondiff_array_t(a):
    if isinstance(a, type):
        if not is_array_v(a):
            raise Exception("diff_array_t(): requires an Enoki input array!")
        if not a.IsDiff:
            return a
        mod = a.__module__ \
            .replace('cuda.ad', 'cuda') \
            .replace('llvm.ad', 'llvm')
        if mod == a.__module__:
            raise Exception("diff_array_t(): input type unsupported!")
        return getattr(_sys.modules.get(mod), a.__name__)
    else:
        return nondiff_array_t(type(a))(a)
