#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
	"device/xiaomi/raphael",
	"hardware/qcom-caf/sm8150",
	"hardware/qcom-caf/wlan",
	"hardware/xiaomi",
	"vendor/qcom/opensource/dataservices",
	"vendor/qcom/opensource/commonsys-intf/display",
	"vendor/qcom/opensource/commonsys/display",
	"vendor/qcom/opensource/display",
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.fm@1.0',
        'libmmosal',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/lib/hw/audio.primary.raphael.so', 'vendor/lib/libaudioroute_ext.so'): blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    'vendor/lib64/camera/components/com.qti.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    (
     'vendor/lib64/libalAILDC.so',
     'vendor/lib64/libalLDC.so',
     'vendor/lib64/libalhLDC.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
     (
      'vendor/lib64/libarcsoft_dualcam_refocus_front.so',
      'vendor/lib64/libarcsoft_dualcam_refocus_rear_t.so',
      'vendor/lib64/libarcsoft_dualcam_refocus_rear_w.so'
      ): blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open')
        .clear_symbol_version('remote_register_buf_attr')
        .clear_symbol_version('remote_register_buf'),
    (
    'vendor/etc/wfdconfig.xml'
    ): blob_fixup()
        .regex_replace('<AudioStreamInSuspend>0</AudioStreamInSuspend>', '<AudioStreamInSuspend>1</AudioStreamInSuspend>')
        .regex_replace('<HID>0</HID>', '<HID>1</HID>'),
    (
        'vendor/lib64/libwvhidl.so',
        'vendor/lib/mediadrm/libwvdrmengine.so',
        'vendor/lib64/mediadrm/libwvdrmengine.so'
    ): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    (
        'vendor/etc/init/vendor.qti.media.c2@1.0-service.rc'
    ): blob_fixup()
        .regex_replace(r'writepid.*', 'task_profiles ProcessCapacityHigh HighPerformance'),
    (
        'vendor/lib/libaudioroute_ext.so',
    ): blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    (
    'vendor/etc/seccomp_policy/vendor.qti.hardware.dsp.policy' 
    ): blob_fixup()
        .add_line_if_missing('madvise: 1')
        .add_line_if_missing('+gettimeofday:: 1'),
}  # fmt: skip

module = ExtractUtilsModule(
    'raphael',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

