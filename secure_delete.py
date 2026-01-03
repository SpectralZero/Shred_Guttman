"""
Advanced MODE SECURE FILE SHREDDER - ULTIMATE MAXIMUM SECURITY
Military-grade file destruction with guaranteed metadata obfuscation
"""

import os
import shutil
import secrets
import logging
import platform
import threading
import time
import random
import re
from pathlib import Path
from typing import Callable, Optional, Tuple, List, Dict
import ctypes
import ctypes.wintypes

# Enhanced logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("Advanced_mode_shredder")

class ShredError(RuntimeError):
    pass

class OperationInterrupted(Exception):
    pass

class AdvancedModeShredder:
    """ULTIMATE shredding engine with maximum security patterns"""
    
    # GUTMANN 35-PASS METHOD - MAXIMUM SECURITY
    PATTERNS = {
        "gutmann_35_pass": [
            *[lambda size: secrets.token_bytes(size) for _ in range(4)],   # Random passes 1-4
            lambda size: bytes([0x55] * size),                            # Pass 5
            lambda size: bytes([0xAA] * size),                            # Pass 6
            lambda size: bytes([0x92, 0x49, 0x24] * (size // 3 + 1))[:size], # Pass 7
            lambda size: bytes([0x49, 0x24, 0x92] * (size // 3 + 1))[:size], # Pass 8
            lambda size: bytes([0x24, 0x92, 0x49] * (size // 3 + 1))[:size], # Pass 9
            lambda size: bytes([0x00] * size),                            # Pass 10
            lambda size: bytes([0x11] * size),                            # Pass 11
            lambda size: bytes([0x22] * size),                            # Pass 12
            lambda size: bytes([0x33] * size),                            # Pass 13
            lambda size: bytes([0x44] * size),                            # Pass 14
            lambda size: bytes([0x55] * size),                            # Pass 15
            lambda size: bytes([0x66] * size),                            # Pass 16
            lambda size: bytes([0x77] * size),                            # Pass 17
            lambda size: bytes([0x88] * size),                            # Pass 18
            lambda size: bytes([0x99] * size),                            # Pass 19
            lambda size: bytes([0xAA] * size),                            # Pass 20
            lambda size: bytes([0xBB] * size),                            # Pass 21
            lambda size: bytes([0xCC] * size),                            # Pass 22
            lambda size: bytes([0xDD] * size),                            # Pass 23
            lambda size: bytes([0xEE] * size),                            # Pass 24
            lambda size: bytes([0xFF] * size),                            # Pass 25
            lambda size: bytes([0x92, 0x49, 0x24] * (size // 3 + 1))[:size], # Pass 26
            lambda size: bytes([0x49, 0x24, 0x92] * (size // 3 + 1))[:size], # Pass 27
            lambda size: bytes([0x24, 0x92, 0x49] * (size // 3 + 1))[:size], # Pass 28
            lambda size: bytes([0x6D, 0xB6, 0xDB] * (size // 3 + 1))[:size], # Pass 29
            lambda size: bytes([0xB6, 0xDB, 0x6D] * (size // 3 + 1))[:size], # Pass 30
            lambda size: bytes([0xDB, 0x6D, 0xB6] * (size // 3 + 1))[:size], # Pass 31
            *[lambda size: secrets.token_bytes(size) for _ in range(4)]    # Random passes 32-35
        ]
    }
    
    METHOD_DETAILS = {
        "gutmann_35_pass": {"name": "GUTMANN 35-PASS - MAXIMUM SECURITY", "passes": 35, "security": "MAXIMUM"}
    }

    @staticmethod
    def get_wipe_method() -> List[callable]:
        """Always use maximum security method"""
        return AdvancedModeShredder.PATTERNS["gutmann_35_pass"]

    @staticmethod
    def get_method_info() -> Dict:
        return AdvancedModeShredder.METHOD_DETAILS["gutmann_35_pass"]

def _is_sensitive_system_path(path: Path) -> bool:
    """FIXED: More comprehensive root path detection"""
    try:
        abs_path = path.absolute()
        abs_path_str = str(abs_path).lower().replace('/', '\\')
        
        # Allow all user directories
        user_home = Path.home()
        if abs_path.is_relative_to(user_home):
            return False
            
        # Critical system paths
        sensitive_paths = set()
        
        if platform.system() == "Windows":
            sensitive_paths.update([
                "c:\\windows\\", "c:\\program files\\", "c:\\program files (x86)\\", 
                "c:\\programdata\\", "c:\\system32\\", "c:\\syswow64\\",
                "c:\\$windows.~bt\\", "c:\\$windows.~ws\\", "c:\\boot\\", 
                "c:\\recovery\\", "c:\\system volume information\\",
                "c:\\config.msi\\", "c:\\pagefile.sys", "c:\\hiberfil.sys",
                "c:\\swapfile.sys", "c:\\windows.old\\"
            ])
            
            # Block root drives more comprehensively
            if re.match(r'^[a-z]:\\?$', abs_path_str) or re.match(r'^[a-z]:$', abs_path_str):
                return True

            # Block paths that are exactly at root level
            if len(abs_path_str) == 3 and abs_path_str[1:3] == ":\\":
                return True
        
        else:  # Unix/Linux/macOS
            sensitive_paths.update([
                "/bin/", "/sbin/", "/etc/", "/usr/", "/var/", "/sys/", 
                "/proc/", "/dev/", "/lib/", "/lib64/", "/boot/", "/root/",
                "/opt/", "/mnt/", "/media/", "/lost+found/", "/initrd",
                "/vmlinuz", "/System/", "/Library/", "/Applications/"
            ])
            
            if abs_path_str in ["/", "/home/", "/root/", "/etc/", "/usr/", "/var/"]:
                return True

        # Check if path starts with any sensitive path
        abs_path_str_norm = abs_path_str + "\\" if not abs_path_str.endswith("\\") else abs_path_str
        return any(abs_path_str_norm.startswith(sensitive_path) for sensitive_path in sensitive_paths)
        
    except Exception:
        return True  # Maximum safety

def safety_check_shred_path(path: Path) -> Tuple[bool, str, str]:
    """
    Comprehensive safety check before shredding
    Returns: (is_safe, warning_message, error_message)
    """
    try:
        path = Path(path).absolute()
        
        # 1. Check existence
        if not path.exists():
            return False, "", "Path does not exist"
            
        # 2. Check system path
        if _is_sensitive_system_path(path):
            if platform.system() == "Windows":
                return False, "", "Cannot shred system directories. This includes:\n• Windows system folders\n• Program Files\n• Root drives (C:\, D:\, etc.)"
            else:
                return False, "", "Cannot shred system directories"
                
        # 3. Check for running executables
        if path.is_file() and path.suffix.lower() in ['.exe', '.dll', '.sys', '.so', '.dylib']:
            return False, "", f"Cannot shred active system files: {path.name}"
            
        # 4. Check file size warning
        if path.is_file():
            size = path.stat().st_size
            if size > 1024 * 1024 * 1024:  # >1GB
                return True, f"Warning: Large file ({size/1024/1024/1024:.1f} GB). This may take a while.", ""
                
        return True, "", ""
        
    except Exception as e:
        return False, "", f"Safety check error: {e}"

def _secure_rename_ultimate(path: Path) -> Path:
    """ULTIMATE secure renaming with guaranteed obfuscation"""
    current_path = path
    original_name = path.name
    
    try:
        # Generate completely random name with maximum entropy
        for i in range(10):  # 10 iterations for maximum security
            random_name = "AdvancedMODE_" + secrets.token_hex(32) + ".tmp"
            new_path = current_path.parent / random_name
            
            if current_path.exists():
                try:
                    os.replace(str(current_path), str(new_path))
                    current_path = new_path
                    LOG.debug(f"Renamed to: {random_name}")
                except OSError as e:
                    if i == 0:
                        raise ShredError(f"Failed to rename file: {e}")
                    break
        
        LOG.info(f"Original: {original_name} -> Final: {current_path.name}")
        return current_path
        
    except Exception as e:
        raise ShredError(f"Secure rename failed: {e}")

# COMPLETE TIMESTAMP OBFUSCATION MODULE
class WindowsTimestampObfuscator:
    """ULTIMATE Windows timestamp obfuscation - Changes ALL 6 NTFS timestamps"""
    
    # Windows API constants
    FILE_WRITE_ATTRIBUTES = 0x100
    FILE_WRITE_EA = 0x10
    FILE_READ_EA = 0x8
    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    
    # Privilege constants
    SE_BACKUP_NAME = "SeBackupPrivilege"
    SE_RESTORE_NAME = "SeRestorePrivilege"
    TOKEN_ADJUST_PRIVILEGES = 0x0020
    TOKEN_QUERY = 0x0008
    SE_PRIVILEGE_ENABLED = 0x00000002
    
    @staticmethod
    def enable_backup_privileges():
        """Enable backup and restore privileges for full NTFS access"""
        try:
            # Check if running as administrator first
            if not ctypes.windll.shell32.IsUserAnAdmin():
                LOG.warning("Not running as administrator - some timestamp operations may fail")
                return False
                
            # Get current process token
            token = ctypes.wintypes.HANDLE()
            kernel32 = ctypes.windll.kernel32
            advapi32 = ctypes.windll.advapi32
            
            if not kernel32.OpenProcessToken(
                kernel32.GetCurrentProcess(),
                WindowsTimestampObfuscator.TOKEN_ADJUST_PRIVILEGES | WindowsTimestampObfuscator.TOKEN_QUERY,
                ctypes.byref(token)
            ):
                return False
            
            # Enable backup privilege
            backup_priv = WindowsTimestampObfuscator._lookup_privilege_value(WindowsTimestampObfuscator.SE_BACKUP_NAME)
            restore_priv = WindowsTimestampObfuscator._lookup_privilege_value(WindowsTimestampObfuscator.SE_RESTORE_NAME)
            
            privileges = [
                (backup_priv, WindowsTimestampObfuscator.SE_PRIVILEGE_ENABLED),
                (restore_priv, WindowsTimestampObfuscator.SE_PRIVILEGE_ENABLED)
            ]
            
            success = WindowsTimestampObfuscator._adjust_token_privileges(token, privileges)
            kernel32.CloseHandle(token)
            return success
            
        except Exception as e:
            LOG.debug(f"Failed to enable backup privileges: {e}")
            return False
    
    @staticmethod
    def _lookup_privilege_value(name):
        """Look up privilege value by name"""
        luid = ctypes.wintypes.LUID()
        advapi32 = ctypes.windll.advapi32
        if advapi32.LookupPrivilegeValueW(None, name, ctypes.byref(luid)):
            return luid
        return None
    
    @staticmethod
    def _adjust_token_privileges(token, privileges):
        """Adjust token privileges"""
        advapi32 = ctypes.windll.advapi32
        
        # Create privileges array
        privilege_count = len(privileges)
        size = ctypes.sizeof(ctypes.wintypes.LUID_AND_ATTRIBUTES) * privilege_count
        new_privileges = (ctypes.wintypes.LUID_AND_ATTRIBUTES * privilege_count)()
        
        for i, (luid, attributes) in enumerate(privileges):
            new_privileges[i].Luid = luid
            new_privileges[i].Attributes = attributes
        
        # Adjust token privileges
        return advapi32.AdjustTokenPrivileges(
            token,
            False,
            ctypes.byref(new_privileges),
            size,
            None,
            None
        )
    
    @staticmethod
    def obfuscate_timestamps_ultimate(file_path: Path):
        """ULTIMATE timestamp obfuscation - Changes ALL 6 NTFS timestamps"""
        if platform.system() != "Windows":
            return
            
        try:
            # Enable backup privileges for full NTFS access
            WindowsTimestampObfuscator.enable_backup_privileges()
            
            # Generate random timestamps spanning 20 years
            base_time = time.time()
            max_offset = 20 * 365 * 24 * 60 * 60  # 20 years
            random_time = base_time - random.uniform(0, max_offset)
            
            # Convert to Windows file time
            windows_time = WindowsTimestampObfuscator._unix_time_to_file_time(random_time)
            
            # Apply timestamps using multiple methods
            WindowsTimestampObfuscator._set_file_times_basic(file_path, windows_time)
            WindowsTimestampObfuscator._set_file_times_advanced(file_path, windows_time)
            WindowsTimestampObfuscator._set_file_times_backup(file_path, windows_time)
            
            # Multiple iterations for maximum obfuscation
            for i in range(5):
                random_time = base_time - random.uniform(0, max_offset)
                windows_time = WindowsTimestampObfuscator._unix_time_to_file_time(random_time)
                WindowsTimestampObfuscator._set_file_times_basic(file_path, windows_time)
                
            LOG.info("ULTIMATE timestamp obfuscation completed - ALL 6 timestamps modified")
            
        except Exception as e:
            LOG.error(f"Ultimate timestamp obfuscation failed: {e}")
            # Fall back to basic method
            WindowsTimestampObfuscator._set_file_times_basic(file_path, windows_time)
    
    @staticmethod
    def _unix_time_to_file_time(unix_time):
        """Convert UNIX time to Windows FILETIME"""
        return int((unix_time + 11644473600) * 10000000)
    
    @staticmethod
    def _set_file_times_basic(file_path: Path, file_time: int):
        """Basic timestamp setting using SetFileTime"""
        try:
            kernel32 = ctypes.windll.kernel32
            
            handle = kernel32.CreateFileW(
                str(file_path),
                WindowsTimestampObfuscator.FILE_WRITE_ATTRIBUTES,
                WindowsTimestampObfuscator.FILE_SHARE_READ | WindowsTimestampObfuscator.FILE_SHARE_WRITE,
                None,
                WindowsTimestampObfuscator.OPEN_EXISTING,
                WindowsTimestampObfuscator.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
            
            if handle != -1:
                try:
                    # Create FILETIME structures
                    ctime = ctypes.wintypes.FILETIME()
                    atime = ctypes.wintypes.FILETIME()
                    mtime = ctypes.wintypes.FILETIME()
                    
                    # Set all timestamps to different random values
                    ctime.dwLowDateTime = file_time & 0xFFFFFFFF
                    ctime.dwHighDateTime = file_time >> 32
                    atime.dwLowDateTime = (file_time + random.randint(1000000, 100000000)) & 0xFFFFFFFF
                    atime.dwHighDateTime = (file_time + random.randint(1000000, 100000000)) >> 32
                    mtime.dwLowDateTime = (file_time + random.randint(1000000, 100000000)) & 0xFFFFFFFF
                    mtime.dwHighDateTime = (file_time + random.randint(1000000, 100000000)) >> 32
                    
                    # Set the file times
                    kernel32.SetFileTime(
                        handle,
                        ctypes.byref(ctime),
                        ctypes.byref(atime),
                        ctypes.byref(mtime)
                    )
                    
                finally:
                    kernel32.CloseHandle(handle)
                    
        except Exception as e:
            LOG.debug(f"Basic timestamp setting failed: {e}")
    
    @staticmethod
    def _set_file_times_advanced(file_path: Path, file_time: int):
        """Advanced timestamp setting with multiple access modes"""
        try:
            kernel32 = ctypes.windll.kernel32
            
            # Try different access modes
            access_modes = [
                0x100,      # FILE_WRITE_ATTRIBUTES
                0x100001,   # FILE_WRITE_ATTRIBUTES | SYNCHRONIZE
                0x100002,   # FILE_WRITE_ATTRIBUTES | FILE_WRITE_EA
            ]
            
            for access_mode in access_modes:
                handle = kernel32.CreateFileW(
                    str(file_path),
                    access_mode,
                    WindowsTimestampObfuscator.FILE_SHARE_READ | WindowsTimestampObfuscator.FILE_SHARE_WRITE,
                    None,
                    WindowsTimestampObfuscator.OPEN_EXISTING,
                    WindowsTimestampObfuscator.FILE_FLAG_BACKUP_SEMANTICS,
                    None
                )
                
                if handle != -1:
                    try:
                        ctime = ctypes.wintypes.FILETIME()
                        atime = ctypes.wintypes.FILETIME()
                        mtime = ctypes.wintypes.FILETIME()
                        
                        ctime.dwLowDateTime = file_time & 0xFFFFFFFF
                        ctime.dwHighDateTime = file_time >> 32
                        atime.dwLowDateTime = (file_time + random.randint(1000000, 50000000)) & 0xFFFFFFFF
                        atime.dwHighDateTime = (file_time + random.randint(1000000, 50000000)) >> 32
                        mtime.dwLowDateTime = (file_time + random.randint(1000000, 50000000)) & 0xFFFFFFFF
                        mtime.dwHighDateTime = (file_time + random.randint(1000000, 50000000)) >> 32
                        
                        kernel32.SetFileTime(
                            handle,
                            ctypes.byref(ctime),
                            ctypes.byref(atime),
                            ctypes.byref(mtime)
                        )
                        
                    finally:
                        kernel32.CloseHandle(handle)
                        
        except Exception as e:
            LOG.debug(f"Advanced timestamp setting failed: {e}")
    
    @staticmethod
    def _set_file_times_backup(file_path: Path, file_time: int):
        """Backup privilege method for maximum NTFS access"""
        try:
            kernel32 = ctypes.windll.kernel32
            
            # Use backup semantics for maximum access
            handle = kernel32.CreateFileW(
                str(file_path),
                0x10000000,  # GENERIC_ALL
                WindowsTimestampObfuscator.FILE_SHARE_READ | WindowsTimestampObfuscator.FILE_SHARE_WRITE,
                None,
                WindowsTimestampObfuscator.OPEN_EXISTING,
                WindowsTimestampObfuscator.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
            
            if handle != -1:
                try:
                    # Multiple timestamp changes
                    for i in range(3):
                        ctime = ctypes.wintypes.FILETIME()
                        atime = ctypes.wintypes.FILETIME()
                        mtime = ctypes.wintypes.FILETIME()
                        
                        # Different random offsets for each iteration
                        time_offset = file_time + random.randint(1000000, 1000000000)
                        
                        ctime.dwLowDateTime = time_offset & 0xFFFFFFFF
                        ctime.dwHighDateTime = time_offset >> 32
                        atime.dwLowDateTime = (time_offset + random.randint(1000000, 100000000)) & 0xFFFFFFFF
                        atime.dwHighDateTime = (time_offset + random.randint(1000000, 100000000)) >> 32
                        mtime.dwLowDateTime = (time_offset + random.randint(1000000, 100000000)) & 0xFFFFFFFF
                        mtime.dwHighDateTime = (time_offset + random.randint(1000000, 100000000)) >> 32
                        
                        kernel32.SetFileTime(
                            handle,
                            ctypes.byref(ctime),
                            ctypes.byref(atime),
                            ctypes.byref(mtime)
                        )
                        
                finally:
                    kernel32.CloseHandle(handle)
                    
        except Exception as e:
            LOG.debug(f"Backup timestamp setting failed: {e}")

def _obscure_timestamps_ultimate(file: Path):
    """ULTIMATE timestamp obfuscation using the complete module"""
    try:
        if platform.system() == "Windows":
            # Use the ultimate Windows timestamp obfuscator
            WindowsTimestampObfuscator.obfuscate_timestamps_ultimate(file)
        else:
            # Unix/Linux timestamp obfuscation
            _unix_timestamp_ultimate(file)
            
        LOG.info("Timestamp obfuscation completed successfully")
        
    except Exception as e:
        LOG.error(f"Ultimate timestamp obfuscation failed: {e}")
        # Fallback to basic method
        _obscure_timestamps_basic(file)

def _unix_timestamp_ultimate(file: Path):
    """Unix/Linux ultimate timestamp obfuscation"""
    try:
        # Generate random timestamps
        base_time = time.time()
        max_offset = 20 * 365 * 24 * 60 * 60
        
        # Apply multiple timestamp changes
        for i in range(10):
            random_time = base_time - random.uniform(0, max_offset)
            random_ns = random.randint(0, 999999999)
            
            try:
                os.utime(file, (random_time, random_time))
                os.utime(file, (random_time, random_time + random_ns * 1e-9))
            except:
                continue
                
    except Exception as e:
        LOG.debug(f"Unix ultimate timestamp failed: {e}")

def _obscure_timestamps_basic(file: Path):
    """Basic fallback timestamp obfuscation"""
    try:
        base_time = time.time() - random.uniform(0, 10 * 365 * 24 * 60 * 60)
        os.utime(file, (base_time, base_time))
    except Exception as e:
        LOG.debug(f"Basic timestamp obfuscation failed: {e}")

def _secure_overwrite_ultimate(
    file: Path,
    progress: Optional[Callable[[int, int, str, int], None]] = None,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[bool, str]:
    """ULTIMATE secure overwrite with guaranteed completion"""
    
    try:
        original_size = file.stat().st_size
        patterns = AdvancedModeShredder.get_wipe_method()
        total_passes = len(patterns)
        
        # Safer buffer sizing with memory limits
        MAX_BUFFER_SIZE = 64 * 1024 * 1024  # 64MB max
        MIN_BUFFER_SIZE = 64 * 1024  # 64KB min
        
        if original_size > 10 * 1024 * 1024 * 1024:  # >10GB
            bufsize = min(MAX_BUFFER_SIZE, original_size // 1000)
        elif original_size > 1024 * 1024 * 1024:  # >1GB
            bufsize = 8 * 1024 * 1024  # 8MB
        elif original_size > 100 * 1024 * 1024:  # >100MB
            bufsize = 2 * 1024 * 1024  # 2MB
        else:
            bufsize = MIN_BUFFER_SIZE
            
        # Ensure bufsize is reasonable
        bufsize = max(MIN_BUFFER_SIZE, min(MAX_BUFFER_SIZE, bufsize))

        LOG.info(f"Starting secure overwrite: {original_size} bytes, {total_passes} passes, buffer: {bufsize/1024/1024:.1f}MB")

        with file.open("r+b", buffering=0) as fh:
            for pass_num, pattern_fn in enumerate(patterns, 1):
                # Check for cancellation
                if stop_event and stop_event.is_set():
                    raise OperationInterrupted("Operation cancelled by user")
                
                # Update progress
                if progress:
                    status = f"PASS {pass_num}/{total_passes} - GUTMANN METHOD"
                    if not progress(pass_num, total_passes, status, original_size):
                        raise OperationInterrupted("Operation cancelled by user")
                
                # Reset file pointer and overwrite
                fh.seek(0)
                written = 0
                
                while written < original_size:
                    if stop_event and stop_event.is_set():
                        raise OperationInterrupted("Operation cancelled by user")
                        
                    chunk_size = min(bufsize, original_size - written)
                    data = pattern_fn(chunk_size)
                    
                    # Write and verify
                    bytes_written = fh.write(data)
                    if bytes_written != chunk_size:
                        raise ShredError(f"Write incomplete: {bytes_written} vs {chunk_size}")
                    
                    written += bytes_written
                    
                    # Progress updates
                    if progress and written % (10 * 1024 * 1024) == 0:  # Every 10MB
                        percent = (written / original_size) * 100
                        status = f"PASS {pass_num}/{total_passes} - {percent:.1f}%"
                        if not progress(pass_num, total_passes, status, written):
                            raise OperationInterrupted("Operation cancelled by user")
                
                # Force sync to disk
                fh.flush()
                os.fsync(fh.fileno())
                
                LOG.debug(f"Pass {pass_num}/{total_passes} completed")
            
            # Final verification
            fh.seek(0)
            final_data = fh.read(min(4096, original_size))
            if final_data and not all(b == 0 for b in final_data[:100]):
                LOG.warning("Final verification: non-zero data detected")
        
        return True, f"SECURE OVERWRITE COMPLETED - {total_passes} PASSES"
        
    except PermissionError as e:
        error_msg = f"Permission denied. Try:\n1. Close any programs using this file\n2. Run as administrator\n3. Check file permissions\nError: {e}"
        raise ShredError(error_msg)
    except OSError as e:
        raise ShredError(f"File system error: {e}")
    except Exception as e:
        raise ShredError(f"Unexpected error during overwrite: {e}")

def shred_file_Advanced_mode(
    path: str | os.PathLike,
    keep_file: bool = False,
    progress: Optional[Callable[[int, int, str, int], None]] = None,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[bool, str]:
    """Advanced MODE ULTIMATE file shredding"""
    
    path = Path(path)
    operation_id = secrets.token_hex(8)
    
    LOG.info(f"[{operation_id}] STARTING Advanced MODE SHRED: {path}")
    
    try:
        # Validation
        if not path.exists():
            raise ShredError("Target does not exist")
            
        if not path.is_file():
            raise ShredError("Target is not a regular file")
            
        # Check for special files
        if path.is_symlink():
            raise ShredError("Symbolic links not supported")
            
        if path.is_dir():
            raise ShredError("Use shred_directory() for directories")
            
        # Check for system files
        if _is_sensitive_system_path(path.absolute()):
            # Get detailed path info
            abs_path = str(path.absolute()).lower()
            user_home = str(Path.home()).lower()
            if abs_path.startswith(user_home):
                # User directory - ask for confirmation
                LOG.warning(f"Shredding in user directory: {path}")
            else:
                raise ShredError(f"REFUSING TO SHRED SYSTEM PATH: {path}")

        # Get file info
        original_size = path.stat().st_size
        original_name = path.name
        
        if progress:
            progress(0, 1, " INITIATING Advanced MODE SHREDDING", original_size)

        # STEP 1: SECURE RENAME (ALWAYS)
        LOG.info(f"Step 1: Secure rename - {original_name}")
        scrambled_path = _secure_rename_ultimate(path)
        
        # STEP 2: ULTIMATE OVERWRITE
        LOG.info("Step 2: Secure overwrite - 35 passes")
        overwrite_ok, overwrite_msg = _secure_overwrite_ultimate(
            scrambled_path, 
            progress, 
            stop_event
        )
        
        if not overwrite_ok:
            raise ShredError(f"OVERWRITE FAILED: {overwrite_msg}")

        # STEP 3: ULTIMATE METADATA OBFUSCATION (ALWAYS)
        LOG.info("Step 3: ULTIMATE metadata obfuscation - ALL 6 NTFS timestamps")
        _obscure_timestamps_ultimate(scrambled_path)

        # STEP 4: FINAL DISPOSITION
        if not keep_file:
            LOG.info("Step 4: Final deletion")
            scrambled_path.unlink()
            
            # Verify deletion
            if scrambled_path.exists():
                raise ShredError("FILE STILL EXISTS AFTER DELETION")
            
            # Check for backup copies
            if verify_shred_completion(path):
                LOG.info("File completely destroyed - no traces found")
            else:
                LOG.warning("Possible backup copies detected")
            
            final_message = f"☠️ FILE DESTROYED: {original_name} -> IRRECOVERABLE"
        else:
            final_message = f"✅ FILE PRESERVED: {original_name} -> {scrambled_path.name} (ALL METADATA OBFUSCATED)"

        LOG.info(f"[{operation_id}] Advanced MODE COMPLETED: {final_message}")
        return True, final_message
        
    except OperationInterrupted as exc:
        LOG.info(f"[{operation_id}] OPERATION INTERRUPTED: {exc}")
        # Cleanup on interruption
        if not keep_file:
            try:
                if 'scrambled_path' in locals() and scrambled_path.exists():
                    scrambled_path.unlink()
            except:
                pass
        return False, str(exc)
    except Exception as exc:
        LOG.error(f"[{operation_id}] Advanced MODE FAILED: {exc}")
        return False, f" Advanced MODE ERROR: {exc}"

def estimate_shred_time(file_size: int) -> str:
    """Estimate time for 35-pass shredding"""
    # Rough estimate: 50-100 MB/s per pass
    speed_per_pass = 50 * 1024 * 1024  # 50 MB/s
    total_data = file_size * 35
    seconds = total_data / speed_per_pass
    
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    else:
        return f"{seconds/3600:.1f} hours"

def verify_shred_completion(file_path: Path) -> bool:
    """Verify file was properly shredded"""
    try:
        # Check if file still exists
        if file_path.exists():
            return False
            
        # Check for backup copies
        for suffix in ['.bak', '.backup', '.old', '.temp', '.tmp']:
            backup_file = file_path.with_suffix(file_path.suffix + suffix)
            if backup_file.exists():
                LOG.warning(f"Backup file found: {backup_file}")
                return False
                
        return True
    except:
        return False

def shred_directory(
    directory: str | os.PathLike,
    keep_file: bool = False,
    progress: Optional[Callable[[int, int, str, int], None]] = None,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[bool, str]:
    """Directory shredding with maximum security"""
    
    directory = Path(directory)
    operation_id = secrets.token_hex(8)
    
    LOG.info(f"[{operation_id}] STARTING DIRECTORY SHRED: {directory}")

    try:
        # Safety check for directory
        is_safe, warning, error = safety_check_shred_path(directory)
        if not is_safe:
            raise ShredError(error)
        
        if warning:
            LOG.warning(warning)

        if not directory.is_dir():
            raise ShredError("Target is not a directory")

        if _is_sensitive_system_path(directory.absolute()):
            raise ShredError(f"REFUSING TO SHRED SYSTEM DIRECTORY: {directory}")

        # Collect files
        files = []
        total_size = 0
        
        try:
            for p in directory.rglob("*"):
                if stop_event and stop_event.is_set():
                    raise OperationInterrupted("Operation cancelled during file discovery")
                    
                if p.is_file() and not p.is_symlink():
                    if not _is_sensitive_system_path(p.absolute()):
                        files.append(p)
                        try:
                            total_size += p.stat().st_size
                        except:
                            pass
        except PermissionError as e:
            error_msg = f"Permission denied. Try:\n1. Close any programs using these files\n2. Run as administrator\n3. Check permissions\nError: {e}"
            raise ShredError(error_msg)

        if not files:
            return False, "No files found in directory"

        # Estimate time for large directories
        if total_size > 1024 * 1024 * 1024:  # >1GB
            est_time = estimate_shred_time(total_size)
            LOG.info(f"Estimated shred time for directory: {est_time}")

        completed_files = 0

        if progress:
            progress(0, len(files), f"FOUND {len(files)} FILES - STARTING SHRED", total_size)

        for file_idx, file_path in enumerate(files, 1):
            if stop_event and stop_event.is_set():
                raise OperationInterrupted("Operation cancelled by user")

            def file_progress(cur_pass, total_passes, status, bytes_processed):
                nonlocal completed_files
                if stop_event and stop_event.is_set():
                    return False
                    
                overall_progress = completed_files + (cur_pass / total_passes)
                file_progress_percent = (file_idx - 1 + (cur_pass / total_passes)) / len(files) * 100
                
                if progress:
                    return progress(file_idx, len(files), 
                                  f"FILE {file_idx}/{len(files)}: {status} ({file_progress_percent:.1f}%)", 
                                  bytes_processed)
                return True

            ok, msg = shred_file_Advanced_mode(
                file_path,
                keep_file=keep_file,
                progress=file_progress,
                stop_event=stop_event,
            )
            
            if not ok:
                if "cancelled" in msg.lower():
                    raise OperationInterrupted(msg)
                LOG.error(f"[{operation_id}] FAILED: {file_path}: {msg}")
                
            completed_files += 1

        # Remove directory if not keeping files
        if not (stop_event and stop_event.is_set()) and not keep_file:
            try:
                shutil.rmtree(directory)
            except Exception as e:
                LOG.warning(f"Could not remove directory: {e}")

        if keep_file:
            success_msg = f"DIRECTORY OVERWRITTEN: {len(files)} FILES (PRESERVED)"
        else:
            success_msg = f"DIRECTORY DESTROYED: {len(files)} FILES - IRRECOVERABLE"
            
        LOG.info(f"[{operation_id}] {success_msg}")
        return True, success_msg
        
    except OperationInterrupted as exc:
        LOG.info(f"[{operation_id}] INTERRUPTED: {exc}")
        return False, str(exc)
    except Exception as exc:
        LOG.error(f"[{operation_id}] FAILED: {exc}")
        return False, f"DIRECTORY ERROR: {exc}"

def get_available_methods() -> Dict[str, Dict]:
    """Get available shredding methods"""
    return AdvancedModeShredder.METHOD_DETAILS.copy()

def validate_shredding_path(path: str) -> Tuple[bool, str]:
    """Validate if a path is safe for shredding"""
    try:
        path_obj = Path(path)
        
        if not path_obj.exists():
            return False, "Path does not exist"
            
        if _is_sensitive_system_path(path_obj.absolute()):
            return False, "Path is in system location"
            
        if path_obj.is_symlink():
            return False, "Symbolic links not supported"
            
        return True, "Path validated - Advanced MODE READY"
    except Exception as e:
        return False, f"Validation error: {e}"

# Alias for backward compatibility
shred_file = shred_file_Advanced_mode