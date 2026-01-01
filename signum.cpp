/*
 * signum.cpp
 * A versatile, branchless implementation of the universal sign function for Python.
 * Version: 1.1.0
 * Released: December 31, 2025 ❄️ New Year Edition
 * Author: Alexandru Colesnicov
 * License: MIT
 */

#include <Python.h>

static PyObject *signum_sign(PyObject *module, PyObject *args, PyObject *kwds)
{
    /* Processing arguments */
    PyObject *x;
    PyObject *if_exc = Py_None;
    PyObject *preprocess = Py_None;
    static const char *kwlist[] = {"x", "if_exc", "preprocess", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|$OO", const_cast<char**>(kwlist),
                                     &x, &if_exc, &preprocess)) {
        return NULL; /* Error in arguments: delegated to Python */
    }

    /* preprocess */
    PyObject *to_free = NULL;
    if (preprocess != Py_None) { /* 'preprocess' argument exists, call it without checking */
        PyObject *ppres = PyObject_CallFunctionObjArgs(preprocess, x, NULL);
        if (ppres == NULL) { /* Error inside 'preprocess(x)': ignore */
            PyErr_Clear();
        } else {
            if (PyTuple_Check(ppres)) { /* 'ppres' is a tuple */
                Py_ssize_t t_size = PyTuple_Size(ppres);

                /* Optimization: Tell the compiler that 'tsize' >= 0 */
                #if __has_cpp_attribute(assume)
                    [[assume(0 <= t_size)]];
                #elif defined(_MSC_VER)
                    __assume(0 <= t_size);
                #elif defined(__GNUC__) || defined(__clang__)
                    if (t_size < 0) __builtin_unreachable();
                #endif

                switch (t_size) {
                    case 0: break; /* Ignore the empty tuple */
                    case 1: {      /* Replace argument */
                        PyObject *item0 = PyTuple_GetItem(ppres, 0);
                        Py_INCREF(item0);
                        x = item0;
                        to_free = item0;
                        break;
                    }
                    default: {     /* 't_size' > 1: replace result */
                        PyObject *item1 = PyTuple_GetItem(ppres, 1);
                        Py_INCREF(item1);
                        Py_DECREF(ppres);
                        return item1;
                    }
                }
            }
            Py_DECREF(ppres);
        }
    }

    /* Check for numeric NaN */
    double d = PyFloat_AsDouble(x);
    if (Py_IS_NAN(d)) {
        Py_XDECREF(to_free);
        return PyFloat_FromDouble(Py_NAN);
    }
    /* If it is something special, we will nevertheless try comparisons */
    if (PyErr_Occurred()) PyErr_Clear();

    PyObject *zero = PyLong_FromLong(0);
    if (!zero) { /* Memory Error? */
        Py_XDECREF(to_free);
        return NULL;
    }

    /* Start of the ternary logic block */
    int gt, lt, eq, res, code, self_eq;

    gt = PyObject_RichCompareBool(x, zero, Py_GT) + 1; /* 0: Error; 1: False; 2: True */
    code = gt;

    lt = PyObject_RichCompareBool(x, zero, Py_LT) + 1;
    res = gt - lt; /* Result, if nothing special */

    /* Optimization: Tell the compiler that 'lt' is strictly within [0, 2] */
    #if __has_cpp_attribute(assume)
        [[assume(0 <= lt && lt <= 2)]];
    #elif defined(_MSC_VER)
        __assume(0 <= lt && lt <= 2);
    #elif defined(__GNUC__) || defined(__clang__)
        if (!(0 <= lt && lt <= 2)) __builtin_unreachable();
    #endif

    switch (lt) {
        case 0: goto error;
        case 1: break; /* 'code == gt' is mutiplied by 'lt == 1' */
        case 2: code = (code << 1) & 3; /* 'code == gt' is shift-mutiplied by 'lt == 2'
                                                        and truncated mod 4 */
    }

    eq = PyObject_RichCompareBool(x, zero, Py_EQ) + 1; /* Used only to process NaN and errors */
    Py_DECREF(zero); /* Not used anymore */

    #if __has_cpp_attribute(assume)
        [[assume(0 <= eq && eq <= 2)]];
    #elif defined(_MSC_VER)
        __assume(0 <= eq && eq <= 2);
    #elif defined(__GNUC__) || defined(__clang__)
        if (!(0 <= eq && eq <= 2)) __builtin_unreachable();
    #endif

    switch (eq) {
        case 0: goto error;
        case 1: break; /* 'code == (gt * lt) & 3' is mutiplied by 'eq == 1' */
        case 2: code = (code << 1) & 3; /* 'code == (gt * lt) & 3' is shift-mutiplied by 'eq == 2'
                                                                   and truncated mod 4 */
    }

    /* Short Logic Overview:
       - 'code == 0': Multiple 'True' flags or an error occurred. Maps to 0, 4, 8; this is 0 mod 4.
       - 'code == 1': Triple 'False' state (1,1,1). Potential NaN; requires self-comparison.
       - 'code == 2': Exactly one 'True' flag, no errors. Valid numeric state.
    */

    /* Detailed Logic Overview:
       'gt', 'lt', 'eq' can be 0 for 'Error', 1 for 'False', 2 for 'True' (ternary logic).
       'code = (gt*lt*eq) & 3'; equivalent is '(gt*lt*eq) % 4'.
       'code' is 0:
         - if we have one, two, or three errors; then the product is 0;
           (we already processed errors in 'lt' or 'eq' directly by 'goto error;');
         - if we have two 'True' and one 'False', or three 'True'; the product is 4 or 8,
              which gives 0 (mod 4).
       'code' is 1:
         - if we have triple 'False', that indicates a potential NaN, and we perform
           an additional self-comparison;
       'code' is 2:
         - only if we have one 'True' and two 'False': it's a valid number */

    #if __has_cpp_attribute(assume)
        [[assume(0 <= code && code <= 2)]];
    #elif defined(_MSC_VER)
        __assume(0 <= code && code <= 2);
    #elif defined(__GNUC__) || defined(__clang__)
        if (!(0 <= code && code <= 2)) __builtin_unreachable();
    #endif

    switch (code) {
        case 0: goto error;
        case 1: { /* possible NaN '(False, False, False)' */
            self_eq = PyObject_RichCompareBool(x, x, Py_EQ);

            #if __has_cpp_attribute(assume)
                [[assume(-1 <= self_eq && self_eq <= 1)]];
            #elif defined(_MSC_VER)
                __assume(-1 <= self_eq && self_eq <= 1);
            #elif defined(__GNUC__) || defined(__clang__)
                if (!(-1 <= self_eq && self_eq <= 1)) __builtin_unreachable();
            #endif

            switch (self_eq) {
                case -1: { /* Error in __eq__, we keep current Python error */
                    Py_XDECREF(to_free);
                    return NULL;
                }
                case  0: {
                    Py_XDECREF(to_free);
                    return PyFloat_FromDouble(Py_NAN); /* NaN: not equal to itself */
                }
                case  1: goto error; /* Not a NaN: equals to itself; not comparable to 0 */
            }
        }
        case 2: {
            Py_XDECREF(to_free);
            return PyLong_FromLong((long)res);
        }
    }
    goto error;

error:

    if (if_exc != Py_None) { /* 'if_exc' argument exists, return its 0th element instead of error */
        PyErr_Clear();
        PyObject *item = PyTuple_GetItem(if_exc, 0); /* We don't check 'if_exc' that should be tuple */
        Py_INCREF(item);
        Py_XDECREF(to_free);
        return item;
    }

    if (PyErr_Occurred()) {
        PyObject *type, *value, *traceback;
        /* Extract the current error */
        PyErr_Fetch(&type, &value, &traceback);
        PyErr_NormalizeException(&type, &value, &traceback);

        /* Prepare the argument details */
        PyObject *repr = PyObject_Repr(x);
        const char *type_name = Py_TYPE(x)->tp_name;

        /* Prepare the old error as string */
        PyObject *old_msg = PyObject_Str(value);
        const char *old_msg_str = old_msg ? PyUnicode_AsUTF8(old_msg) : "unknown error";

        /* Format the new message */
        PyErr_Format(PyExc_TypeError,
            "signum.sign: invalid argument `%.160s` (type '%.80s'). "
            "Inner error: %.320s",
            repr ? PyUnicode_AsUTF8(repr) : "???",
            type_name,
            old_msg_str);

        /* Clean memory */
        Py_XDECREF(repr);
        Py_XDECREF(old_msg);
        Py_XDECREF(type);
        Py_XDECREF(value);
        Py_XDECREF(traceback);
    }
    else {
        PyObject *repr = PyObject_Repr(x);
        const char *type_name = Py_TYPE(x)->tp_name;

        if (repr) {
            PyErr_Format(PyExc_TypeError,
                "signum.sign: invalid argument `%.160s`. "
                "Type '%.80s' does not support order comparisons (>, <, ==) "
                "or NaN detection.",
                PyUnicode_AsUTF8(repr),
                type_name);
            Py_DECREF(repr);
        }
        else {
            PyErr_Format(PyExc_TypeError,
                "signum.sign: invalid argument of type '%.80s', "
                "which does not support order comparisons (>, <, ==) and printing.",
                type_name);
        }
    }
    Py_XDECREF(to_free);
    return NULL;
}

/* --- FORMALITIES --- */

/* List of implemented methods */
static PyMethodDef SignumMethods[] = {
    {"sign", (PyCFunction)signum_sign, METH_VARARGS | METH_KEYWORDS, "Return the sign of x: -1, 0, 1, or NaN."},
    {NULL, NULL, 0, NULL} /* Stop-string */
};

/* Module description */
static struct PyModuleDef signummodule = {
    PyModuleDef_HEAD_INIT,
    "signum",  /* Module name for import */
    "Fast signum implementation with ternary logic.",
    -1,
    SignumMethods
};

/* Module initialization */
PyMODINIT_FUNC PyInit_signum(void) {
    return PyModule_Create(&signummodule);
}
