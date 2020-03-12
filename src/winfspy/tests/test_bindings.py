import os
import sys
import subprocess

from winfspy.plumbing.get_winfsp_dir import get_winfsp_dir, get_winfsp_library_name


def run_import_winfspy(env):
    command = [sys.executable, "-c", "import winfspy"]
    return subprocess.run(command, stderr=subprocess.PIPE, env=env)


def test_load_bindings(tmp_path):
    env = dict(os.environ)
    library_path = str(get_winfsp_dir())
    env["PATH"] = env["PATH"].replace(library_path, "")

    result = run_import_winfspy(env)
    assert result.returncode == 0

    env["WINFSP_LIBRARY_PATH"] = library_path
    result = run_import_winfspy(env)
    assert result.returncode == 0

    env["WINFSP_LIBRARY_PATH"] = "wrong"
    result = run_import_winfspy(env)
    assert result.returncode == 1
    stderr = result.stderr.decode()
    assert "RuntimeError: The provided WinFsp library path does not exist" in stderr

    env["WINFSP_LIBRARY_PATH"] = str(tmp_path)
    result = run_import_winfspy(env)
    assert result.returncode == 1
    stderr = result.stderr.decode()
    assert "RuntimeError: The provided WinFsp binary path does not exist" in stderr

    (tmp_path / "bin").mkdir()
    result = run_import_winfspy(env)
    assert result.returncode == 1
    stderr = result.stderr.decode()
    assert "RuntimeError: The WinFsp DLL could not be found in" in stderr

    (tmp_path / "bin" / f"{get_winfsp_library_name()}.dll").touch()
    result = run_import_winfspy(env)
    assert result.returncode == 1
    stderr = result.stderr.decode()
    assert "The winfsp binding could not be imported" in stderr
