/*
 * Padded allocations for ArcSoft's libmpbase.
 *
 * The ArcSoft dual-camera refocus engine reads a little past the end of
 * large working buffers it gets from MMemAlloc(). Android 11's allocator
 * left readable memory there; Scudo puts a guard page right after large
 * (secondary) allocations, so Portrait capture faults with SEGV_ACCERR.
 * libmpbase's malloc/realloc imports are renamed to these, which add slack
 * after large blocks so the over-read stays inside the allocation.
 */
#include <stdint.h>
#include <stdlib.h>

#define PAD_THRESHOLD (64 * 1024)
#define PAD (16 * 1024)

static size_t padded(size_t n) {
    if (n < PAD_THRESHOLD || n > SIZE_MAX - PAD) return n;
    return n + PAD;
}

void *mpbase_shim_malloc(size_t n) {
    return malloc(padded(n));
}

void *mpbase_shim_realloc(void *p, size_t n) {
    return realloc(p, padded(n));
}
