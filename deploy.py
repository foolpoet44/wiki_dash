# -*- coding: utf-8 -*-
"""
GitHub Pages 배포 자동화 스크립트 (deploy.py)

이 스크립트는 로컬의 정적 웹 페이지 파일들을 깃허브(GitHub) 저장소로 푸시하여
전 세계 어디서나 접속할 수 있는 웹 페이지로 호스팅하는 과정을 자동화합니다.

원칙: "Do it once, automate it forever"
"""

import os
import sys
import subprocess

def run_command(command, error_message):
    """
    터미널 명령어를 실행하고 에러 발생 시 처리하는 단일 책임 함수입니다.
    """
    try:
        # 명령어를 실행하고 출력 결과를 받아옵니다.
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\n[오류 발생] {error_message}")
        print(f"상세 에러 내용: {e.stderr.strip()}")
        sys.exit(1)

def check_git_installed():
    """
    시스템에 Git이 설치되어 있는지 확인합니다.
    """
    run_command("git --version", "Git이 시스템에 설치되어 있지 않거나 환경 변수에 등록되지 않았습니다. Git을 먼저 설치해주세요.")

def initialize_git_if_needed():
    """
    현재 폴더에 Git 저장소(.git)가 없다면 새로 초기화합니다.
    """
    if not os.path.exists(".git"):
        print("▶ 현재 폴더에서 Git 저장소를 초기화합니다 (git init)...")
        run_command("git init", "Git 저장소 초기화에 실패했습니다.")
        # 기본 브랜치 이름을 main으로 설정합니다.
        run_command("git branch -M main", "기본 브랜치명을 main으로 설정하지 못했습니다.")
        print("✓ Git 저장소가 성공적으로 초기화되었습니다.")

def configure_remote_repository():
    """
    깃허브 원격 저장소(Remote Repository) 연결을 관리합니다.
    """
    # 현재 연결된 원격 저장소가 있는지 확인합니다.
    remotes = run_command("git remote -v", "원격 저장소 목록을 조회하는 데 실패했습니다.")
    
    if "origin" not in remotes:
        print("\n=== 깃허브 저장소(Repository) 연결 ===")
        print("아직 깃허브 저장소가 연결되어 있지 않습니다.")
        print("웹브라우저에서 생성하신 깃허브 저장소 주소(HTTPS)를 입력해주세요.")
        print("예: https://github.com/사용자이름/저장소이름.git")
        
        repo_url = input("깃허브 저장소 URL: ").strip()
        if not repo_url:
            print("[경고] 주소가 입력되지 않아 배포를 중단합니다.")
            sys.exit(1)
            
        run_command(f"git remote add origin {repo_url}", "원격 저장소 연결에 실패했습니다. URL을 다시 확인해주세요.")
        print("✓ 원격 저장소(origin) 연결이 완료되었습니다.")
    else:
        print("✓ 이미 깃허브 원격 저장소가 연결되어 있습니다.")

def deploy_to_github():
    """
    코드를 추가하고 커밋한 뒤 깃허브로 푸시하는 핵심 배포 프로세스입니다.
    """
    print("\n▶ 1. 변경된 정적 파일들을 임시 상자(Staging Area)에 담습니다...")
    # index.html, data.json 등 웹서버 구동에 필요한 파일과 함께 현재 스크립트도 버전을 보관하기 위해 전체를 추가합니다.
    run_command("git add .", "파일을 추가(git add)하는 과정에서 오류가 발생했습니다.")
    
    # 커밋 메시지 작성
    print("\n▶ 2. 이번 배포에 대한 메모(Commit Message)를 작성합니다...")
    commit_msg = input("변경 사항을 간략히 적어주세요 (엔터 입력 시 기본 메시지로 저장): ").strip()
    if not commit_msg:
        commit_msg = "Deploy static web files via deploy.py"
        
    # 커밋 실행
    run_command(f'git commit -m "{commit_msg}"', "새로운 변경사항이 없거나 커밋(git commit) 중에 오류가 발생했습니다.")
    print(f"✓ '{commit_msg}' 메시지로 성공적으로 기록되었습니다.")
    
    # 푸시 실행
    print("\n▶ 3. 깃허브 서버로 안전하게 발송합니다 (git push)...")
    run_command("git push -u origin main", "깃허브로 파일 전송(git push)을 완료하지 못했습니다. 로그인 상태나 권한을 확인해주세요.")
    print("✓ 깃허브로 안전하게 업로드가 완료되었습니다!")

def main():
    print("==========================================")
    print("      GitHub Pages 배포 자동화 프로그램    ")
    print("==========================================")
    
    # 작업 디렉토리를 현재 스크립트가 위치한 곳으로 명확하게 고정합니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # 순서대로 프로세스 진행
    check_git_installed()
    initialize_git_if_needed()
    configure_remote_repository()
    deploy_to_github()
    
    print("\n==========================================")
    print("🎉 모든 배포 절차가 완료되었습니다!")
    print("1. 이제 깃허브 저장소의 [Settings] -> [Pages] 메뉴로 이동합니다.")
    print("2. 'Build and deployment'의 Source가 'Deploy from a branch'로 되어 있는지 확인합니다.")
    print("3. Branch를 'main' (혹은 기본 브랜치)로 선택하고 / (root) 폴더를 선택한 뒤 [Save]를 누릅니다.")
    print("4. 약 1~2분 후 깃허브가 제공하는 고유 주소로 나만의 대시보드가 오픈됩니다!")
    print("==========================================")

if __name__ == "__main__":
    main()
