import sys
import io
import importlib.util
import shutil
import os
from pathlib import Path


def run_with_input_simulation(target_py, input_data):
    """模擬輸入並執行 py 檔，攔截輸出"""
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    sys.stdin = io.StringIO(input_data)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        spec = importlib.util.spec_from_file_location("module.name", target_py)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
    except Exception as e:
        sys.stdout = original_stdout
        sys.stdin = original_stdin
        print(f"\n【執行出錯】{target_py.name}: {e}")
        return None
    finally:
        sys.stdout = original_stdout
        sys.stdin = original_stdin
    return captured_output.getvalue().replace("\r\n", "\n").strip()


def run_manual_and_record_input(target_py):
    """執行第一個檔案，讓使用者手動輸入並記錄過程"""
    original_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    user_inputs = []
    original_input = __builtins__.input

    def mocked_input(prompt=""):
        val = original_input(prompt)
        user_inputs.append(val)
        return val

    __builtins__.input = mocked_input

    try:
        spec = importlib.util.spec_from_file_location("module.name", target_py)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
    except Exception as e:
        print(f"\n【執行錯誤】{e}")
    finally:
        sys.stdout = original_stdout
        __builtins__.input = original_input

    return captured_output.getvalue().replace("\r\n", "\n").strip(), "\n".join(
        user_inputs
    )


def main():
    base = Path(__file__).parent
    source_dir = base / "transfer"

    # --- 第一階段：確認題型與檔案 ---
    while True:
        print("\n" + "=" * 30)
        print("=== TQC 自動化改題系統 ===")
        # 修改點 1：改成 Y/N
        mode_input = input(
            "是否需讀寫檔案 (第九類題型)?\n[Y] 需要  [N] 不需要\n請輸入: "
        ).upper()

        confirm_transfer = input(
            "\n請先將測試檔案複製到資料夾 transfer\n是否已複製? [Y] 下一步  [N] 返回重選: "
        ).upper()

        if confirm_transfer == "Y":
            mode = "1" if mode_input == "Y" else "0"
            break

    # --- 第二階段：檔案選擇與確認 ---
    while True:
        py_files = sorted(list(source_dir.glob("*.py")))
        py_files = [f for f in py_files if "_checkedOK" not in f.name]

        if len(py_files) < 2:
            print("\n【錯誤】transfer 資料夾內剩餘檔案不足 2 個。")
            return

        print("\n--- 待測檔案清單 ---")
        # 修改點 2：編號從 1 開始
        for i, f in enumerate(py_files, start=1):
            print(f"[{i}] {f.name}")

        try:
            ans_idx = int(input("\n請確認「正解檔」編號: ")) - 1
            file_ans = py_files[ans_idx]
            stu_idx = int(input("請確認「學生檔」編號: ")) - 1
            file_stu = py_files[stu_idx]

            print(f"\n已選定檔案：\n正解 -> {file_ans.name}\n學生 -> {file_stu.name}")
            confirm_file = input("是否確認無誤? [Y] 下一步  [N] 返回重選: ").upper()
            if confirm_file == "Y":
                break
        except (ValueError, IndexError):
            print("編號輸入錯誤，請輸入清單中的數字。")

    # --- 第三階段：執行比對 ---
    res_ans, res_stu = "", ""

    if mode == "1":
        txt_files = list(source_dir.glob("*.txt"))
        for txt in txt_files:
            shutil.copy(txt, base / txt.name)
        print("\n【系統】已自動同步 transfer 內所有 .txt 原始檔。")

        print(f"正在自動執行比對輸出內容...")
        res_ans = run_with_input_simulation(file_ans, "")
        res_stu = run_with_input_simulation(file_stu, "")
    else:
        print(f"\n>>> 執行正解檔 ({file_ans.name})，請在此手動輸入測資：")
        res_ans, captured_inputs = run_manual_and_record_input(file_ans)

        print(f"\n>>> 系統自動帶入剛才的測資，執行學生檔 ({file_stu.name})...")
        res_stu = run_with_input_simulation(file_stu, captured_inputs)

    # --- 第四階段：結果處理與清理 ---
    if res_ans is None or res_stu is None:
        print("\n【終止】執行過程異常，不進行檔案異動。")
        return

    print("\n" + "=" * 45)
    if res_ans == res_stu:
        print("***** 比較結果：完全一致 (PASS) *****")
        print("正在執行正確後的檔案處理...")

        if file_ans.exists():
            os.remove(file_ans)
            print(f"  [已清理正解]: {file_ans.name}")

        new_name = source_dir / f"{file_stu.stem}_checkedOK.py"
        if file_stu.exists():
            os.rename(file_stu, new_name)
            print(f"  [已完成改名]: {new_name.name}")
    else:
        print("***** 比較結果：發現差異 (FAIL) *****")
        lines1, lines2 = res_ans.split("\n"), res_stu.split("\n")
        for i in range(max(len(lines1), len(lines2))):
            l1 = lines1[i] if i < len(lines1) else "[EOF]"
            l2 = lines2[i] if i < len(lines2) else "[EOF]"
            if l1 != l2:
                print(f"第 {i + 1} 行差異：\n  正解: {repr(l1)}\n  學生: {repr(l2)}")
        print("\n【注意】比對失敗，原始檔案均保留在 transfer/ 資料夾中。")
    print("="*45)

if __name__ == "__main__":
    main()