import os
import subprocess
import platform
import shlex
from pathlib import Path
import re
import time
from packaging import version

class CrocUtils:
    def __init__(self, config):
        self.config = config
        self._check_croc_installed()
    
    def _check_croc_installed(self):
        """Check if croc is installed and available in PATH"""
        try:
            result = subprocess.run(
                ["croc", "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            if result.returncode != 0:
                raise FileNotFoundError("Croc executable not found")
            
            # Extract version
            match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
            if match:
                self.version = match.group(1)
            else:
                self.version = "Unknown"
                
            # Check if version is sufficient
            if self.version != "Unknown" and version.parse(self.version) < version.parse("9.0.0"):
                raise RuntimeError(f"Croc version {self.version} is too old, please upgrade to 9.0.0 or newer")
                
        except FileNotFoundError:
            raise FileNotFoundError(
                "Croc executable not found in PATH. Please install croc first:\n"
                "- Linux/macOS: curl https://getcroc.schollz.com | bash\n"
                "- Windows: Download from https://github.com/schollz/croc/releases"
            )
    
    def get_version(self):
        """Get the installed croc version"""
        return self.version
    
    def send_file(self, file_path, code=None, relay=None, callback=None):
        """Send a file using croc"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Build command
        cmd = ["croc", "send"]
        
        # Add optional arguments
        if code:
            cmd.extend(["--code", code])
        
        # Add file
        cmd.append(file_path)
        
        # 디버깅을 위한 로그 출력
        print(f"[DEBUG] 실행 명령어: {' '.join(cmd)}")
        
        try:
            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            code_phrase = None
            waiting_for_receiver = False
            connection_established = False
            
            # Process output
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                print(f"[DEBUG] croc 출력: {line}")  # 디버깅 로그
                
                # Try to extract code phrase
                if "Code is:" in line:
                    code_phrase = line.split("Code is:")[1].strip()
                    # 코드 생성 후 대기 상태로 전환
                    waiting_for_receiver = True
                    
                    if callback:
                        callback({
                            "status": "waiting",
                            "code": code_phrase,
                            "message": "Waiting for receiver to connect..."
                        })
                
                # Check for connection with receiver patterns
                elif (("Sending" in line and ("MB" in line or "KB" in line or "B)" in line)) or 
                      "Connection established" in line or
                      "Exchanged" in line):
                    waiting_for_receiver = False
                    
                    if not connection_established:
                        connection_established = True
                        if callback:
                            callback({
                                "status": "connected",
                                "code": code_phrase,
                                "message": "Connection established, starting transfer..."
                            })
                
                # Extract progress information - improve pattern matching
                progress_match = re.search(r'(\d+\.\d+)%\s+(\d+\.\d+\s+\w+\/s)', line)
                if progress_match:
                    percent = float(progress_match.group(1))
                    speed = progress_match.group(2)
                    
                    if callback:
                        print(f"[DEBUG] 진행률 업데이트: {percent}%, 속도: {speed}")  # 디버깅 로그
                        callback({
                            "status": "transferring",
                            "progress": percent,
                            "speed": speed,
                            "code": code_phrase
                        })
                # Alternative progress pattern
                elif "%" in line and "/" in line:
                    # Try to find percent and speed in alternative format
                    alt_progress = re.search(r'(\d+)%', line)
                    alt_speed = re.search(r'(\d+\.\d+\s+\w+\/s)', line)
                    
                    if alt_progress:
                        percent = float(alt_progress.group(1))
                        speed = alt_speed.group(1) if alt_speed else "N/A"
                        
                        if callback:
                            print(f"[DEBUG] 대체 패턴 진행률: {percent}%, 속도: {speed}")  # 디버깅 로그
                            callback({
                                "status": "transferring",
                                "progress": percent,
                                "speed": speed,
                                "code": code_phrase
                            })
                            
                # Check for completion
                if "File sent" in line or "Sent" in line:
                    if callback:
                        callback({
                            "status": "completed",
                            "progress": 100,
                            "code": code_phrase
                        })
                
                # Check for errors
                if "Error:" in line:
                    error_message = line
                    if callback:
                        callback({
                            "status": "error",
                            "message": error_message,
                            "code": code_phrase
                        })
            
            # Wait for process to complete
            process.wait()
            print(f"[DEBUG] 프로세스 종료 코드: {process.returncode}")  # 디버깅 로그
            
            # 추가: 전송 후 잠시 대기하여 리소스 정리
            try:
                time.sleep(0.5)  # 0.5초 대기
            except:
                pass
                
            # 콜백 호출 전 검증
            if process.returncode != 0 and callback:
                try:
                    callback({
                        "status": "error",
                        "message": "Transfer failed with unknown error",
                        "code": code_phrase
                    })
                except Exception as e:
                    print(f"[DEBUG] 에러 콜백 호출 오류: {str(e)}")
            
            return {
                "code": code_phrase,
                "status": "completed" if process.returncode == 0 else "error",
                "returncode": process.returncode
            }
        except Exception as e:
            print(f"[DEBUG] 예외 발생: {str(e)}")  # 디버깅 로그
            if callback:
                try:
                    callback({
                        "status": "error",
                        "message": f"Exception: {str(e)}",
                        "code": code
                    })
                except Exception as cb_error:
                    print(f"[DEBUG] 예외 콜백 호출 오류: {str(cb_error)}")
            raise
    
    def receive_file(self, code, destination=None, callback=None):
        """Receive a file using croc"""
        # Build command
        cmd = ["croc", code, "--yes"]  # 자동 승인 옵션 추가
        
        # Add destination if specified
        if destination:
            cmd.extend(["--out", destination])
        else:
            # Use default save directory
            save_dir = self.config.get_value("save_directory")
            if save_dir:
                cmd.extend(["--out", save_dir])
        
        # 디버깅을 위한 로그 출력
        print(f"[DEBUG] 수신 명령어: {' '.join(cmd)}")
        
        # Start process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,  # stdin 추가하여 사용자 입력을 처리할 수 있도록 함
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        received_file = None
        connection_established = False
        transfer_started = False
        
        try:
            # Process output
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                print(f"[DEBUG] croc 수신 출력: {line}")  # 디버깅 로그
                
                # 파일 수신 확인 메시지 확인
                if "Accept" in line and "?" in line:
                    # 이 부분은 "--yes" 옵션으로 인해 더 이상 필요하지 않지만, 혹시 모를 경우에 대비
                    if callback:
                        try:
                            callback({
                                "status": "confirmation",
                                "message": line,
                                "file": received_file
                            })
                        except Exception as e:
                            print(f"[DEBUG] 확인 콜백 오류: {str(e)}")
                            
                    # 자동으로 'y' 입력 (승인)
                    try:
                        process.stdin.write("y\n")
                        process.stdin.flush()
                        print("[DEBUG] 파일 수신 자동 승인됨")
                    except Exception as e:
                        print(f"[DEBUG] 파일 수신 자동 승인 실패: {str(e)}")
                
                # Check for connection establishment
                if "Connection" in line or "Joined" in line or "Requesting" in line:
                    if not connection_established:
                        connection_established = True
                        if callback:
                            try:
                                callback({
                                    "status": "connecting",
                                    "message": "Connecting to sender..."
                                })
                            except Exception as e:
                                print(f"[DEBUG] 연결 콜백 오류: {str(e)}")
                
                # Try to extract file name
                if "Receiving" in line:
                    match = re.search(r'Receiving (.+) \(', line)
                    if match:
                        received_file = match.group(1)
                        transfer_started = True
                        
                        if callback:
                            callback({
                                "status": "receiving",
                                "message": f"Receiving file: {received_file}",
                                "file": received_file,
                                "progress": 0
                            })
                
                # Extract progress information - improve pattern matching
                progress_match = re.search(r'(\d+\.\d+)%\s+(\d+\.\d+\s+\w+\/s)', line)
                if progress_match:
                    percent = float(progress_match.group(1))
                    speed = progress_match.group(2)
                    
                    if callback:
                        print(f"[DEBUG] 수신 진행률 업데이트: {percent}%, 속도: {speed}")  # 디버깅 로그
                        callback({
                            "status": "receiving",
                            "progress": percent,
                            "speed": speed,
                            "file": received_file
                        })
                # Alternative progress pattern
                elif "%" in line and "/" in line:
                    # Try to find percent and speed in alternative format
                    alt_progress = re.search(r'(\d+)%', line)
                    alt_speed = re.search(r'(\d+\.\d+\s+\w+\/s)', line)
                    
                    if alt_progress:
                        percent = float(alt_progress.group(1))
                        speed = alt_speed.group(1) if alt_speed else "N/A"
                        
                        if callback:
                            print(f"[DEBUG] 대체 패턴 수신 진행률: {percent}%, 속도: {speed}")  # 디버깅 로그
                            callback({
                                "status": "receiving",
                                "progress": percent,
                                "speed": speed,
                                "file": received_file
                            })
                
                # Check for completion
                if "Received" in line or "saved" in line:
                    if callback:
                        callback({
                            "status": "completed",
                            "progress": 100,
                            "file": received_file
                        })
                
                # Check for errors
                if "Error:" in line or "error" in line.lower():
                    error_message = line
                    if callback:
                        callback({
                            "status": "error",
                            "message": error_message,
                        })
            
            # 프로세스 완료 대기
            process.wait()
            print(f"[DEBUG] 수신 프로세스 종료 코드: {process.returncode}")
            
            # 추가: 수신 후 잠시 대기하여 리소스 정리
            try:
                time.sleep(0.5)  # 0.5초 대기
            except:
                pass
                
            # 콜백 호출 안전하게 처리
            if callback:
                try:
                    # 정상 종료 시 완료 콜백
                    if process.returncode == 0:
                        callback({
                            "status": "completed",
                            "message": "File received successfully",
                            "file": received_file
                        })
                    # 오류 발생 시 오류 콜백
                    else:
                        callback({
                            "status": "error",
                            "message": "File reception failed with unknown error",
                            "returncode": process.returncode
                        })
                except Exception as e:
                    print(f"[DEBUG] 수신 완료 콜백 오류: {str(e)}")
            
            return {
                "status": "completed" if process.returncode == 0 else "error",
                "file": received_file,
                "returncode": process.returncode
            }
            
        except Exception as e:
            print(f"[DEBUG] 수신 예외 발생: {str(e)}")
            if callback:
                try:
                    callback({
                        "status": "error",
                        "message": f"Exception: {str(e)}"
                    })
                except Exception as cb_error:
                    print(f"[DEBUG] 수신 예외 콜백 오류: {str(cb_error)}")
            raise 