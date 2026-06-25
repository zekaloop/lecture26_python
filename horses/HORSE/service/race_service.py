import random
import time
import os

RESET = '\033[0m'
YELLOW = '\033[93m'

class RaceService:
    def __init__(self):
        self.finish_line = 30
        
    def start_race(self, entry_horses):
        for h in entry_horses:
            h.pos = 0
            
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{YELLOW}=== 🏁 내 말 출전 친선 경기! 🏁 ==={RESET}\n")
            
            winner = None
            for h in entry_horses:
                h.pos += random.randint(1, h.speed)
                
                run_dist = " " * h.pos
                remain_dist = "." * max(0, self.finish_line - h.pos)
                print(f"[{h.name}(스피드:{h.speed})] {h.color}🐎{RESET}{remain_dist}| 결승선")
                print("----------------------------------------------------------")
                
                if h.pos >= self.finish_line and winner == None:
                    winner = h
                    
            if winner != None:
                print(f"\n🎉 우승! [{winner.color}{winner.name}{RESET}] ({winner.owner}님 소유) 🎉")
                print(f"압도적인 스피드를 보여주었습니다!")
                input("\n엔터를 누르면 마구간으로 돌아갑니다...")
                return
                
            time.sleep(0.2)